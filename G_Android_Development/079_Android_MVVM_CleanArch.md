================================================================================
  FILE 079: Android MVVM & Clean Architecture
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. TITLE & OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android MVVM & Clean Architecture

  MVVM (Model-View-ViewModel) paired with Clean Architecture provides a robust 
  and scalable blueprint for building Android applications. This architecture 
  separates the user interface (View), the presentation logic (ViewModel), and 
  the business rules and data layers (Model / Clean Architecture layers). By 
  dividing the application into Presentation, Domain, and Data layers, developers 
  ensure that business logic is completely isolated from framework-specific code. 
  This isolation dramatically improves testability, maintainability, and scalability.

  Prerequisites: Basic understanding of Kotlin, Android UI (Activities/Fragments/Compose), 
  and basic software design principles (SOLID).

  What you'll learn:
  * The components of MVVM and their responsibilities
  * The layers of Clean Architecture (Presentation, Domain, Data)
  * The Role of UseCases (Interactors) and Repositories
  * Data Transfer Objects (DTOs) vs. Domain Models vs. UI Models
  * Unidirectional Data Flow (UDF)
  * Comparing MVVM with MVI (Model-View-Intent)
  * Building a full project structure
  * Production considerations and common pitfalls

────────────────────────────────────────────────────────────────────────────────
  2. CORE CONCEPTS & TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  MVVM (Model-View-ViewModel): An architectural pattern that separates the graphical 
  user interface from the business logic.
  
  View: The UI component (Activity, Fragment, or Composable) that observes the 
  ViewModel and renders the state. It handles user interactions but contains zero 
  business logic.
  
  ViewModel: The presentation logic component. It exposes streams of state (like 
  StateFlow or LiveData) to the View and processes intents/actions from the View 
  by invoking Domain layer components. It survives configuration changes in Android.
  
  Model: In MVVM, this represents the data and business logic. When combined with 
  Clean Architecture, the Model expands into the Domain and Data layers.

  Clean Architecture: A software design philosophy by Robert C. Martin (Uncle Bob) 
  that aims to separate concerns by dividing software into rings. The inner rings 
  contain business policies, while outer rings contain mechanisms. The dependency 
  rule dictates that source code dependencies must point only inward.

  Presentation Layer: Contains the Views and ViewModels. It depends on the Domain 
  layer to execute business logic.

  Domain Layer: The core of the application. It contains entities (business models) 
  and UseCases (business rules). It is pure Kotlin and does not depend on any Android 
  framework libraries or other layers.

  Data Layer: Responsible for fetching and storing data. It contains Repository 
  implementations, Data Sources (local database, remote network API), and DTOs. 
  It depends on the Domain layer (implements the Repository interfaces defined in Domain).

  UseCase (Interactor): A class that encapsulates a single, specific business task 
  or use case of the application (e.g., LoginUserUseCase). It orchestrates data flow 
  to and from entities.

  Repository Pattern: An abstraction that mediates between the domain and data 
  mapping layers, acting like an in-memory domain object collection. The Domain 
  layer defines the Repository Interface, and the Data layer implements it.

  DTO (Data Transfer Object): An object that carries data between processes, typically 
  reflecting the exact JSON structure of a network response or a database schema.

  Domain Model: The pure representation of data used within the business logic, 
  stripped of any framework-specific annotations or fields.

  UI Model: A representation of data specifically formatted for the View to render 
  easily (e.g., formatting a Date into a "MM/dd/yyyy" String).

  Unidirectional Data Flow (UDF): A pattern where state flows down from the ViewModel 
  to the View, and events flow up from the View to the ViewModel.

  MVI (Model-View-Intent): An evolution of MVVM where the state is modeled as a 
  single source of truth (a single data class) and user actions are modeled as Intents.

────────────────────────────────────────────────────────────────────────────────
  3. ASCII / TEXT DIAGRAMS
