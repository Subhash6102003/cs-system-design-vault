================================================================================
  FILE 080: ANDROID ARCHITECTURE & TESTING
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Clean Architecture and Testing in Android
  This file covers advanced architectural patterns and testing methodologies for Android applications. You will learn about MVVM (Model-View-ViewModel), Clean Architecture (Presentation, Domain, Data layers), Dependency Injection (Hilt/Dagger), and how to write robust Unit Tests (JUnit, MockK) and UI Tests (Espresso, Compose Testing). Prerequisite: Experience building a complete Android app.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

MVVM
    Model-View-ViewModel. An architectural pattern separating UI logic (View) from business logic (ViewModel) and data access (Model).
  CLEAN ARCHITECTURE
    A layered architecture concept promoting separation of concerns:
  DATA LAYER
    Handles APIs, DBs, Repositories.
  DOMAIN LAYER
    Contains pure business logic (Use Cases/Interactors), has NO Android dependencies.
  PRESENTATION LAYER
    UI, ViewModels, Compose/Fragments.
  DEPENDENCY INJECTION (DI)
    A technique where an object receives other objects that it depends on, rather than creating them itself. (Hilt/Dagger).
  JUNIT
    The standard testing framework for Java/Kotlin.
  MOCKING
    Creating fake versions of dependencies (like a fake Repository) to isolate the class being tested. (MockK, Mockito).
  ESPRESSO
    Google's UI testing framework for Android views.
  COMPOSE TESTING RULE
    The testing framework for Jetpack Compose UI.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  CLEAN ARCHITECTURE LAYERS (ONION ARCHITECTURE)                         │
  │                                                                         │
  │             +---------------------------------------------+             │
  │             |               PRESENTATION LAYER            |             │
  │             |    (Activities, Compose, ViewModels)        |             │
  │             +----------------------+----------------------+             │
  │                                    | depends on                         │
  │             +----------------------v----------------------+             │
  │             |                  DOMAIN LAYER               |             │
  │             |      (Use Cases, Entities, Interfaces)      |             │
  │             |          * NO ANDROID IMPORTS *             |             │
  │             +----------------------+----------------------+             │
  │                                    ^ depends on (Inversion of Control)  │
  │             +----------------------+----------------------+             │
  │             |                  DATA LAYER                 |             │
  │             |   (Repositories, Room, Retrofit, APIs)      |             │
  │             +---------------------------------------------+             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Dependency Injection with Hilt                                       │
  │                                                                          │
  │  import dagger.hilt.android.lifecycle.HiltViewModel                      │
  │  import javax.inject.Inject                                              │
  │                                                                          │
  │  // Hilt provides the Repository automatically!                          │
  │  @HiltViewModel                                                          │
  │  class MainViewModel @Inject constructor(                                │
  │      private val repository: UserRepository                              │
  │  ) : ViewModel() {                                                       │
  │      // ...                                                              │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Unit Testing a ViewModel with MockK and Coroutines                   │
  │                                                                          │
  │  import io.mockk.coEvery                                                 │
  │  import io.mockk.mockk                                                   │
  │  import kotlinx.coroutines.ExperimentalCoroutinesApi                     │
  │  import kotlinx.coroutines.test.runTest                                  │
  │  import org.junit.Assert.assertEquals                                    │
  │  import org.junit.Rule                                                   │
  │  import org.junit.Test                                                   │
  │                                                                          │
  │  @OptIn(ExperimentalCoroutinesApi::class)                                │
  │  class UserViewModelTest {                                               │
  │                                                                          │
  │      // A JUnit rule to swap the Main dispatcher with a Test dispatcher  │
  │      @get:Rule                                                           │
  │      val mainDispatcherRule = MainDispatcherRule()                       │
  │                                                                          │
  │      // Mock the dependency                                              │
  │      private val repository = mockk<UserRepository>()                    │
  │                                                                          │
  │      @Test                                                               │
  │      fun `fetch users successfully updates state to Success`() = runTest {│
  │          // 1. Arrange: Define mock behavior                             │
  │          val mockUsers = listOf(User("Alice"))                           │
  │          coEvery { repository.getUsers() } returns mockUsers             │
  │                                                                          │
  │          // 2. Act: Instantiate VM and trigger action                    │
  │          val viewModel = UserViewModel(repository) // Dependency Injection allows testing!│
  │                                                                          │
  │          // 3. Assert: Check the StateFlow                               │
  │          assertEquals(UIState.Success(mockUsers), viewModel.uiState.value)│
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is the difference between MVVM and Clean Architecture?

  ANSWER:
    MVVM is a presentation pattern that separates UI from logic. Clean Architecture is a broader application-level pattern that dictates how different layers (Data, Domain, Presentation) interact and depend on each other.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the Domain Layer and why is it important?

  ANSWER:
    The Domain layer encapsulates the core business rules (Use Cases). It is the most important part of the app and should have NO dependencies on Android frameworks (like Context) or external libraries (like Retrofit). This makes it 100% unit-testable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Dependency Injection and why use Hilt?

  ANSWER:
    DI means passing dependencies into a class (e.g., via constructor) rather than the class creating them. It makes code modular and testable. Hilt is a DI library by Google built on Dagger, specifically designed to inject Android classes (ViewModels, Activities) easily.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the Dependency Inversion Principle?

  ANSWER:
    The "D" in SOLID. High-level modules (Domain) should not depend on low-level modules (Data). Both should depend on abstractions (Interfaces). The Data layer *implements* the repository interface defined in the Domain layer.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you test Kotlin Coroutines?

  ANSWER:
    You use kotlinx-coroutines-test. You swap the Dispatchers.Main with a TestDispatcher (using a JUnit Rule), and use runTest { ... } to execute suspend functions in a controlled, synchronous manner without actual delays.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is Mocking?

  ANSWER:
    Replacing real dependencies with fake objects during a test. E.g., replacing a real Network API with a Mock that instantly returns a predefined JSON string, so you are only testing the logic of your class, not the network.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Explain UI testing vs Unit testing.

  ANSWER:
    Unit testing tests small, isolated pieces of logic (like a ViewModel or UseCase) very quickly on the JVM. UI testing (Instrumented testing with Espresso/Compose) runs on a real device/emulator, clicks buttons, and verifies what is drawn on the screen.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Use Case (or Interactor)?

  ANSWER:
    A class in the Domain layer that represents a single, specific action a user can perform in the app (e.g., LoginUserUseCase, FormatDateUseCase). It keeps ViewModels small and reusable.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I sit between the Presentation and the Data, dictating the rules of the business. I refuse to import anything from android.os. What layer am I?

  SOLUTION:
    The Domain Layer.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I pretend to be your database or your network. I lie to your ViewModel, returning whatever data you tell me to return, just so you can pass your tests. Who am I?

  SOLUTION:
    A Mock Object.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  class LoginViewModel : ViewModel() {
      // Creating dependency internally
      private val api = RetrofitClient.create() 

      fun login() {
          api.performLogin()
      }
  }

  SOLUTION:
    Because LoginViewModel creates its own dependency (api), you cannot replace it with a mock during testing. The test will actually hit the real network and fail. Fix: Pass the dependency via constructor (Constructor Injection).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Inside Domain Layer Use Case
  class CheckNetworkUseCase(private val context: Context) {
      fun hasInternet(): Boolean {
          // Uses Android Context
      }
  }

  SOLUTION:
    The Domain layer must be pure Kotlin/Java to ensure portability and fast JVM unit testing. Importing android.content.Context breaks Clean Architecture. Fix: Create an interface NetworkChecker in Domain, and implement it in the Data/Framework layer.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without Clean Architecture and Dependency Injection, apps become "Big Balls of Mud" where changing a network library breaks the UI. Without Unit Tests, every new feature risks breaking existing functionality (regressions), slowing down deployment and ruining user trust.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 076: 076 Activity Fragment Lifecycle (MVVM usage.)
  -> File 079: 079 Android Network Data (The Data layer in Clean Architecture.)

================================================================================
  END OF FILE 080
================================================================================
