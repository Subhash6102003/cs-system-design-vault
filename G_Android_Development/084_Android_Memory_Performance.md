================================================================================
  FILE 084: ANDROID MEMORY & PERFORMANCE OPTIMIZATION
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Smooth user experiences on Android require adhering to strict memory constraints and frame rendering budgets. Memory leaks cause OutOfMemory (OOM) crashes, while blocking the main thread drops frames, causing visible stutter (jank). This guide dives deep into profiling tools, memory management, garbage collection, and RecyclerView/Compose performance optimizations.
  Prerequisites: Understanding of the Android Lifecycle, Garbage Collection in Java/Kotlin.
  What you'll learn: Process memory structures, LeakCanary, frame budgets, avoiding UI thread blocks, Bitmap memory calculations, and R8/ProGuard optimizations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  PROCESS MEMORY LIMITS
    Android devices have strict per-app heap sizes (often ~128MB to 512MB depending on device class). Exceeding this throws OutOfMemoryError.

  GARBAGE COLLECTION (GC)
    ART (Android Runtime) manages memory dynamically. However, stopping the world to run GC pauses the app, potentially skipping frames.

  MEMORY LEAK
    Occurs when an object is no longer needed but is still referenced by another long-living object, preventing GC from cleaning it up (e.g., a static field holding an Activity).

  LEAKCANARY
    An open-source library by Square that automatically detects and traces memory leaks in debug builds.

  JANK
    Stuttering or jerky animations caused by dropping frames.

  16MS FRAME BUDGET
    To achieve 60 FPS (Frames Per Second), the system must measure, layout, and draw the entire screen every 16.6 milliseconds. On 120Hz displays, the budget is 8.3ms.

  CHOREOGRAPHER
    The system service that coordinates animations, input, and drawing, dispatching Vsync signals to the app.

  STRICT MODE
    A developer tool that detects accidental disk or network I/O on the main thread and flashes the screen red or logs errors.

  R8 / PROGUARD
    Build tools that shrink (remove unused code), obfuscate (rename classes/variables), and optimize code for release builds.

  BITMAPS
    The largest memory consumers in Android. They represent images loaded into memory.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  FRAME RENDERING PIPELINE                                               │
  │                                                                         │
  │  If any step blocks the Main Thread, the frame misses the VSYNC deadline -> JANK.│
  │                                                                         │
  │   VSYNC Signal                                                          │
  │        |                                                                │
  │        v                                                                │
  │    +---------------------------------------------------------+          │
  │    |                   MAIN THREAD (16.6ms)                  |          │
  │    |                                                         |          │
  │    | [Input Events] -> [Animations] -> [Measure / Layout]    |          │
  │    |                                         |               |          │
  │    |                                   [Draw (Record)]       |          │
  │    +-----------------------------------------|---------------+          │
  │                                              v                          │
  │    +---------------------------------------------------------+          │
  │    |                   RENDER THREAD                         |          │
  │    | [Sync DisplayList] -> [Issue OpenGL/Vulkan Commands]    |          │
  │    +-----------------------------------------|---------------+          │
  │                                              v                          │
  │                                          [GPU] -> [Display]             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ANDROID PROCESS MEMORY LAYOUT                                          │
  │                                                                         │
  │   +---------------------+  <-- Max Heap Limit (e.g., 256MB)             │
  │   |                     |                                               │
  │   |    Java/Kotlin      |  (Managed by ART Garbage Collector)           │
  │   |    Object Heap      |  (Bitmaps, Strings, Objects)                  │
  │   |                     |                                               │
  │   +---------------------+                                               │
  │   |    Native Heap      |  (C++ code, Native libs like SQLite)          │
  │   +---------------------+                                               │
  │   |    Graphics         |  (GL surfaces, textures)                      │
  │   +---------------------+                                               │
  │   |    Code / Stack     |  (Dex code, thread execution stacks)          │
  │   +---------------------+                                               │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Calculating Bitmap Memory & Optimization                             │
  │                                                                          │
  │  // A 1080x1920 image in ARGB_8888 (4 bytes per pixel) takes:            │
  │  // 1080 * 1920 * 4 = 8,294,400 bytes (~8.3 MB) RAM!                     │
  │                                                                          │
  │  fun loadDownsampledBitmap(res: Resources, resId: Int, reqWidth: Int, reqHeight: Int): Bitmap {│
  │      val options = BitmapFactory.Options().apply {                       │
  │          // 1. Read dimensions only, don't load image into memory yet    │
  │          inJustDecodeBounds = true                                       │
  │          BitmapFactory.decodeResource(res, resId, this)                  │
  │                                                                          │
  │          // 2. Calculate optimal downsampling scale (power of 2)         │
  │          inSampleSize = calculateInSampleSize(this, reqWidth, reqHeight) │
  │                                                                          │
  │          // 3. Decode actual bitmap with downsampling                    │
  │          inJustDecodeBounds = false                                      │
  │      }                                                                   │
  │      return BitmapFactory.decodeResource(res, resId, options)            │
  │  }                                                                       │
  │                                                                          │
  │  fun calculateInSampleSize(options: BitmapFactory.Options, reqWidth: Int, reqHeight: Int): Int {│
  │      val (height: Int, width: Int) = options.outHeight to options.outWidth│
  │      var inSampleSize = 1                                                │
  │                                                                          │
  │      if (height > reqHeight || width > reqWidth) {                       │
  │          val halfHeight: Int = height / 2                                │
  │          val halfWidth: Int = width / 2                                  │
  │          while (halfHeight / inSampleSize >= reqHeight && halfWidth / inSampleSize >= reqWidth) {│
  │              inSampleSize *= 2                                           │
  │          }                                                               │
  │      }                                                                   │
  │      return inSampleSize                                                 │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  class MyApplication : Application() {                                   │
  │      override fun onCreate() {                                           │
  │          super.onCreate()                                                │
  │                                                                          │
  │          // 1. Configure StrictMode for Debug builds                     │
  │          if (BuildConfig.DEBUG) {                                        │
  │              StrictMode.setThreadPolicy(                                 │
  │                  StrictMode.ThreadPolicy.Builder()                       │
  │                      .detectDiskReads()                                  │
  │                      .detectDiskWrites()                                 │
  │                      .detectNetwork()   // Will crash if network on main thread│
  │                      .penaltyLog()                                       │
  │                      .penaltyFlashScreen() // Visual indicator of jank   │
  │                      .build()                                            │
  │              )                                                           │
  │                                                                          │
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
  │  // 2. Safely passing context to avoid Memory Leaks                      │
  │  class SharedPreferenceHelper(context: Context) {                        │
  │      // IMPORTANT: use applicationContext to prevent leaking an Activity │
  │      private val prefs = context.applicationContext.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)│
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is a Memory Leak in Android and how does it happen?

  ANSWER:
    A memory leak happens when the Garbage Collector cannot free an object because an active reference to it still exists. The most common leak is a static field or background thread holding a reference to an Activity after it has been destroyed by the system (e.g., on rotation).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does LeakCanary work?

  ANSWER:
    LeakCanary hooks into the Android Lifecycle. When an Activity or Fragment is destroyed, it passes a WeakReference of it to a background queue. After a few seconds, if the object is still in memory (not garbage collected), LeakCanary triggers a heap dump, analyzes it using Shark, and provides a leak trace.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the 16ms rule?

  ANSWER:
    To achieve a smooth 60 frames per second, the UI must update every 16.6 milliseconds (1000ms / 60). If the main thread takes longer than 16ms to execute logic and draw the screen, it drops a frame, causing visual jank.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you optimize a RecyclerView?

  ANSWER:
    - Use DiffUtil instead of notifyDataSetChanged().
    - Set setHasFixedSize(true) if the list bounds don't change.
    - Use view types (getItemViewType()) to recycle different layouts properly.
    - Flatten item view layouts (ConstraintLayout) to avoid deep view hierarchies.
    - Load images asynchronously and use caching (Glide/Coil).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is ProGuard or R8?

  ANSWER:
    Build tools that optimize release APKs. Shrinking removes unused classes/methods. Obfuscation renames classes/methods to short letters (a, b, c) making reverse-engineering harder and reducing DEX size. Optimization rewrites code logic (e.g., inlining functions) to run faster.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why shouldn't you pass a Context to a ViewModel?

  ANSWER:
    ViewModels survive configuration changes (like screen rotations). If you pass an Activity context, the ViewModel holds onto the destroyed Activity, preventing GC and causing a massive memory leak. Use AndroidViewModel (which provides Application) or inject context providers securely.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is PSS vs VSS vs RSS?

  ANSWER:
    Metrics for measuring memory. VSS (Virtual Set Size): total address space allocated. RSS (Resident Set Size): physical memory allocated. PSS (Proportional Set Size): memory used by the process PLUS a proportional share of memory shared across other processes (like shared native libraries). Android primarily uses PSS to judge an app's footprint.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What causes an OutOfMemoryError specifically related to Bitmaps?

  ANSWER:
    Loading a massive uncompressed image directly into RAM. An 8MP camera photo can consume 32MB of RAM if loaded at full resolution. You must downsample it using inSampleSize before loading, or use an image loading library like Coil/Glide which handles this automatically.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Classic Leak

  class MainActivity : AppCompatActivity() {
      companion object {
          var myTextView: TextView? = null
      }
  
      override fun onCreate(savedInstanceState: Bundle?) {
          super.onCreate(savedInstanceState)
          setContentView(R.layout.activity_main)
          myTextView = findViewById(R.id.text)
      }
  }

  SOLUTION:
    Problem: TextView holds a strong reference to the Context (the Activity) it was created in. By putting myTextView in a companion object (static field), the Activity is leaked forever when the user rotates the screen.
    Fix: Never store UI components, Views, or Contexts in static fields.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Rogue Listener

  class SensorManagerHelper(private val context: Context) {
      fun registerListener(listener: SensorListener) {
          val manager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
          manager.registerListener(listener, ...)
      }
  }

  SOLUTION:
    Problem: If the SensorListener is implemented by an Activity, and the app forgets to call unregisterListener in onDestroy(), the system-level SensorManager keeps a strong reference to the Activity, leaking it.
    Fix: Always pair register in onStart/onResume with unregister in onStop/onPause.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Heavy Main Thread

  button.setOnClickListener {
      val prefs = getSharedPreferences("data", Context.MODE_PRIVATE)
      prefs.edit().putString("huge_json", generateHugeJson()).commit()
  }

  SOLUTION:
    Problem: commit() writes to the disk synchronously on the main thread. Disk I/O is slow. This will block the thread for >16ms and cause UI freeze/jank.
    Fix: Use apply() instead of commit(), which writes the data to memory synchronously but handles the disk I/O asynchronously in the background.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Performance is directly tied to retention. An app that stutters during scrolling feels cheap. An app that crashes from OOM errors gets uninstalled. In production, tools like Firebase Performance Monitoring and Play Console Vitals are closely monitored for ANR (Application Not Responding) rates and Crash rates. Falling below Google's vital thresholds reduces your app's discoverability on the Play Store.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 083: Background Processing (Avoiding Main Thread Work) (relationship description)
  -> File 088: Android Publishing (App Vitals & R8) (relationship description)

================================================================================
  END OF FILE 084
================================================================================
