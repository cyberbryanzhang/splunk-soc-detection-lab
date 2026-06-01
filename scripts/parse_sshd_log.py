import re
from collections import Counter

log_file = "sshd_lab.log"

ip_pattern = re.compile(r"from (\d+\.\d+\.\d+\.\d+)")
failed = Counter()
accepted = Counter()

with open(log_file, "r", errors="ignore") as f:
    for line in f:
        ip_match = ip_pattern.search(line)
        if not ip_match:
            continue

        ip = ip_match.group(1)

        if "Failed password" in line:
            failed[ip] += 1
        elif "Accepted password" in line:
            accepted[ip] += 1

print("=== SSH Login Detection Summary ===")

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
