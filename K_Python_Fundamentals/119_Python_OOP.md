================================================================================
  FILE 119: Python Object-Oriented Programming
  Section: K - Python Fundamentals
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW

────────────────────────────────────────────────────────────────────────────────
  This file explores Object-Oriented Programming (OOP) in Python. Python's OOP system is dynamic and leverages "duck typing" and a comprehensive suite of "magic methods" (dunder methods) to integrate custom objects seamlessly with built-in functions.
  Prerequisites: Python Core Fundamentals.
  What you'll learn: Classes, inheritance, polymorphism, encapsulation, magic methods, decorators, dataclasses, and slots.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY

────────────────────────────────────────────────────────────────────────────────
  CLASS VS INSTANCE VARIABLES
    Class variables are shared among all instances. Instance variables are unique to each instance.

  ENCAPSULATION
    Python doesn't have strict access modifiers. Prefixing with `_` indicates protected (convention). Prefixing with `__` triggers name mangling (pseudo-private).

  INHERITANCE & MRO
    Python supports multiple inheritance. The Method Resolution Order (MRO) determines the order classes are searched for attributes, resolved via the C3 linearization algorithm.

  DUCK TYPING
    "If it walks like a duck and quacks like a duck, it must be a duck." Python checks for the presence of methods (like `__iter__`) rather than explicit inheritance from interfaces.

  DUNDER METHODS (MAGIC METHODS)
    Methods starting and ending with double underscores (`__init__`, `__str__`). They define how objects behave with operators and built-in functions.

  DATACLASSES
    Introduced in Python 3.7 via `@dataclass`, they automatically generate boilerplate code like `__init__`, `__repr__`, and `__eq__`.

────────────────────────────────────────────────────────────────────────────────
  3. DEMO CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  from abc import ABC, abstractmethod                                     │
  │                                                                          │
  │  class Animal(ABC):                                                      │
  │      def __init__(self, name):                                           │
  │          self.name = name                                                │
  │                                                                          │
  │      @abstractmethod                                                     │
  │      def speak(self):                                                    │
  │          pass                                                            │
  │                                                                          │
  │  class Dog(Animal):                                                      │
  │      # Class variable                                                    │
  │      species = "Canis familiaris"                                        │
  │                                                                          │
  │      def __init__(self, name, breed):                                    │
  │          super().__init__(name) # Call parent constructor                │
  │          self.breed = breed                                              │
  │          self.__secret = "Loves shoes" # Name mangled                    │
  │                                                                          │
  │      def speak(self):                                                    │
  │          return "Woof!"                                                  │
  │                                                                          │
  │      @property                                                           │
  │      def secret(self):                                                   │
  │          return self.__secret                                            │
  │                                                                          │
  │      @classmethod                                                        │
  │      def get_species(cls):                                               │
  │          return cls.species                                              │
  │                                                                          │
  │      @staticmethod                                                       │
  │      def is_valid_name(name):                                            │
  │          return isinstance(name, str) and len(name) > 0                  │
  │                                                                          │
  │      # Magic methods                                                     │
  │      def __str__(self):                                                  │
  │          return f"{self.name} the {self.breed}"                          │
  │                                                                          │
  │      def __repr__(self):                                                 │
  │          return f"Dog(name='{self.name}', breed='{self.breed}')"         │
  │                                                                          │
  │      def __eq__(self, other):                                            │
  │          if not isinstance(other, Dog):                                  │
  │              return NotImplemented                                       │
  │          return self.name == other.name and self.breed == other.breed    │
  │                                                                          │
  │  # Usage                                                                 │
  │  d1 = Dog("Rex", "German Shepherd")                                      │
  │  d2 = Dog("Rex", "German Shepherd")                                      │
  │  print(d1 == d2) # True (uses __eq__)                                    │
  │  print(str(d1))  # Rex the German Shepherd                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. PRODUCTION CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  from dataclasses import dataclass, field                                │
  │  import uuid                                                             │
  │  from typing import List                                                 │
  │                                                                          │
  │  @dataclass(order=True)                                                  │
  │  class Task:                                                             │
  │      """A task in a task management system."""                           │
  │      # sort_index is used for ordering, excluded from init               │
  │      sort_index: int = field(init=False, repr=False)                     │
  │                                                                          │
  │      name: str                                                           │
  │      priority: int                                                       │
  │      task_id: str = field(default_factory=lambda: uuid.uuid4().hex)      │
  │      tags: List[str] = field(default_factory=list)                       │
  │                                                                          │
  │      def __post_init__(self):                                            │
  │          # Called automatically after __init__                           │
  │          # Sort by priority                                              │
  │          self.sort_index = self.priority                                 │
  │                                                                          │
  │  class CustomCollection:                                                 │
  │      """A custom iterable collection leveraging magic methods."""        │
  │      __slots__ = ['_items'] # Memory optimization: prevents __dict__ creation│
  │                                                                          │
  │      def __init__(self):                                                 │
  │          self._items = []                                                │
  │                                                                          │
  │      def add(self, item: Task):                                          │
  │          self._items.append(item)                                        │
  │                                                                          │
  │      def __len__(self):                                                  │
  │          return len(self._items)                                         │
  │                                                                          │
  │      def __getitem__(self, index):                                       │
  │          return self._items[index]                                       │
  │                                                                          │
  │      def __setitem__(self, index, value):                                │
  │          self._items[index] = value                                      │
  │                                                                          │
  │      def __iter__(self):                                                 │
  │          return iter(self._items)                                        │
  │                                                                          │
  │      def __contains__(self, item):                                       │
  │          return item in self._items                                      │
  │                                                                          │
  │  # Usage in production context                                           │
  │  collection = CustomCollection()                                         │
  │  collection.add(Task(name="Deploy to Prod", priority=1))                 │
  │  collection.add(Task(name="Write Tests", priority=2))                    │
  │                                                                          │
  │  # Because of __len__, __iter__, __getitem__, we can do:                 │
  │  print(f"Total tasks: {len(collection)}")                                │
  │  for task in sorted(collection): # sorted works because Task is ordered via dataclass│
  │      print(task.name)                                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. INTERVIEW QUESTIONS

