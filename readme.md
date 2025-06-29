# One-to-One Chat Simulation

This project is a simple simulation of a WhatsApp-like one-to-one chat system using Python, `asyncio`, and `websockets`. It demonstrates core concepts of real-time messaging, user presence, and asynchronous server-client communication.

---

### 1. Chat Server (`server.py`)

- **Role:** Central hub for all chat communication.
- **Responsibilities:**
  - Registers users and manages their WebSocket connections.
  - Routes messages between users.
  - Handles user presence (online/offline) via the Presence Server.
  - Broadcasts presence updates to all connected users.
  - Responds to queries like "who is online".

### 2. Presence Server (`presenceserver.py`)

- **Role:** Tracks which users are currently online.
- **Responsibilities:**
  - Maintains a set of online users.
  - Updates presence status on user connect/disconnect.
  - Provides the list of online users to the Chat Server.

### 3. Chat Client (`client.py`)

- **Role:** User interface for sending and receiving messages.
- **Responsibilities:**

  - Connects to the Chat Server via WebSocket.
  - Allows the user to send messages to other users.
  - Receives and displays messages, acknowledgments, and presence updates.
  - Can query the server for the list of online users.

  ***

## Architecture Overview

The system consists of three main components:

1. **Chat Server (`server.py`)**
2. **Presence Server (`presenceserver.py`)**
3. **Chat Client (`client.py`)**

## Message Delivery and Acknowledgment Flow

The following diagram illustrates how a message is sent from Alice to Bob through the server, and how acknowledgments (ACKs) or read receipts are handled in this chat simulation:

Alice Server Bob │ │ │ │ ── Send Msg ──> │ │ │ │ ──> Deliver ─> │ │ │ │ │ <── ACK / Read <─┘ │

### Explanation

1. **Alice Sends a Message**

   - Alice composes a message and sends it to the server, specifying Bob as the recipient.

2. **Server Delivers the Message**

   - The server receives Alice's message and forwards (delivers) it to Bob.

3. **Bob Receives the Message**

   - Bob's client receives the message from the server.

4. **Bob Sends an Acknowledgment (ACK) or Read Receipt**

   - Upon receiving the message, Bob's client automatically sends an acknowledgment (ACK) or read receipt back to the server, indicating that the message was received (and possibly read).

5. **Server Forwards the ACK to Alice**

   - The server receives the ACK/read receipt from Bob and forwards it to Alice.

6. **Alice Receives the ACK**
   - Alice's client receives the acknowledgment, confirming that Bob has received (and possibly read) the message.

### Purpose

- **Reliability:** Ensures that Alice knows her message was delivered to Bob.
- **Feedback:** Provides real-time feedback to the sender about the status of their message.
- **User Experience:** Mimics the delivery/read receipts found in modern chat applications like WhatsApp.

---

This flow is implemented in the simulation using message types and acknowledgment packets exchanged between clients and
