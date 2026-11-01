================================================================================
  FILE 122: Python Concurrency & Parallelism
  Section: K - Python Fundamentals
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW

────────────────────────────────────────────────────────────────────────────────
  This file covers how Python handles executing multiple tasks. It explains the Global Interpreter Lock (GIL) constraint in CPython and explores the three primary paradigms for concurrent execution: Threading, Multiprocessing, and AsyncIO.
  Prerequisites: Python Core Fundamentals, OS basics (threads vs processes).
  What you'll learn: GIL deep dive, `threading`, `multiprocessing`, `concurrent.futures`, `asyncio`, and how to choose the right concurrency model.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY

────────────────────────────────────────────────────────────────────────────────
  CONCURRENCY VS PARALLELISM
    Concurrency is dealing with lots of things at once (task switching). Parallelism is doing lots of things at once (multi-core).

  GIL (GLOBAL INTERPRETER LOCK)
    A mutex in CPython that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.

  CPU-BOUND VS I/O-BOUND
    CPU-bound tasks rely heavily on processor calculations (e.g., math, image processing). I/O-bound tasks spend most of their time waiting for network or disk operations (e.g., API calls, DB queries).

  THREADING
    Concurrency using OS threads. Useful for I/O-bound tasks.

  MULTIPROCESSING
    Parallelism using separate OS processes. Each process has its own memory and its own Python interpreter (bypassing the GIL). Useful for CPU-bound tasks.

  ASYNCIO
    Single-threaded, single-process concurrency using an event loop and coroutines. Highly efficient for massive I/O-bound workloads.

────────────────────────────────────────────────────────────────────────────────
  3. DEMO CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import time                                                             │
  │  import threading                                                        │
  │  import multiprocessing                                                  │
  │  import asyncio                                                          │
  │                                                                          │
  │  # --- 1. THREADING (Good for blocking I/O) ---                          │
  │  def io_task(name):                                                      │
  │      print(f"Thread {name} starting I/O")                                │
  │      time.sleep(1) # Simulates network wait. GIL is released here!       │
  │      print(f"Thread {name} finished")                                    │
  │                                                                          │
  │  def run_threads():                                                      │
  │      threads = [threading.Thread(target=io_task, args=(i,)) for i in range(3)]│
  │      for t in threads: t.start()                                         │
  │      for t in threads: t.join()                                          │
  │                                                                          │
  │  # --- 2. MULTIPROCESSING (Good for CPU math) ---                        │
  │  def cpu_task(x):                                                        │
  │      return sum(i * i for i in range(10**6)) # Heavy math                │
  │                                                                          │
  │  def run_multiprocessing():                                              │
  │      # Bypasses GIL by spawning new processes                            │
  │      with multiprocessing.Pool(processes=4) as pool:                     │
  │          results = pool.map(cpu_task, range(4))                          │
  │      print("Multiprocessing done.")                                      │
  │                                                                          │
  │  # --- 3. ASYNCIO (Good for massive non-blocking I/O) ---                │
  │  async def async_io_task(name):                                          │
  │      print(f"Async {name} starting")                                     │
  │      await asyncio.sleep(1) # Gives control back to event loop           │
  │      print(f"Async {name} finished")                                     │
  │                                                                          │
  │  async def main_async():                                                 │
  │      # Run concurrently on a single thread!                              │
  │      tasks = [asyncio.create_task(async_io_task(i)) for i in range(3)]   │
  │      await asyncio.gather(*tasks)                                        │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      # run_threads()                                                     │
  │      # run_multiprocessing()                                             │
  │      # asyncio.run(main_async())                                         │
  │      pass                                                                │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. PRODUCTION CODE

────────────────────────────────────────────────────────────────────────────────
  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  import concurrent.futures                                               │
  │  import requests                                                         │
  │  import time                                                             │
  │                                                                          │
  │  URLS = [                                                                │
  │      "http://httpbin.org/delay/1",                                       │
  │      "http://httpbin.org/delay/1",                                       │
  │      "http://httpbin.org/delay/1"                                        │
  │  ]                                                                       │
  │                                                                          │
  │  def fetch_url(url: str) -> dict:                                        │
  │      """Synchronous network call."""                                     │
  │      response = requests.get(url)                                        │
  │      return {"url": url, "status": response.status_code}                 │
  │                                                                          │
  │  def main_threadpool():                                                  │
  │      """Production standard way to handle Threading using Futures."""    │
  │      print("Starting ThreadPool downloads...")                           │
  │      start_time = time.time()                                            │
  │                                                                          │
  │      # ThreadPoolExecutor manages the lifecycle of threads               │
  │      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:│
  │          # Map inputs to the function concurrently                       │
  │          results = list(executor.map(fetch_url, URLS))                   │
  │                                                                          │
  │      end_time = time.time()                                              │
  │      print(f"Results: {results}")                                        │
  │      print(f"Time taken: {end_time - start_time:.2f}s")                  │
  │      # Time taken will be ~1 second, not 3 seconds!                      │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      main_threadpool()                                                   │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. INTERVIEW QUESTIONS