────────────────────────────────────────────────────────────────────────────────
  Q1: What is MRO and how does Python compute it?

  ANSWER:
    Method Resolution Order dictates how Python looks up methods/attributes in inheritance. It uses the C3 Linearization algorithm to ensure parents are checked after children, preserving order.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain `@property`, `@classmethod`, and `@staticmethod`.

  ANSWER:
    `@property` exposes a method as an attribute (getter/setter). `@classmethod` takes `cls` as the first argument, useful for alternative constructors. `@staticmethod` takes neither `self` nor `cls`, acting like a plain function inside a class namespace.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is name mangling?

  ANSWER:
    When an attribute starts with `__` (and not ends with `__`), Python renames it internally to `_ClassName__attribute` to prevent accidental overriding in subclasses.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What are `__slots__`?

  ANSWER:
    Defining `__slots__` explicitly declares instance attributes and prevents the creation of `__dict__` for each instance, saving memory for classes with many instances.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How does duck typing relate to polymorphism in Python?

  ANSWER:
    Python doesn't require explicit inheritance to achieve polymorphism. An object just needs to implement the correct magic methods (e.g., `__len__`) to be treated polymorphically (e.g., passing it to `len()`).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the difference between `__str__` and `__repr__`?

  ANSWER:
    `__str__` is for readable, user-facing output. `__repr__` is for unambiguous, developer-facing output (ideally valid Python code to recreate the object).


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the `__post_init__` method in dataclasses?

  ANSWER:
    A hook that runs immediately after the auto-generated `__init__`, useful for validation or deriving fields.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What are metaclasses? (Briefly)

  ANSWER:
    Classes are templates for objects. Metaclasses are templates for classes. They control the creation and behavior of classes (e.g., `type` is the default metaclass).

────────────────────────────────────────────────────────────────────────────────
  6. RIDDLES & DEBUGGING CHALLENGES

────────────────────────────────────────────────────────────────────────────────
  CHALLENGE 1: Class Variable Modification



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class Employee:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      company = "TechCorp"


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  e1 = Employee()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  e2 = Employee()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  e1.company = "NewTech"


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(e2.company)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Assigning `e1.company` creates an instance variable on `e1` that shadows the class variable. `e2.company` remains "TechCorp".


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Super with Multiple Inheritance



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class A:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def greet(self): print("A")


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class B(A):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def greet(self): print("B"); super().greet()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class C(A):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def greet(self): print("C"); super().greet()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class D(B, C):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def greet(self): print("D"); super().greet()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  D().greet()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Nothing is strictly wrong, but the output surprises many. Output: D, B, C, A. MRO is D -> B -> C -> A. `super()` delegates to the *next* class in the MRO, so `B`'s `super()` calls `C`, not `A`!


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: __eq__ without __hash__



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  class Point:


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def __init__(self, x, y): self.x = x; self.y = y


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      def __eq__(self, other): return self.x == other.x and self.y == other.y


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  p1 = Point(1, 2)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  s = {p1}


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    Overriding `__eq__` automatically sets `__hash__` to `None`. This makes the object unhashable, so it cannot be put in a set or used as a dict key. Fix: Implement `__hash__` (e.g., `return hash((self.x, self.y))`).

────────────────────────────────────────────────────────────────────────────────
  7. WHY THIS MATTERS IN PRODUCTION

────────────────────────────────────────────────────────────────────────────────
  Understanding OOP features like `__slots__` can drastically reduce memory footprints when loading millions of objects (e.g., rows from a database). Knowing MRO prevents critical bugs in complex frameworks like Django, which rely heavily on mixins.

────────────────────────────────────────────────────────────────────────────────
  8. CROSS-REFERENCES

────────────────────────────────────────────────────────────────────────────────
  -> File 118: Python Core Fundamentals
  -> File 120: Python Advanced
================================================================================
  END OF FILE 119
================================================================================
