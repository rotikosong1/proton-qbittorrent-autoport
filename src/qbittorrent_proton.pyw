import natpmp
import requests
import time
import sys
import json

# --- CONFIGURATION ---
QB_URL = "http://127.0.0.1:8090"
QB_USER = "admin"
QB_PASS = "adminadmin"
GATEWAY_IP = "10.2.0.1"
RENEWAL_INTERVAL = 45
# ---------------------

def update_qbittorrent(port):
    session = requests.Session()
    session.headers.update({
        "Referer": QB_URL,
        "Origin": QB_URL,
        "Host": "127.0.0.1:8090",
    })

    try:
        login_res = session.post(
            f"{QB_URL}/api/v2/auth/login",
            data={"username": QB_USER, "password": QB_PASS},
        )

        # qBittorrent 5.x returns 204 No Content on success (was 200 "Ok." in 4.x)
        # 403 = banned IP, anything else = bad credentials or misconfiguration
        if login_res.status_code == 403:
            print("Login blocked (403) — your IP may be temporarily banned by qBittorrent. "
                  "Restart qBittorrent or check WebUI settings.")
            return
        if login_res.status_code not in (200, 204):
            print(f"Failed to login to qBittorrent (status: {login_res.status_code}, "
                  f"body: {login_res.text!r}).")
            return
        # For 200, still check for "Fails." body (wrong credentials)
        if login_res.status_code == 200 and login_res.text.strip() == "Fails.":
            print("Failed to login to qBittorrent — wrong username or password.")
            return

        prefs_res = session.get(f"{QB_URL}/api/v2/app/preferences")
        prefs = prefs_res.json()
        if prefs.get("listen_port") == port:
            print(f"Port {port} is already set in qBittorrent.")
            return

        payload = {"json": json.dumps({"listen_port": port})}
        update_res = session.post(f"{QB_URL}/api/v2/app/setPreferences", data=payload)

        if update_res.status_code == 200:
            print(f"Successfully updated qBittorrent port to {port}")
        else:
            print(f"Failed to update port: {update_res.text}")

    except Exception as e:
        print(f"Web UI Error: {e}")


def run_port_forwarding():
    print("Starting Proton VPN Port Forwarding Automation...")
    last_port = None

    while True:
        try:
            resp = natpmp.map_port(
                natpmp.NATPMP_PROTOCOL_TCP, 0, 0,
                lifetime=RENEWAL_INTERVAL + 30,
                gateway_ip=GATEWAY_IP,
            )
            current_port = resp.public_port
            print(f"[{time.strftime('%H:%M:%S')}] Active Port: {current_port}")

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