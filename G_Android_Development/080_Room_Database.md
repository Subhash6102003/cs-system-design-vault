================================================================================
  FILE 080: Room Database
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. TITLE & OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Room Database

  Room is an abstraction layer over SQLite that allows fluent database access while 
  harnessing the full power of SQLite. As part of Android Jetpack, Room provides 
  compile-time verification of SQL queries, minimizing runtime crashes due to typos 
  in SQL strings. It integrates seamlessly with Kotlin Coroutines, Flow, and LiveData, 
  making it the standard for local data persistence in modern Android applications.

  Prerequisites: Basic knowledge of SQL, Kotlin Coroutines, and the Android context.

  What you'll learn:
  * Room Architecture: @Database, @Entity, @Dao
  * Defining Entities with Primary Keys and Relationships
  * Implementing DAOs for CRUD operations
  * Reactive queries using Kotlin Flow
  * Using TypeConverters for complex data types
  * Handling Database Migrations safely
  * Room internals and SQLite behavior on Android
  * Testing Room Databases
  * Integration with Paging 3

────────────────────────────────────────────────────────────────────────────────
  2. CORE CONCEPTS & TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Room: An ORM (Object-Relational Mapping) style library for Android that simplifies 
  SQLite database operations.

  @Entity: An annotation that marks a Kotlin data class as a database table. The 
  properties of the class represent the columns of the table.

  @Dao (Data Access Object): An interface containing methods annotated with SQL 
  operations (@Insert, @Update, @Delete, @Query). Room auto-generates the 
  implementation of these methods at compile time.

  @Database: An abstract class that extends RoomDatabase. It serves as the main 
  access point for the underlying SQLite database, holding references to DAOs and 
  defining the database version.

  @PrimaryKey: An annotation applied to a field in an @Entity to designate it as 
  the unique identifier for the row. Can be configured to auto-generate.

  @TypeConverter: Methods that instruct Room how to convert custom data types 
  (like Dates, Enums, or custom objects) into primitive types that SQLite can 
  store (like Long or String).

  Reactive Queries: Queries in a DAO that return observable data streams, such as 
  Flow<T> or LiveData<T>. Room automatically updates the stream whenever the underlying 
  database tables change.

  Migrations: The process of safely altering the database schema (e.g., adding a 
  column) when releasing a new version of the app, without losing existing user data.

  Paging 3: A Jetpack library that loads and displays small chunks of data at a time, 
  which integrates beautifully with Room via PagingSource.

────────────────────────────────────────────────────────────────────────────────
  3. ASCII / TEXT DIAGRAMS
