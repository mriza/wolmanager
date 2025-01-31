# Wake On Lan web based manager

WOLManager is a web-based application that sends magic packets to PCs on your LAN. WoLManager is installed on a server within the same network as the PC to be powered on using Wake-On-Lan. If your router or firewall allows it (typically with specific configuration on the router, usually with NAT or Destination NAT), this application can be accessed from the internet, enabling you to turn on PCs in the LAN remotely from the internet.

Installation Steps:

1. Create a Python Virtual Environment, for example, using venv: `python -m venv wolmanager`
2. Navigate to the directory that was created: `cd wolmanager`
3. Clone this repository: `git clone https://github.com/mriza/wolmanager.git`
4. Create a new user: `./woladduser`
5. Run the application: `./wolmanager`
6. The application can also be run as a service using systemd or supervisor.