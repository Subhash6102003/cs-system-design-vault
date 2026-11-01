================================================================================
  FILE 081: RETROFIT & OKHTTP
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Retrofit & OkHttp: The Android Networking Stack
  Modern Android networking is overwhelmingly powered by two Square libraries: OkHttp (the HTTP client) and Retrofit (the type-safe REST client built on top of OkHttp). This guide covers how to architect a robust, production-ready network layer, manage authentication intercepts, connection pooling, and handle API parsing using Kotlin Coroutines and Serialization.
  Prerequisites: Understanding of HTTP protocols, REST APIs, JSON, and Kotlin Coroutines.
  What you'll learn: Retrofit annotations, Converter Factories, OkHttp Interceptor chains, Token Refresh logic, and configuring Connection Pools and Timeouts.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  OKHTTP
    A highly efficient HTTP client that handles connection pooling, gzip compression, caching, and HTTP/2 multiplexing natively.

  RETROFIT
    A type-safe HTTP client for Android and Java. It uses annotations to translate Kotlin interfaces into concrete HTTP requests, wrapping OkHttp calls.

  CALL<T>
    The core Retrofit object representing a single HTTP request and its response. Modern Kotlin apps usually replace this with suspend functions returning the parsed model or Response<T>.

  CONVERTER FACTORY
    Responsible for parsing raw HTTP response bodies (JSON/XML) into Kotlin objects. Popular choices: GsonConverterFactory, MoshiConverterFactory, KotlinXSerializationConverterFactory.

  INTERCEPTOR
    An OkHttp concept. A hook that can observe, modify, and short-circuit requests going out and responses coming in.

  APPLICATION INTERCEPTOR
    Runs once per execute() call. Good for logging and adding application-level headers.

  NETWORK INTERCEPTOR
    Runs directly over the network wire. It runs multiple times for redirects/retries. Good for observing exact bytes or caching.

  AUTHENTICATOR
    A special OkHttp interface designed specifically to handle 401 Unauthorized responses and seamlessly refresh tokens.

  CERTIFICATE PINNING
    Hardcoding the hash of the server's public key (or certificate) into the app to prevent Man-in-the-Middle (MITM) attacks, even if the device trusts a malicious root CA.

  CONNECTION POOLING
    Keeping HTTP connections open for reuse to save on the heavy TCP/TLS handshake overhead for subsequent requests.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  RETROFIT & OKHTTP REQUEST PIPELINE                                     │
  │                                                                         │
  │    [App Layer] -> `api.getUser("123")`                                  │
  │         |                                                               │
  │         v                                                               │
  │    +---------------------------------------------------+                │
  │    |                  Retrofit                         |                │
  │    |  - Reads @GET, @Path annotations                  |                │
  │    |  - Serializes request body (Converter)            |                │
  │    +------------------------+--------------------------+                │
  │                             | builds Request object                     │
  │    +------------------------v--------------------------+                │
  │    |                   OkHttp Core                     |                │
  │    |                                                   |                │
  │    |  [ Application Interceptors ] (Logging, Headers)  |                │
  │    |                 |                                 |                │
  │    |  [ Cache Interceptor ] (Checks local disk cache)  |                │
  │    |                 |                                 |                │
  │    |  [ Network Interceptors ] (Low-level network)     |                │
  │    |                 |                                 |                │
  │    |  [ Connection Pool ] (Reuses TCP/TLS sockets)     |                │
  │    +------------------------+--------------------------+                │
  │                             |                                           │
  │                       (Network Wire)                                    │
  │                             |                                           │
  │                       [Remote Server]                                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Retrofit Interface and Annotations                                   │
  │                                                                          │
  │  interface TwitterApi {                                                  │
  │      // Basic GET request with a query parameter                         │
  │      @GET("tweets")                                                      │
  │      suspend fun getTweets(@Query("author") authorId: String): List<TweetDto>│
  │                                                                          │
  │      // Dynamic URL path parameter                                       │
  │      @GET("users/{id}")                                                  │
  │      suspend fun getUserProfile(@Path("id") userId: String): UserDto     │
  │                                                                          │
  │      // POST request with a JSON body                                    │
  │      @POST("tweets")                                                     │
  │      suspend fun createTweet(@Body request: CreateTweetRequest): TweetDto│
  │                                                                          │
  │      // Multipart request (Uploading an image)                           │
  │      @Multipart                                                          │
  │      @POST("media/upload")                                               │
  │      suspend fun uploadImage(                                            │
  │          @Part("description") description: RequestBody,                  │
  │          @Part image: MultipartBody.Part                                 │
  │      ): MediaUploadResponse                                              │
  │                                                                          │
  │      // Custom Headers                                                   │
  │      @Headers(                                                           │
  │          "Cache-Control: max-age=640000",                                │
  │          "User-Agent: MyAndroidApp"                                      │
  │      )                                                                   │
  │      @GET("config")                                                      │
  │      suspend fun getServerConfig(): ConfigDto                            │
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
  │  // 1. Auth Interceptor (Attaches Tokens)                                │
  │  // ==========================================                           │
  │  class AuthInterceptor(private val tokenManager: TokenManager) : Interceptor {│
  │      override fun intercept(chain: Interceptor.Chain): Response {        │
  │          val originalRequest = chain.request()                           │
  │                                                                          │
  │          // Don't add token to login/register endpoints                  │
  │          if (originalRequest.url.encodedPath.contains("/auth/")) {       │
  │              return chain.proceed(originalRequest)                       │
  │          }                                                               │
  │                                                                          │
  │          val token = tokenManager.getAccessToken()                       │
  │          val requestBuilder = originalRequest.newBuilder()               │
  │              .header("Authorization", "Bearer $token")                   │
  │                                                                          │
  │          return chain.proceed(requestBuilder.build())                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 2. Authenticator (Handles 401 Token Refresh)                         │
  │  // ==========================================                           │
  │  class TokenAuthenticator(                                               │
  │      private val tokenManager: TokenManager,                             │
  │      private val authApiProvider: () -> AuthApi // Lazy provider to avoid circular dependencies│
  │  ) : Authenticator {                                                     │
  │                                                                          │
  │      override fun authenticate(route: Route?, response: Response): Request? {│
  │          // If the request itself was a refresh call that failed, don't loop forever.│
  │          if (response.request.url.encodedPath.contains("/auth/refresh")) {│
  │              tokenManager.clearTokens() // Force logout                  │
  │              return null                                                 │
  │          }                                                               │
  │                                                                          │
  │          synchronized(this) {                                            │
  │              // Check if token was refreshed by another thread while this thread was waiting│
  │              val currentToken = tokenManager.getAccessToken()            │
  │              val previousToken = response.request.header("Authorization")?.removePrefix("Bearer ")│
  │                                                                          │
  │              if (currentToken != null && currentToken != previousToken) {│
  │                  // Another thread refreshed the token, just retry with the new one│
  │                  return response.request.newBuilder()                    │
  │                      .header("Authorization", "Bearer $currentToken")    │
  │                      .build()                                            │
  │              }                                                           │
  │                                                                          │
  │              // Perform synchronous refresh network call using OkHttp (avoid suspend here)│
  │              val refreshCall = authApiProvider().refreshToken(           │
  │                  RefreshRequest(tokenManager.getRefreshToken())          │
  │              ).execute()                                                 │
  │                                                                          │
  │              if (refreshCall.isSuccessful) {                             │
  │                  val newTokens = refreshCall.body()                      │
  │                  if (newTokens != null) {                                │
  │                      tokenManager.saveTokens(newTokens.access, newTokens.refresh)│
  │                      return response.request.newBuilder()                │
  │                          .header("Authorization", "Bearer ${newTokens.access}")│
  │                          .build()                                        │
  │                  }                                                       │
  │              }                                                           │
  │                                                                          │
  │              // Refresh failed, log user out                             │
  │              tokenManager.clearTokens()                                  │
  │              return null                                                 │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // ==========================================                           │
  │  // 3. Dependency Injection Module (Hilt example)                        │
  │  // ==========================================                           │
  │  @Module                                                                 │
  │  @InstallIn(SingletonComponent::class)                                   │
  │  object NetworkModule {                                                  │
  │                                                                          │
  │      @Provides                                                           │
  │      @Singleton                                                          │
  │      fun provideOkHttpClient(                                            │
  │          authInterceptor: AuthInterceptor,                               │
  │          authenticator: TokenAuthenticator                               │
  │      ): OkHttpClient {                                                   │
  │          val logging = HttpLoggingInterceptor().apply {                  │
  │              level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY│
  │                      else HttpLoggingInterceptor.Level.NONE              │
  │          }                                                               │
  │                                                                          │
  │          return OkHttpClient.Builder()                                   │
  │              .addInterceptor(authInterceptor)                            │
  │              .addInterceptor(logging)                                    │
  │              .authenticator(authenticator)                               │
  │              .connectTimeout(15, TimeUnit.SECONDS)                       │
  │              .readTimeout(15, TimeUnit.SECONDS)                          │
  │              .writeTimeout(15, TimeUnit.SECONDS)                         │
  │              .connectionPool(ConnectionPool(5, 5, TimeUnit.MINUTES)) // Keep max 5 idle connections│
  │              .build()                                                    │
  │      }                                                                   │
  │                                                                          │
  │      @Provides                                                           │
  │      @Singleton                                                          │
  │      fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {         │
  │          val json = Json { ignoreUnknownKeys = true }                    │
  │                                                                          │
  │          return Retrofit.Builder()                                       │
  │              .baseUrl("https://api.production-server.com/v1/")           │
  │              .client(okHttpClient)                                       │
  │              .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))│
  │              .build()                                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between an Application Interceptor and a Network Interceptor?

  ANSWER:
    Application interceptors are triggered exactly once per request, regardless of whether it's served from cache, redirects, or fails. Network interceptors run just before the data goes over the wire; they will NOT run if a request is fulfilled via disk cache, but they WILL run multiple times if there are network redirects or retries.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How do you handle Token Expiration (401 Unauthorized)?

  ANSWER:
    By implementing OkHttp's Authenticator interface. When OkHttp sees a 401, it calls authenticate(). Inside, you block the thread, securely request a new token, update the local storage, and return the original request with the new Authorization header. OkHttp will automatically retry the request.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why should you use suspend functions instead of Call<T> in Retrofit?

  ANSWER:
    Call<T> requires dealing with callbacks (enqueue) or manual threading (execute). suspend functions natively integrate with Coroutines, suspending execution on a background thread without blocking it, and directly returning the parsed result or throwing an exception in a try-catch block, resulting in cleaner, imperative-style code.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is OkHttp Connection Pooling?

  ANSWER:
    TCP handshakes and TLS negotiations are expensive. OkHttp maintains a ConnectionPool that keeps idle connections open for a specific duration (default 5 minutes). Subsequent requests to the same host can reuse these connections, drastically reducing latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does Retrofit work under the hood?

  ANSWER:
    Retrofit uses Java's Proxy class to dynamically generate implementations of your API interfaces at runtime. It inspects the annotations via reflection, constructs an OkHttp Request, sends it via an OkHttpClient, and uses the ConverterFactory to map the ResponseBody back to objects.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you cancel a Retrofit request?

  ANSWER:
    If using suspend functions, canceling the Coroutine Job running the request automatically cancels the underlying OkHttp call. If using Call<T>, you manually invoke call.cancel().

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Certificate Pinning and how do you implement it in OkHttp?

  ANSWER:
    Certificate Pinning ensures your app only communicates with servers holding a specific certificate, preventing MITM attacks. You implement it using OkHttp's CertificatePinner class, passing the host domain and the SHA-256 hash of the public key.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you send a file using Retrofit?

  ANSWER:
    Use the @Multipart annotation on the function. Pass the file as a MultipartBody.Part parameter.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The UI Blocker

  @GET("users")
  fun getUsers(): Call<List<User>>
  
  // Inside Activity onCreate:
  val response = api.getUsers().execute()
  textView.text = response.body().toString()

  SOLUTION:
    Problem: execute() is synchronous. It runs the network call on the main thread, throwing a NetworkOnMainThreadException and instantly crashing the app.
    Fix: Use suspend fun getUsers(): List<User> and call it from a viewModelScope.launch, or use enqueue() for callback-based async execution.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Infinite Token Loop

  class MyAuthenticator : Authenticator {
      override fun authenticate(route: Route?, response: Response): Request? {
          val newToken = fetchNewTokenSynchronously()
          return response.request.newBuilder().header("Authorization", newToken).build()
      }
  }

  SOLUTION:
    Problem: If the fetchNewTokenSynchronously() call fails or returns an invalid token, OkHttp will retry the request with the "new" token, receive another 401, call authenticate again, resulting in an infinite loop that drains battery and hammers the server.
    Fix: Always check the response's retry count, or ensure the endpoint that failed wasn't the refresh endpoint itself. If refresh fails, return null to fail the request and log the user out.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Forgotten Slash

  val retrofit = Retrofit.Builder()
      .baseUrl("https://api.example.com/v1") // Notice no trailing slash
      .build()
  
  interface Api {
      @GET("users") // Notice no leading slash
      suspend fun getUsers()
  }

  SOLUTION:
    Problem: Retrofit throws an IllegalArgumentException at runtime: baseUrl must end in /.
    Fix: Always end your base URL with a slash: https://api.example.com/v1/.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Mobile networks are inherently unreliable (changing from 5G to 3G, traversing dead zones). Robust OkHttp configurations handle retries, timeouts, and connection reuse invisibly, ensuring the app feels fast. Furthermore, centralized Interceptors and Authenticators decouple complex token management from the UI layer, preventing bug-prone duplicate logic across ViewModels.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 079: Android MVVM & Clean Arch (relationship description)
  -> File 082: Hilt Dependency Injection (relationship description)
  -> File 085: Offline-First Sync Architecture (relationship description)

================================================================================
  END OF FILE 081
================================================================================
