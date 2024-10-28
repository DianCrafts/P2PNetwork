# P2P File Distribution System
This project implements a peer-to-peer (P2P) file-sharing network where multiple nodes communicate over TCP and UDP protocols to share and request files within a local network. The system allows for peer discovery, file requests, and file transfers.
(computer networks course project)

## Project Structure
- peer.py: Contains the code for the peer-to-peer UDP socket and the send function to initiate data transfer to other peers.
- main.py: Implements the core functionality of the P2P network, including TCP and UDP server/client setup, file discovery, and file transfer mechanisms.

## How It Works
Peer Discovery:
Each peer sends a UDP discovery message every few seconds to update its list of available peers. This allows each peer to stay updated with the IP addresses of other nodes in the network.
File Request and Transfer:

When a peer needs a file, it sends a UDP "get" request to all known peers.
Peers receiving the request check if they have the file and, if available, respond with a UDP "found" message containing file location details.
The requesting peer then initiates a TCP connection to the peer that has the file and transfers it over the TCP connection.
Communication Protocols:

UDP is used for broadcasting discovery messages and initial file requests to all peers.
TCP is used for reliable file transfers once a specific peer has been identified as having the requested file.
Installation and Setup
Python Version: This code is compatible with Python 3.x. Make sure to have Python installed on your system.
Dependencies: No additional libraries are required outside of Python's standard library.

## Usage
Configure Peer Node:

Run main.py and provide inputs for:
- Peer node name
- IP address
- The name of an initial file list (e.g., node1.txt) that contains a list of files each peer has.

## File Discovery:
Peers will periodically send discovery messages to keep track of each other.
File Request:

To request a file, a peer will input the file's name, triggering a "get" request to be sent to other peers. If another peer has the file, it will respond, and the file will be transferred via TCP.

## Code Structure Overview
peer.py:
Sets up the UDP socket and provides a sendData() function to send data to another peer.
main.py:
- readFile(): Reads a list of files from a specified text file.
- UDPServerSocket(): Creates a UDP server socket for handling UDP messages.
- UDPClientSocket(): Creates a UDP client socket for sending messages to other peers.
- TCPServerSocket(): Creates a TCP server socket for file transfers.
- TCPServer(): Handles incoming TCP requests for file transfers.
- TCPClient(): Connects to another peer via TCP to request or send files.
- UDPServer(): Listens for incoming UDP messages and handles requests for files or peer discovery.
- getFile(): Sends a file over TCP to another peer.
- sendRequestForFile(): Sends a file request message to all known peers.
- sendForDiscovery(): Periodically sends a discovery message to find other peers on the network.
- discover(): Updates the list of known peers based on discovery messages.
## Example
Start multiple instances of main.py on different terminals with different node names.
Each node will periodically discover other nodes.
To request a file, enter the file name when prompted in one node's terminal.
If another node has the file, it will initiate a TCP transfer to the requesting node.
