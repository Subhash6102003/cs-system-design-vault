================================================================================
  FILE 088: ANDROID APP PUBLISHING & CI/CD
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android App Publishing & CI/CD
  The final step in Android development is safely delivering the app to users. This involves code shrinking, security via keystores, transitioning from APKs to App Bundles (AAB), and automating the deployment pipeline. This guide explains build variants, ProGuard/R8 optimizations, app signing mechanics, and setting up GitHub Actions for automated Play Store deployment.
  Prerequisites: Gradle build system basics, Git version control.
  What you'll learn: Debug vs Release builds, keystore management, Android App Bundles, R8 rule configuration, Play Console tracks, and automated CI/CD pipelines.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  BUILD TYPE
    Defines how the code is compiled. E.g., debug (unoptimized, unminified, signed with local debug key) vs release (minified, optimized, signed with production key).

  PRODUCT FLAVOR
    Used to create different versions of the app from the same codebase (e.g., free, premium, dev, prod).

  BUILD VARIANT
    The combination of Build Type + Product Flavor (e.g., freeDebug, premiumRelease).

  R8 / PROGUARD
    Build-time tools that perform Code Shrinking (removing unused code), Obfuscation (renaming variables/classes to make reverse engineering hard), and Optimization (inlining code).

  KEYSTORE (.JKS)
    A secure file containing cryptographic keys used to sign the Android app.

  APK (ANDROID PACKAGE)
    The traditional executable format. It contains resources for all screen densities and architectures, making the file massive.

  AAB (ANDROID APP BUNDLE)
    The modern publishing format. You upload the .aab to Google Play, and Google Play generates tailored, minimal APKs for the specific user's device (e.g., only downloading high-res images for a high-res phone).

  PLAY APP SIGNING
    Google manages your final app signing key in the cloud. You sign the AAB with an "Upload Key", and Google re-signs it with the "App Signing Key" before distributing it.

  CI/CD
    Continuous Integration (automated building/testing) and Continuous Deployment (automated publishing to Beta/Production tracks).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CI/CD PIPELINE FOR ANDROID                                             │
  │                                                                         │
  │    [Developer Push to GitHub]                                           │
  │               |                                                         │
  │               v                                                         │
  │     +--------------------+                                              │
  │     |  GitHub Actions    |                                              │
  │     |  (Virtual Machine) |                                              │
  │     +---------+----------+                                              │
  │               |                                                         │
  │    (1. Checkout Code)                                                   │
  │    (2. Setup JDK 17)                                                    │
  │    (3. Decode Base64 Keystore)                                          │
  │    (4. Run Unit Tests) -> if fail, stop.                                │
  │    (5. Build Release AAB)                                               │
  │               |                                                         │
  │               v                                                         │
  │    [Upload to Google Play Console]                                      │
  │               |                                                         │
  │               v                                                         │
  │      [ Internal Track ] -> QA Testers                                   │
  │               |                                                         │
  │      [ Open Beta Track ] -> Public Beta Users                           │
  │               |                                                         │
  │      [ Production ] -> Final Release                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  APK VS ANDROID APP BUNDLE (AAB)                                        │
  │                                                                         │
  │             [ APK ]                      [ AAB (App Bundle) ]           │
  │   +---------------------------+     +----------------------------+      │
  │   | Contains:                 |     | Uploaded to Google         |      │
  │   | - English, Spanish, Hindi |     |                            |      │
  │   | - x86, ARM32, ARM64       |     | Google generates tailored  |      │
  │   | - MDPI, HDPI, XXHDPI      |     | APK for the downloader:    |      │
  │   +---------------------------+     |                            |      │
  │      (50 MB downloaded)             |   (e.g., Pixel 5 gets      |      │
  │                                     |    English, ARM64, XXHDPI) |      │
  │                                     +-------------+--------------+      │
  │                                                   |                     │
  │                                           (15 MB downloaded)            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Gradle Setup for Release (app/build.gradle.kts)                      │
  │                                                                          │
  │  android {                                                               │
  │      // 1. Keystore configuration (Never hardcode passwords in Git!)     │
  │      signingConfigs {                                                    │
  │          create("release") {                                             │
  │              storeFile = file(System.getenv("KEYSTORE_PATH") ?: "keystore.jks")│
  │              storePassword = System.getenv("KEYSTORE_PASSWORD")          │
  │              keyAlias = System.getenv("KEY_ALIAS")                       │
  │              keyPassword = System.getenv("KEY_PASSWORD")                 │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      buildTypes {                                                        │
  │          getByName("release") {                                          │
  │              // 2. Enable R8 code shrinking and obfuscation              │
  │              isMinifyEnabled = true                                      │
  │              isShrinkResources = true                                    │
  │                                                                          │
  │              // 3. Apply ProGuard rules                                  │
  │              proguardFiles(                                              │
  │                  getDefaultProguardFile("proguard-android-optimize.txt"),│
  │                  "proguard-rules.pro"                                    │
  │              )                                                           │
  │                                                                          │
  │              // 4. Attach signing config                                 │
  │              signingConfig = signingConfigs.getByName("release")         │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      flavorDimensions += "environment"                                   │
  │      productFlavors {                                                    │
  │          create("dev") {                                                 │
  │              dimension = "environment"                                   │
  │              applicationIdSuffix = ".dev"                                │
  │              versionNameSuffix = "-dev"                                  │
  │          }                                                               │
  │          create("prod") {                                                │
  │              dimension = "environment"                                   │
  │              // No suffix, normal package name                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: yaml]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  name: Android CI/CD Pipeline                                            │
  │                                                                          │
  │  on:                                                                     │
  │    push:                                                                 │
  │      branches: [ "main" ]                                                │
  │                                                                          │
  │  jobs:                                                                   │
  │    build_and_deploy:                                                     │
  │      runs-on: ubuntu-latest                                              │
  │      steps:                                                              │
  │        - name: Checkout Code                                             │
  │          uses: actions/checkout@v3                                       │
  │                                                                          │
  │        - name: Setup Java JDK                                            │
  │          uses: actions/setup-java@v3                                     │
  │          with:                                                           │
  │            distribution: 'zulu'                                          │
  │            java-version: '17'                                            │
  │                                                                          │
  │        - name: Decode Keystore                                           │
  │          env:                                                            │
  │            ENCODED_STRING: ${{ secrets.KEYSTORE_BASE64 }}                │
  │          run: |                                                          │
  │            echo $ENCODED_STRING | base64 -d > app/keystore.jks           │
  │                                                                          │
  │        - name: Run Unit Tests                                            │
  │          run: ./gradlew testProdReleaseUnitTest                          │
  │                                                                          │
  │        - name: Build Release Bundle (AAB)                                │
  │          env:                                                            │
  │            KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}           │
  │            KEY_ALIAS: ${{ secrets.KEY_ALIAS }}                           │
  │            KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}                     │
  │            KEYSTORE_PATH: "keystore.jks"                                 │
  │          run: ./gradlew bundleProdRelease                                │
  │                                                                          │
  │        - name: Upload to Google Play Console                             │
  │          uses: r0adkll/upload-google-play@v1                             │
  │          with:                                                           │
  │            serviceAccountJsonPlainText: ${{ secrets.GCP_SERVICE_ACCOUNT_JSON }}│
  │            packageName: com.mycompany.app                                │
  │            releaseFiles: app/build/outputs/bundle/prodRelease/app-prod-release.aab│
  │            track: internal                                               │
  │            status: completed                                             │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between an APK and an AAB?

  ANSWER:
    An APK contains the compiled code and resources for all device configurations (all languages, all screen densities, all CPU architectures). An AAB (Android App Bundle) is a publishing format uploaded to Google Play. Play's servers read the AAB and generate highly optimized, device-specific APKs. AABs significantly reduce app download size.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What does isMinifyEnabled = true actually do?

  ANSWER:
    It enables R8 (formerly ProGuard), which performs static analysis on the bytecode. It removes unreachable code/libraries (Shrinking), renames remaining classes and variables to short meaningless names like a.b.c (Obfuscation), and applies optimizations (like inlining simple methods).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a proguard-rules.pro file used for?

  ANSWER:
    Since R8 removes "unused" code, it often incorrectly removes code that is only accessed via reflection (e.g., GSON parsing data models, or classes instantiated dynamically). The proguard-rules.pro file contains @Keep rules telling R8, "Do not rename or delete these specific classes."

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Play App Signing work?

  ANSWER:
    Historically, losing your Keystore meant you could never update your app again. With Play App Signing, Google securely holds your official production key. Developers sign their AABs with a local "Upload Key". When uploaded, Google validates the Upload Key, strips it, and re-signs the APKs with the actual App Signing Key. If you lose the Upload Key, Google can reset it for you.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is an Application ID vs a Package Name?

  ANSWER:
    The package in the AndroidManifest.xml represents the Kotlin/Java directory structure. The applicationId in build.gradle is the unique identifier on the Google Play Store. By changing the applicationIdSuffix in Product Flavors, you can install a "Dev" and "Prod" version of the app on the same device simultaneously.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you automate versioning in CI/CD?

  ANSWER:
    Instead of manually changing versionCode in Gradle, you pass it as an environment variable in GitHub actions (using ${{ github.run_number }}), so every commit pushed to main increments the version code automatically during the build: ./gradlew bundleRelease -PversionCode=${{ github.run_number }}.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an ANR?

  ANSWER:
    Application Not Responding. It occurs when the main thread is blocked for more than 5 seconds. Google Play Vitals tracks the ANR rate; if it exceeds the bad behavior threshold (~0.47%), Google severely penalizes the app's ranking in the store.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is In-App Updates (AppUpdateManager)?

  ANSWER:
    A Play Core library feature that prompts users to update the app from within the app itself. It has two modes: Flexible (downloads in background, user can still use app) and Immediate (blocks the entire screen demanding an update before continuing, used for critical security fixes).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Missing Reflection Rule

  data class UserResponse(
      @SerializedName("id") val id: String,
      @SerializedName("name") val name: String
  )
  
  // Network call completes successfully, but UserResponse fields are all null in Release build!

  SOLUTION:
    Problem: In the Release build, R8 minification is enabled. The UserResponse class isn't directly instantiated in the code (Retrofit/Gson instantiates it via reflection). R8 renames the variables from id/name to a/b, so Gson can't map the JSON.
    Fix: Add @Keep annotation to the data class, or add a rule in proguard-rules.pro: -keep class com.app.models.** { *; }.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Committed Keystore

  # In terminal
  git add keystore.jks
  git add build.gradle
  git commit -m "Added release signing configurations"
  git push origin main

  SOLUTION:
    Problem: Committing the physical .jks file and hardcoding the passwords inside build.gradle exposes your signing keys to anyone with repository access. This is a massive security breach.
    Fix: Add *.jks to .gitignore. Store the keystore as a Base64-encoded GitHub Secret, and inject it dynamically during the CI pipeline.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Overwriting the User

  buildTypes {
      getByName("debug") { applicationIdSuffix = ".debug" }
      getByName("release") { /* normal */ }
  }

  SOLUTION:
    Problem: You install the Release version from the Play Store. Then you plug your phone into Android Studio and hit "Run" (Debug build). The debug app installs as a completely separate app (because of .debug), creating two app icons on your phone. However, if they share a ContentProvider authority string that isn't suffixed, Android Studio will throw an INSTALL_FAILED_CONFLICTING_PROVIDER error.
    Fix: Append the applicationId to authorities in the Manifest: android:authorities="${applicationId}.provider".

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  A manual release process relies on human perfection. A developer might accidentally build a release APK using the wrong keystore, forget to bump the version code, or accidentally leave a debug logging flag on. CI/CD pipelines guarantee that every release is built in a clean, reproducible environment. Understanding AABs and R8 is mandatory; without them, your app will be 3x larger than necessary and vulnerable to reverse-engineering.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 084: Memory & Performance (R8 Optimization specifics) (relationship description)
  -> File 087: Testing (Running tests in CI before deploying) (relationship description)

================================================================================
  END OF FILE 088
================================================================================
