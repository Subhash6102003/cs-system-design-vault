================================================================================
  FILE 073: KOTLIN FUNDAMENTALS
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Kotlin Fundamentals: Null Safety, Collections, and Scope Functions
  This file covers the foundational features of Kotlin that make it a modern, concise, and safe alternative to Java for Android development. You will learn about Kotlin's strict null safety, data classes, sealed classes, extension functions, standard library collection operations, and the nuances of scope functions (let, run, with, apply, also). Prerequisite: Basic programming knowledge (Java experience is helpful but not required).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

NULL SAFETY
    Kotlin's type system distinguishes between references that can hold null and those that cannot, eliminating the dreaded NullPointerException.
  NULLABLE TYPE (?)
    Suffixing a type with ? (e.g., String?) explicitly allows it to hold null.
  SAFE CALL (?.)
    Executes a method or accesses a property only if the receiver is not null.
  ELVIS OPERATOR (?:)
    Provides a default value if the expression to its left is null.
  DATA CLASS
    A class explicitly designed to hold data, automatically generating equals(), hashCode(), toString(), and copy().
  SEALED CLASS/INTERFACE
    Represents restricted class hierarchies, useful for defining a strict set of possible states (exhaustive when).
  EXTENSION FUNCTION
    Allows you to add new functions to existing classes without modifying their source code.
  SCOPE FUNCTIONS
    Functions whose sole purpose is to execute a block of code within the context of an object (let, run, with, apply, also).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  SCOPE FUNCTIONS DECISION MATRIX                                        │
  │                                                                         │
  │  Does the block return the Context Object or the Lambda Result?         │
  │                                                                         │
  │  +-------------------+----------------------+---------------------+     │
  │  | Context Object is | Returns Context Obj  | Returns Lambda Res  |     │
  │  +-------------------+----------------------+---------------------+     │
  │  | accessed via 'it' |        also          |         let         |     │
  │  +-------------------+----------------------+---------------------+     │
  │  | accessed via 'this'|       apply         |     run / with      |     │
  │  +-------------------+----------------------+---------------------+     │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Null Safety Operators                                                │
  │                                                                          │
  │  fun processName(name: String?) {                                        │
  │      // 1. Safe Call: Length will be null if name is null                │
  │      val length: Int? = name?.length                                     │
  │                                                                          │
  │      // 2. Elvis Operator: If name is null, use "Unknown"                │
  │      val validName: String = name ?: "Unknown"                           │
  │                                                                          │
  │      // 3. Safe Cast: Returns null if it's not an Int                    │
  │      val ageObj: Any = "25"                                              │
  │      val ageInt: Int? = ageObj as? Int                                   │
  │                                                                          │
  │      // 4. Not-Null Assertion: Throws NPE if name is null (AVOID THIS)   │
  │      // val forceLength: Int = name!!.length                             │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

  [Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Data and Sealed Classes                                              │
  │                                                                          │
  │  // Automatically gets equals, hashCode, toString, copy                  │
  │  data class User(val id: Int, val name: String)                          │
  │                                                                          │
  │  // Restricted hierarchy for state management                            │
  │  sealed class UIState {                                                  │
  │      object Loading : UIState()                                          │
  │      data class Success(val data: List<User>) : UIState()                │
  │      data class Error(val message: String) : UIState()                   │
  │  }                                                                       │
  │                                                                          │
  │  fun render(state: UIState) {                                            │
  │      // 'when' expression is exhaustive; no 'else' required              │
  │      when (state) {                                                      │
  │          is UIState.Loading -> showSpinner()                             │
  │          is UIState.Success -> showList(state.data)                      │
  │          is UIState.Error -> showError(state.message)                    │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Advanced Collections and Scope Functions                             │
  │                                                                          │
  │  data class Order(val id: String, val amount: Double, val isDelivered: Boolean)│
  │                                                                          │
  │  fun processOrders(orders: List<Order>?) {                               │
  │      // Using let to handle nullability safely                           │
  │      orders?.let { safeOrders ->                                         │
  │          // Collection operations: filter, map, fold                     │
  │          val totalDeliveredRevenue = safeOrders                          │
  │              .filter { it.isDelivered }                                  │
  │              .map { it.amount }                                          │
  │              .fold(0.0) { acc, amount -> acc + amount }                  │
  │                                                                          │
  │          println("Total Revenue: $totalDeliveredRevenue")                │
  │      }                                                                   │
  │                                                                          │
  │      // Using apply for object configuration                             │
  │      val newOrder = Order("ord_123", 99.99, false).apply {               │
  │          // setup logic here, 'this' refers to the Order instance        │
  │          // E.g., Database.save(this)                                    │
  │          println("Created order with ID: $id")                           │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Explain the difference between val and var.

  ANSWER:
    val (value) declares a read-only (immutable) reference, similar to final in Java. var (variable) declares a mutable reference.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the Elvis operator and when do you use it?

  ANSWER:
    ?: is the Elvis operator. It returns the left-hand side if it is not null; otherwise, it evaluates and returns the right-hand side. Used for assigning default values when dealing with nullable types.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the difference between == and === in Kotlin?

  ANSWER:
    == checks for structural equality (calls .equals() under the hood). === checks for referential equality (checks if both references point to the exact same object in memory).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why are Data Classes useful?

  ANSWER:
    They reduce boilerplate by automatically generating equals(), hashCode(), toString(), and copy() methods based on the primary constructor properties.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does a Sealed Class differ from an Enum?

  ANSWER:
    Enums represent a set of identical constants. Sealed classes allow subclasses to have multiple instances and different state/properties (e.g., Success holding data, Error holding a message).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the difference between let and apply.

  ANSWER:
    let refers to the context object as it and returns the result of the lambda. apply refers to the context object as this and returns the context object itself.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an Extension Function?

  ANSWER:
    A feature allowing you to add methods to existing classes (even final ones like String) without inheriting from them. e.g., fun String.isEmail(): Boolean = ...

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What does the !! operator do?

  ANSWER:
    The not-null assertion operator forces a nullable type to a non-null type, throwing a NullPointerException if the value is null. Its use is highly discouraged.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I let you pretend you own a class you didn't write. You attach new behaviors to me, but under the hood, I'm just a static disguise. What am I?

  SOLUTION:
    An Extension Function.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am the strict bouncer of Kotlin. If you try to enter without a question mark, I won't let you hold nothing. What am I?

  SOLUTION:
    Null Safety (Non-nullable types).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  fun printLength(text: String?) {
      val length = text?.length ?: throw IllegalArgumentException("Text is null")
      val upper = text!!.toUpperCase() // What's wrong?
  }

  SOLUTION:
    The exception will catch the null, making text!! logically safe here, but using !! is a bad practice. Kotlin's smart cast won't promote text to non-null because the Elvis operator threw an exception implicitly. Better: requireNotNull(text) { "Text is null" }; val upper = text.toUpperCase()

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  class Person(val name: String) // Not a data class
  val p1 = Person("Alice")
  // val p2 = p1.copy(name = "Bob") // Unresolved reference: copy

  SOLUTION:
    The copy() function is only automatically generated for data class. Change class Person to data class Person.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Kotlin's null safety single-handedly eradicates a massive class of crashes (NPEs) that plague Java Android apps. Utilizing sealed classes for UI state and scope functions for concise data manipulation results in code that is incredibly robust, readable, and less prone to logic errors.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 074: 074 Kotlin Advanced (For advanced Kotlin features like Coroutines.)
  -> File 076: 076 Activity Fragment Lifecycle (Using Kotlin to manage Android components.)

================================================================================
  END OF FILE 073
================================================================================