────────────────────────────────────────────────────────────────────────────────
  Q1: What is the GIL and why does CPython have it?

  ANSWER:
    The Global Interpreter Lock prevents multiple native threads from executing Python bytecodes simultaneously. It exists because CPython's memory management (reference counting) is not thread-safe.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: If the GIL limits to one CPU core, why use threading at all?

  ANSWER:
    Threading is still highly effective for I/O-bound tasks. When a thread makes a network request or reads a file, it releases the GIL, allowing other threads to run while it waits.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How does `multiprocessing` bypass the GIL?

  ANSWER:
    It creates entirely separate OS processes. Each process gets its own memory space and its own instance of the Python interpreter, meaning each has its own GIL.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between Threading and AsyncIO?

  ANSWER:
    Threading relies on the OS to preemptively switch context between threads (costs memory and context-switching overhead). AsyncIO uses cooperative multitasking on a single thread; tasks explicitly yield control via `await`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is a race condition?

  ANSWER:
    When two or more threads/processes access shared data and try to change it at the same time, leading to unpredictable results. Solved using Locks/Mutexes.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain what `asyncio.gather` does.

  ANSWER:
    It runs multiple awaitable objects concurrently and waits for all of them to finish, returning a list of their results.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: Can you share memory between processes?

  ANSWER:
    Yes, but it's hard. Since processes have separate memory, you must use inter-process communication (IPC) tools like `multiprocessing.Queue`, `Pipe`, or `Value`/`Array` with shared memory blocks.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: When would you use `concurrent.futures` over `threading` or `multiprocessing` modules directly?

  ANSWER:
    `concurrent.futures` provides a higher-level, cleaner API (`ThreadPoolExecutor`, `ProcessPoolExecutor`) for executing callables asynchronously and managing worker pools without dealing with raw Thread or Process objects.

────────────────────────────────────────────────────────────────────────────────
  6. RIDDLES & DEBUGGING CHALLENGES

────────────────────────────────────────────────────────────────────────────────
  CHALLENGE 1: The Blocking Async Code



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  import asyncio, time


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  async def do_work():


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      time.sleep(1) # Blocking call!


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      print("Done")


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  async def main():


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      await asyncio.gather(do_work(), do_work())


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    `time.sleep(1)` is a synchronous, blocking call. It blocks the entire event loop. The code will take 2 seconds instead of 1. Fix: Use `await asyncio.sleep(1)`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Threading Math



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  import threading


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  count = 0


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  def increment():


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      global count


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      for _ in range(1000000):


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

          count += 1 # Not thread-safe!


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  threads = [threading.Thread(target=increment) for _ in range(4)]


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for t in threads: t.start()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  for t in threads: t.join()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  print(count)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    `count += 1` is not atomic in Python. It's read, add, write. Threads will overwrite each other, resulting in a final count less than 4,000,000. Fix: Use a `threading.Lock`.


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Unintentional Forking Bomb (Windows)



  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  import multiprocessing


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  def worker():


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

      print("Working")


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  # No if __name__ == "__main__":


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  p = multiprocessing.Process(target=worker)


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  p.start()


  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─




  SOLUTION:
    On Windows, `multiprocessing` imports the main module to spawn a process. Without the `if __name__ == "__main__":` guard, it recursively spawns processes until it crashes (Fork Bomb).

────────────────────────────────────────────────────────────────────────────────
  7. WHY THIS MATTERS IN PRODUCTION

────────────────────────────────────────────────────────────────────────────────
  Concurrency is the difference between an API that handles 10 requests per second and one that handles 10,000. Web frameworks like FastAPI utilize AsyncIO to achieve massive throughput. Data engineering pipelines use multiprocessing to chunk and process terabytes of data across multiple CPU cores.

────────────────────────────────────────────────────────────────────────────────
  8. CROSS-REFERENCES

────────────────────────────────────────────────────────────────────────────────
  -> File 120: Python Advanced
================================================================================
  END OF FILE 122
================================================================================
