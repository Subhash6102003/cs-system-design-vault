================================================================================
  FILE 075: ANDROID INTERNALS & RUNTIME
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android OS Internals: ART, Zygote, and IPC
  This file explains the underlying architecture of the Android Operating System. You will learn about the Android Runtime (ART) vs. Dalvik, how the Zygote process magically accelerates app startup, the Binder IPC mechanism, Process Priorities, and what triggers an ANR (Application Not Responding). Prerequisite: Advanced Android development experience.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

DALVIK / ART
    The runtime environments for Android. Dalvik (pre-Lollipop) used Just-In-Time (JIT) compilation. ART uses Ahead-Of-Time (AOT) and JIT, producing optimized .oat files.
  ZYGOTE PROCESS
    A special process created at boot. It preloads core framework classes and resources. Every new app process is a fork() of Zygote.
  BINDER IPC
    The inter-process communication mechanism unique to Android. It allows processes to talk to system services efficiently using shared memory and Parcelable data.
  PROCESS PRIORITY
    Android kills apps based on priority (OOM Killer): Foreground > Visible > Service > Cached > Empty.
  COLD START
    App starts from scratch (no process exists). Needs to load classes and inflate UI.
  WARM START
    Process exists, but UI needs recreation.
  HOT START
    App is just brought to foreground.
  ANR (APPLICATION NOT RESPONDING)
    A dialog shown when the UI thread is blocked for too long.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  ANDROID OS ARCHITECTURE                                                │
  │                                                                         │
  │  +-------------------------------------------------+                    │
  │  | System Apps (Dialer, Browser, Your App)         |                    │
  │  +-------------------------------------------------+                    │
  │  | Java API Framework (Activity Manager, Location) |                    │
  │  +-------------------------------------------------+                    │
  │  | Native C/C++ Libs   |   Android Runtime (ART)   |                    │
  │  | (OpenGL, SQLite)    |   (Core Libs)             |                    │
  │  +-------------------------------------------------+                    │
  │  | Hardware Abstraction Layer (HAL)                |                    │
  │  | (Audio, Bluetooth, Camera)                      |                    │
  │  +-------------------------------------------------+                    │
  │  | Linux Kernel                                    |                    │
  │  | (Drivers, Power Management, Binder IPC)         |                    │
  │  +-------------------------------------------------+                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ZYGOTE FORK PROCESS                                                    │
  │                                                                         │
  │  BOOT -> Init Process                                                   │
  │            |                                                            │
  │            v                                                            │
  │         [ Zygote ] (Preloads 4000+ classes / resources)                 │
  │            |                                                            │
  │      +-----+-----+-----+                                                │
  │      |           |     |                                                │
  │   fork()      fork() fork()                                             │
  │      |           |     |                                                │
  │   [App 1]     [App 2] [App 3]                                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Aidl]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Using IPC (AIDL - Android Interface Definition Language)             │
  │                                                                          │
  │  // IMyAidlInterface.aidl                                                │
  │  package com.example.ipc;                                                │
  │                                                                          │
  │  // Declare any non-default types here with import statements            │
  │  interface IMyAidlInterface {                                            │
  │      /**                                                                 │
  │       * Demonstrates some basic types that you can use as parameters     │
  │       * and return values in AIDL.                                       │
  │       */                                                                 │
  │      void basicTypes(int anInt, long aLong, boolean aBoolean, float aFloat,│
  │              double aDouble, String aString);                            │
  │                                                                          │
  │      int calculateSum(int a, int b);                                     │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Detecting and Preventing ANRs using StrictMode                       │
  │                                                                          │
  │  import android.os.StrictMode                                            │
  │  import android.app.Application                                          │
  │                                                                          │
  │  class MyApplication : Application() {                                   │
  │      override fun onCreate() {                                           │
  │          super.onCreate()                                                │
  │                                                                          │
  │          if (BuildConfig.DEBUG) {                                        │
  │              // Thread policy: Detect network, disk IO on the Main Thread│
  │              StrictMode.setThreadPolicy(                                 │
  │                  StrictMode.ThreadPolicy.Builder()                       │
  │                      .detectDiskReads()                                  │
  │                      .detectDiskWrites()                                 │
  │                      .detectNetwork()                                    │
  │                      .penaltyLog() // Log to Logcat                      │
  │                      .penaltyDeath() // Crash the app if violated!       │
  │                      .build()                                            │
  │              )                                                           │
  │                                                                          │
  │              // VM policy: Detect memory leaks, unclosed cursors         │
  │              StrictMode.setVmPolicy(                                     │
  │                  StrictMode.VmPolicy.Builder()                           │
  │                      .detectLeakedSqlLiteObjects()                       │
  │                      .detectLeakedClosableObjects()                      │
  │                      .detectActivityLeaks()                              │
  │                      .penaltyLog()                                       │
  │                      .build()                                            │
  │              )                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Explain the difference between Dalvik and ART.

  ANSWER:
    Dalvik was a JIT compiler (compiled code dynamically at runtime, causing battery/CPU drain). ART uses AOT (Ahead-Of-Time) compilation (compiles during installation) combined with Profile-Guided JIT to make apps run faster and save battery, though it uses more storage space.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the Zygote process and why does Android use it?

  ANSWER:
    Zygote is a daemon process launched at boot. It preloads all heavy framework classes and resources. When you launch an app, instead of starting from scratch, Android fork()s the Zygote process. This drastically reduces Cold Start time and shares memory across apps (Copy-on-Write).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Binder and how does it relate to Parcelable?

  ANSWER:
    Binder is Android's custom IPC (Inter-Process Communication) mechanism in the Linux kernel. To pass objects between processes via Binder, they must be flattened into byte streams; Parcelable is the Android-specific, highly optimized interface for doing this.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What triggers an ANR?

  ANSWER:
    An ANR occurs if the main thread is blocked. Specific triggers: No response to input events within 5 seconds, BroadcastReceiver executing for >10-20 seconds, or a Foreground Service taking >20 seconds to start.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does the Android system decide which app process to kill when it runs out of memory (OOM)?

  ANSWER:
    It relies on Process Priority (oom_adj score). It kills Empty processes first, then Cached (background apps), then Services, then Visible apps, and only as a last resort, the Foreground app.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the difference between Cold, Warm, and Hot app startups.

  ANSWER:
    Cold: No process exists; requires creating process, instantiating Application, and Activity. Warm: Process exists, but Activity needs recreation (e.g., navigating back to it). Hot: Activity is already in memory and just brought to the foreground.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the "Black/White Screen" issue during app launch and how do you fix it?

  ANSWER:
    Before the app's UI is inflated during a Cold Start, Android displays the window background of the app's theme. If it's a heavy app, the user sees a blank screen for a second. Fix it using the new AndroidX Splash Screen API.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Copy-on-Write (COW) memory in relation to Zygote?

  ANSWER:
    When Zygote forks a new app, the new process shares the same memory pages as Zygote. Memory is only copied and allocated specifically to the app when the app attempts to *modify* (write) to that memory.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I am the mother of all apps. I sit quietly with thousands of classes in my belly. When an app needs to live, I fork myself. Who am I?

  SOLUTION:
    The Zygote Process.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  Five seconds without a word from you, and I will show the user a dialog of death, offering to kill you. What am I?

  SOLUTION:
    Application Not Responding (ANR).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  override fun onCreate(savedInstanceState: Bundle?) {
      super.onCreate(savedInstanceState)
      setContentView(R.layout.activity_main)

      // Fetching config from server on boot
      val jsonString = URL("https://api.config.com").readText()
      parseConfig(jsonString)
  }

  SOLUTION:
    readText() blocks the main thread to perform a network request. On modern Android versions, this throws a NetworkOnMainThreadException. Even if it didn't, it would cause an ANR. Fix: Use Coroutines (Dispatchers.IO) to fetch the data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Passing a massive object via Intent
  val intent = Intent(this, DetailActivity::class.java)
  intent.putExtra("DATA", massiveDataList as java.io.Serializable)
  startActivity(intent)

  SOLUTION:
    Serializable uses Java reflection and is incredibly slow on Android, causing frame drops during navigation. Also, Binder has a 1MB transaction limit, so massive data will throw TransactionTooLargeException. Fix: Use Parcelable (or @Parcelize) and avoid passing huge datasets via Intents (use a ViewModel/Repository).

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Writing an app that works is easy; writing an app that respects system resources is hard. Understanding the runtime allows you to optimize startup times, prevent ANRs, use memory efficiently, and ensure your app isn't killed prematurely by the OS.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 074: 074 Kotlin Advanced (Using Coroutines to prevent ANRs.)
  -> File 076: 076 Activity Fragment Lifecycle (Activity state saving during process death.)

================================================================================
  END OF FILE 075
================================================================================
