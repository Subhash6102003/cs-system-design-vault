================================================================================
  FILE 085: ANDROID OFFLINE-FIRST & SYNC ARCHITECTURE
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Modern mobile apps are expected to work flawlessly regardless of network conditions. "Offline-first" means designing the app so that the local database is the single source of truth; network calls exist purely to sync the local database with the server. This guide covers the NetworkBoundResource pattern, conflict resolution strategies, work queues, and optimistic UI updates.
  Prerequisites: Room Database, Kotlin Flows, Coroutines, WorkManager, Retrofit.
  What you'll learn: Implementing a single source of truth, creating robust sync adapters, managing local pending updates, and handling data conflicts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  OFFLINE-FIRST
    An architectural paradigm where data is read from and written to a local cache (database) first. The UI never waits on a network request directly.

  SINGLE SOURCE OF TRUTH (SSOT)
    A principle stating that data should only be consumed from one place (in Android, usually the Room Database).

  NETWORKBOUNDRESOURCE
    A popular design pattern/class that orchestrates loading data from a local database, fetching updates from a network, saving those updates back to the database, and emitting the final result as a stream.

  OPTIMISTIC UI UPDATES
    Updating the UI immediately assuming a server request will succeed, making the app feel instantaneous. If the background sync fails, the UI is rolled back.

  PENDING ACTION QUEUE
    A local database table used to store user actions (POST, PUT, DELETE) that happened while offline. WorkManager processes this queue when the connection is restored.

  PULL-BASED SYNC
    The app actively polls or requests data from the server at intervals.

  PUSH-BASED SYNC
    The server notifies the app (via FCM/WebSockets) that data has changed, prompting the app to fetch the delta.

  CONFLICT RESOLUTION
    Rules applied when a user modifies local data, but the server data was also modified by someone else. Strategies include Last-Write-Wins (LWW), Version Vectors, or manual Merge Functions.

  EXPONENTIAL BACKOFF
    A strategy for retrying failed network requests, waiting progressively longer between each attempt (e.g., 2s, 4s, 8s, 16s) to avoid overwhelming the server or draining the battery.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  NETWORKBOUNDRESOURCE FLOW                                              │
  │                                                                         │
  │         [ UI / ViewModel ]                                              │
  │                 ^                                                       │
  │                 | (Observes Flow)                                       │
  │                 v                                                       │
  │   +-----------------------------+                                       │
  │   |     NetworkBoundResource    |                                       │
  │   +-----------------------------+                                       │
  │     | (1) Read    ^ (2) Emit      (4) Save                              │
  │     v             |               |   Network                           │
  │   [ Local Database (Room) ] <-----+   Result                            │
  │     |             ^               |                                     │
  │     | (3) Fetch   |               v                                     │
  │     +-------------+------> [ Remote API (Retrofit) ]                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  OFFLINE-FIRST ARCHITECTURE (PENDING QUEUE)                             │
  │                                                                         │
  │   User Action ->  Save to Room DB                                       │
  │                       +                                                 │
  │                   Add to `PendingSyncTable`                             │
  │                       |                                                 │
  │                       v                                                 │
  │               Trigger WorkManager                                       │
  │                       |                                                 │
  │          +------------+-------------+                                   │
  │          |            |             |                                   │
  │       (Offline)   (Wait for      (Online)                               │
  │        Sleep       Network)      Execute Network Request                │
  │                                     |                                   │
  │                               Clear from `PendingSyncTable`             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // NetworkBoundResource Implementation                                  │
  │                                                                          │
  │  // A generic helper function to build the Offline-First flow            │
  │  inline fun <ResultType, RequestType> networkBoundResource(              │
  │      crossinline query: () -> Flow<ResultType>,                          │
  │      crossinline fetch: suspend () -> RequestType,                       │
  │      crossinline saveFetchResult: suspend (RequestType) -> Unit,         │
  │      crossinline shouldFetch: (ResultType) -> Boolean = { true }         │
  │  ) = flow {                                                              │
  │      // 1. Emit loading state with current DB data                       │
  │      val data = query().first()                                          │
  │      emit(Resource.Loading(data))                                        │
  │                                                                          │
  │      try {                                                               │
  │          if (shouldFetch(data)) {                                        │
  │              // 2. Fetch from network                                    │
  │              val networkResult = fetch()                                 │
  │              // 3. Save to database (SSOT)                               │
  │              saveFetchResult(networkResult)                              │
  │          }                                                               │
  │          // 4. Emit success with a new flow directly from the database   │
  │          emitAll(query().map { Resource.Success(it) })                   │
  │      } catch (throwable: Throwable) {                                    │
  │          // 5. If network fails, emit error but keep the database data   │
  │          emitAll(query().map { Resource.Error(throwable, it) })          │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Sealed class for UI State                                            │
  │  sealed class Resource<T>(val data: T? = null, val error: Throwable? = null) {│
  │      class Success<T>(data: T) : Resource<T>(data)                       │
  │      class Loading<T>(data: T? = null) : Resource<T>(data)               │
  │      class Error<T>(throwable: Throwable, data: T? = null) : Resource<T>(data, throwable)│
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
  │  // 1. Entity and DAO for Pending Actions                                │
  │  // ==========================================                           │
  │  @Entity(tableName = "pending_actions")                                  │
  │  data class PendingAction(                                               │
  │      @PrimaryKey val id: String = UUID.randomUUID().toString(),          │
  │      val actionType: String, // e.g., "CREATE_TWEET", "LIKE_POST"        │
  │      val payloadJson: String, // Data needed for the network call        │
  │      val createdAt: Long = System.currentTimeMillis()                    │
  │  )                                                                       │
  │                                                                          │
  │  @Dao                                                                    │
  │  interface PendingActionDao {                                            │
  │      @Insert(onConflict = OnConflictStrategy.REPLACE)                    │
  │      suspend fun insertAction(action: PendingAction)                     │
  │                                                                          │
  │      @Query("SELECT * FROM pending_actions ORDER BY createdAt ASC")      │
  │      suspend fun getAllPendingActions(): List<PendingAction>             │
  │                                                                          │
  │      @Delete                                                             │
  │      suspend fun deleteAction(action: PendingAction)                     │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 2. The Sync Worker                                                   │
  │  // ==========================================                           │
  │  @HiltWorker                                                             │
  │  class SyncWorker @AssistedInject constructor(                           │
  │      @Assisted context: Context,                                         │
  │      @Assisted params: WorkerParameters,                                 │
  │      private val pendingActionDao: PendingActionDao,                     │
  │      private val api: RemoteApi                                          │
  │  ) : CoroutineWorker(context, params) {                                  │
  │                                                                          │
  │      override suspend fun doWork(): Result {                             │
  │          val pendingActions = pendingActionDao.getAllPendingActions()    │
  │                                                                          │
  │          if (pendingActions.isEmpty()) return Result.success()           │
  │                                                                          │
  │          for (action in pendingActions) {                                │
  │              try {                                                       │
  │                  // Execute network call based on action type            │
  │                  when (action.actionType) {                              │
  │                      "LIKE_POST" -> {                                    │
  │                          val postId = parseJsonForPostId(action.payloadJson)│
  │                          api.likePost(postId)                            │
  │                      }                                                   │
  │                      // handle other actions...                          │
  │                  }                                                       │
  │                  // If successful, remove from queue                     │
  │                  pendingActionDao.deleteAction(action)                   │
  │              } catch (e: HttpException) {                                │
  │                  // Client errors (4xx) usually shouldn't be retried blindly│
  │                  if (e.code() in 400..499) {                             │
  │                      pendingActionDao.deleteAction(action) // Drop invalid request│
  │                  } else {                                                │
  │                      return Result.retry() // Server error (5xx), retry later│
  │                  }                                                       │
  │              } catch (e: IOException) {                                  │
  │                  return Result.retry() // Network disconnected, retry later│
  │              }                                                           │
  │          }                                                               │
  │          return Result.success()                                         │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 3. Triggering Optimistic Update & Sync                               │
  │  // ==========================================                           │
  │  class PostRepository(                                                   │
  │      private val postDao: PostDao,                                       │
  │      private val pendingActionDao: PendingActionDao,                     │
  │      private val workManager: WorkManager                                │
  │  ) {                                                                     │
  │      suspend fun toggleLike(postId: String, isLiked: Boolean) {          │
  │          // 1. Optimistic Update (Immediate UI response)                 │
  │          postDao.updateLikeStatus(postId, isLiked)                       │
  │                                                                          │
  │          // 2. Queue network action                                      │
  │          val action = PendingAction(                                     │
  │              actionType = "LIKE_POST",                                   │
  │              payloadJson = """{"postId": "$postId", "liked": $isLiked}"""│
  │          )                                                               │
  │          pendingActionDao.insertAction(action)                           │
  │                                                                          │
  │          // 3. Trigger WorkManager to run when network is available      │
  │          val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()       │
  │              .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())│
  │              .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 10, TimeUnit.SECONDS)│
  │              .build()                                                    │
  │                                                                          │
  │          workManager.enqueueUniqueWork(                                  │
  │              "sync_actions",                                             │
  │              ExistingWorkPolicy.APPEND_OR_REPLACE,                       │
  │              syncRequest                                                 │
  │          )                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the Single Source of Truth (SSOT) principle in Android?

  ANSWER:
    It dictates that the UI should only observe state from exactly one source (typically the local SQLite/Room database). Network requests do not return data directly to the UI; instead, they update the database, which then emits the updated data to the UI via a Flow.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What are the benefits of the NetworkBoundResource pattern?

  ANSWER:
    It guarantees the user sees cached data instantly on app load. It prevents the UI from managing the complex states of loading from DB, fetching from network, and error handling. It naturally supports offline use cases.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you handle Optimistic UI Updates?

  ANSWER:
    When a user performs an action (e.g., liking a post), you instantly update the local database so the UI reacts immediately. Simultaneously, you enqueue a background task to sync the change to the server. If the server rejects the action (e.g., permission denied), the app must roll back the local database change and optionally notify the user.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is a "Pending Action Queue" and why is it needed?

  ANSWER:
    A local DB table that stores intents/actions the user performed while offline. Because WorkManager inputs (Data) have strict size limits and shouldn't hold complex JSON, it's safer to write the actions to a DB table and have the Worker read from that table sequentially.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you resolve sync conflicts (Last-Write-Wins vs Versioning)?

  ANSWER:
    - Last-Write-Wins (LWW): The server just accepts whatever timestamp is newest. Easiest to implement, but can overwrite valid data.
    - Versioning/ETags: Each record has a version number. If the client tries to update v2 but the server is already at v3, the server rejects it (409 Conflict). The client must fetch v3, merge changes locally, and try again.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: When should a background sync Worker return Result.retry() vs Result.failure()?

  ANSWER:
    Return retry() for transient errors (e.g., IOException for no internet, HTTP 500 Server Error). Return failure() for terminal errors that will never succeed no matter how many times you retry (e.g., HTTP 401 Unauthorized, HTTP 400 Bad Request, malformed JSON payload).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does Push-based sync via FCM work for database updates?

  ANSWER:
    Instead of the app pulling data every X minutes, the server sends an invisible FCM "data message" to the device when data changes. The app's FirebaseMessagingService receives it, wakes up the app, and triggers a WorkManager job to fetch the specific updated records.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The UI Waiter

  fun loadUserProfile(userId: String) {
      viewModelScope.launch {
          val user = api.fetchUser(userId) // Network call
          userDao.insert(user)
          _uiState.value = user
      }
  }

  SOLUTION:
    Problem: This violates SSOT. The UI waits entirely on the network. If the user is offline, the screen will be blank or throw an exception, completely ignoring the fact that userDao might already have the cached user.
    Fix: Read from the userDao as a Flow to drive the UI. Perform the api.fetchUser in the background, updating the DAO upon success.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Silent Overwrite

  // User A is offline. Modifies 'Note 1'.
  // User B is online. Modifies 'Note 1' and syncs to server.
  // User A connects to internet. 
  syncWorker.upload(userA_Note) // Server saves User A's note, overwriting User B completely.

  SOLUTION:
    Problem: Blind Last-Write-Wins without conflict detection causes silent data loss for concurrent users.
    Fix: Implement versioning (e.g., updatedAt or versionCounter). The server should return a 409 Conflict if User A tries to upload an older version than what's on the server. The client must handle the 409 by fetching the new note and merging or prompting the user.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Payload Too Large

  val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()
      .setInputData(workDataOf("HUGE_JSON_IMAGE" to massiveBase64String))
      .build()
  WorkManager.getInstance(context).enqueue(syncRequest)

  SOLUTION:
    Problem: WorkManager's Data object is serialized and has a hard limit of 10KB (often resulting in IllegalStateException: Data cannot occupy more than 10240 bytes when serialized).
    Fix: Never pass massive payloads directly into WorkManager intents. Save the payload to a local SQLite database/file and pass the URI or ID via Data so the Worker can look it up.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Modern users do not tolerate "Loading..." spinners every time they open an app, especially for data they already loaded yesterday. Applications like WhatsApp, Twitter, and Spotify are heavily offline-first—you can queue messages, like songs, and read feeds without an internet connection. Implementing a robust NetworkBoundResource with WorkManager elevates an app from an "amateur network wrapper" to a resilient, production-grade mobile experience.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 080: Room Database (Data layer) (relationship description)
  -> File 081: Retrofit & OkHttp (Network layer) (relationship description)
  -> File 083: Background Processing (WorkManager details) (relationship description)

================================================================================
  END OF FILE 085
================================================================================
