================================================================================
  FILE 005: Operating System Fundamentals
  Section: A - Hardware & CS Foundations
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  OS Fundamentals: Processes, Threads, & I/O Multiplexing
  
  This document covers the core responsibilities of an Operating System: managing CPU execution via processes and threads, executing system calls, and handling I/O efficiently. You'll learn how the OS juggles thousands of tasks concurrently using scheduling algorithms and high-performance I/O models like epoll.
  Prerequisites: Basic understanding of computer hardware and programming.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Process
    An instance of an executing program. It has its own isolated virtual memory space (code, data, heap, stack) and OS resources (file descriptors). Heavyweight.

  Thread
    A unit of execution within a process. Threads within the same process share the heap, data, and file descriptors, but have their own registers and stack. Lightweight.

  Context Switch
    The process of saving the state (registers, program counter) of a running process/thread and loading the state of another. Costs ~1-10 microseconds. Switching processes is more expensive than switching threads because it requires a TLB flush (changing virtual memory mappings).

  Process States
    

  New
    Process is being created.

  Ready
    Process is in memory, waiting for CPU time.

  Running
    Instructions are being executed on the CPU.

  Waiting (Blocked)
    Process is waiting for an event (e.g., I/O completion, a lock).

  Terminated
    Process has finished execution.

  CPU Scheduling Algorithms
    

  FCFS (First-Come, First-Served)
    Simple queue. Can cause Convoy Effect (short processes stuck behind a long one).

  SJF (Shortest Job First)
    Optimal for average wait time, but impossible to know exact job length. Can cause starvation.

  Round Robin (RR)
    Each process gets a time slice (quantum). If it doesn't finish, it's preempted and put at the back of the queue. Great for responsiveness.

  CFS (Completely Fair Scheduler)
    The default Linux scheduler. Uses a Red-Black tree to track the virtual runtime of processes, always scheduling the one that has run the least.

  System Calls (Syscalls)
    The interface between user programs and the kernel. User space cannot access hardware directly; it must trap into the kernel via a syscall.

  fork()
    Creates a duplicate child process.

  exec()
    Replaces the current process image with a new program.

  wait()
    Parent waits for child to terminate.

  File Descriptors (FD)
    An integer representing an open file, socket, or pipe. 0=stdin, 1=stdout, 2=stderr. Stored in a per-process File Descriptor Table.

  Inter-Process Communication (IPC)
    How isolated processes talk to each other.

  Pipes
    Unidirectional byte stream (e.g., ls | grep).

  Shared Memory
    Mapping the same physical RAM to the virtual memory of two processes. Fastest IPC.

  Sockets
    Bidirectional communication, works over a network or locally (Unix Domain Sockets).

  I/O Models
    

  Blocking I/O
    Thread calls read() and halts completely until data arrives.

  Non-blocking I/O
    read() returns immediately. If no data, returns an error (EAGAIN). Requires busy-polling.

  I/O Multiplexing (epoll / kqueue / select)
    A single thread monitors thousands of file descriptors. The OS notifies the thread only when an FD is ready to read/write.

  Async I/O (AIO / io_uring)
    Program submits a read request and continues working. OS copies data to user buffer and notifies program when completely finished.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PROCESS STATE TRANSITIONS                                              │
  │                                                                         │
  │                    +-------+                                            │
  │                    |  New  |                                            │
  │                    +---+---+                                            │
  │                        | (admitted)                                     │
  │                        v                                                │
  │  +---------+       +-------+  (dispatch)   +---------+                  │
  │  | Waiting |<------| Ready |-------------->| Running |                  │
  │  +---------+ (wait)+---+---+               +----+----+                  │
  │        |               ^      (preempt /        |                       │
  │        |               |       timeout)         |                       │
  │        +---------------+                        | (exit)                │
  │         (event completion)                      v                       │
  │                                            +---------+                  │
  │                                            |Terminated|                 │
  │                                            +---------+                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  I/O MULTIPLEXING (EPOLL) VS BLOCKING I/O                               │
  │                                                                         │
  │  Blocking I/O (1 Thread per Connection - Doesn't Scale):                │
  │  Conn 1 --> [ Thread 1 (Blocked on read) ]                              │
  │  Conn 2 --> [ Thread 2 (Blocked on read) ]                              │
  │  Conn 3 --> [ Thread 3 (Processing)      ]                              │
  │                                                                         │
  │  epoll (Event Loop - High Scalability - Node.js/Nginx/Redis/Netty):     │
  │  Conn 1 --+                                                             │
  │  Conn 2 --|--> [ epoll instance in OS ] ---> (Only Conn 3 is ready!)    │
  │  Conn 3 --+            |                                                │
  │                        v                                                │
  │                [ Single Event Loop Thread ]                             │
  │                "Ah, Conn 3 has data. I will read and process it now."   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: C]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  #include <stdio.h>                                                      │
  │  #include <unistd.h>                                                     │
  │  #include <sys/wait.h>                                                   │
  │                                                                          │
  │  int main() {                                                            │
  │      printf("Parent Process (PID: %d) starting...\n", getpid());         │
  │                                                                          │
  │      // fork() creates an exact duplicate of the current process         │
  │      pid_t pid = fork();                                                 │
  │                                                                          │
  │      if (pid < 0) {                                                      │
  │          // Fork failed                                                  │
  │          perror("fork failed");                                          │
  │          return 1;                                                       │
  │      } else if (pid == 0) {                                              │
  │          // Child Process                                                │
  │          printf("Child Process (PID: %d) executing 'ls -l'...\n", getpid());│
  │                                                                          │
  │          // exec() replaces the child's memory space with the new program│
  │          char *args[] = {"ls", "-l", NULL};                              │
  │          execvp("ls", args);                                             │
  │                                                                          │
  │          // This line is NEVER reached unless execvp fails               │
  │          perror("exec failed");                                          │
  │      } else {                                                            │
  │          // Parent Process                                               │
  │          printf("Parent Process waiting for Child (PID: %d) to finish...\n", pid);│
  │                                                                          │
  │          // wait() blocks parent until child terminates                  │
  │          int status;                                                     │
  │          wait(&status);                                                  │
  │                                                                          │
  │          printf("Child finished. Parent exiting.\n");                    │
  │      }                                                                   │
  │                                                                          │
  │      return 0;                                                           │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: C]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  #include <stdio.h>                                                      │
  │  #include <stdlib.h>                                                     │
  │  #include <unistd.h>                                                     │
  │  #include <sys/epoll.h>                                                  │
  │  #include <fcntl.h>                                                      │
  │                                                                          │
  │  #define MAX_EVENTS 10                                                   │
  │                                                                          │
  │  // Helper to make a socket non-blocking                                 │
  │  void set_nonblocking(int fd) {                                          │
  │      int flags = fcntl(fd, F_GETFL, 0);                                  │
  │      fcntl(fd, F_SETFL, flags | O_NONBLOCK);                             │
  │  }                                                                       │
  │                                                                          │
  │  int main() {                                                            │
  │      // 1. Create epoll instance                                         │
  │      int epoll_fd = epoll_create1(0);                                    │
  │      if (epoll_fd == -1) {                                               │
  │          perror("epoll_create1");                                        │
  │          return 1;                                                       │
  │      }                                                                   │
  │                                                                          │
  │      // In a real server, 'listen_sock' would be a bound TCP socket.     │
  │      // For compilation sake, let's just pretend stdin (fd 0) is a socket.│
  │      int listen_sock = 0; // stdin                                       │
  │      set_nonblocking(listen_sock);                                       │
  │                                                                          │
  │      struct epoll_event ev, events[MAX_EVENTS];                          │
  │                                                                          │
  │      // 2. Register interest in the socket (read events)                 │
  │      ev.events = EPOLLIN;                                                │
  │      ev.data.fd = listen_sock;                                           │
  │      if (epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_sock, &ev) == -1) {   │
  │          perror("epoll_ctl");                                            │
  │          return 1;                                                       │
  │      }                                                                   │
  │                                                                          │
  │      printf("Starting epoll event loop...\n");                           │
  │                                                                          │
  │      // 3. The Event Loop                                                │
  │      while (1) {                                                         │
  │          // epoll_wait blocks until at least one FD is ready             │
  │          int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);        │
  │                                                                          │
  │          for (int n = 0; n < nfds; ++n) {                                │
  │              if (events[n].data.fd == listen_sock) {                     │
  │                  // The socket has data! We can read without blocking.   │
  │                  char buf[128];                                          │
  │                  ssize_t count = read(listen_sock, buf, sizeof(buf) - 1);│
  │                  if (count > 0) {                                        │
  │                      buf[count] = '\0';                                  │
  │                      printf("Read non-blocking: %s", buf);               │
  │                  }                                                       │
  │              } else {                                                    │
  │                  // Handle other connections...                          │
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      close(epoll_fd);                                                    │
  │      return 0;                                                           │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between a Process and a Thread?

  ANSWER:
    Process is isolated; has its own memory space (heap, data, code). If a process crashes, it doesn't affect others. Thread is a unit of execution within a process; shares heap and file descriptors with peer threads. Threads are faster to create and context switch, but a crash in one thread crashes the whole process.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What are the four necessary conditions for Deadlock?

  ANSWER:
    (Coffman conditions) 1) Mutual Exclusion (resource cannot be shared). 2) Hold and Wait (holding a resource while requesting another). 3) No Preemption (resource cannot be forcibly taken away). 4) Circular Wait (A waits for B, B waits for C, C waits for A).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is Priority Inversion and how is it solved?

  ANSWER:
    A low-priority task holds a lock needed by a high-priority task. A medium-priority task preempts the low-priority task, indirectly delaying the high-priority task indefinitely. Solution: Priority Inheritance (the low-priority task temporarily inherits the high priority until it releases the lock).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Why is context switching expensive?

  ANSWER:
    It involves saving CPU registers, swapping out the memory map (CR3 register on x86), flushing the TLB (which causes subsequent memory accesses to be slow due to cache misses), and loading new state.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What happens during a System Call?

  ANSWER:
    CPU transitions from User Mode (Ring 3) to Kernel Mode (Ring 0) via a trap/interrupt. The OS checks arguments, executes privileged hardware instructions, places the result in a register, and transitions back to User Mode.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the difference between `select`/`poll` and `epoll`.

  ANSWER:
    `select` and `poll` require the OS to scan the entire list of file descriptors every time to check which are ready, which scales poorly (O(N)). `epoll` uses callbacks in the kernel to maintain a ready-list; when `epoll_wait` is called, it simply returns the ready list instantly (O(1) relative to total connections).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an Orphan process and a Zombie process?

  ANSWER:
    Orphan: Parent dies before child; child is adopted by `init`/`systemd` (PID 1). Zombie: Child dies, but parent hasn't called `wait()` to read its exit status. The OS keeps the child's PID in the process table until the parent acknowledges it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the File Descriptor Table?

  ANSWER:
    An array inside the OS process control block. The index is the file descriptor integer (e.g., 3), and the value is a pointer to the system-wide open file table, which points to the actual inode/device.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Fork Bomb

  c
  while(1) {
  fork();
  }

  SOLUTION:
    This will exponentially create processes (1->2->4->8) until it hits the OS process limit, completely starving the system of CPU and RAM, requiring a hard reboot.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Multi-threaded Counter

  java
  int count = 0;
  // Thread 1 and Thread 2 both run this loop 10,000 times:
  count++;

  SOLUTION:
    count++ is not an atomic operation at the CPU level. It is 3 instructions: Load, Increment, Store. A context switch can happen between Load and Store, causing lost updates (Race Condition). Result will likely be < 20,000. Fix: Use atomic variables, Mutex, or Spinlocks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Zombie Apocalypse

  c
  if (fork() == 0) {
  exit(0); // Child immediately dies
  }
  // Parent loops forever without calling wait()
  while(1) { sleep(1); }

  SOLUTION:
    The child becomes a Zombie. Its resources are freed, but its entry in the process table remains. If the parent does this in a loop, the OS will run out of PIDs and fail to start new processes.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Server Architecture: Node.js, Redis, and Nginx are built entirely on single-threaded `epoll` Event Loops. Understanding why this outperforms multi-threaded Apache blocking I/O is fundamental to modern backend scaling.
  - Microservices & IPC: When microservices run on the same physical host (e.g., Kubernetes pods), understanding IPC allows optimizing network overhead (e.g., using Unix Domain Sockets instead of TCP).
  - Concurrency Bugs: Deadlocks and race conditions in production can crash distributed systems. Understanding OS locks and scheduler behavior helps debug production outages.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 001: 001_CPU_Architecture_Instruction_Pipeline.md (How context switches manipulate CPU registers.)
  -> File 003: 003_Virtual_Memory_Pages_PageFaults.md (The virtual memory backing processes.)

================================================================================
  END OF FILE 005
================================================================================
