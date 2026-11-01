================================================================================
  FILE 074: KOTLIN ADVANCED & COROUTINES
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Advanced Kotlin: Coroutines, Flows, and Concurrency
  This file dives deep into Kotlin's powerful concurrency framework. You will learn the mechanics of Coroutines (suspend functions, scopes, builders), how Structured Concurrency prevents memory leaks, the different Dispatchers, exception handling strategies, and reactive programming using Flow (StateFlow, SharedFlow) and Channels. Prerequisite: Strong grasp of Kotlin Fundamentals.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

COROUTINE
    A lightweight thread. Coroutines are conceptually similar to threads but don't map 1:1 to OS threads. You can run 100,000 coroutines concurrently without crashing.
  SUSPEND FUNCTION
    A function marked with suspend that can be paused and resumed without blocking the underlying thread.
  COROUTINESCOPE
    Defines a lifecycle for coroutines. All coroutines must run in a scope (e.g., viewModelScope in Android).
  COROUTINE BUILDERS
    Functions like launch (fire and forget) and async (returns a Deferred result) that start new coroutines.
  DISPATCHERS
    Determine which thread pool a coroutine uses.
  MAIN
    UI thread (Android).
  IO
    Network/Disk operations.
  DEFAULT
    CPU-intensive work (sorting, parsing).
  STRUCTURED CONCURRENCY
    A principle where parent coroutines wait for children, and cancellation of a parent recursively cancels all children.
  FLOW
    Kotlin's cold asynchronous stream, conceptually similar to RxJava Observables.
  STATEFLOW / SHAREDFLOW
    Hot streams used for state management and event broadcasting.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  STRUCTURED CONCURRENCY & CANCELLATION                                  │
  │                                                                         │
  │  [ viewModelScope ] (Parent)                                            │
  │          |                                                              │
  │          +---> launch (Child 1: Fetch User)                             │
  │          |                                                              │
  │          +---> launch (Child 2: Fetch Posts)                            │
  │                   |                                                     │
  │                   +---> async (Grandchild: Parse JSON)                  │
  │                                                                         │
  │  * If Parent is cancelled, Child 1, Child 2, and Grandchild are automatically cancelled.│
  │  * If Child 2 fails with exception, it cancels Parent, which cancels Child 1. (Unless SupervisorJob is used).│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Suspend, Launch, and Async                                           │
  │                                                                          │
  │  import kotlinx.coroutines.*                                             │
  │                                                                          │
  │  suspend fun fetchUserData(): String {                                   │
  │      delay(1000) // Non-blocking delay                                   │
  │      return "User: Alice"                                                │
  │  }                                                                       │
  │                                                                          │
  │  suspend fun fetchUserOrders(): Int {                                    │
  │      delay(1000)                                                         │
  │      return 42                                                           │
  │  }                                                                       │
  │                                                                          │
  │  fun main() = runBlocking { // runBlocking bridges blocking/non-blocking worlds│
  │      // launch (fire and forget)                                         │
  │      launch(Dispatchers.Default) {                                       │
  │          println("Doing background work on: ${Thread.currentThread().name}")│
  │      }                                                                   │
  │                                                                          │
  │      // async (concurrent execution returning values)                    │
  │      val userDeferred = async { fetchUserData() }                        │
  │      val ordersDeferred = async { fetchUserOrders() }                    │
  │                                                                          │
  │      // await() suspends until result is ready                           │
  │      println("Result: ${userDeferred.await()} has ${ordersDeferred.await()} orders")│
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // ViewModel with StateFlow and Exception Handling                      │
  │                                                                          │
  │  import androidx.lifecycle.ViewModel                                     │
  │  import androidx.lifecycle.viewModelScope                                │
  │  import kotlinx.coroutines.flow.MutableStateFlow                         │
  │  import kotlinx.coroutines.flow.StateFlow                                │
  │  import kotlinx.coroutines.flow.asStateFlow                              │
  │  import kotlinx.coroutines.launch                                        │
  │  import kotlinx.coroutines.Dispatchers                                   │
  │  import kotlinx.coroutines.CoroutineExceptionHandler                     │
  │                                                                          │
  │  class UserViewModel(private val repository: UserRepository) : ViewModel() {│
  │                                                                          │
  │      // Internal mutable state                                           │
  │      private val _uiState = MutableStateFlow<UIState>(UIState.Loading)   │
  │      // Exposed immutable state                                          │
  │      val uiState: StateFlow<UIState> = _uiState.asStateFlow()            │
  │                                                                          │
  │      // Global exception handler for this scope                          │
  │      private val exceptionHandler = CoroutineExceptionHandler { _, exception ->│
  │          _uiState.value = UIState.Error("Network failure: ${exception.message}")│
  │      }                                                                   │
  │                                                                          │
  │      init {                                                              │
  │          fetchData()                                                     │
  │      }                                                                   │
  │                                                                          │
  │      private fun fetchData() {                                           │
  │          // Launch in viewModelScope (auto-cancelled on ViewModel clear) │
  │          viewModelScope.launch(Dispatchers.IO + exceptionHandler) {      │
  │              _uiState.value = UIState.Loading                            │
  │                                                                          │
  │              // Suspend function call on IO dispatcher                   │
  │              val data = repository.getUsers()                            │
  │                                                                          │
  │              // Switch back to Main is not strictly necessary for StateFlow, │
  │              // but shown here for demonstration.                        │
  │              withContext(Dispatchers.Main) {                             │
  │                  _uiState.value = UIState.Success(data)                  │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is a suspend function?

  ANSWER:
    A function that can be paused (suspended) and resumed later without blocking the thread it's running on. It can only be called from another suspend function or a coroutine.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the difference between launch and async.

  ANSWER:
    Both are coroutine builders. launch is "fire and forget" and returns a Job. async expects a result and returns a Deferred<T> (which implements Job); you call .await() to get the result.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Structured Concurrency?

  ANSWER:
    It guarantees that a coroutine is bound to a specific scope. It prevents coroutine leaks by ensuring that when a scope (like a ViewModel) is destroyed, all its running coroutines are automatically cancelled.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: When should you use Dispatchers.IO vs Dispatchers.Default?

  ANSWER:
    Use IO for blocking operations (network calls, database/file reads). It has a large thread pool. Use Default for CPU-intensive work (sorting large lists, JSON parsing). Its pool size equals the number of CPU cores.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between a cold stream (Flow) and a hot stream (StateFlow/SharedFlow)?

  ANSWER:
    A cold Flow only starts emitting data when someone collects it (each collector gets its own execution). A hot StateFlow/SharedFlow is active regardless of collectors, and multiple collectors share the same data stream.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How does SupervisorJob differ from a regular Job?

  ANSWER:
    In a regular Job, if a child coroutine throws an exception, it cancels the parent and all other children. With SupervisorJob, the failure of a child does not affect the parent or sibling coroutines.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is withContext used for?

  ANSWER:
    It is used to shift the execution of a block of code to a different Dispatcher within a coroutine, returning the result. It is equivalent to an async {}.await().

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Explain the difference between StateFlow and SharedFlow.

  ANSWER:
    StateFlow is a specific type of SharedFlow. StateFlow always has an initial state, only emits the latest value (conflation), and comparing old/new values triggers emission. SharedFlow is for generic events (like navigation clicks) where you might want no replay or multiple replayed events.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I am incredibly light; you can spawn a hundred thousand of me and I won't crush your memory. I pause without blocking. What am I?

  SOLUTION:
    A Coroutine.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am cold by nature. If nobody is listening, I make no sound. But as soon as you collect me, my stream begins to flow. What am I?

  SOLUTION:
    Kotlin Flow.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  fun main() = runBlocking {
      launch {
          Thread.sleep(5000) // What's wrong?
          println("Done")
      }
  }

  SOLUTION:
    Thread.sleep blocks the underlying thread entirely, defeating the purpose of coroutines. Fix: Use the suspend function delay(5000) which frees the thread while waiting.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  viewModelScope.launch {
      try {
          launch { throw Exception("Boom") }
      } catch (e: Exception) {
          println("Caught!")
      }
  }

  SOLUTION:
    This will crash the app. The exception inside the inner launch propagates up the Job hierarchy to the viewModelScope and to the thread's uncaught exception handler, bypassing the try/catch block. Fix: Use supervisorScope or CoroutineExceptionHandler.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Asynchronous programming is the backbone of Android. Doing work on the Main thread freezes the UI (ANR). Coroutines provide a clean, sequential-looking syntax for complex concurrent tasks, replacing the Callback Hell of the past. Flow replaces RxJava, providing a native, lifecycle-aware reactive streams solution.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 073: 073 Kotlin Fundamentals (related topic)
  -> File 076: 076 Activity Fragment Lifecycle (Understanding how ViewModel scope ties to coroutines.)

================================================================================
  END OF FILE 074
================================================================================
