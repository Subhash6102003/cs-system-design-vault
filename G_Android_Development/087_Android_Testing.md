================================================================================
  FILE 087: ANDROID TESTING FRAMEWORKS
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android Testing: Unit, UI, and Coroutines
  Testing is essential for building scalable Android applications. Android relies on a dual-environment testing structure: Local JVM tests (fast, no device) and Instrumented tests (slow, runs on an emulator/device). This guide covers modern testing tools including JUnit 5, MockK, Coroutine Test Dispatchers, Turbine (for Flows), and Compose UI Testing.
  Prerequisites: Kotlin Coroutines, MVVM Architecture.
  What you'll learn: Mocking dependencies with MockK, testing suspending functions, asserting StateFlow emissions, and writing robust Jetpack Compose UI tests.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  TEST PYRAMID
    - Unit Tests (70%): Run on local JVM (src/test). Fast, pure Kotlin logic.
    - Integration Tests (20%): Test interactions between layers (e.g., ViewModel + Room).
    - UI / E2E Tests (10%): Run on Android Emulator (src/androidTest). Uses Espresso or ComposeTestRule.

  JUNIT
    The foundational testing framework. Android uses JUnit 4 extensively, but modern apps migrate to JUnit 5 for better lifecycle and parameterized tests.

  MOCKK
    A mocking library built specifically for Kotlin. Unlike Mockito, it fully supports Kotlin's features (coroutines, sealed classes, final by default).

  RUNTEST
    A coroutine builder designed for testing. It skips delays (e.g., delay(1000) executes instantly) and provides a TestScope.

  TESTCOROUTINEDISPATCHER
    Replaces the main thread dispatcher (Dispatchers.Main) so UI logic can run on the JVM without throwing MainThreadException.

  TURBINE
    A small testing library for Kotlin Flows. It allows you to consume items from a Flow sequentially in tests.

  COMPOSE UI TESTING
    Provides ComposeTestRule to find UI nodes (onNodeWithText), perform actions (performClick), and assert state (assertIsDisplayed).

  ROBOLECTRIC
    A framework that provides a simulated Android environment inside a local JVM, allowing you to test Android-dependent code (like Context) without an emulator.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ANDROID TESTING DIRECTORIES                                            │
  │                                                                         │
  │   app/src/                                                              │
  │    ├── main/         -> Application Code                                │
  │    ├── test/         -> Local JVM Unit Tests (Fast, No Android Framework)│
  │    │                    (Testing ViewModels, UseCases, Mappers)         │
  │    └── androidTest/  -> Instrumented Tests (Slow, Needs Emulator/Device)│
  │                         (Testing Compose UI, Room DB, NavGraphs)        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MOCKING FLOW WITH MOCKK                                                │
  │                                                                         │
  │   1. Create Mock     ->  val repo = mockk<Repository>()                 │
  │   2. Define Behavior ->  coEvery { repo.getData() } returns "MockData"  │
  │   3. Execute Code    ->  val result = viewModel.fetch()                 │
  │   4. Verify Call     ->  coVerify(exactly = 1) { repo.getData() }       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Unit Testing a ViewModel with Coroutines and MockK                   │
  │                                                                          │
  │  // ViewModel to test                                                    │
  │  class LoginViewModel(private val repository: LoginRepository) : ViewModel() {│
  │      private val _state = MutableStateFlow("Idle")                       │
  │      val state = _state.asStateFlow()                                    │
  │                                                                          │
  │      fun login(user: String) {                                           │
  │          viewModelScope.launch {                                         │
  │              _state.value = "Loading"                                    │
  │              val success = repository.authenticate(user)                 │
  │              _state.value = if (success) "Success" else "Error"          │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // JUnit 4/5 Test Class                                                 │
  │  class LoginViewModelTest {                                              │
  │                                                                          │
  │      private lateinit var viewModel: LoginViewModel                      │
  │      private val mockRepo: LoginRepository = mockk() // 1. Create mock   │
  │                                                                          │
  │      @Before                                                             │
  │      fun setup() {                                                       │
  │          // Replace Main dispatcher with UnconfinedTestDispatcher        │
  │          Dispatchers.setMain(UnconfinedTestDispatcher())                 │
  │          viewModel = LoginViewModel(mockRepo)                            │
  │      }                                                                   │
  │                                                                          │
  │      @After                                                              │
  │      fun tearDown() {                                                    │
  │          Dispatchers.resetMain()                                         │
  │      }                                                                   │
  │                                                                          │
  │      @Test                                                               │
  │      fun `login success updates state to Success`() = runTest {          │
  │          // 2. Define behavior (coEvery handles suspend functions)       │
  │          coEvery { mockRepo.authenticate(any()) } returns true           │
  │                                                                          │
  │          // 3. Execute                                                   │
  │          viewModel.login("user123")                                      │
  │                                                                          │
  │          // 4. Assert State                                              │
  │          assertEquals("Success", viewModel.state.value)                  │
  │                                                                          │
  │          // 5. Verify interaction                                        │
  │          coVerify { mockRepo.authenticate("user123") }                   │
  │      }                                                                   │
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
  │  // 1. Testing Flow Emissions using Turbine                              │
  │  // ==========================================                           │
  │  @Test                                                                   │
  │  fun `login emits Loading then Success states`() = runTest {             │
  │      coEvery { mockRepo.authenticate(any()) } returns true               │
  │                                                                          │
  │      // Use Turbine to test StateFlow emissions                          │
  │      viewModel.state.test {                                              │
  │          // Initial state emission                                       │
  │          assertEquals("Idle", awaitItem())                               │
  │                                                                          │
  │          viewModel.login("user123")                                      │
  │                                                                          │
  │          // Assert subsequent states                                     │
  │          assertEquals("Loading", awaitItem())                            │
  │          assertEquals("Success", awaitItem())                            │
  │                                                                          │
  │          // Ensure no other unexpected states are emitted                │
  │          expectNoEvents()                                                │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 2. Testing Jetpack Compose UI (Instrumented)                         │
  │  // ==========================================                           │
  │  @RunWith(AndroidJUnit4::class)                                          │
  │  class LoginScreenTest {                                                 │
  │                                                                          │
  │      // Rule to setup Compose environment                                │
  │      @get:Rule                                                           │
  │      val composeTestRule = createComposeRule()                           │
  │                                                                          │
  │      @Test                                                               │
  │      fun loginButton_showsError_onInvalidCredentials() {                 │
  │          // 1. Setup UI                                                  │
  │          composeTestRule.setContent {                                    │
  │              MyTheme {                                                   │
  │                  LoginScreen(                                            │
  │                      onLoginClick = { /* Do nothing in UI test */ },     │
  │                      errorMessage = "Invalid Password" // Pre-feed error state│
  │                  )                                                       │
  │              }                                                               │
  │          }                                                               │
  │                                                                          │
  │          // 2. Assert UI Elements                                        │
  │          composeTestRule.onNodeWithText("Username")                      │
  │              .performTextInput("testuser")                               │
  │                                                                          │
  │          composeTestRule.onNodeWithText("Login")                         │
  │              .performClick()                                             │
  │                                                                          │
  │          // 3. Assert Error Text is Displayed                            │
  │          composeTestRule.onNodeWithText("Invalid Password")              │
  │              .assertIsDisplayed()                                        │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why do we need Dispatchers.setMain in Unit Tests?

  ANSWER:
    The Dispatchers.Main uses the Android Looper.getMainLooper(), which does not exist in the standard JVM environment where local unit tests run. Calling a coroutine on Main in a unit test throws an exception. setMain replaces it with a test dispatcher that can run on the JVM.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between runTest and runBlocking?

  ANSWER:
    runBlocking blocks the current thread until the coroutine finishes, and respects delay() calls in real-time (e.g., delay(5000) waits 5 seconds). runTest is designed for testing; it uses virtual time, allowing delay(5000) to execute instantly, making tests incredibly fast.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why use MockK instead of Mockito in Kotlin?

  ANSWER:
    Mockito was built for Java. It struggles with Kotlin features: it cannot mock final classes (Kotlin classes are final by default), struggles with suspend functions, and requires workarounds for inline/value classes. MockK handles all these Kotlin-specific features natively (e.g., coEvery for suspend functions).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you test a Room Database?

  ANSWER:
    Room should be tested via Instrumented Tests (src/androidTest). You initialize an in-memory database using Room.inMemoryDatabaseBuilder(). This creates a database entirely in RAM that is destroyed when the process dies, ensuring isolation between tests.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is Turbine used for?

  ANSWER:
    Turbine is a library that makes testing Flow and StateFlow significantly easier. It provides a .test {} extension block where you can sequentially call awaitItem() to verify each emission as the flow updates over time.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is Robolectric?

  ANSWER:
    Robolectric rewrites Android SDK classes (like Context, Intent, Activity) to run on the local JVM. This allows you to write tests that depend on the Android framework but execute them locally without the massive overhead and slowness of booting up an emulator.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the purpose of IdlingResource in Espresso UI tests?

  ANSWER:
    When running UI tests, Espresso waits for the UI thread to be idle before performing clicks. However, it doesn't know about background network calls. An IdlingResource tells Espresso, "I am doing background work, pause the test until I transition back to idle."

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Screenshot Testing (Paparazzi/Roborazzi)?

  ANSWER:
    Screenshot testing renders a Compose UI or View, saves it as an image, and compares it pixel-by-pixel against a baseline "golden" image. It catches visual regressions (e.g., padding changes) that are impossible to catch with text-based UI assertions.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Hanging Test

  @Test
  fun testFlow() = runTest {
      val flow = flowOf(1, 2, 3)
      val resultList = mutableListOf<Int>()
      
      flow.collect { resultList.add(it) }
      
      assertEquals(3, resultList.size)
  }

  SOLUTION:
    Problem: If flow is an infinite stream (like StateFlow or SharedFlow), collect will suspend forever, and the test will hang indefinitely.
    Fix: Use backgroundScope.launch { flow.collect... } or use Turbine's flow.test { ... } which handles lifecycle and collection cancellation automatically.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: InstantTaskExecutorRule Missing

  @Test
  fun testLiveData() {
      viewModel.loadData()
      assertEquals("Success", viewModel.liveData.value)
  }

  SOLUTION:
    Problem: If you are testing LiveData (legacy), it uses Android's main looper under the hood to set values. Running this on the JVM throws an error: Method getMainLooper in android.os.Looper not mocked.
    Fix: You must add @get:Rule val instantExecutorRule = InstantTaskExecutorRule() to the test class, which forces LiveData to update synchronously on the executing thread.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Real Delays

  class Repo {
      suspend fun fetchData(): String {
          delay(10_000) // 10 second delay
          return "Data"
      }
  }
  // Test:
  @Test
  fun testFetch() = runBlocking {
      val data = repo.fetchData()
      assertEquals("Data", data)
  }

  SOLUTION:
    Problem: The test will actually wait 10 seconds because runBlocking respects real time. If you have 100 tests like this, your CI pipeline will take hours.
    Fix: Change runBlocking to runTest. The delay(10_000) will be skipped instantly via virtual time.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without robust tests, every new feature risks breaking old features (regressions). A massive app codebase without tests turns into a "legacy" nightmare where developers are afraid to refactor anything. Fast, reliable unit tests (using MockK and runTest) provide confidence, while Compose UI tests prevent critical user journeys (like checkout flows) from breaking before deployment.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 079: Android MVVM & Clean Arch (Testable Architecture) (relationship description)
  -> File 082: Hilt Dependency Injection (Testing DI) (relationship description)

================================================================================
  END OF FILE 087
================================================================================
