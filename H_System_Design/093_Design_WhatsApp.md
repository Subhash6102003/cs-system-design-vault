================================================================================
  FILE 093: DESIGN WHATSAPP
  Section: H - System Design at Scale
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Design WhatsApp focuses on building a real-time, highly concurrent, end-to-end encrypted messaging system. Prerequisites include TCP/IP, WebSockets, and NoSQL databases. You will learn how to manage millions of persistent connections, implement message queues for offline delivery, build presence (online/offline) indicators, and ensure secure encryption.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  WEBSOCKETS
    A persistent, bi-directional communication protocol over TCP. Essential for real-time chat.

  CONNECTION SERVER (GATEWAY)
    A server that holds millions of open WebSocket connections. Usually written in C++, Erlang, or Go.

  SESSION SERVICE
    A distributed cache (Redis) mapping a user_id to their current Connection Server IP.

  E2EE (END-TO-END ENCRYPTION)
    Signal Protocol. The server only sees encrypted ciphertexts. Keys are managed by clients.

  MESSAGE QUEUE
    Temporarily stores messages if the recipient is offline.

  DOUBLE TICK / READ RECEIPTS
    Acknowledgment (ACK) events routed from recipient back to sender.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  1:1 MESSAGE FLOW ARCHITECTURE                                          │
  │                                                                         │
  │  [ Alice ]  ---(1. Send Msg)-->  [ Connection Server A ]                │
  │                                        |                                │
  │                                (2. Lookup Bob's IP)                     │
  │                                        v                                │
  │                               [ Session Service (Redis) ]               │
  │                                        |                                │
  │                                (3. Route to Queue)                      │
  │                                        v                                │
  │                                 [ Message Queue ]                       │
  │                                        |                                │
  │                                (4. Push to Bob)                         │
  │                                        v                                │
  │  [ Bob ]    <---(5. Delivery)--- [ Connection Server B ]                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  END-TO-END ENCRYPTION (SIMPLIFIED)                                     │
  │                                                                         │
  │  Alice creates Public/Private Key pair. Uploads Public Key to WhatsApp. │
  │  Bob creates Public/Private Key pair. Uploads Public Key to WhatsApp.   │
  │                                                                         │
  │  Alice wants to message Bob:                                            │
  │  1. Alice fetches Bob's Public Key.                                     │
  │  2. Alice encrypts message with Bob's Public Key.                       │
  │  3. WhatsApp relays the unreadable ciphertext.                          │
  │  4. Bob decrypts with his Private Key.                                  │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: javascript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Simple WebSocket Chat Server (Node.js + 'ws' library)                │
  │  const WebSocket = require('ws');                                        │
  │  const wss = new WebSocket.Server({ port: 8080 });                       │
  │                                                                          │
  │  // Mock Session Store: userId -> websocket instance                     │
  │  const activeConnections = new Map();                                    │
  │                                                                          │
  │  wss.on('connection', function connection(ws, req) {                     │
  │      // Authenticate and get userId (simplified)                         │
  │      const userId = req.headers['user-id'];                              │
  │      activeConnections.set(userId, ws);                                  │
  │      console.log(`User ${userId} connected.`);                           │
  │                                                                          │
  │      ws.on('message', function incoming(messageStr) {                    │
  │          const message = JSON.parse(messageStr);                         │
  │          const recipientWs = activeConnections.get(message.to);          │
  │                                                                          │
  │          if (recipientWs && recipientWs.readyState === WebSocket.OPEN) { │
  │              // Push message to recipient                                │
  │              recipientWs.send(JSON.stringify({                           │
  │                  from: userId,                                           │
  │                  content: message.content                                │
  │              }));                                                        │
  │              // Send single ACK back to sender (Delivered)               │
  │              ws.send(JSON.stringify({ status: "DELIVERED", msgId: message.id }));│
  │          } else {                                                        │
  │              // Offline: Send to database/queue for later delivery       │
  │              saveToOfflineQueue(message.to, message);                    │
  │          }                                                               │
  │      });                                                                 │
  │                                                                          │
  │      ws.on('close', () => {                                              │
  │          activeConnections.delete(userId);                               │
  │      });                                                                 │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  # Presence Service (Online/Offline/Last Seen) using Redis               │
  │  import redis                                                            │
  │  import time                                                             │
  │                                                                          │
  │  r = redis.Redis(host='localhost', port=6379, db=0)                      │
  │                                                                          │
  │  def mark_user_online(user_id):                                          │
  │      """                                                                 │
  │      Heartbeat called every 10 seconds while app is open.                │
  │      Sets key with 30s TTL. If heartbeat fails, key expires.             │
  │      """                                                                 │
  │      r.setex(f"presence:{user_id}", 30, "online")                        │
  │                                                                          │
  │  def mark_user_offline(user_id):                                         │
  │      """                                                                 │
  │      Explicitly handle user disconnecting.                               │
  │      """                                                                 │
  │      r.delete(f"presence:{user_id}")                                     │
  │      r.set(f"last_seen:{user_id}", int(time.time()))                     │
  │                                                                          │
  │  def get_user_status(user_id):                                           │
  │      is_online = r.get(f"presence:{user_id}")                            │
  │      if is_online:                                                       │
  │          return "Online"                                                 │
  │                                                                          │
  │      last_seen = r.get(f"last_seen:{user_id}")                           │
  │      if last_seen:                                                       │
  │          return f"Last seen at {last_seen.decode('utf-8')}"              │
  │      return "Offline"                                                    │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why use WebSockets instead of HTTP Long Polling?

  ANSWER:
    HTTP polling creates massive header overhead and requires re-establishing TCP connections repeatedly. WebSockets maintain a single lightweight, full-duplex TCP connection, reducing server CPU and latency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: How does the server know which Connection Server a user is connected to?

  ANSWER:
    Using a Session Service (Redis Cluster). When a user connects to Server A, it writes userId: Server_A_IP to Redis. When Alice messages Bob, the system queries Redis to find Bob's IP.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do group chats scale?

  ANSWER:
    Fan-out. A message is sent to a Group Controller, which looks up the 50 members. It duplicates the message 50 times and routes it to 50 individual users via their respective Connection Servers. (Problematic for massive 100k groups, but fine for WhatsApp's limits).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Where are messages stored?

  ANSWER:
    WhatsApp explicitly states they do not store messages on servers permanently. They are written to a temporary NoSQL store (e.g., Cassandra/HBase) ONLY if the user is offline, and deleted immediately upon delivery. History is stored entirely on the client device (SQLite).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How are Read Receipts (Blue Ticks) implemented?

  ANSWER:
    As system messages. When Bob reads Alice's message, Bob's client fires a READ_ACK event to the server, which is routed to Alice just like a normal chat message. Alice's client parses it and updates the UI.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: How do you handle a Connection Server crashing?

  ANSWER:
    1 million WebSockets drop. Clients have retry logic with exponential backoff. The Load Balancer routes them to healthy servers. The Session Service is updated with their new IPs.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: How does typing indicator ("Alice is typing...") work?

  ANSWER:
    Similar to messages, but they are transient and not queued. If Bob is offline, the typing event is simply dropped.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you handle media (images/video)?

  ANSWER:
    E2EE applies here too. Client encrypts media, uploads to Blob Store (S3), gets an S3 URL. Client sends the S3 URL + Decryption Key inside the encrypted WhatsApp text message. Recipient downloads from S3 and decrypts locally.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: Riddle 1

  "I guarantee you alone can read the letter, but I leave the envelope for the postman to see."

  SOLUTION:
    Problem: 
    Fix: E2E Encryption (Ciphertext is hidden, Metadata/IPs are visible).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: Riddle 2

  # Group chat fan-out
  for member_id in get_group_members(group_id):
      send_push_notification(member_id, message)

  SOLUTION:
    Problem: 
    Fix: It assumes all members are offline. Push notifications (APNs/FCM) are expensive and slow. It should first check if the user has an active WebSocket and send real-time; only fall back to push notifications if offline.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Holding 1 billion concurrent TCP connections requires OS-level tuning (epoll/kqueue, file descriptor limits) and memory management (C/Go/Erlang) that standard REST API developers rarely touch. Understanding this architecture is vital for IoT device management, live gaming, and trading platforms.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 090: Load Balancing, CDN, & API Gateway (L4 Load balancers for long-lived TCP)
  -> File 094: Design URLShortener RateLimiter (Notification service architecture)

================================================================================
  END OF FILE 093
================================================================================
