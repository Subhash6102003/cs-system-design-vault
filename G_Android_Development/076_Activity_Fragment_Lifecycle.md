================================================================================
  FILE 076: ACTIVITY & FRAGMENT LIFECYCLE
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  The Android Lifecycle: Activities, Fragments, and State Survival
  This file covers the complex lifecycles of Android UI components. You will learn the exact sequence of Activity and Fragment callbacks, how to handle configuration changes (like screen rotations), how to simulate process death, and how ViewModels interact with these lifecycles to preserve data. Prerequisite: Basic Android app structure.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

ACTIVITY
    A single screen with a user interface.
  FRAGMENT
    A reusable portion of UI within an Activity.
  CONFIGURATION CHANGE
    Hardware/software changes (rotation, keyboard, language) that cause the system to destroy and recreate the Activity by default.
  PROCESS DEATH
    The system killing your app's process while it is in the background to reclaim memory.
  VIEWMODEL
    A class designed to store and manage UI-related data in a lifecycle conscious way. It survives configuration changes.
  ONSAVEINSTANCESTATE
    A callback used to save small, primitive UI state (like scroll position or partial form data) into a Bundle before destruction.
  SAVEDSTATEHANDLE
    A key-value map within a ViewModel that survives both configuration changes *and* process death.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  ACTIVITY LIFECYCLE STATE MACHINE                                       │
  │                                                                         │
  │             +---------+                                                 │
  │             | onCreate|                                                 │
  │             +----+----+                                                 │
  │                  |                                                      │
  │             +----+----+                                                 │
  │             | onStart | <---------+                                     │
  │             +----+----+           |                                     │
  │                  |                |                                     │
  │             +----+----+           | User returns                        │
  │             | onResume| <------+  | to app                              │
  │             +----+----+        |  |                                     │
  │                  |             |  |                                     │
  │             (App is running)   |  |                                     │
  │                  |             |  |                                     │
  │     Another app  |        +----+--+-+                                   │
  │  comes to front  +------> | onPause |                                   │
  │                           +----+----+                                   │
  │                                |                                        │
  │    App goes to                 |                                        │
  │    background                  v                                        │
  │                           +---------+                                   │
  │                           | onStop  |                                   │
  │                           +----+----+                                   │
  │                                |                                        │
  │    App is                      |                                        │
  │    finished                    v                                        │
  │                           +---------+                                   │
  │                           |onDestroy|                                   │
  │                           +---------+                                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Basic Activity Lifecycle Logging                                     │
  │                                                                          │
  │  class LifecycleActivity : AppCompatActivity() {                         │
  │      private val TAG = "LifecycleDemo"                                   │
  │                                                                          │
  │      override fun onCreate(savedInstanceState: Bundle?) {                │
  │          super.onCreate(savedInstanceState)                              │
  │          Log.d(TAG, "onCreate: Activity created. savedInstanceState is $savedInstanceState")│
  │      }                                                                   │
  │                                                                          │
  │      override fun onStart() {                                            │
  │          super.onStart()                                                 │
  │          Log.d(TAG, "onStart: UI becoming visible")                      │
  │      }                                                                   │
  │                                                                          │
  │      override fun onResume() {                                           │
  │          super.onResume()                                                │
  │          Log.d(TAG, "onResume: UI is interactive")                       │
  │      }                                                                   │
  │                                                                          │
  │      override fun onPause() {                                            │
  │          super.onPause()                                                 │
  │          Log.d(TAG, "onPause: UI losing focus (partially visible)")      │
  │      }                                                                   │
  │                                                                          │
  │      override fun onStop() {                                             │
  │          super.onStop()                                                  │
  │          Log.d(TAG, "onStop: UI hidden completely")                      │
  │      }                                                                   │
  │                                                                          │
  │      override fun onDestroy() {                                          │
  │          super.onDestroy()                                               │
  │          Log.d(TAG, "onDestroy: Activity memory cleared")                │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Bulletproof State Survival (ViewModel + SavedStateHandle)            │
  │                                                                          │
  │  import androidx.lifecycle.SavedStateHandle                              │
  │  import androidx.lifecycle.ViewModel                                     │
  │  import kotlinx.coroutines.flow.StateFlow                                │
  │                                                                          │
  │  class FormViewModel(                                                    │
  │      private val savedStateHandle: SavedStateHandle,                     │
  │      private val repository: Repository                                  │
  │  ) : ViewModel() {                                                       │
  │                                                                          │
  │      // 1. Survives Config Changes AND Process Death                     │
  │      val username: StateFlow<String> = savedStateHandle.getStateFlow("USERNAME", "")│
  │                                                                          │
  │      fun updateUsername(name: String) {                                  │
  │          savedStateHandle["USERNAME"] = name                             │
  │      }                                                                   │
  │                                                                          │
  │      // 2. Survives Config Changes only (Normal ViewModel data)          │
  │      private var complexDataCache: List<User>? = null                    │
  │                                                                          │
  │      // Called when the Activity/Fragment is FINALLY destroyed (not just rotated)│
  │      override fun onCleared() {                                          │
  │          super.onCleared()                                               │
  │          // Cleanup resources like custom thread pools or streams        │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Walk me through the Activity Lifecycle when an app is opened, sent to the background, and brought back.

  ANSWER:
    Open: onCreate -> onStart -> onResume. Background: onPause -> onStop. Foreground again: onStart -> onResume.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What happens to the lifecycle when the device is rotated?

  ANSWER:
    The current Activity goes through onPause -> onStop -> onDestroy. Then a new instance is created: onCreate -> onStart -> onResume.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between onPause and onStop?

  ANSWER:
    onPause means the Activity has lost focus but is still partially visible (e.g., a transparent dialog opened over it, or multi-window mode). onStop means it is completely hidden from the user.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does a ViewModel survive configuration changes?

  ANSWER:
    The ViewModelStore retains ViewModels. When an Activity undergoes a config change, the system retains the ViewModelStore. The new Activity instance retrieves the exact same ViewModel from the store.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: If a ViewModel survives rotation, why do we need onSaveInstanceState / SavedStateHandle?

  ANSWER:
    ViewModels do NOT survive Process Death (when the system kills background apps). SavedStateHandle serializes data to the OS via IPC, allowing critical UI state (like typed text) to be restored when the user reopens the app from the recents menu.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between Fragment onDestroyView and onDestroy?

  ANSWER:
    onDestroyView is called when the Fragment's UI is removed from the screen (e.g., navigating forward in the backstack). The Fragment instance itself is still alive in memory. onDestroy is called when the Fragment object is completely removed.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How do you test Process Death on an emulator?

  ANSWER:
    Go to Developer Options, enable "Don't keep activities". Background your app, then return to it. Or use adb shell am kill <package-name> while the app is in the background.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is commitAllowingStateLoss in FragmentTransactions?

  ANSWER:
    Normally, committing a transaction after onSaveInstanceState throws an exception to prevent data loss. commitAllowingStateLoss overrides this, but should be used carefully (e.g., dismissing UI after a delayed network call).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I flip the world upside down. I destroy what you've built, only to rebuild it instantly. If you didn't save your work in a ViewModel, I erase it forever. What am I?

  SOLUTION:
    A Configuration Change (Screen Rotation).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  The user left me for another app. The system needed memory. Now I am gone, but my Bundle remains with the OS. What happened to me?

  SOLUTION:
    System Process Death.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  class MyViewModel(val context: Context) : ViewModel() {
      // ...
  }

  // In Activity:
  val viewModel = MyViewModel(this) 

  SOLUTION:
    Passing an Activity context into a ViewModel causes a massive Memory Leak. The ViewModel outlives the Activity during rotation, holding a reference to the old Activity. Fix: Use AndroidViewModel(application) or inject dependencies without Context.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  class MyFragment : Fragment(R.layout.fragment_my) {
      private var myButton: Button? = null

      override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
          myButton = view.findViewById(R.id.btn)
      }

      // Navigating away (fragment put in backstack), then fetching data...
      fun onDataLoaded() {
          myButton?.text = "Loaded" // Memory leak warning?
      }
  }

  SOLUTION:
    When a Fragment is placed in the backstack, onDestroyView is called, destroying the View. However, myButton still holds a strong reference to the destroyed view, causing a memory leak. Fix: Set myButton = null in onDestroyView.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Improper lifecycle handling is the #1 cause of crashes (IllegalStateException, NPEs) and memory leaks in Android apps. Failing to handle process death results in user frustration when they return to an app and find their form data erased.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 075: 075 Android Internals Runtime (Why Process Death occurs.)
  -> File 077: 077 JetpackCompose Fundamentals (How Compose handles state instead of fragments.)

================================================================================
  END OF FILE 076
================================================================================