────────────────────────────────────────────────────────────────────────────────

  Clean Architecture Layers & Dependency Rule
  
  Outer Layers (Frameworks/Drivers) -> Inner Layers (Enterprise/Business Rules)
  Dependencies point INWARD.

    ┌─────────────────────────────────────────────────────────────┐
    │                       PRESENTATION LAYER                    │
    │  ┌────────────┐       ┌─────────────────┐                   │
    │  │   View     │ ────> │   ViewModel     │                   │
    │  │ (Activity) │ <──── │ (State Holders) │                   │
    │  └────────────┘       └─────────────────┘                   │
    └────────│───────────────────────│────────────────────────────┘
             │                       │  Depends on
             V                       V
    ┌─────────────────────────────────────────────────────────────┐
    │                          DOMAIN LAYER                       │
    │                       (Pure Kotlin / Java)                  │
    │  ┌────────────┐       ┌─────────────────┐                   │
    │  │ UseCases   │ ────> │ Repository      │                   │
    │  │ (Business) │       │ INTERFACES      │                   │
    │  └────────────┘       └─────────────────┘                   │
    │                                │                            │
    │  ┌───────────────────────────────────────────────────────┐  │
    │  │                  Domain Entities                      │  │
    │  └───────────────────────────────────────────────────────┘  │
    └────────────────────────────────│────────────────────────────┘
                                     ^  Implements Interface
                                     │  (Dependency Inversion)
    ┌────────────────────────────────│─────────────────────────────┐
    │                           DATA LAYER                         │
    │  ┌────────────┐       ┌─────────────────┐                    │
    │  │ Repository │ <──── │ Data Sources    │                    │
    │  │ IMPLEMENT  │       │ (Remote / Local)│                    │
    │  └────────────┘       └─────────────────┘                    │
    │                                │                             │
    │  ┌─────────────────────────────V─────────────────────────┐   │
    │  │                 DTOs / Database Entities              │   │
    │  └───────────────────────────────────────────────────────┘   │
    └──────────────────────────────────────────────────────────────┘


  Unidirectional Data Flow (UDF) in MVVM

       State Flow (Down)
    ┌───────────────────────┐
    │       ViewModel       │
    └───────────────────────┘
       │                 ^
       │                 │
     State             Event/
     (UI Model)        Intent
       │                 │
       V                 │
    ┌───────────────────────┐
    │         View          │
    │  (Compose / Fragment) │
    └───────────────────────┘
       Events Flow (Up)


  Mapping Data Across Layers

  [ API / Network ]
          │ (JSON)
          V
  [ Data Layer ] ---> UserDto (Network Model)
          │
          │ mapping logic (toDomain)
          V
  [ Domain Layer ] -> User (Domain Entity, no framework annotations)
          │
          │ mapping logic (toUiModel - usually in ViewModel)
          V
  [ Presentation ] -> UserUiState (Formatted strings, specific UI flags)

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Let's look at small snippets demonstrating individual concepts.

  Snippet 1: Domain Entity vs DTO
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ // Data Layer: Network DTO (Contains framework annotations like Moshi/Gson)  │
│ @JsonClass(generateAdapter = true)                                           │
│ data class UserDto(                                                          │
│     @Json(name = "id") val id: Int,                                          │
│     @Json(name = "first_name") val firstName: String?,                       │
│     @Json(name = "last_name") val lastName: String?,                         │
│     @Json(name = "avatar_url") val avatarUrl: String?                        │
│ )                                                                            │
│                                                                              │
│ // Domain Layer: Pure Entity (No annotations, clean data)                    │
│ data class User(                                                             │
│     val id: Int,                                                             │
│     val fullName: String,                                                    │
│     val profileImageUrl: String                                              │
│ )                                                                            │
│                                                                              │
│ // Mapper Extension Function (Data Layer)                                    │
│ fun UserDto.toDomain(): User {                                               │
│     return User(                                                             │
│         id = this.id,                                                        │
│         fullName = "${this.firstName.orEmpty()} ${this.lastName.orEmpty()}".trim(),
│         profileImageUrl = this.avatarUrl ?: "default_url"                    │
│     )                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

  Snippet 2: The Domain Repository Interface & Data Implementation
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ // Domain Layer - Repository Interface                                       │
│ interface UserRepository {                                                   │
│     suspend fun getUser(id: Int): Result<User>                               │
│ }                                                                            │
│                                                                              │
│ // Data Layer - Repository Implementation                                    │
│ class UserRepositoryImpl(                                                    │
│     private val apiService: UserApiService // Data Source                    │
│ ) : UserRepository {                                                         │
│     override suspend fun getUser(id: Int): Result<User> {                    │
│         return try {                                                         │
│             val response = apiService.fetchUser(id)                          │
│             Result.success(response.toDomain())                              │
│         } catch (e: Exception) {                                             │
│             Result.failure(e)                                                │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

  Snippet 3: UseCase in the Domain Layer
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ class GetUserUseCase(                                                        │
│     private val userRepository: UserRepository                               │
│ ) {                                                                          │
│     // Operator invoke allows calling the class instance like a function     │
│     // e.g., val result = getUserUseCase(123)                                │
│     suspend operator fun invoke(userId: Int): Result<User> {                 │
│         // Business rules can go here (e.g., validate userId)                │
│         if (userId <= 0) return Result.failure(IllegalArgumentException())   │
│         return userRepository.getUser(userId)                                │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION-READY CODE
────────────────────────────────────────────────────────────────────────────────

  Below is a full vertical slice for fetching and displaying a User Profile.

┌──────────────────────────────────────────────────────────────────────────────┐
│ // --- PRESENTATION LAYER ---                                                │
│                                                                              │
│ // 1. UI State (UDF Model)                                                   │
│ data class ProfileUiState(                                                   │
│     val isLoading: Boolean = false,                                          │
│     val userName: String = "",                                               │
│     val avatarUrl: String = "",                                              │
│     val errorMessage: String? = null                                         │
│ )                                                                            │
│                                                                              │
│ // 2. ViewModel                                                              │
│ @HiltViewModel                                                               │
│ class ProfileViewModel @Inject constructor(                                  │
│     private val getUserUseCase: GetUserUseCase                               │
│ ) : ViewModel() {                                                            │
│                                                                              │
│     private val _uiState = MutableStateFlow(ProfileUiState())                │
│     val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()          │
│                                                                              │
│     fun fetchProfile(userId: Int) {                                          │
│         viewModelScope.launch {                                              │
│             _uiState.update { it.copy(isLoading = true, errorMessage = null) }
│                                                                              │
│             val result = getUserUseCase(userId)                              │
│             result.fold(                                                     │
│                 onSuccess = { user ->                                        │
│                     _uiState.update {                                        │
│                         it.copy(                                             │
│                             isLoading = false,                               │
│                             userName = user.fullName,                        │
│                             avatarUrl = user.profileImageUrl                 │
│                         )                                                    │
│                     }                                                        │
│                 },                                                           │
│                 onFailure = { error ->                                       │
│                     _uiState.update {                                        │
│                         it.copy(                                             │
│                             isLoading = false,                               │
│                             errorMessage = error.message ?: "Unknown Error"  │
│                         )                                                    │
│                     }                                                        │
│                 }                                                            │
│             )                                                                │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
│                                                                              │
│ // 3. View (Compose)                                                         │
│ @Composable                                                                  │
│ fun ProfileScreen(viewModel: ProfileViewModel) {                             │
│     val uiState by viewModel.uiState.collectAsStateWithLifecycle()           │
│                                                                              │
│     Column(modifier = Modifier.fillMaxSize()) {                              │
│         if (uiState.isLoading) {                                             │
│             CircularProgressIndicator()                                      │
│         } else if (uiState.errorMessage != null) {                           │
│             Text(text = "Error: ${uiState.errorMessage}")                    │
│             Button(onClick = { viewModel.fetchProfile(1) }) {                │
│                 Text("Retry")                                                │
│             }                                                                │
│         } else {                                                             │
│             Text(text = "Name: ${uiState.userName}")                         │
│             AsyncImage(model = uiState.avatarUrl, contentDescription = null) │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the main purpose of the Domain Layer in Clean Architecture?
  ANSWER: The Domain Layer encapsulates the core business logic of the application. 
  It contains business entities and use cases. Its main purpose is to be completely 
  independent of any framework, UI, or data storage mechanisms, ensuring that the 
  business rules are pure, easily testable, and reusable.

  Q2: Explain the Dependency Inversion Principle in the context of Clean Architecture.
  ANSWER: According to standard dependency flows, high-level policies (business logic) 
  depend on low-level details (database, network). Clean Architecture reverses this 
  using interfaces. The Domain Layer defines a Repository Interface, and the Data 
  Layer implements it. Thus, the Data Layer depends on the Domain Layer, allowing 
  the Domain to remain pure and independent.

  Q3: Why should we map DTOs to Domain Entities instead of using DTOs everywhere?
  ANSWER: DTOs often contain framework-specific annotations (like @SerializedName or 
  @Entity) and reflect the structure of a specific data source (e.g., API JSON). If 
  the API changes, the DTO changes. By mapping DTOs to pure Domain Entities, we 
  insulate the core business logic and UI from external API or database changes.

  Q4: What is the difference between MVVM and MVI?
  ANSWER: In MVVM, ViewModels often expose multiple distinct state streams (e.g., 
  LiveData<String> for name, LiveData<Boolean> for loading). In MVI (Model-View-Intent), 
  the state is modeled as a single source of truth (a single data class), and user 
  actions are modeled as explicit Intents or Events flowing to a reducer or intent 
  processor. MVI enforces stricter Unidirectional Data Flow.

  Q5: Should ViewModels contain business logic?
  ANSWER: In a strict Clean Architecture setup, ViewModels should only contain 
  presentation logic (formatting data for the UI, holding state, handling UI navigation). 
  Core business logic (calculations, validation across multiple data sources) should 
  be pushed down to the Domain Layer via UseCases.

  Q6: What is a UseCase (Interactor), and when should you create one?
  ANSWER: A UseCase represents a single action or business rule that a user can 
  trigger (e.g., TransferMoneyUseCase, LogoutUseCase). You should create one to 
  prevent "Fat ViewModels" and to reuse business logic across multiple ViewModels. 
  Even if it only forwards a call to a repository initially, it provides a place 
  to add future business logic without modifying the ViewModel.

  Q7: How do you handle exceptions in the Data Layer to prevent app crashes?
  ANSWER: Exceptions in the Data Layer (like Network or Database errors) should be 
  caught and wrapped in a Result class (like Kotlin's native Result or a custom 
  sealed class like Either/NetworkResponse). This ensures the Domain and Presentation 
  layers receive a controlled failure state rather than uncaught exceptions.

  Q8: Why does the presentation layer depend on the domain layer but not the data layer?
  ANSWER: The Presentation layer should only care about executing business logic and 
  displaying the resulting data. By restricting its dependency to the Domain layer, 
  we ensure that UI components cannot accidentally bypass business rules to directly 
  mutate or fetch data from databases or APIs. It enforces separation of concerns.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & "WHAT'S WRONG WITH THIS CODE?"
────────────────────────────────────────────────────────────────────────────────

  Challenge 1: The "Fat" ViewModel
  Context: A developer complains the ViewModel is hard to test.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ class CheckoutViewModel(private val api: PaymentApi) : ViewModel() {         │
│     fun processPayment(amount: Double, card: Card) {                         │
│         if (amount > 0 && card.isValid()) {                                  │
│             viewModelScope.launch {                                          │
│                 val response = api.charge(amount, card)                      │
│                 // handle response...                                        │
│             }                                                                │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: This code violates Clean Architecture. The ViewModel directly depends 
  on a data source (`PaymentApi`) and contains business logic (validation checks). 
  It should depend on a UseCase (e.g., `ProcessPaymentUseCase`), which in turn 
  depends on a `PaymentRepository` interface.

  Challenge 2: Leaking Frameworks into Domain
  Context: A developer added a nice utility to a Domain entity.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ package com.app.domain.model                                                 │
│ import android.os.Parcelable                                                 │
│ import kotlinx.parcelize.Parcelize                                           │
│                                                                              │
│ @Parcelize                                                                   │
│ data class Product(val id: String, val name: String) : Parcelable            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: The Domain layer must be pure Kotlin. By importing `android.os.Parcelable` 
  and using `@Parcelize`, the Domain layer is now coupled to the Android framework. 
  If you need to pass objects between Android components, map the Domain entity 
  to a UI model that implements Parcelable in the Presentation layer.

  Challenge 3: The UI Lifecycle Leak
  Context: Observing state in an Activity.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ class MainActivity : AppCompatActivity() {                                   │
│     override fun onCreate(savedInstanceState: Bundle?) {                     │
│         super.onCreate(savedInstanceState)                                   │
│         lifecycleScope.launch {                                              │
│             viewModel.uiState.collect { state ->                             │
│                 updateUi(state)                                              │
│             }                                                                │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: Collecting a `StateFlow` directly in `lifecycleScope.launch` does 
  not stop collection when the app goes to the background. This can lead to crashes 
  (if UI is updated while stopped) or wasted resources. The correct approach is to 
  use `repeatOnLifecycle(Lifecycle.State.STARTED)` or, in Compose, use 
  `collectAsStateWithLifecycle()`.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  In small personal projects, Clean Architecture might seem like boilerplate. But 
  in production environments with large teams, it is absolutely essential:

  1. Parallel Development: The UI team can work on the Presentation layer using 
  mock data from the Domain layer interfaces, while the backend/data team implements 
  the Data layer in parallel.
  
  2. Scalability: As the app grows, you might switch from REST APIs to GraphQL, or 
  from SQLite to Room, or to Realm. Because the Domain layer only knows about interfaces, 
  you can completely rewrite the Data layer without changing a single line of UI or 
  business logic.
  
  3. Testing: Testing UI is slow (instrumentation tests). Testing APIs is brittle. 
  But testing pure Kotlin Domain logic (UseCases) is incredibly fast and reliable. 
  Clean Architecture maximizes the amount of pure unit-testable code.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  * 080_Room_Database.md - Detailed look at implementing the Data Layer locally.
  * 085_Dagger_Hilt_Dependency_Injection.md - How to inject Repositories and UseCases.
  * 090_Coroutines_Flow_Android.md - Deep dive into StateFlow and threading in MVVM.

================================================================================
  END OF FILE 079
================================================================================
