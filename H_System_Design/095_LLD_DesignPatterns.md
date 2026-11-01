================================================================================
  FILE 095: LLD & DESIGN PATTERNS
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Low-Level Design (LLD) & Design Patterns focuses on Object-Oriented Design, SOLID principles, and the Gang of Four (GoF) design patterns. Prerequisites include OOP concepts (Inheritance, Polymorphism). You will learn how to write maintainable, extensible code and tackle classic LLD interview questions (Parking Lot, Elevator).

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  SOLID PRINCIPLES
    - S (Single Responsibility): A class should have one reason to change.
    - O (Open/Closed): Open for extension, closed for modification.
    - L (Liskov Substitution): Subclasses should be replaceable for their base classes.
    - I (Interface Segregation): Many client-specific interfaces are better than one general interface.
    - D (Dependency Inversion): Depend on abstractions, not concretions.

  CREATIONAL PATTERNS
    Deal with object creation mechanisms (Singleton, Factory, Builder).

  STRUCTURAL PATTERNS
    Deal with object composition and relationships (Adapter, Decorator, Facade).

  BEHAVIORAL PATTERNS
    Deal with communication between objects (Observer, Strategy, Command).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  OBSERVER PATTERN                                                       │
  │                                                                         │
  │  [ Subject (Publisher) ]                                                │
  │    |-- List<Observer>                                                   │
  │    |-- notify() --------+                                               │
  │                         |                                               │
  │               +---------v---------+                                     │
  │               |                   |                                     │
  │      [ Observer A ]      [ Observer B ]                                 │
  │      |-- update() |      |-- update() |                                 │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  STRATEGY PATTERN                                                       │
  │                                                                         │
  │  [ Context (PaymentProcessor) ] --> holds reference to --> <<Interface Strategy>> (pay)│
  │                                                                   ^     │
  │                                                         __________|__________│
  │                                                        |                     |│
  │                                            [ CreditCardStrategy ]   [ PayPalStrategy ]│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // SOLID: Strategy Pattern adhering to Open/Closed and Dependency Inversion│
  │  interface PaymentStrategy {                                             │
  │      void pay(int amount);                                               │
  │  }                                                                       │
  │                                                                          │
  │  class CreditCardPayment implements PaymentStrategy {                    │
  │      public void pay(int amount) { System.out.println("Paid " + amount + " via CC"); }│
  │  }                                                                       │
  │                                                                          │
  │  class PayPalPayment implements PaymentStrategy {                        │
  │      public void pay(int amount) { System.out.println("Paid " + amount + " via PayPal"); }│
  │  }                                                                       │
  │                                                                          │
  │  // ShoppingCart is CLOSED for modification, OPEN for extension (new payment methods)│
  │  class ShoppingCart {                                                    │
  │      public void checkout(int amount, PaymentStrategy method) {          │
  │          method.pay(amount);                                             │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: java]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  // Thread-Safe Singleton using Double-Checked Locking                   │
  │  public class DatabaseConnection {                                       │
  │      // volatile ensures changes are immediately visible to other threads│
  │      private static volatile DatabaseConnection instance;                │
  │      private String connectionString;                                    │
  │                                                                          │
  │      private DatabaseConnection() {                                      │
  │          // Private constructor prevents instantiation                   │
  │          this.connectionString = "jdbc:mysql://localhost:3306/db";       │
  │      }                                                                   │
  │                                                                          │
  │      public static DatabaseConnection getInstance() {                    │
  │          if (instance == null) { // First check (no locking, fast)       │
  │              synchronized (DatabaseConnection.class) {                   │
  │                  if (instance == null) { // Second check (locked, thread-safe)│
  │                      instance = new DatabaseConnection();                │
  │                  }                                                       │
  │              }                                                           │
  │          }                                                               │
  │          return instance;                                                │
  │      }                                                                   │
  │                                                                          │
  │      public void executeQuery(String query) {                            │
  │          System.out.println("Executing: " + query);                      │
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Design a Parking Lot.

  ANSWER:
    - Entities: ParkingLot (Singleton), Level, ParkingSpot, Vehicle (abstract), Car, Bike.
    - Logic: ParkingSpot has canFitVehicle(). Level manages spots. Ticket tracks entry time. PaymentProcessor uses Strategy (Cash/Card).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Design an Elevator System.

  ANSWER:
    - Entities: ElevatorSystem (dispatcher), ElevatorCar, Button (Inside/Outside), Door, State (MovingUp, Idle).
    - Logic: Dispatcher algorithm (e.g., SCAN/LOOK algorithm). Use State Pattern for elevator movement.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is the Factory Method pattern?

  ANSWER:
    It defines an interface for creating an object, but lets subclasses decide which class to instantiate.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does the Decorator differ from Inheritance?

  ANSWER:
    Inheritance adds behavior at compile-time (static). Decorator adds behavior at run-time (dynamic) by wrapping the object, preventing class explosion.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Where is the Observer pattern used in the real world?

  ANSWER:
    Event listeners in UI frameworks (React, Android), publish-subscribe systems (Kafka), RxJava/RxJS.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the Liskov Substitution Principle violation?

  ANSWER:
    A Square class extending a Rectangle class. If you change the width of a Square, the height must change. Code expecting a Rectangle will break if given a Square.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does the Builder pattern solve constructor issues?

  ANSWER:
    It solves the "Telescoping Constructor" anti-pattern (constructors with 10+ optional parameters) by providing a step-by-step fluent API (new UserBuilder().setName("A").setAge(20).build()).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the Facade Pattern?

  ANSWER:
    Provides a simplified, unified interface to a complex subsystem. Example: A ComputerFacade that hides CPU.start(), Memory.load(), HardDrive.read().

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I wrap myself in clothes of the same type as me, gaining new powers with every layer, yet to the outside world, I am exactly what I was."

  SOLUTION:
    Problem: 
    Fix: The Decorator Pattern.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  // What SOLID principle is violated?
  class Bird {
      void fly() {}
  }
  class Ostrich extends Bird {
      void fly() { throw new UnsupportedOperationException(); }
  }

  SOLUTION:
    Problem: 
    Fix: Liskov Substitution Principle. Ostrich cannot substitute Bird safely. It should be separated into FlyingBird and NonFlyingBird.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Without LLD principles, large codebases devolve into "Spaghetti Code" and "God Classes" (a single class doing everything). Design patterns provide a shared vocabulary for engineers. Saying "Use a Factory here" instantly communicates the exact architecture, saving hours of explanation and preventing brittle, hard-to-test code.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 089: SystemDesign Fundamentals (High-level vs Low-level design)
  -> File 093: Design WhatsApp (State pattern used in Connection management)

================================================================================
  END OF FILE 095
================================================================================
