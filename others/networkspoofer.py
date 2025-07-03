import subprocess

ssid = "Free_Public_WiFi"
hostapd_conf = f"""
interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
ignore_broadcast_ssid=0
"""

with open("/tmp/fakeap.conf", "w") as f:
    f.write(hostapd_conf)

# Start hostapd
subprocess.run(["sudo", "systemctl", "stop", "wpa_supplicant"])
subprocess.run(["sudo", "systemctl", "stop", "dhcpcd"])
subprocess.run(["sudo", "systemctl", "stop", "NetworkManager"])
subprocess.run(["sudo", "hostapd", "/tmp/fakeap.conf"])