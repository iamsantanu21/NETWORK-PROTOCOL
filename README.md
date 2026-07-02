# NETWORK-PROTOCOL

A collection of **network-protocol simulations and demonstrations** in Python, each paired with a presentation (`.pptx`). The repository explores several protocols — a DLSw Client Access Protocol (CAP/DCAP) handshake, a distance-vector routing simulation (IRAP), and MIME email — as a set of small, self-contained examples for a networking course/seminar.

## Contents

### CAP / DCAP — DLSw Client Access Protocol
`cap_server.py` + `cap_client.py` (root), duplicated in `DCAP/`.

A mock **Data Link Switching (DLSw) Client Access Protocol** exchange over TCP. The client performs a simple handshake and then streams frames:

1. Client → `CAP_CONNECT_REQUEST`; server replies `CAP_CONNECT_ACK`.
2. Client sends several `SNA_DATA:…` frames (mock SNA/mainframe data); server acknowledges each with `SNA_DATA_ACK`.
3. Client sends `DISCONNECT` to close the session.

Illustrates how DLSw tunnels legacy SNA traffic over TCP/IP using a capabilities-exchange handshake.

### IRAP — routing simulation (`irap_simulation/`)
`router.py` + `network_config.json`.

A **distance-vector routing** simulation. Each router process (defined in `network_config.json` with a port and its neighbors) runs three threads: one to listen (UDP), one to periodically **broadcast its routing table** to neighbors every 5 seconds, and one for user commands. Routers learn least-cost routes (Bellman–Ford style: neighbor cost + 1) and can send messages that are **forwarded hop-by-hop**, printing the full path taken.

Example topology (`Router1 — Router2 — Router3`):
```json
{ "Router1": { "port": 5000, "neighbors": { "Router2": 5001 } },
  "Router2": { "port": 5001, "neighbors": { "Router1": 5000, "Router3": 5002 } },
  "Router3": { "port": 5002, "neighbors": { "Router2": 5001 } } }
```

### MIME — email with MIME content (`MIME/`)
`send_mime_email.py` + `santanu.png`.

Builds a **multipart MIME email** (plain-text body + an HTML alternative + a PNG attachment) using Python's `email.message.EmailMessage`, and sends it through Gmail's SMTP server over STARTTLS. Demonstrates how MIME carries multiple content types and attachments in a single message.

### Presentations & images
- `DCAP.pptx`, `IRCP.pptx`, `MIME.pptx`, `RAP.pptx` — slide decks explaining each protocol.
- `WhatsApp Image 2025-04-29 …jpeg` — supporting photos/screenshots.

## Requirements

- **Python 3** (standard library only — `socket`, `threading`, `json`, `smtplib`, `email`). No third-party packages required.
- For the MIME example: a mail account with SMTP access (the script targets Gmail on port 587).

## Running

**CAP / DCAP** — start the server, then the client in a second terminal:
```bash
python cap_server.py        # terminal 1
python cap_client.py        # terminal 2
```

**IRAP routing simulation** — start each router in its own terminal, passing the router name:
```bash
cd irap_simulation
python router.py Router1    # terminal 1
python router.py Router2    # terminal 2
python router.py Router3    # terminal 3
```
Wait a few seconds for routing tables to converge, then at any router's prompt:
```
send Router3 hello there
```
The message is routed hop-by-hop and the destination prints the path taken.

**MIME email:**
```bash
cd MIME
python send_mime_email.py
```

## ⚠️ Security warning

`MIME/send_mime_email.py` currently contains a **hard-coded email address and Gmail app password in plaintext**. This is a real credential committed to source control.

- **Revoke/regenerate that Gmail app password now** (Google Account → Security → App passwords), since it is exposed in the repo history.
- Replace the hard-coded values with environment variables (e.g. `os.environ["EMAIL_PASSWORD"]`) or a local, git-ignored config file.
- Because the secret is in the Git history, rotating the password is the important step — simply editing the file does not remove it from past commits.

## Notes

- These are educational simulations that run on `localhost`; they use minimal error handling and no authentication.
- The root `cap_*.py` files and those under `DCAP/` are duplicates.
- `.DS_Store` files are macOS metadata and can be ignored.
