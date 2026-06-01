import re
from collections import Counter, defaultdict

log_file = "data/sshd_lab.log"

ip_pattern = re.compile(r"from (\d+\.\d+\.\d+\.\d+)")
user_pattern = re.compile(r"for (?:invalid user )?(?P<user>\w+) from")
port_pattern = re.compile(r"port (?P<port>\d+)")

failed = Counter()
accepted = Counter()
events = []

with open(log_file, "r", errors="ignore") as f:
    for line in f:
        ip_match = ip_pattern.search(line)
        if not ip_match:
            continue

        src_ip = ip_match.group(1)
        user_match = user_pattern.search(line)
        port_match = port_pattern.search(line)

        user = user_match.group("user") if user_match else "unknown"
        port = port_match.group("port") if port_match else "unknown"

        if "Failed password" in line:
            failed[src_ip] += 1
            events.append(("FAILED", src_ip, user, port))
        elif "Accepted password" in line:
            accepted[src_ip] += 1
            events.append(("ACCEPTED", src_ip, user, port))

print("=== SSH Authentication Detection Summary ===")

print("\nFailed SSH logins by source IP:")
for ip, count in failed.most_common():
    print(f"{ip}: {count}")

print("\nAccepted SSH logins by source IP:")
for ip, count in accepted.most_common():
    print(f"{ip}: {count}")

print("\nPotential brute-force indicators:")
for ip, count in failed.items():
    if count >= 5:
        print(f"[ALERT] {ip} had {count} failed SSH login attempts")

print("\nEvent timeline:")
for idx, event in enumerate(events, start=1):
    status, src_ip, user, port = event
    print(f"{idx:02d}. {status} src_ip={src_ip} user={user} src_port={port}")
