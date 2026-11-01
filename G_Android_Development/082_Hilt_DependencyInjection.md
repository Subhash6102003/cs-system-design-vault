================================================================================
  FILE 082: HILT & DEPENDENCY INJECTION
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Dependency Injection (DI) is a software design pattern that implements Inversion of Control for resolving dependencies. Hilt, built on top of Dagger, is Google's recommended DI solution for Android. It operates at compile-time to generate boilerplate, providing a standard way to incorporate Dagger into an Android application without the immense learning curve.
  Prerequisites: Knowledge of Kotlin, Android lifecycles, and solid Object-Oriented Programming principles.
  What you'll learn: Setting up Hilt, defining modules and scopes, component hierarchies, constructor injection, and testing DI setups.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  DEPENDENCY INJECTION (DI)
    A technique where an object receives other objects that it depends on (dependencies) from an external source rather than creating them internally.

  HILT
    A compile-time dependency injection library for Android that simplifies Dagger-related infrastructure.

  @HILTANDROIDAPP
    Placed on the Application class. It triggers Hilt's code generation, serving as the application-level dependency container.

  @ANDROIDENTRYPOINT
    Placed on Android classes (Activity, Fragment, View, Service, BroadcastReceiver) to allow them to receive injected dependencies.

  @INJECT
    Used on a constructor to tell Hilt how to create instances of a class. Used on fields in Android components to request an instance from Hilt.

  @MODULE
    A class annotated to indicate it contributes to the dependency graph, usually containing @Provides or @Binds methods.

  @INSTALLIN
    Used with @Module to specify which Hilt Component (e.g., SingletonComponent, ViewModelComponent) the module's dependencies should be installed into.

  @PROVIDES
    Used inside modules to tell Hilt how to create instances of classes you don't own (e.g., Retrofit, Room DB, external libraries).

  @BINDS
    Used inside modules to map an interface to its concrete implementation. Must be an abstract function.

  SCOPE ANNOTATIONS
    Dictate the lifetime of a dependency. @Singleton lasts the lifetime of the app. @ActivityScoped lasts the lifetime of the Activity, etc.

  QUALIFIERS
    Used when there are multiple bindings for the exact same type (e.g., providing two different Retrofit instances for different URLs). @Named is a default qualifier, but custom ones can be created.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  HILT COMPONENT HIERARCHY                                               │
  │                                                                         │
  │  Dependencies flow *down* the hierarchy. A Fragment can access dependencies from the Activity and Singleton components, but a Singleton component cannot access Fragment components.│
  │                                                                         │
  │         +-------------------------+                                     │
  │         |   SingletonComponent    |  (@Singleton)                       │
  │         |   (Application Scope)   |                                     │
  │         +-----------+-------------+                                     │
  │                     |                                                   │
  │         +-----------v-------------+                                     │
  │         | ActivityRetainedComponent|  (@ActivityRetainedScoped / ViewModels)│
  │         | (Survives Config Change)|                                     │
  │         +-----------+-------------+                                     │
  │                     |                                                   │
  │         +-----------v-------------+                                     │
  │         |    ActivityComponent    |  (@ActivityScoped)                  │
  │         |   (Activity Lifecycle)  |                                     │
  │         +-----------+-------------+                                     │
  │                     |                                                   │
  │         +-----------v-------------+                                     │
  │         |    FragmentComponent    |  (@FragmentScoped)                  │
  │         |   (Fragment Lifecycle)  |                                     │
  │         +-----------+-------------+                                     │
  │                     |                                                   │
  │         +-----------v-------------+                                     │
  │         |     ViewComponent       |  (@ViewScoped)                      │
  │         |    (View Lifecycle)     |                                     │
  │         +-------------------------+                                     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Basic Constructor Injection & Field Injection                        │
  │                                                                          │
  │  // 1. A dependency that Hilt knows how to create                        │
  │  class NetworkValidator @Inject constructor() {                          │
  │      fun hasNetwork(): Boolean = true                                    │
  │  }                                                                       │
  │                                                                          │
  │  // 2. A ViewModel utilizing Constructor Injection                       │
  │  @HiltViewModel                                                          │
  │  class MainViewModel @Inject constructor(                                │
  │      private val validator: NetworkValidator                             │
  │  ) : ViewModel() {                                                       │
  │      // Logic here                                                       │
  │  }                                                                       │
  │                                                                          │
  │  // 3. An Activity utilizing Field Injection                             │
  │  @AndroidEntryPoint                                                      │
  │  class MainActivity : AppCompatActivity() {                              │
  │                                                                          │
  │      // Field injection for standard classes                             │
  │      @Inject lateinit var validator: NetworkValidator                    │
  │                                                                          │
  │      // ViewModels are injected via delegates                            │
  │      private val viewModel: MainViewModel by viewModels()                │
  │                                                                          │
  │      override fun onCreate(savedInstanceState: Bundle?) {                │
  │          super.onCreate(savedInstanceState)                              │
  │          // dependencies are ready to use                                │
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
  │  // 1. Defining the Application                                          │
  │  @HiltAndroidApp                                                         │
  │  class MainApplication : Application()                                   │
  │                                                                          │
  │  // ==========================================                           │
  │  // 2. Network Module (@Provides)                                        │
  │  // ==========================================                           │
  │  @Module                                                                 │
  │  @InstallIn(SingletonComponent::class)                                   │
  │  object NetworkModule {                                                  │
  │                                                                          │
  │      // Custom qualifier for specific HTTP clients                       │
  │      @Qualifier                                                          │
  │      @Retention(AnnotationRetention.BINARY)                              │
  │      annotation class AuthOkHttpClient                                   │
  │                                                                          │
  │      @Provides                                                           │
  │      @Singleton                                                          │
  │      fun provideRetrofit(@AuthOkHttpClient okHttpClient: OkHttpClient): Retrofit {│
  │          return Retrofit.Builder()                                       │
  │              .baseUrl("https://api.example.com/")                        │
  │              .client(okHttpClient)                                       │
  │              .build()                                                    │
  │      }                                                                   │
  │                                                                          │
  │      @Provides                                                           │
  │      @AuthOkHttpClient                                                   │
  │      fun provideOkHttpClient(): OkHttpClient {                           │
  │          return OkHttpClient.Builder().build()                           │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 3. Database Module (@Provides)                                       │
  │  // ==========================================                           │
  │  @Module                                                                 │
  │  @InstallIn(SingletonComponent::class)                                   │
  │  object DatabaseModule {                                                 │
  │                                                                          │
  │      @Provides                                                           │
  │      @Singleton                                                          │
  │      fun provideDatabase(@ApplicationContext context: Context): AppDatabase {│
  │          return Room.databaseBuilder(                                    │
  │              context,                                                    │
  │              AppDatabase::class.java,                                    │
  │              "app_db"                                                    │
  │          ).build()                                                       │
  │      }                                                                   │
  │                                                                          │
  │      @Provides                                                           │
  │      fun provideUserDao(database: AppDatabase): UserDao {                │
  │          return database.userDao()                                       │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 4. Repository Module (@Binds)                                        │
  │  // ==========================================                           │
  │  // Interfaces and Implementations                                       │
  │  interface UserRepository {                                              │
  │      fun getUser(): User                                                 │
  │  }                                                                       │
  │                                                                          │
  │  // Notice constructor injection on the implementation!                  │
  │  class UserRepositoryImpl @Inject constructor(                           │
  │      private val userDao: UserDao                                        │
  │  ) : UserRepository {                                                    │
  │      override fun getUser(): User = userDao.getUser()                    │
  │  }                                                                       │
  │                                                                          │
  │  // Binds module must be abstract                                        │
  │  @Module                                                                 │
  │  @InstallIn(ViewModelComponent::class) // Only needed in ViewModels, not Singleton!│
  │  abstract class RepositoryModule {                                       │
  │                                                                          │
  │      @Binds                                                              │
  │      @ViewModelScoped                                                    │
  │      abstract fun bindUserRepository(                                    │
  │          userRepositoryImpl: UserRepositoryImpl                          │
  │      ): UserRepository                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why do we need Dependency Injection?

  ANSWER:
    It decouples the creation of objects from their usage, making classes completely independent of how their dependencies are constructed. This allows for easily swapping real implementations with fake ones during unit testing (e.g., swapping a real Database with an In-Memory DB).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between @Provides and @Binds?

  ANSWER:
    @Provides is a standard function inside an object or class where you manually write the code to construct and return an instance (used for classes you don't own like Retrofit). @Binds is an abstract function used strictly to map an interface to its concrete implementation. @Binds is more efficient because it generates less code under the hood.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between Hilt and Koin?

  ANSWER:
    Hilt (Dagger) is a compile-time DI framework. It verifies the dependency graph during compilation, meaning missing dependencies crash at build time. Koin is a runtime Service Locator framework. It relies on Kotlin DSL and inline reified types to resolve dependencies at runtime, which can cause runtime crashes if a dependency is missing.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How do you inject a dependency into a Worker or Service?

  ANSWER:
    Use the @HiltWorker annotation and @AssistedInject on the constructor of the Worker. You also need to configure Hilt's WorkerFactory in your Application class. For Services, annotate them with @AndroidEntryPoint and use field injection (@Inject lateinit var).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What does the @ViewModelScoped annotation do?

  ANSWER:
    It ensures that a single instance of the dependency is shared across the entire lifecycle of that specific ViewModel. If the same dependency is injected multiple times within that ViewModel, the exact same object reference is returned.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Can a component in the FragmentComponent access dependencies from the SingletonComponent? What about the reverse?

  ANSWER:
    Yes, Hilt component hierarchy flows downwards. A Fragment can inject Singletons. The reverse is false: you cannot inject a @FragmentScoped dependency into a @Singleton class because the Fragment's lifecycle is much shorter than the Application's lifecycle (it would cause a memory leak).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a Qualifier and when is it used?

  ANSWER:
    A Qualifier is a custom annotation used to distinguish between multiple bindings of the exact same return type. For example, if your app needs two different Retrofit instances (one for an Auth API, one for a Data API), Hilt won't know which one to provide unless you tag them with distinct Qualifiers.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you replace modules for UI Testing in Hilt?

  ANSWER:
    Use @UninstallModules(MyModule::class) on your test class, and define a new inner module annotated with @Module @InstallIn(SingletonComponent::class) to provide mock or test doubles in its place.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Missing Constructor

  class PaymentProcessor {
      fun process() { /*...*/ }
  }
  
  @HiltViewModel
  class CheckoutViewModel @Inject constructor(
      private val processor: PaymentProcessor
  ) : ViewModel()

  SOLUTION:
    Problem: Hilt doesn't know how to create PaymentProcessor because its class definition lacks the @Inject constructor() annotation, and it is not provided in any @Module. Build will fail.
    Fix: Add @Inject constructor() to PaymentProcessor.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The UI Leak

  @Module
  @InstallIn(SingletonComponent::class)
  object AppContextModule {
      @Provides
      @Singleton
      fun provideSharedPreferences(activity: Activity): SharedPreferences {
          return activity.getSharedPreferences("prefs", Context.MODE_PRIVATE)
      }
  }

  SOLUTION:
    Problem: A SingletonComponent outlives any Activity. By trying to inject an Activity context into a Singleton module, Hilt will throw a compile-time error because Activity is not available in the SingletonComponent hierarchy.
    Fix: Use @ApplicationContext context: Context as the parameter instead.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Field Injection on Private Variables

  @AndroidEntryPoint
  class MainActivity : AppCompatActivity() {
      @Inject private lateinit var analyticsTracker: AnalyticsTracker
  }

  SOLUTION:
    Problem: Dagger/Hilt performs field injection directly on the property. If the property is marked private, the generated Java code cannot access it.
    Fix: Remove the private modifier. It must be at least package-private (default visibility in Java, or internal/public in Kotlin).

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without Dependency Injection, production applications become tightly coupled rigid structures. A change in the constructor of a low-level class (e.g., adding an API key to a Database class) forces you to update every single class that instantiates it across the entire app. Hilt centralizes these configurations. Moreover, automated testing is practically impossible without DI, as you cannot mock real network requests or databases in tests if classes instantiate them directly.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 079: Android MVVM & Clean Arch (relationship description)
  -> File 081: Retrofit & OkHttp (relationship description)
  -> File 087: Android Testing (Testing Hilt) (relationship description)

================================================================================
  END OF FILE 082
================================================================================
