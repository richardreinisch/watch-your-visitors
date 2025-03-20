
import time
import socket
import psutil
import requests
import json
import re
import argparse
import ipaddress

from collections import deque

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table


check_url = 'https://api.abuseipdb.com/api/v2/check'
abuse_blacklist = deque(maxlen=500)

def find_remote_connections(blacklist, check_api_key: str):

    remote_processes = []

    for proc in psutil.process_iter(["pid", "name"]):

        try:
            connections = proc.net_connections(kind="inet")
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

        for conn in connections:

            if not conn.raddr:
                continue

            remote_ip = extract_ip(conn.raddr.ip)

            if remote_ip in ("127.0.0.1", "::1", ""):
                continue

            conn_type = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"

            try:
                hostname = socket.gethostbyaddr(remote_ip)[0]
            except (socket.herror, socket.gaierror, OSError):
                hostname = "N/A"

            country, blacklist_count = "N/A", -1

            if check_api_key and remote_ip not in blacklist:
                result = check_ip(remote_ip, check_api_key)
                if result:
                    country, blacklist_count = result
                    blacklist.append((remote_ip, country, blacklist_count))

            remote_processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "remote_ip": remote_ip,
                "hostname": hostname,
                "remote_port": conn.raddr.port,
                "status": conn.status,
                "type": conn_type,
                "country": country,
                "blacklist": blacklist_count
            })

    return remote_processes

def check_ip(ip: str, key: str):

    querystring = { "ipAddress": ip, "maxAgeInDays": "90" }
    headers = { "Accept": "application/json", "Key": key }

    try:
        response = requests.get(check_url, headers=headers, params=querystring)
        response.raise_for_status()
        response_json = response.json()
        return response_json["data"].get("countryCode", "N/A"), response_json["data"].get("totalReports", 0)
    except requests.exceptions.RequestException as e:
        print(f"API Error for {ip}: {e}")
        return "N/A", -1

def extract_ip(ip_str):
    try:
        return str(ipaddress.ip_address(ip_str))
    except ValueError:
        return ip_str

def generate_table(connections) -> Table:

    table = Table(
        "Process", "IP", "Port", "Hostname", "Type", "Status", "Country", "Blacklist",
        box=box.SQUARE
    )

    for entry in connections:
        count = entry['blacklist']
        blacklist_count_display = "N/A" if count < 0 else (f"[red]{count}" if count > 0 else f"[green]{count}")
        table.add_row(
            f"{entry['name']}", f"{entry['remote_ip']}", f"{entry['remote_port']}", f"{entry['hostname']}",
            f"{entry['type']}", f"{entry['status']}", f"{entry['country']}", blacklist_count_display
        )

    return table


def main():

    parser = argparse.ArgumentParser("watch-your-visitors")
    parser.add_argument("--api", help="API Key for abuseipdb.com", type=str, default=None)
    args = parser.parse_args()

    console = Console()

    with Live(console=console, screen=True, auto_refresh=False) as live:

        remote_connections = find_remote_connections(abuse_blacklist, check_api_key=args.api)

        try:
            while True:
                live.update(generate_table(remote_connections), refresh=True)
                time.sleep(5)
                remote_connections = find_remote_connections(abuse_blacklist, check_api_key=args.api)
        except KeyboardInterrupt:
            console.print("\nShutting down...")

if __name__ == '__main__':
    main()

