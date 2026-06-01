# SSH Brute-Force Investigation Report

## Executive Summary
A controlled Docker-based SOC lab was created to simulate SSH authentication activity between a Kali Linux attacker container and an Ubuntu victim container. The investigation identified repeated failed SSH login attempts from a single source IP, followed by one successful login.

## Environment
- Host system: macOS
- Attacker: Kali Linux Docker container
- Victim: Ubuntu Docker container
- Network: isolated Docker bridge network
- Service: OpenSSH on TCP port 22
- Log source: `/var/log/sshd_lab.log`

## Observed Activity
The victim SSH log recorded multiple failed login attempts for the user `labuser` from source IP `172.18.0.2`.

Observed event types:
- Failed password events
- Accepted password event
- SSH session disconnect event

## Detection Logic
A Python script parsed the SSH log and extracted source IP addresses from authentication events. It counted failed and accepted SSH logins by source IP.

Alert threshold:
- Source IP with 5 or more failed SSH login attempts

## Detection Result
The source IP `172.18.0.2` generated 10 failed SSH login attempts and 1 accepted login.

This pattern is consistent with potential SSH password guessing or brute-force behavior in a controlled lab scenario.

## Security Relevance
Repeated failed authentication attempts from the same source IP may indicate:
- Password guessing
- Credential stuffing
- Brute-force attack behavior
- Misconfigured automation

A successful login following repeated failures increases the severity of the event and should be investigated further.

## Recommended Response
For a real environment:
1. Confirm whether the source IP is expected or suspicious.
2. Review successful login activity from the same IP.
3. Check whether the target account performed unusual actions after login.
4. Consider temporary IP blocking or rate limiting.
5. Enforce strong passwords and multi-factor authentication.
6. Review SSH exposure and restrict access where possible.

## Limitations
This was a controlled Docker lab. Container IP addresses are internal to the Docker network and do not represent public attacker infrastructure.

## Next Steps
- Ingest the SSH log into Splunk
- Write SPL detections for failed and accepted login events
- Build a dashboard for authentication monitoring
- Add timeline analysis
