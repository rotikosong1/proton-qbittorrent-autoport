\# Proton VPN Port Forwarding for qBittorrent



A lightweight Python automation script for Windows that retrieves the forwarded port from Proton VPN via NAT-PMP and automatically updates the qBittorrent listening port.



\## 🚀 Features

\- Automatic Port Retrieval: Uses NAT-PMP to talk directly to the Proton VPN gateway.

\- qBittorrent Integration: Updates the listening port via the Web API instantly.

\- Persistent Heartbeat: Keeps the port alive by renewing the lease every 45 seconds.

\- Silent Operation: Can be run as a .pyw file to stay hidden in the background.



\## 🛠 Setup



\### 1. qBittorrent Configuration

To allow the script to communicate with qBittorrent:

1\. Open qBittorrent and go to Tools > Options > Web UI.

2\. Enable the Web User Interface.

3\. Change the Port to 8090 (Port 8080 is often conflicted on Windows).

4\. Under Authentication, check "Bypass authentication for clients on localhost".

5\. Under Security, uncheck "Enable Cross-Site Request Forgery (CSRF) protection".



\### 2. Installation

Clone this repository and install the dependencies:



pip install -r requirements.txt

