# One-to-One and Group Chat Simulation

This project is a simple simulation of a WhatsApp-like one-to-one chat system using Python, `asyncio`, and `websockets`. It demonstrates core concepts of real-time messaging, user presence, and asynchronous server-client communication.

---

## Message Delivery and Acknowledgment Flow

The following diagram illustrates how a message is sent from Alice to Bob through the server, and how acknowledgments (ACKs) or read receipts are handled in this chat simulation:

Alice Server Bob │ │ │ │ ── Send Msg ──> │ │ │ │ ──> Deliver ─> │ │ │ │ │ <── ACK / Read <─┘ │

This flow is implemented in the simulation using message types and acknowledgment packets exchanged between clients and

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

### Group Chat

1. **Group Creation**

   - A user can create a group by specifying a group name and a list of members.
   - The server maintains a mapping of group names to their member lists.

2. **Sending a Group Message**

   - When a user sends a message to a group, the server looks up the group members.
   - The server forwards the message to all online members of the group except the sender.
   - Optionally, the server can store messages for offline users to deliver when they come online.

3. **Receiving Group Messages**

   - Each group member receives the message as if it was sent directly to them, but with the group context.

4. **Acknowledgments**
   - Clients can send acknowledgments for group messages, and the server can forward these to the sender.

---

## Presence Server

The **Presence Server** is a dedicated component responsible for tracking which users are online or offline.

### How Presence Works

- When a user connects, the server notifies the Presence Server, which adds the user to its set of online users.
- When a user disconnects, the Presence Server removes the user from the online set.
- The server can query the Presence Server at any time to get a list of currently online users.

### Presence Broadcast

- Whenever a user comes online or goes offline, the server broadcasts a presence update to all connected clients.
- Clients display these updates in real time, so users always know who is available.
