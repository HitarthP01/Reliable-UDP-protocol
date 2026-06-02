### 1. Guaranteeing Reliable Delivery & Ordering
* Sequence & ACK Numbers: Every packet sent is assigned a unique Sequence Number. The receiver tracks expected sequences and responds with an Acknowledgment (ACK) Number to confirm successful receipt.
* Checksum/Integrity: Ensures data corruption is caught, prompting a retransmission.
* Handling Packet Loss: The sender maintains a retransmission timer. If an ACK for a sent packet does not arrive within a specified timeout period, the protocol flags a dropped packet and retransmits.

### 2. Flow Control (Sliding Window)
To prevent the sender from overwhelming the receiver's buffer, a Sliding Window Protocol (such as Go-Back-N or Selective Repeat) is implemented:
* The sender is allowed to transmit multiple packets (up to the size of the window) before stopping to wait for an ACK.
* As ACKs arrive, the window "slides" forward, allowing new packets to be sent out continuously, maximizing network throughput.

### 3. Congestion Control
To safely utilize available network bandwidth without causing a network collapse, the protocol dynamically throttles its transmission speed based on network conditions:
* Slow Start: The congestion window (cwnd) starts small and increases exponentially with every successful ACK to quickly discover available bandwidth.
* Congestion Avoidance: Once cwnd hits a certain threshold, it switches to a linear increase phase.
* Loss Recovery: If a timeout or packet drop occurs, the protocol interprets this as network congestion, cuts the window size down, and resets its threshold to back off safely.

---

## Repository Structure

* client.py: Client/Sender architecture containing timeouts and window logic
* server.py: Server/Receiver handling sequential packet delivery and ACKs
* pointers.md: Architectural notes, design protocols, and development blueprints
* MP2_report.pdf: Detailed report covering architectural choices and protocol limitations
* MP2_results.pdf: Performance analysis charts evaluated against synthetic network conditions

---

## Getting Started

### Prerequisites
- Python 3.x
- Standard built-in libraries: socket, sys, time

### Running the Project Locally

1. Start the Receiver / Server
   Open a terminal window and run the server so it can listen for incoming connections:
   python server.py

2. Start the Sender / Client
   Open a second terminal window and run the client to begin the reliable data transfer experiment:
   python client.py

---

## Evaluation & Metrics

The protocol's robustness was benchmarked under simulated network environments with varying drop rates and delays. You can view the full graphical breakdown of throughput, link utilization, and response time variations inside MP2_results.pdf.
