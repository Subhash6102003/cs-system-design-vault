================================================================================
  FILE 083: BACKGROUND PROCESSING & WORKMANAGER
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android fiercely manages battery and memory, regularly killing apps or suspending their background execution. To reliably perform tasks when the app is minimized or closed (e.g., uploading files, syncing data), developers must use the proper APIs. This guide covers WorkManager, Foreground Services, Alarms, and the intricate OS-level constraints like Doze Mode and App Standby Buckets.
  Prerequisites: Knowledge of Kotlin Coroutines, Android application lifecycle, and manifest permissions.
  What you'll learn: WorkManager APIs (OneTime vs Periodic), defining constraints, Foreground Services vs WorkManager, and navigating battery optimizations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  WORKMANAGER
    Jetpack library for deferrable, guaranteed background work. It guarantees execution even if the app exits or the device restarts.

  DEFERRABLE WORK
    Work that doesn't need to happen immediately and can wait for optimal system conditions (e.g., device connected to Wi-Fi and charging).

  WORKER
    An abstract class where the actual background logic is implemented.

  WORKREQUEST
    Represents a request to do work. Can be OneTimeWorkRequest or PeriodicWorkRequest.

  CONSTRAINTS
    Conditions that must be met for the work to run (e.g., NetworkType.UNMETERED, RequiresCharging).

  FOREGROUND SERVICE
    A service that performs operations noticeable to the user (e.g., playing music, active navigation). It requires a persistent notification and bypasses most Doze restrictions.

  DOZE MODE
    An OS-level battery-saving feature. If a device is stationary, unplugged, and screen off, the OS defers background CPU, network, and alarms into narrow "maintenance windows".

  APP STANDBY BUCKETS
    Android categorizes apps into buckets (Active, Working Set, Frequent, Rare, Restricted) based on user interaction frequency. Lower buckets have severe restrictions on job execution and network access.

  ALARMMANAGER
    An API used strictly for exact time-based events (e.g., a calendar reminder at 8:00 AM). It should not be used for general background work.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  BACKGROUND WORK DECISION TREE                                          │
  │                                                                         │
  │                             [What kind of work?]                        │
  │                                     |                                   │
  │             +-----------------------+------------------------+          │
  │             |                       |                        |          │
  │      [Immediate]               [Exact Time]            [Deferrable]     │
  │     (Must happen now)        (e.g. Alarm Clock)       (Guaranteed to run)│
  │             |                       |                        |          │
  │             v                       v                        v          │
  │   +-------------------+    +-----------------+     +-------------------+│
  │   | Leaves the app?   |    |  AlarmManager   |     |   WorkManager     |│
  │   +---------+---------+    +-----------------+     +-------------------+│
  │             |                                                           │
  │         +---+---+                                                       │
  │       Yes       No                                                      │
  │        |         |                                                      │
  │        v         v                                                      │
  │  [Foreground] [Coroutines]                                              │
  │   [Service]                                                             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DOZE MODE TIMELINE                                                     │
  │                                                                         │
  │   Screen Off                                                            │
  │    |                                                                    │
  │    v       +---+    +---+        +---+            +---+                 │
  │  [Active]->|D|M|--->|D|M|------->|D|M|----------->|D|M|-->...           │
  │            +-|-+    +-|-+        +-|-+            +-|-+                 │
  │              |        |            |                |                   │
  │             Idle    Maintenance   Longer Idle      Maintenance          │
  │                     Window        (Network/Jobs    Window               │
  │                     (Network/Jobs  Deferred)                            │
  │                     Allowed)                                            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // WorkManager Basics                                                   │
  │                                                                          │
  │  // 1. Define the Worker                                                 │
  │  class SyncWorker(appContext: Context, workerParams: WorkerParameters):  │
  │         CoroutineWorker(appContext, workerParams) {                      │
  │                                                                          │
  │      override suspend fun doWork(): Result {                             │
  │          return try {                                                    │
  │              // Simulate network sync                                    │
  │              delay(2000)                                                 │
  │              Log.d("SyncWorker", "Data synced successfully!")            │
  │              Result.success()                                            │
  │          } catch (e: Exception) {                                        │
  │              // Automatically retry with exponential backoff             │
  │              Result.retry()                                              │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // 2. Enqueue the Work (in Activity/ViewModel)                          │
  │  fun scheduleSync(context: Context) {                                    │
  │      val constraints = Constraints.Builder()                             │
  │          .setRequiredNetworkType(NetworkType.CONNECTED)                  │
  │          .setRequiresBatteryNotLow(true)                                 │
  │          .build()                                                        │
  │                                                                          │
  │      val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()           │
  │          .setConstraints(constraints)                                    │
  │          .build()                                                        │
  │                                                                          │
  │      WorkManager.getInstance(context).enqueue(syncRequest)               │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // ==========================================                           │
  │  // 1. Image Filter Worker (Receives and Returns Data)                   │
  │  // ==========================================                           │
  │  class FilterWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {│
  │      override suspend fun doWork(): Result {                             │
  │          // Retrieve input data                                          │
  │          val imageUri = inputData.getString("IMAGE_URI") ?: return Result.failure()│
  │                                                                          │
  │          // Process image (Fake delay)                                   │
  │          delay(3000)                                                     │
  │          val outUri = "content://filtered_$imageUri"                     │
  │                                                                          │
  │          // Pass output data                                             │
  │          val outputData = workDataOf("FILTERED_URI" to outUri)           │
  │          return Result.success(outputData)                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  class UploadWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {│
  │      override suspend fun doWork(): Result {                             │
  │          // Output from FilterWorker becomes Input for UploadWorker      │
  │          val imageUri = inputData.getString("FILTERED_URI") ?: return Result.failure()│
  │          delay(2000)                                                     │
  │          return Result.success()                                         │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 2. Chaining & Scheduling                                             │
  │  // ==========================================                           │
  │  fun processAndUploadImage(context: Context, uri: String) {              │
  │      val workManager = WorkManager.getInstance(context)                  │
  │                                                                          │
  │      val filterRequest = OneTimeWorkRequestBuilder<FilterWorker>()       │
  │          .setInputData(workDataOf("IMAGE_URI" to uri))                   │
  │          .build()                                                        │
  │                                                                          │
  │      val uploadRequest = OneTimeWorkRequestBuilder<UploadWorker>()       │
  │          .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())│
  │          .build()                                                        │
  │                                                                          │
  │      // Chaining: Filter first, THEN Upload                              │
  │      workManager.beginUniqueWork(                                        │
  │          "image_process_chain",                                          │
  │          ExistingWorkPolicy.REPLACE, // Overwrite if already running     │
  │          filterRequest                                                   │
  │      )                                                                   │
  │      .then(uploadRequest)                                                │
  │      .enqueue()                                                          │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 3. Observing Work Status in UI (Compose/ViewModel)                   │
  │  // ==========================================                           │
  │  @Composable                                                             │
  │  fun UploadStatusScreen(context: Context = LocalContext.current) {       │
  │      val workInfos by WorkManager.getInstance(context)                   │
  │          .getWorkInfosForUniqueWorkLiveData("image_process_chain")       │
  │          .observeAsState(emptyList())                                    │
  │                                                                          │
  │      val statusText = workInfos.firstOrNull()?.let { info ->             │
  │          when (info.state) {                                             │
  │              WorkInfo.State.ENQUEUED -> "Waiting for constraints..."     │
  │              WorkInfo.State.RUNNING -> "Processing..."                   │
  │              WorkInfo.State.SUCCEEDED -> "Upload Complete!"              │
  │              WorkInfo.State.FAILED -> "Upload Failed"                    │
  │              else -> "Idle"                                              │
  │          }                                                               │
  │      } ?: "Idle"                                                         │
  │                                                                          │
  │      Text(text = "Status: $statusText")                                  │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: When should you use WorkManager vs Foreground Service?

  ANSWER:
    Use WorkManager for deferrable background tasks (e.g., analytics upload, syncing database) that don't need to happen immediately. Use a Foreground Service for tasks that must run immediately and continuously, and are noticeable to the user (e.g., playing a podcast, recording GPS for a run).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does WorkManager guarantee execution?

  ANSWER:
    WorkManager persists its WorkRequests to a local SQLite database. Even if the device reboots or the app is force-killed, WorkManager reads from this database on OS startup/app launch and reschedules the jobs using JobScheduler (API 23+) or AlarmManager (older APIs).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Doze Mode and how does it affect background work?

  ANSWER:
    Introduced in API 23, Doze Mode saves battery by deferring background network access, CPU wakelocks, and alarms when the device is idle, unplugged, and screen-off. It groups deferred tasks into periodic "maintenance windows". WorkManager handles this natively by waiting for these windows.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What happens if a user force-stops your app from settings?

  ANSWER:
    Force-stopping an app kills all its processes and clears all scheduled alarms and jobs (including WorkManager requests). The app will NOT run in the background again until the user explicitly launches the app from the launcher.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does data flow in a chained WorkManager sequence?

  ANSWER:
    The Result.success(Data) output of the first Worker is automatically merged and passed as the inputData to the next Worker in the chain.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the minimum interval for a PeriodicWorkRequest?

  ANSWER:
    The absolute minimum interval enforced by the OS is 15 minutes. This prevents rogue apps from draining the battery by waking the device constantly.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an App Standby Bucket?

  ANSWER:
    Android categorizes apps into buckets based on user interaction (Active, Working Set, Frequent, Rare). An app in the "Rare" bucket (not used for days) is heavily restricted—jobs might only run once a day, and network access is throttled.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why not use Coroutines (GlobalScope or viewModelScope) for uploads instead of WorkManager?

  ANSWER:
    Coroutines are bound to the process lifecycle. If the user swipes the app away (killing the UI process), the coroutine is cancelled, and the upload fails. WorkManager guarantees execution regardless of process death.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Infinite Retry

  override suspend fun doWork(): Result {
      return try {
          val response = api.fetchData()
          if (response.isSuccessful) Result.success() else Result.retry()
      } catch (e: Exception) {
          Result.retry()
      }
  }

  SOLUTION:
    Problem: If the server is permanently down or returns a 404 (Not Found), Result.retry() will trigger exponential backoff. However, it will keep retrying until the maximum retry limit is reached, wasting battery.
    Fix: Differentiate between transient errors (Network failure/500s -> retry()) and terminal errors (400 Bad Request/404 -> failure()).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The UI-Blocked Worker

  class HeavyWorker(context: Context, params: WorkerParameters) : Worker(context, params) {
      override fun doWork(): Result {
          val bitmap = BitmapFactory.decodeFile(inputData.getString("FILE"))
          // Apply heavy CPU filter...
          return Result.success()
      }
  }

  SOLUTION:
    Problem: Worker.doWork() executes synchronously on WorkManager's background thread pool, but if multiple heavy image processings are queued, it can exhaust the thread pool. More importantly, in Kotlin, developers should prefer CoroutineWorker.
    Fix: Extend CoroutineWorker and run heavy CPU tasks using withContext(Dispatchers.Default).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Exact Alarm Disaster

  val alarmManager = getSystemService(Context.ALARM_SERVICE) as AlarmManager
  val intent = Intent(context, SyncReceiver::class.java)
  val pendingIntent = PendingIntent.getBroadcast(context, 0, intent, 0)
  // Run sync every minute exactly
  alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, System.currentTimeMillis(), 60000, pendingIntent)

  SOLUTION:
    Problem: Waking the device exactly every 60 seconds is incredibly destructive to battery life. Since Android 6, exact alarms are heavily restricted and Doze mode will ignore this. Since Android 12, exact alarms require explicit user permission.
    Fix: Use WorkManager for syncing data, allowing the OS to batch network requests efficiently.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Poor background processing is the #1 reason for 1-star reviews on the Play Store ("This app drains my battery!"). Misunderstanding Doze mode or attempting to run silent foreground services will cause Android OS to explicitly warn users that your app is a battery hog, prompting them to uninstall it. WorkManager safely abstracts these OS-level complications.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 081: Retrofit & OkHttp (Network Constraints) (relationship description)
  -> File 085: Offline-First Sync Architecture (Applying WorkManager) (relationship description)
  -> File 086: Notifications & Permissions (Foreground Services) (relationship description)

================================================================================
  END OF FILE 083
================================================================================