────────────────────────────────────────────────────────────────────────────────

  Room Architecture Data Flow

    ┌─────────────────────────────────────────────────────────┐
    │                        UI / ViewModel                   │
    │  Collects Flow<List<User>> to render data reactively    │
    └─────────────────────────────────────────────────────────┘
                               ^
                               │  Flow / LiveData
                               │
    ┌─────────────────────────────────────────────────────────┐
    │                      Repository                         │
    │  Mediates between network and Room (Single Source of    │
    │  Truth pattern).                                        │
    └─────────────────────────────────────────────────────────┘
          │ (Insert Data)                  ^ (Read Data)
          V                                │
    ┌─────────────────────────────────────────────────────────┐
    │                     Room @Dao                           │
    │  UserDao: @Insert, @Query("SELECT * FROM users")        │
    └─────────────────────────────────────────────────────────┘
          │                                ^
          V                                │
    ┌─────────────────────────────────────────────────────────┐
    │                   Room @Database                        │
    │  AppDatabase (Version, Entities declaration)            │
    └─────────────────────────────────────────────────────────┘
          │                                ^
          V                                │
    ┌─────────────────────────────────────────────────────────┐
    │                       SQLite                            │
    │  On-device file storage (e.g., /data/data/pkg/app.db)   │
    └─────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Snippet 1: Defining an Entity and TypeConverter
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ @Entity(tableName = "users_table")                                           │
│ data class UserEntity(                                                       │
│     @PrimaryKey(autoGenerate = true)                                         │
│     val id: Int = 0,                                                         │
│     @ColumnInfo(name = "full_name")                                          │
│     val fullName: String,                                                    │
│     val birthDate: Date                                                      │
│ )                                                                            │
│                                                                              │
│ // SQLite doesn't understand Date objects natively.                          │
│ class DateConverters {                                                       │
│     @TypeConverter                                                           │
│     fun fromTimestamp(value: Long?): Date? {                                 │
│         return value?.let { Date(it) }                                       │
│     }                                                                        │
│                                                                              │
│     @TypeConverter                                                           │
│     fun dateToTimestamp(date: Date?): Long? {                                │
│         return date?.time                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

  Snippet 2: The Data Access Object (DAO)
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ @Dao                                                                         │
│ interface UserDao {                                                          │
│                                                                              │
│     // Suspend function for one-shot operations                              │
│     @Insert(onConflict = OnConflictStrategy.REPLACE)                         │
│     suspend fun insertUser(user: UserEntity)                                 │
│                                                                              │
│     @Delete                                                                  │
│     suspend fun deleteUser(user: UserEntity)                                 │
│                                                                              │
│     // Flow for reactive streams (NOT suspend)                               │
│     @Query("SELECT * FROM users_table ORDER BY full_name ASC")               │
│     fun getAllUsers(): Flow<List<UserEntity>>                                │
│                                                                              │
│     // Compile-time checked query with parameters                            │
│     @Query("SELECT * FROM users_table WHERE id = :userId")                   │
│     suspend fun getUserById(userId: Int): UserEntity?                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION-READY CODE
────────────────────────────────────────────────────────────────────────────────

  Below is a complete implementation showing Database creation, DI (Hilt) integration, 
  and Migrations.

┌──────────────────────────────────────────────────────────────────────────────┐
│ // 1. Database Definition                                                    │
│ @Database(                                                                   │
│     entities = [UserEntity::class],                                          │
│     version = 2,                                                             │
│     exportSchema = true                                                      │
│ )                                                                            │
│ @TypeConverters(DateConverters::class)                                       │
│ abstract class AppDatabase : RoomDatabase() {                                │
│     abstract fun userDao(): UserDao                                          │
│ }                                                                            │
│                                                                              │
│ // 2. Migrations                                                             │
│ // Migration from version 1 to 2 (e.g., adding an age column)                │
│ val MIGRATION_1_2 = object : Migration(1, 2) {                               │
│     override fun migrate(database: SupportSQLiteDatabase) {                  │
│         database.execSQL("ALTER TABLE users_table ADD COLUMN age INTEGER NOT NULL DEFAULT 0")
│     }                                                                        │
│ }                                                                            │
│                                                                              │
│ // 3. Dependency Injection (Hilt Module)                                     │
│ @Module                                                                      │
│ @InstallIn(SingletonComponent::class)                                        │
│ object DatabaseModule {                                                      │
│                                                                              │
│     @Provides                                                                │
│     @Singleton                                                               │
│     fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
│         return Room.databaseBuilder(                                         │
│             context,                                                         │
│             AppDatabase::class.java,                                         │
│             "my_production_database.db"                                      │
│         )                                                                    │
│         .addMigrations(MIGRATION_1_2)                                        │
│         .fallbackToDestructiveMigration() // Use carefully in production!    │
│         .build()                                                             │
│     }                                                                        │
│                                                                              │
│     @Provides                                                                │
│     fun provideUserDao(database: AppDatabase): UserDao {                     │
│         return database.userDao()                                            │
│     }                                                                        │
│ }                                                                            │
│                                                                              │
│ // 4. Repository Implementation                                              │
│ class UserRepositoryImpl @Inject constructor(                                │
│     private val userDao: UserDao                                             │
│ ) : UserRepository {                                                         │
│     override fun getReactiveUsers(): Flow<List<User>> {                      │
│         return userDao.getAllUsers().map { entityList ->                     │
│             entityList.map { it.toDomain() }                                 │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What happens if you run a Room Database query on the main thread?
  ANSWER: By default, Room will throw an IllegalStateException. Database operations 
  can be slow and block the main thread, causing ANRs (Application Not Responding). 
  Room enforces thread safety by requiring database access to happen on background 
  threads (via Coroutines, RxJava, or Executor services) unless explicitly bypassed 
  with `allowMainThreadQueries()` (which should only be used for testing).

  Q2: How does Room compile-time checking work?
  ANSWER: Room uses an annotation processor (KAPT/KSP) to analyze @Dao interfaces 
  and @Database classes at compile time. It validates SQL syntax inside @Query 
  annotations and checks that the returned types match the expected column outputs. 
  If a query has a typo, the build fails with a helpful error message.

  Q3: What is the significance of the `exportSchema` property in @Database?
  ANSWER: When `exportSchema = true`, Room generates a JSON file at compile time 
  detailing the exact database schema. These schema files should be committed to 
  version control so developers can track changes over time and test migrations 
  safely using the `MigrationTestHelper`.

  Q4: How does returning a Flow from a DAO work under the hood?
  ANSWER: Room automatically implements an invalidation tracker. When you return 
  a Flow from a query, Room creates a background observer on the database tables 
  used in that query. Whenever a write operation (Insert/Update/Delete) occurs on 
  those tables, the tracker notifies the Flow to re-query the database and emit 
  the new results to the collector.

  Q5: Explain how `fallbackToDestructiveMigration()` works.
  ANSWER: If Room detects a version upgrade but no explicit `Migration` has been 
  provided mapping the old version to the new version, the app will crash. If you 
  use `fallbackToDestructiveMigration()`, Room will instead drop all tables and 
  recreate them, resulting in a total loss of local data, but preventing a crash.

  Q6: How does Room integrate with Jetpack Paging 3?
  ANSWER: You can return a `PagingSource<Int, Entity>` directly from a DAO `@Query`. 
  The Paging library uses this source to request specific pages of data from the 
  database using SQL LIMIT and OFFSET behind the scenes, allowing you to load massive 
  lists efficiently into a LazyColumn or RecyclerView.

  Q7: How do you handle One-to-Many relationships in Room?
  ANSWER: Room handles relationships via intermediate data classes. You use the 
  `@Relation` annotation in a data class that maps a parent entity to its child 
  entities. When you write a DAO query to fetch this composite data class, Room 
  automatically runs additional queries to fetch the associated children. Note: you 
  must annotate the query with `@Transaction` to ensure consistency.

  Q8: Why would you use the @Transaction annotation in a DAO?
  ANSWER: First, to ensure multiple operations (like inserting a user and then 
  inserting their preferences) succeed or fail as a single atomic unit. Second, 
  Room requires it when querying data classes that use `@Relation`, to ensure the 
  parent and child rows are fetched without being modified by another thread mid-query.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & "WHAT'S WRONG WITH THIS CODE?"
────────────────────────────────────────────────────────────────────────────────

  Challenge 1: The Infinite Loop Flow
  Context: A developer wants to fetch data, manipulate it, and save it back.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ class UserRepo(val dao: UserDao) {                                           │
│     fun syncUsers() {                                                        │
│         CoroutineScope(Dispatchers.IO).launch {                              │
│             dao.getAllUsersFlow().collect { users ->                         │
│                 val modified = users.map { it.copy(age = it.age + 1) }       │
│                 dao.insertAll(modified)                                      │
│             }                                                                │
│         }                                                                    │
│     }                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: This causes an infinite loop! `getAllUsersFlow()` emits whenever 
  the table changes. Inside the `collect` block, the developer inserts data, which 
  modifies the table, causing the Flow to emit again immediately, repeating forever. 
  For one-off sync logic, use a suspend function returning `List<UserEntity>`, not 
  a Flow.

  Challenge 2: The Suspended Flow
  Context: Defining a DAO interface.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ @Dao                                                                         │
│ interface ProductDao {                                                       │
│     @Query("SELECT * FROM products")                                         │
│     suspend fun getProductsFlow(): Flow<List<Product>>                       │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: You cannot use `suspend` with `Flow` in Room. A suspend function 
  returns a single async value and finishes. A Flow is a continuous stream that 
  does not block the thread when requested. Remove the `suspend` keyword.

  Challenge 3: The Missing Transaction
  Context: Querying a relationship.
  
┌──────────────────────────────────────────────────────────────────────────────┐
│ data class UserWithPlaylists(                                                │
│     @Embedded val user: User,                                                │
│     @Relation(                                                               │
│         parentColumn = "userId",                                             │
│         entityColumn = "userOwnerId"                                         │
│     )                                                                        │
│     val playlists: List<Playlist>                                            │
│ )                                                                            │
│                                                                              │
│ @Dao                                                                         │
│ interface UserDao {                                                          │
│     @Query("SELECT * FROM users")                                            │
│     fun getUsersWithPlaylists(): List<UserWithPlaylists>                     │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
  Explanation: The query `getUsersWithPlaylists` lacks the `@Transaction` annotation. 
  Since Room actually runs two separate queries to build this relationship (one for 
  Users, one for Playlists), without a transaction, the database could change between 
  the two queries, leading to inconsistent data. Add `@Transaction` above `@Query`.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Offline-First Architecture is critical for modern mobile apps. Users expect 
  apps to launch immediately and display cached data while background requests 
  fetch fresh content. Room makes implementing the "Single Source of Truth" pattern 
  (where UI observes Room, and network calls only update Room) safe, reactive, 
  and highly performant. Furthermore, its compile-time safety eliminates a massive 
  category of bugs related to raw SQLite execution.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  * 017_B_Plus_Trees.md - Deep dive into how SQLite indexes work under the hood.
  * 028_PostgreSQL.md - Compare Android's embedded SQLite behavior to a dedicated server RDBMS.
  * 079_Android_MVVM_CleanArch.md - How Room fits into the Data Layer of Clean Architecture.

================================================================================
  END OF FILE 080
================================================================================
