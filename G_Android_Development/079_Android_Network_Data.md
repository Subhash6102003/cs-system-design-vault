================================================================================
  FILE 079: ANDROID NETWORKING & DATA PERSISTENCE
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Data Management in Android: Retrofit, Room, and Repositories
  This file covers how Android applications interact with data, both over the network and locally on the device. You will learn how to make REST API calls using Retrofit, parse JSON with Moshi/Gson, and persist data using the Room persistence library (an abstraction over SQLite). We will also cover the Repository pattern to mediate between these data sources. Prerequisite: Kotlin Coroutines.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

RETROFIT
    A type-safe HTTP client for Android and Java by Square. It turns an HTTP API into a Kotlin interface.
  ROOM
    An architecture component providing an abstraction layer over SQLite to allow fluent database access while harnessing the full power of SQLite.
  ENTITY
    A data class annotated with @Entity that represents a table in the Room database.
  DAO (DATA ACCESS OBJECT)
    An interface annotated with @Dao containing the methods to access the database.
  REPOSITORY PATTERN
    A design pattern that abstracts data sources (network vs. local) from the rest of the app, providing a clean API for data access.
  SINGLE SOURCE OF TRUTH (SSOT)
    A principle where data is only consumed from one place (usually the local DB), and the network just acts as a sync mechanism to update that DB.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  REPOSITORY PATTERN WITH SSOT                                           │
  │                                                                         │
  │                         +-------------------+                           │
  │                         |    ViewModel      |                           │
  │                         +---------+---------+                           │
  │                                   |                                     │
  │                                   v                                     │
  │                         +---------+---------+                           │
  │                         |    Repository     |                           │
  │                         +----+---------+----+                           │
  │             Local Data       |         |       Remote Data              │
  │       +----------------------+         +----------------------+         │
  │       |                                                       |         │
  │       v                                                       v         │
  │  +----+----+                                             +----+----+    │
  │  | Room DB | <====== (Network Sync Updates DB) ========= | Retrofit|    │
  │  | (DAO)   |                                             | (API)   |    │
  │  +---------+                                             +---------+    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Retrofit Network Interface                                           │
  │                                                                          │
  │  import retrofit2.http.GET                                               │
  │  import retrofit2.http.Path                                              │
  │                                                                          │
  │  // Define the API interface                                             │
  │  interface UserApi {                                                     │
  │      @GET("users/{id}")                                                  │
  │      suspend fun getUserById(@Path("id") userId: Int): UserResponse      │
  │  }                                                                       │
  │                                                                          │
  │  // Data class for JSON parsing (e.g., Moshi or Gson)                    │
  │  data class UserResponse(                                                │
  │      val id: Int,                                                        │
  │      val name: String,                                                   │
  │      val email: String                                                   │
  │  )                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Room Database Setup & DAO                                            │
  │                                                                          │
  │  import androidx.room.*                                                  │
  │  import kotlinx.coroutines.flow.Flow                                     │
  │                                                                          │
  │  // 1. Entity (Table)                                                    │
  │  @Entity(tableName = "users")                                            │
  │  data class UserEntity(                                                  │
  │      @PrimaryKey val id: Int,                                            │
  │      val name: String,                                                   │
  │      val email: String                                                   │
  │  )                                                                       │
  │                                                                          │
  │  // 2. DAO (Queries)                                                     │
  │  @Dao                                                                    │
  │  interface UserDao {                                                     │
  │      // Room supports Coroutines natively.                               │
  │      // Suspend for one-shot queries.                                    │
  │      @Insert(onConflict = OnConflictStrategy.REPLACE)                    │
  │      suspend fun insertUser(user: UserEntity)                            │
  │                                                                          │
  │      // Flow for reactive streams. Emits a new list whenever the DB changes!│
  │      @Query("SELECT * FROM users")                                       │
  │      fun getAllUsers(): Flow<List<UserEntity>>                           │
  │  }                                                                       │
  │                                                                          │
  │  // 3. Database                                                          │
  │  @Database(entities = [UserEntity::class], version = 1)                  │
  │  abstract class AppDatabase : RoomDatabase() {                           │
  │      abstract fun userDao(): UserDao                                     │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is the purpose of the Repository Pattern?

  ANSWER:
    It acts as a mediator between different data sources (REST API, local Room database, cache) and the ViewModel. It abstracts the data logic, so the ViewModel doesn't need to know where the data comes from.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the Single Source of Truth (SSOT) principle.

  ANSWER:
    It means the UI always observes data from one definitive source (usually the local Room DB). When data is fetched from the network, it is saved into the DB, which then automatically triggers an update to the UI via a reactive stream (Flow/LiveData).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Retrofit and how does it work under the hood?

  ANSWER:
    Retrofit is a type-safe HTTP client. Under the hood, it uses dynamic proxies and reflection to generate concrete implementations of your API interfaces at runtime, delegating the actual network calls to OkHttp.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why use Room instead of raw SQLite?

  ANSWER:
    Room provides compile-time verification of SQL queries (preventing runtime crashes for typos), eliminates boilerplate code for converting Cursors to objects, and provides native support for Coroutines and Flow/LiveData.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What does the @Dao annotation do?

  ANSWER:
    It defines a Data Access Object. Room uses this interface to generate the actual code that executes the SQL queries against the database.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle database migrations in Room?

  ANSWER:
    You increment the version number in the @Database annotation and provide a Migration object that executes the necessary SQL (like ALTER TABLE) to move from the old schema version to the new one.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is OkHttp and how does it relate to Retrofit?

  ANSWER:
    OkHttp is the underlying HTTP client that actually makes the network requests. Retrofit is just a wrapper on top of OkHttp that handles URL construction, serialization/deserialization (JSON to Kotlin objects), and coroutine support.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Explain the OnConflictStrategy.REPLACE in Room.

  ANSWER:
    It's an insertion strategy where, if a row being inserted has the same Primary Key as an existing row, the old row is deleted and replaced with the new one.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I turn a simple Kotlin interface into a powerful network client using dynamic proxies. I rely on my brother OkHttp for the heavy lifting. Who am I?

  SOLUTION:
    Retrofit.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I check your SQL queries while you are still writing code. If you spell a column name wrong, I won't even let the app compile. What am I?

  SOLUTION:
    Room Database.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  // Inside an Activity
  val db = AppDatabase.getInstance(context)
  val users = db.userDao().getAllUsersList() // List<UserEntity>

  SOLUTION:
    Room throws an IllegalStateException if you try to perform synchronous database operations on the Main Thread, as it would cause UI jank or ANRs. Fix: Mark the DAO function as suspend and call it from a Coroutine (Dispatchers.IO).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  // Data class used directly from Retrofit into Room
  @Entity
  data class NetworkUser(
      @PrimaryKey val id: Int,
      val temporaryServerToken: String, // Don't want this in DB!
      val name: String
  )

  SOLUTION:
    Coupling your Network models directly with your Database models (@Entity) is a bad practice. Network APIs change, and you shouldn't pollute your database schema with temporary API fields. Fix: Use separate data classes (UserDto and UserEntity) and map between them in the Repository.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Mobile networks are flaky. A production app must provide an "Offline First" experience, allowing users to view cached data when they have no internet. Mastering Room, Retrofit, and the Repository pattern is the standard way to achieve this robust data flow in Android.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 074: 074 Kotlin Advanced (Using Coroutines and Flow with Room.)
  -> File 076: 076 Activity Fragment Lifecycle (ViewModels consuming the Repository.)

================================================================================
  END OF FILE 079
================================================================================
