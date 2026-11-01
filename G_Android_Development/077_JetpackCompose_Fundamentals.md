================================================================================
  FILE 077: JETPACK COMPOSE FUNDAMENTALS
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Jetpack Compose: Declarative UI and State Management
  This file introduces Jetpack Compose, modern Android's declarative UI toolkit. You will learn the shift from imperative XML to declarative Kotlin, how @Composable functions work under the hood, state management (remember, mutableStateOf), recomposition mechanics, and basic UI layouts. Prerequisite: Kotlin fundamentals.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

DECLARATIVE UI
    You describe *what* the UI should look like for a given state, rather than explicitly telling it *how* to mutate (like setText(), setVisibility()).
  @COMPOSABLE
    An annotation that tells the Compose compiler plugin this function converts data into UI.
  RECOMPOSITION
    The process of calling composable functions again when inputs/state change to update the UI. Compose is "smart" and skips functions whose inputs haven't changed.
  STATE HOISTING
    Moving state up to a caller to make a composable stateless, promoting reusability and easier testing.
  REMEMBER
    Stores an object in the composition, returning the stored value during recomposition (survives recomposition).
  REMEMBERSAVEABLE
    Similar to remember, but also survives Activity configuration changes (like rotation) by saving into a Bundle.
  MODIFIERS
    Objects used to decorate or add behavior to UI elements (padding, click listeners, sizing).
  SIDE EFFECTS
    Operations that escape the scope of a composable (e.g., launching a coroutine, showing a Snackbar).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  STATE FLOW IN COMPOSE (UNIDIRECTIONAL DATA FLOW)                       │
  │                                                                         │
  │        +-------------------------+                                      │
  │        |        ViewModel        |                                      │
  │        |   (Holds UI State)      |                                      │
  │        +------------+------------+                                      │
  │                     |                                                   │
  │       State (flows down as params)                                      │
  │                     |                                                   │
  │                     v                                                   │
  │        +------------+------------+                                      │
  │        |   Screen Composable     |                                      │
  │        | (Passes events up)      |                                      │
  │        +------------+------------+                                      │
  │                     |                                                   │
  │       State         |       Events                                      │
  │        |            |         ^                                         │
  │        v            v         |                                         │
  │  +-----+---+   +----+----+    |                                         │
  │  | Text UI |   | Button  +----+                                         │
  │  |         |   | (Click) |                                              │
  │  +---------+   +---------+                                              │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Stateful vs Stateless Composables                                    │
  │                                                                          │
  │  import androidx.compose.runtime.*                                       │
  │  import androidx.compose.material3.*                                     │
  │                                                                          │
  │  // Stateful Composable (Self-contained, harder to test/reuse)           │
  │  @Composable                                                             │
  │  fun CounterStateful() {                                                 │
  │      var count by remember { mutableStateOf(0) }                         │
  │                                                                          │
  │      Button(onClick = { count++ }) {                                     │
  │          Text("Clicked $count times")                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Stateless Composable (State is Hoisted)                              │
  │  @Composable                                                             │
  │  fun CounterStateless(count: Int, onIncrement: () -> Unit) {             │
  │      Button(onClick = onIncrement) {                                     │
  │          Text("Clicked $count times")                                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  │  // Caller manages the state                                             │
  │  @Composable                                                             │
  │  fun Screen() {                                                          │
  │      var count by rememberSaveable { mutableStateOf(0) }                 │
  │      CounterStateless(count = count, onIncrement = { count++ })          │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Basic Layout with Modifiers and Material3                            │
  │                                                                          │
  │  import androidx.compose.foundation.Image                                │
  │  import androidx.compose.foundation.layout.*                             │
  │  import androidx.compose.foundation.shape.CircleShape                    │
  │  import androidx.compose.material3.*                                     │
  │  import androidx.compose.runtime.*                                       │
  │  import androidx.compose.ui.Alignment                                    │
  │  import androidx.compose.ui.Modifier                                     │
  │  import androidx.compose.ui.draw.clip                                    │
  │  import androidx.compose.ui.unit.dp                                      │
  │                                                                          │
  │  @Composable                                                             │
  │  fun UserProfileCard(user: User, onFollowClick: () -> Unit) {            │
  │      // Card acts as a surface with elevation and shape                  │
  │      Card(                                                               │
  │          modifier = Modifier                                             │
  │              .fillMaxWidth()                                             │
  │              .padding(16.dp),                                            │
  │          elevation = CardDefaults.cardElevation(defaultElevation = 4.dp) │
  │      ) {                                                                 │
  │          // Row is a horizontal linear layout                            │
  │          Row(                                                            │
  │              modifier = Modifier                                         │
  │                  .padding(16.dp)                                         │
  │                  .fillMaxWidth(),                                        │
  │              verticalAlignment = Alignment.CenterVertically              │
  │          ) {                                                             │
  │              // Profile Image Placeholder                                │
  │              Box(                                                        │
  │                  modifier = Modifier                                     │
  │                      .size(64.dp)                                        │
  │                      .clip(CircleShape)                                  │
  │              )                                                           │
  │                                                                          │
  │              Spacer(modifier = Modifier.width(16.dp))                    │
  │                                                                          │
  │              // Column is a vertical linear layout                       │
  │              Column(modifier = Modifier.weight(1f)) {                    │
  │                  Text(text = user.name, style = MaterialTheme.typography.titleLarge)│
  │                  Text(text = user.bio, style = MaterialTheme.typography.bodyMedium)│
  │              }                                                           │
  │                                                                          │
  │              Button(onClick = onFollowClick) {                           │
  │                  Text("Follow")                                          │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What is the difference between Imperative UI (XML) and Declarative UI (Compose)?

  ANSWER:
    Imperative requires you to manually mutate the UI tree (textView.text = "Hello"). Declarative means you define what the UI should look like based on the current state; when state changes, the framework redraws (recomposes) the UI automatically.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What does the @Composable annotation do?

  ANSWER:
    It tells the Compose compiler plugin to transform the function into a UI node. It changes the function signature under the hood, passing down an implicit Composer object that tracks state and recomposition.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Recomposition?

  ANSWER:
    When the state a composable depends on changes, Compose calls the function again with the new data to update the UI.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does Smart Recomposition work?

  ANSWER:
    Compose traverses the UI tree during recomposition. If a composable's inputs (parameters) have not changed, Compose skips executing that function entirely, saving CPU cycles.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between remember and rememberSaveable?

  ANSWER:
    remember stores a value across recompositions, but it is lost if the Activity is recreated (e.g., rotation). rememberSaveable saves the value into an OS Bundle, surviving rotation and process death.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why is the order of Modifiers important?

  ANSWER:
    Modifiers wrap the composable sequentially from left to right (or top to bottom). Modifier.padding(10.dp).background(Color.Red) creates a red box with padding *inside*. Modifier.background(Color.Red).padding(10.dp) creates a padded box with the red background *outside* the padding.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is State Hoisting?

  ANSWER:
    A pattern of moving state out of a composable to its caller, replacing the state variable with a parameter (value) and an event lambda ((Type) -> Unit).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Side Effect in Compose?

  ANSWER:
    Any operation that affects the system outside the composable function (e.g., API call, DB write, Toast). Because composables can execute multiple times or out of order, side effects must be wrapped in specific APIs like LaunchedEffect to prevent infinite loops.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I remember your secrets when the UI redraws, but if you flip your phone sideways, I forget it all. Who am I?

  SOLUTION:
    The remember function.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I look like a regular function, but without my special annotation, I cannot draw on the screen. What am I?

  SOLUTION:
    A @Composable function.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  @Composable
  fun UserScreen(viewModel: ViewModel) {
      // Calling API directly in composition
      viewModel.fetchUserData() 

      val uiState by viewModel.state.collectAsState()
      Text("User: ${uiState.name}")
  }

  SOLUTION:
    The UI recomposes when uiState changes. Recomposing calls fetchUserData() again, which updates state, triggering recomposition in an infinite loop. Fix: Wrap the API call in a LaunchedEffect(Unit) { ... }.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  @Composable
  fun MyCheckbox() {
      var isChecked = false // What's wrong?

      Checkbox(
          checked = isChecked,
          onCheckedChange = { isChecked = it }
      )
  }

  SOLUTION:
    When isChecked changes, it doesn't trigger recomposition because it's not a Compose State object. Even if it did, the function would re-run and reset isChecked to false. Fix: var isChecked by remember { mutableStateOf(false) }.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Compose is the future of Android development. Understanding recomposition prevents severe performance bottlenecks (jank). Mastering State Hoisting ensures your UI components are testable and reusable across your app.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 078: 078 JetpackCompose Advanced (Advanced Compose techniques.)
  -> File 074: 074 Kotlin Advanced (Using Coroutines/Flow with Compose.)

================================================================================
  END OF FILE 077
================================================================================
