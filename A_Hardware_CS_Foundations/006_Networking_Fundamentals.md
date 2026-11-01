================================================================================
  FILE 006: Networking Fundamentals
  Section: A - Hardware & CS Foundations
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Networking Fundamentals: From Packets to WebSockets
  
  This document breaks down the fundamental protocols that power the internet. You will learn how data traverses the globe, from the physical wires to the application layer. It covers TCP mechanics, DNS resolution, modern web protocols (HTTP/2, HTTP/3), and secure handshakes (TLS 1.3).
  Prerequisites: Basic understanding of computers and the internet.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  OSI 7-Layer Model
    A conceptual framework to understand network interactions.
      1. Physical: Cables, radio waves, bits (e.g., Ethernet PHY, 802.11).
      2. Data Link: MAC addresses, switches, frames (e.g., Ethernet, ARP).
      3. Network: IP addresses, routers, packets (e.g., IPv4, IPv6, ICMP/Ping).
      4. Transport: Ports, reliability, segments (e.g., TCP, UDP).
      5. Session: Maintaining connections (often grouped into App layer in practice).
      6. Presentation: Encryption, compression (e.g., TLS/SSL).
      7. Application: End-user protocols (e.g., HTTP, DNS, WebSockets, SMTP).

  TCP (Transmission Control Protocol)
    Connection-oriented, reliable, ordered delivery.

  3-Way Handshake
    Establishes connection (SYN, SYN-ACK, ACK).

  4-Way Teardown
    Terminates connection (FIN, ACK, FIN, ACK).

  Flow Control (Sliding Window)
    Prevents sender from overwhelming the receiver's buffer.

  Congestion Control
    Prevents sender from overwhelming the network (Slow Start, Congestion Avoidance).

  UDP (User Datagram Protocol)
    Connectionless, unreliable, unordered, but very fast. No handshake, no retries.

  HTTP Evolution
    

  HTTP/1.1
    Text-based. Keep-Alive connection reuse. Suffers from Head-of-Line (HoL) blocking (one slow request blocks subsequent requests on the same connection).

  HTTP/2
    Binary framing. Multiplexing (multiple concurrent requests over a single TCP connection). Header compression (HPACK). Server Push.

  HTTP/3 (QUIC)
    Replaces TCP with QUIC (built on UDP) to fix TCP's transport-level Head-of-Line blocking and enable faster connection migration (e.g., switching from WiFi to Cellular without dropping the call).

  TLS 1.3
    The latest encryption protocol. Reduces handshake from 2-RTT (TLS 1.2) to 1-RTT, and allows 0-RTT for resumed connections.

  DNS (Domain Name System)
    The internet's phonebook, translating google.com to 142.250.190.46. Uses UDP port 53.

  WebSocket
    Provides full-duplex, bidirectional communication over a single TCP connection. Starts as an HTTP request and "upgrades" to a WebSocket.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TCP 3-WAY HANDSHAKE                                                    │
  │                                                                         │
  │    Client (SYN_SENT)                     Server (LISTEN)                │
  │        |                                      |                         │
  │        | -------- [ SYN, Seq=100 ] ---------> |                         │
  │        |                                      | (SYN_RCVD)              │
  │        | <--- [ SYN, ACK, Seq=300, Ack=101] - |                         │
  │        |                                      |                         │
  │   (ESTABLISHED)                               |                         │
  │        | -------- [ ACK, Seq=101, Ack=301 ] > |                         │
  │        |                                      | (ESTABLISHED)           │
  │        |        (Data Transfer Begins)        |                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  HTTP/1.1 VS HTTP/2 MULTIPLEXING                                        │
  │                                                                         │
  │  HTTP/1.1 (Head-of-Line Blocking) - Requires multiple TCP connections for speed:│
  │  Connection 1: [Req 1 (Slow)]-------------------->[Res 1][Req 3]-->     │
  │  Connection 2: [Req 2]---->[Res 2][Req 4]---->[Res 4]                   │
  │                                                                         │
  │  HTTP/2 (Multiplexing) - Single TCP connection:                         │
  │  TCP Conn: [Frame Req1][Frame Req2][Frame Req3] ---------------->       │
  │            <------ [Frame Res2][Frame Res1(pt1)][Frame Res3][Frame Res1(pt2)]│
  │  * Data is chopped into frames. Res2 can finish before Res1!            │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: Python]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Demo Code                                                            │
  │                                                                          │
  │  import socket                                                           │
  │                                                                          │
  │  # 1. Create a TCP socket (IPv4, TCP)                                    │
  │  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       │
  │                                                                          │
  │  # Allow port reuse immediately after restart                            │
  │  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     │
  │                                                                          │
  │  # 2. Bind to an IP and Port                                             │
  │  server_socket.bind(('127.0.0.1', 8080))                                 │
  │                                                                          │
  │  # 3. Listen (tells OS to accept incoming TCP handshakes)                │
  │  server_socket.listen(5) # Backlog of 5 connections                      │
  │  print("Listening on 127.0.0.1:8080...")                                 │
  │                                                                          │
  │  while True:                                                             │
  │      # 4. Accept a connection (Blocks until a 3-way handshake completes) │
  │      client_socket, client_address = server_socket.accept()              │
  │      print(f"Accepted connection from {client_address}")                 │
  │                                                                          │
  │      # 5. Read data (Blocks until data arrives)                          │
  │      data = client_socket.recv(1024)                                     │
  │      print(f"Received: {data.decode('utf-8').strip()}")                  │
  │                                                                          │
  │      # 6. Send response                                                  │
  │      response = "HTTP/1.1 200 OK\r\n\r\nHello from TCP Server!"          │
  │      client_socket.sendall(response.encode('utf-8'))                     │
  │                                                                          │
  │      # 7. Close connection (Initiates 4-way teardown)                    │
  │      client_socket.close()                                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: JavaScript]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  const http = require('http');                                           │
  │  const crypto = require('crypto');                                       │
  │                                                                          │
  │  // Create a standard HTTP Server                                        │
  │  const server = http.createServer((req, res) => {                        │
  │      res.writeHead(200);                                                 │
  │      res.end('Standard HTTP response\n');                                │
  │  });                                                                     │
  │                                                                          │
  │  // Listen to the 'upgrade' event emitted by the HTTP server             │
  │  server.on('upgrade', (req, socket, head) => {                           │
  │      console.log('Client requested protocol upgrade');                   │
  │                                                                          │
  │      // Check if client is requesting a WebSocket upgrade                │
  │      if (req.headers['upgrade'].toLowerCase() === 'websocket') {         │
  │          const clientKey = req.headers['sec-websocket-key'];             │
  │                                                                          │
  │          // WebSocket RFC requires this specific magic string for the handshake hash│
  │          const magicString = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';     │
  │                                                                          │
  │          // Compute the Accept key                                       │
  │          const hash = crypto.createHash('sha1')                          │
  │                             .update(clientKey + magicString)             │
  │                             .digest('base64');                           │
  │                                                                          │
  │          // Construct the HTTP 101 Switching Protocols response          │
  │          const responseHeaders = [                                       │
  │              'HTTP/1.1 101 Switching Protocols',                         │
  │              'Upgrade: websocket',                                       │
  │              'Connection: Upgrade',                                      │
  │              `Sec-WebSocket-Accept: ${hash}`                             │
  │          ];                                                              │
  │                                                                          │
  │          // Complete the handshake                                       │
  │          socket.write(responseHeaders.join('\r\n') + '\r\n\r\n');        │
  │          console.log('WebSocket handshake complete! Connection established.');│
  │                                                                          │
  │          // Setup data listener for WebSocket frames (requires unmasking logic in prod)│
  │          socket.on('data', (buffer) => {                                 │
  │              console.log('Received raw websocket frame data length:', buffer.length);│
  │              // In a real implementation, you'd parse the WebSocket framing here.│
  │          });                                                             │
  │      } else {                                                            │
  │          socket.end('HTTP/1.1 400 Bad Request');                         │
  │      }                                                                   │
  │  });                                                                     │
  │                                                                          │
  │  server.listen(8080, () => {                                             │
  │      console.log('Server listening on port 8080');                       │
  │  });                                                                     │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What happens when you type `google.com` into your browser?

  ANSWER:
    (Summarized) 1) Browser checks local cache. 2) OS checks hosts file. 3) OS makes DNS query (UDP to ISP resolver). 4) DNS returns IP address. 5) Browser initiates TCP 3-way handshake to port 443. 6) TLS handshake establishes secure channel. 7) HTTP GET request sent over TLS. 8) Server responds with HTML. 9) Browser parses HTML, fetches assets, renders DOM.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: TCP vs UDP: When to use which?

  ANSWER:
    TCP is reliable (file transfer, HTTP, SSH). UDP is fast, fire-and-forget, with no retry overhead (video streaming, VoIP, multiplayer gaming, DNS).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is TCP Sliding Window?

  ANSWER:
    Flow control mechanism. The receiver tells the sender "my buffer has X bytes available" (the window). The sender can send up to X bytes without waiting for an ACK. As ACKs return, the window "slides" forward.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: How does DNS resolution work? (Iterative vs Recursive)

  ANSWER:
    Most clients do a Recursive query to their ISP's resolver ("Find this for me"). The resolver does an Iterative query: asks Root server -> gets TLD server (.com) IP -> asks TLD server -> gets Authoritative server IP -> asks Authoritative server -> gets final IP.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: Why was HTTP/2 introduced? What did it fix?

  ANSWER:
    It fixed HTTP/1.1 Application-level Head-of-Line blocking by introducing Multiplexing. It also compressed heavy HTTP headers via HPACK to save bandwidth.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why HTTP/3 over UDP?

  ANSWER:
    Because HTTP/2 over TCP still suffered from *Transport-level* Head-of-Line blocking (if one TCP packet is dropped, the OS halts all streams until it's retransmitted). QUIC handles packet loss per-stream independently.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is a MAC address vs an IP address?

  ANSWER:
    MAC is physical, permanent (burned into NIC), used for local routing within a subnet (Data Link layer). IP is logical, temporary, used for global routing across the internet (Network layer). ARP maps IP to MAC.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is a Reverse Proxy (e.g., Nginx)?

  ANSWER:
    A server that sits in front of backend web servers and forwards client requests to them. Used for load balancing, SSL termination, caching, and DDOS protection.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The UDP Video Stream

  You built a video streaming app using UDP. Users report the video occasionally stutters with grey blocks, but never stops entirely.

  SOLUTION:
    Packets are being dropped over the internet. UDP doesn't retransmit. The video codec receives an incomplete frame, resulting in visual artifacts (grey blocks). This is usually preferred over TCP's behavior, where the video would completely freeze and buffer while waiting for the retransmission.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Exhausted Server (TIME_WAIT)

  A load testing script is hammering an API. The server CPU and RAM are fine, but suddenly it starts refusing connections. netstat shows 60,000 connections in TIME_WAIT state.

  SOLUTION:
    Ephemeral Port Exhaustion. When the server actively closes a TCP connection, the port enters TIME_WAIT for 2 * MSL (Maximum Segment Lifetime, ~1-2 minutes) to ensure stray packets from the old connection don't corrupt a new one. With 60k connections, it ran out of ports.
    Use HTTP Keep-Alive to reuse connections, or enable OS settings like tcp_tw_reuse.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Slow HTTPS

  Connecting to an API in Europe from the US takes 300ms, but downloading data takes only 50ms.

  SOLUTION:
    Network Latency (RTT) + Handshakes. A US-to-EU roundtrip might be 100ms. TCP 3-way handshake takes 1 RTT (100ms). TLS 1.2 takes 2 RTT (200ms). Total setup time is 300ms before the first byte of HTTP data is even requested!
    Upgrade to TLS 1.3 (1-RTT), HTTP/3, and use edge CDNs.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  - Microservices Architecture: Choosing between gRPC (HTTP/2), REST (HTTP/1.1), or messaging queues (AMQP) requires understanding connection overhead and multiplexing capabilities.
  - Cloud Load Balancers: AWS ALBs and Nginx rely on understanding Layer 4 (TCP) vs Layer 7 (HTTP) routing. Layer 4 is faster (just forwarding IP packets), Layer 7 allows routing based on URL paths but requires decrypting TLS.
  - Security: Understanding the TLS handshake is necessary to debug certificate chains and configure mutual TLS (mTLS) in zero-trust environments.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 005: 005_Operating_System_Fundamentals.md (How the OS `epoll` handles these socket file descriptors.)
  -> File 003: 003_Virtual_Memory_Pages_PageFaults.md (High performance networking often uses memory-mapped I/O (Zero-copy) to transfer data straight from disk to NIC.)

================================================================================
  END OF FILE 006
================================================================================
