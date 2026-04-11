import natpmp
import requests
import time
import sys

# --- CONFIGURATION ---
QB_URL = "http://127.0.0.1:8090"
QB_USER = "admin"
QB_PASS = "YOUR_PASSWORD_HERE"
GATEWAY_IP = "10.2.0.1"  # Standard Proton VPN gateway
RENEWAL_INTERVAL = 45    # Seconds (Proton expects renewal < 60s)
# ---------------------

def update_qbittorrent(port):
    session = requests.Session()
    try:
        # 1. Login
        login_res = session.post(f"{QB_URL}/api/v2/auth/login", data={'username': QB_USER, 'password': QB_PASS})
        if login_res.status_code != 200:
            print("Failed to login to qBittorrent.")
            return

        # 2. Get current preferences to check if update is needed
        prefs = session.get(f"{QB_URL}/api/v2/app/preferences").json()
        if prefs.get('listen_port') == port:
            print(f"Port {port} is already set in qBittorrent.")
            return

        # 3. Update the port
        payload = {'json': f'{{"listen_port": {port}}}'}
        update_res = session.post(f"{QB_URL}/api/v2/app/setPreferences", data=payload)
        
        if update_res.status_code == 200:
            print(f"Successfully updated qBittorrent port to {port}")
        else:
            print(f"Failed to update port: {update_res.text}")

    except Exception as e:
        print(f"Web UI Error: {e}")

def run_port_forwarding():
    print(f"Starting Proton VPN Port Forwarding Automation...")
    last_port = None

    while True:
        try:
            # Request/Renew TCP port
            # Protocol 1 = TCP, Protocol 2 = UDP. Most P2P needs both or just TCP.
            resp = natpmp.map_port(
                natpmp.NATPMP_PROTOCOL_TCP, 0, 0, lifetime=RENEWAL_INTERVAL + 30, gateway_ip=GATEWAY_IP
            )
            
            current_port = resp.public_port
            print(f"[{time.strftime('%H:%M:%S')}] Active Port: {current_port}")

            # If the port changed or it's the first run, update qBittorrent
            if current_port != last_port:
                update_qbittorrent(current_port)
                last_port = current_port

        except Exception as e:
            print(f"NAT-PMP Error: {e}. Ensure you are connected to a P2P server.")
        
        time.sleep(RENEWAL_INTERVAL)

if __name__ == "__main__":
    try:
        run_port_forwarding()
    except KeyboardInterrupt:
        print("\nStopping script...")
        sys.exit(0)