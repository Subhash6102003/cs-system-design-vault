================================================================================
  FILE 078: JETPACK COMPOSE ADVANCED
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Advanced Jetpack Compose: Animations, Navigation, and Custom Layouts
  This file takes you beyond basic layouts into building production-ready Compose applications. You will learn about Navigation Compose, implementing complex animations safely, building Custom Layouts using the Layout phase, drawing on the Canvas, and performance optimization for Lazy Lists. Prerequisite: Jetpack Compose Fundamentals.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

NAVIGATION COMPOSE
    The official library for navigating between composables, replacing Fragments entirely.
  ANIMATIONS APIS
    
  ANIMATEDVISIBILITY
    Easiest way to animate appearance/disappearance.
  ANIMATE*ASSTATE
    Simple fire-and-forget animations for single values (Color, Float, Dp).
  TRANSITION
    Manages multiple animations synchronized to a single state change.
  COMPOSE PHASES
    
  1. *COMPOSITION*
    What UI to show (builds the tree).
  2. *LAYOUT*
    Where to place it (measures and places).
  3. *DRAWING*
    How it renders on screen.
  CUSTOM LAYOUT
    Using the Layout composable to manually measure and place children when standard rows/columns aren't enough.
  CANVAS
    A composable that provides a low-level 2D drawing API (DrawScope).
  DERIVEDSTATEOF
    Optimizes performance by only triggering recomposition when a calculated result changes, not every time the raw inputs change.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  THE THREE PHASES OF COMPOSE                                            │
  │                                                                         │
  │  State Change --> 1. COMPOSITION ---> 2. LAYOUT --------> 3. DRAWING ---> Screen Updates│
  │                   (What to show)      (Where to put it)   (How it looks)│
  │                                                                         │
  │  * Optimize by skipping phases!                                         │
  │  * Example: Changing color only triggers Drawing.                       │
  │  * Example: Changing scroll offset only triggers Layout and Drawing.    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Navigation Compose & Arguments                                       │
  │                                                                          │
  │  import androidx.navigation.compose.*                                    │
  │                                                                          │
  │  @Composable                                                             │
  │  fun AppNavigation() {                                                   │
  │      val navController = rememberNavController()                         │
  │                                                                          │
  │      NavHost(navController = navController, startDestination = "home") { │
  │          composable("home") {                                            │
  │              HomeScreen(onNavigate = { id ->                             │
  │                  navController.navigate("profile/$id")                   │
  │              })                                                          │
  │          }                                                               │
  │          composable(                                                     │
  │              route = "profile/{userId}",                                 │
  │              arguments = listOf(navArgument("userId") { type = NavType.IntType })│
  │          ) { backStackEntry ->                                           │
  │              // Extracting argument safely                               │
  │              val userId = backStackEntry.arguments?.getInt("userId") ?: 0│
  │              ProfileScreen(userId)                                       │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Advanced Animations & Performance (derivedStateOf)                   │
  │                                                                          │
  │  import androidx.compose.animation.*                                     │
  │  import androidx.compose.foundation.lazy.*                               │
  │  import androidx.compose.material3.*                                     │
  │  import androidx.compose.runtime.*                                       │
  │                                                                          │
  │  @Composable                                                             │
  │  fun ScrollToTopList(items: List<String>) {                              │
  │      val listState = rememberLazyListState()                             │
  │                                                                          │
  │      // Performance Optimization:                                        │
  │      // If we just read listState.firstVisibleItemIndex in the composable,│
  │      // it would recompose on EVERY pixel scrolled.                      │
  │      // derivedStateOf ensures it only recomposes when the boolean condition flips.│
  │      val showButton by remember {                                        │
  │          derivedStateOf { listState.firstVisibleItemIndex > 5 }          │
  │      }                                                                   │
  │                                                                          │
  │      Box(modifier = Modifier.fillMaxSize()) {                            │
  │          LazyColumn(state = listState) {                                 │
  │              items(items) { item ->                                      │
  │                  Text(text = item, modifier = Modifier.padding(16.dp))   │
  │              }                                                           │
  │          }                                                               │
  │                                                                          │
  │          // AnimatedVisibility handles the enter/exit transitions smoothly│
  │          AnimatedVisibility(                                             │
  │              visible = showButton,                                       │
  │              enter = fadeIn() + slideInVertically(initialOffsetY = { it }),│
  │              exit = fadeOut() + slideOutVertically(targetOffsetY = { it }),│
  │              modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)│
  │          ) {                                                             │
  │              FloatingActionButton(onClick = { /* Scroll to top logic */ }) {│
  │                  Text("Top")                                             │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: What are the three phases of Jetpack Compose?

  ANSWER:
    Composition (determining what composables to call), Layout (measuring and placing them), and Drawing (rendering pixels on the screen).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: When should you use derivedStateOf?

  ANSWER:
    Use it when your UI depends on a rapidly changing state (like scroll position), but you only need to update the UI when that state crosses a specific threshold. It prevents unnecessary recompositions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you animate a size change in Compose?

  ANSWER:
    You can use the Modifier.animateContentSize() modifier. It automatically animates its size when its children change dimensions.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain how Custom Layouts work in Compose.

  ANSWER:
    You use the Layout composable. You are given a list of measurables. You must measure each one exactly once to get placeables. Then you call layout(width, height) { ... } and place each child using placeable.place(x, y).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How do you pass complex objects (like a User object) via Navigation Compose?

  ANSWER:
    It's discouraged. Navigation arguments should be simple IDs (Strings, Ints). The destination screen should use that ID to fetch the complex object from a Repository/ViewModel. (Though technically possible by converting to JSON/Parcelable, it violates SSOT).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is LaunchedEffect and when is it used?

  ANSWER:
    It's a side-effect API that launches a Coroutine scoped to the lifecycle of the composable. It is used to perform suspend functions (like network calls or animations) from within a composable without blocking the UI.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Why is the key parameter important in LazyColumn/LazyRow?

  ANSWER:
    Without keys, Compose identifies items by their position. If an item is added/removed at the top, Compose recomposes the entire list because all positions shifted. Providing a unique ID as a key allows Compose to just move the existing items efficiently.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is Canvas in Compose?

  ANSWER:
    A composable that provides a DrawScope, allowing you to use low-level imperative drawing commands (drawCircle, drawPath, drawRect) directly on the screen, useful for custom graphs or games.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I watch a thousand numbers fly by, but I remain completely silent until the number hits 10. By keeping my mouth shut, I save your battery. What am I?

  SOLUTION:
    derivedStateOf

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am the phase where pixels finally meet the screen. Changing a color invokes me, but changing a width leaves me waiting on my brother. What phase am I?

  SOLUTION:
    The Drawing Phase (Brother is Layout Phase).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  @Composable
  fun MessageList(messages: List<Message>) {
      LazyColumn {
          items(messages) { msg ->
              // Assume formatting dates is a heavy CPU task
              val date = SimpleDateFormat("dd/MM").format(msg.timestamp) 
              Text("${msg.text} - $date")
          }
      }
  }

  SOLUTION:
    Formatting the date inside the items block causes heavy processing on the main thread during scrolling, leading to jank. Fix: Format the data in the ViewModel (or Background thread) before passing it to the UI, or use remember if the input is stable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  val listState = rememberLazyListState()
  // Trying to show a header only when scrolled
  if (listState.firstVisibleItemIndex > 0) {
      Text("Scrolled!")
  }

  SOLUTION:
    Reading firstVisibleItemIndex directly in the composition phase causes the entire screen to recompose on every single pixel of scroll. Fix: Wrap the condition in derivedStateOf.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  While basic Compose is easy to write, poorly written Compose apps perform terribly (jank, battery drain). Mastering derivedStateOf, understanding the Compose phases, and implementing proper keys in Lazy lists separates junior UI devs from Senior Android Engineers.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 077: 077 JetpackCompose Fundamentals (Basic modifiers and state.)
  -> File 074: 074 Kotlin Advanced (Coroutines used inside LaunchedEffect.)

================================================================================
  END OF FILE 078
================================================================================
