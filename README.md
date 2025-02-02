# Wake On Lan web based manager

WOLManager is a web-based application that sends magic packets to PCs on your LAN. WoLManager is installed on a server within the same network as the PC to be powered on using Wake-On-Lan. If your router or firewall allows it (typically with specific configuration on the router, usually with NAT or Destination NAT), this application can be accessed from the internet, enabling you to turn on PCs in the LAN remotely from the internet.

## Requirements

- Python 3.6 or higher
- Required Python modules: Flask, requests

## Installation Steps

1. Clone this repository:
   ```sh
   git clone https://github.com/mriza/wolmanager.git
   ```
2. Navigate to the directory that was created:
   ```sh
   cd wolmanager
   ```
3. Create a Python Virtual Environment:
   ```sh
   python -m venv .
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     Scripts\activate
     ```
   - On Linux or MacOS:
     ```sh
     source bin/activate
     ```
5. Install the required Python modules:
   ```sh
   pip install -r requirements.txt
   ```
6. Create a new user:
   ```sh
   ./woladduser
   ```
7. Run the application:
   ```sh
   ./wolmanager
   ```

## Managing the Program as a Service

### Using systemd

1. Create a systemd service file `/etc/systemd/system/wolmanager.service` with the following content:
   ```ini
   [Unit]
   Description=WOLManager Service
   After=network.target

   [Service]
   User=yourusername
   WorkingDirectory=/path/to/wolmanager
   ExecStart=/path/to/wolmanager/bin/python /path/to/wolmanager/wolmanager.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. Reload systemd to apply the new service:
   ```sh
   sudo systemctl daemon-reload
   ```
3. Start the service:
   ```sh
   sudo systemctl start wolmanager
   ```
4. Enable the service to start on boot:
   ```sh
   sudo systemctl enable wolmanager
   ```

### Using Supervisor

1. Install Supervisor if not already installed:
   ```sh
   sudo apt-get install supervisor
   ```
2. Create a Supervisor configuration file `/etc/supervisor/conf.d/wolmanager.conf` with the following content:
   ```ini
   [program:wolmanager]
   command=/path/to/wolmanager/bin/python /path/to/wolmanager/wolmanager.py
   directory=/path/to/wolmanager
   user=yourusername
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/wolmanager.err.log
   stdout_logfile=/var/log/wolmanager.out.log
   ```
3. Update Supervisor to apply the new configuration:
   ```sh
   sudo supervisorctl reread
   sudo supervisorctl update
   ```
4. Start the WOLManager program:
   ```sh
   sudo supervisorctl start wolmanager
   ```

(screenshots/devices.png)