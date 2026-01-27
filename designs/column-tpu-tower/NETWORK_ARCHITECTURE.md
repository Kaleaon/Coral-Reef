# Coral-Reef Network Architecture

## Overview

The Coral-Reef tower supports multiple network configurations for different deployment scenarios, from local single-user setups to multi-client P2P mesh networks.

```
┌─────────────────────────────────────────────────────────────────┐
│                    NETWORK TOPOLOGY OPTIONS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LOCAL MODE          SERVER MODE           P2P MESH MODE        │
│  ┌─────────┐        ┌─────────┐           ┌─────────┐          │
│  │ Single  │        │ Multi   │           │ Distrib │          │
│  │ Client  │        │ Client  │           │ Network │          │
│  │   │     │        │  │ │ │  │           │ ┌─┬─┬─┐ │          │
│  │   ▼     │        │  ▼ ▼ ▼  │           │ ├─┼─┼─┤ │          │
│  │ ┌───┐   │        │ ┌───┐   │           │ └─┴─┴─┘ │          │
│  │ │TPU│   │        │ │TPU│   │           │         │          │
│  │ │   │   │        │ │   │   │           │ ┌───┐   │          │
│  │ └───┘   │        │ └───┘   │           │ │TPU│   │          │
│  └─────────┘        └─────────┘           └─────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Physical Network Interfaces

### Network I/O Module

```
    NETWORK MODULE (Rear Panel)

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
    │  │  10GbE   │  │   1GbE   │  │   1GbE   │  │   USB    │   │
    │  │  SFP+    │  │  RJ-45   │  │  RJ-45   │  │   3.0    │   │
    │  │  (Data)  │  │  (Data)  │  │  (Mgmt)  │  │ (Serial) │   │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
    │       │             │             │             │          │
    │       │             │             │             │          │
    │       ▼             ▼             ▼             ▼          │
    │  High-speed    Fallback/     Management    Console        │
    │  inference     secondary     IPMI-style   Access          │
    │  traffic       clients       OOB access                   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    Optional WiFi 6E module for standalone operation
```

### Interface Specifications

| Interface | Speed | Purpose | Required |
|-----------|-------|---------|----------|
| 10GbE SFP+ | 10 Gbps | Primary data, high throughput | Recommended |
| 1GbE RJ-45 #1 | 1 Gbps | Secondary data, fallback | Required |
| 1GbE RJ-45 #2 | 1 Gbps | Management, monitoring | Required |
| USB 3.0 Type-B | 5 Gbps | Serial console, debug | Required |
| WiFi 6E (optional) | 2.4 Gbps | Wireless clients | Optional |

---

## Deployment Modes

### Mode 1: Local/Desktop Mode

Single user, direct connection to workstation.

```
    LOCAL DEPLOYMENT

    ┌──────────────────┐          ┌──────────────────┐
    │   WORKSTATION    │          │   CORAL-REEF     │
    │                  │          │                  │
    │  ┌────────────┐  │   USB    │  ┌────────────┐  │
    │  │ Landseek   │  │◄────────►│  │ API Server │  │
    │  │ Desktop    │  │   3.0    │  │            │  │
    │  └────────────┘  │          │  └────────────┘  │
    │                  │          │                  │
    │  ┌────────────┐  │  1GbE    │  ┌────────────┐  │
    │  │ Web        │  │◄────────►│  │ Web UI     │  │
    │  │ Browser    │  │          │  │ (optional) │  │
    │  └────────────┘  │          │  └────────────┘  │
    │                  │          │                  │
    └──────────────────┘          └──────────────────┘

    Latency: <1ms
    Bandwidth: 5 Gbps (USB) / 1 Gbps (Ethernet)
    Clients: 1
```

**Configuration:**
```yaml
# config/network.yaml - Local Mode
mode: local
interfaces:
  primary:
    type: usb
    speed: 5gbps
  secondary:
    type: ethernet
    ip: 192.168.1.100
    dhcp: false
firewall:
  enabled: true
  allow_local_only: true
```

### Mode 2: Home Server Mode

Multiple clients on local network.

```
    HOME SERVER DEPLOYMENT

                        ┌─────────────────────────────────────┐
                        │           HOME NETWORK              │
                        │                                     │
    ┌─────────┐        │  ┌─────────┐      ┌─────────────┐  │
    │ Phone   │◄───────┼──┤         │      │             │  │
    │(Landseek│  WiFi  │  │ Router  │◄────►│ CORAL-REEF  │  │
    └─────────┘        │  │         │ 1GbE │             │  │
                        │  └────┬────┘      └─────────────┘  │
    ┌─────────┐        │       │                            │
    │ Tablet  │◄───────┼───────┘                            │
    │(Landseek│  WiFi  │                                    │
    └─────────┘        │  ┌─────────┐                       │
                        │  │ Desktop │◄─────── 1GbE ───────►│
    ┌─────────┐        │  │   PC    │                       │
    │ Laptop  │◄───────┼──┤         │                       │
    │(Landseek│  WiFi  │  └─────────┘                       │
    └─────────┘        │                                     │
                        └─────────────────────────────────────┘

    Latency: 1-5ms (WiFi), <1ms (wired)
    Bandwidth: 100-500 Mbps per client
    Clients: 5-20 concurrent
```

**Configuration:**
```yaml
# config/network.yaml - Home Server Mode
mode: server
interfaces:
  primary:
    type: ethernet
    ip: 192.168.1.100
    dhcp: false
    gateway: 192.168.1.1
  management:
    type: ethernet
    ip: 192.168.1.101
    vlan: 10  # Separate management VLAN
api:
  bind: 0.0.0.0
  port: 8080
  tls: true
  cert: /etc/coral-reef/certs/server.crt
rate_limiting:
  requests_per_minute: 60
  burst: 10
```

### Mode 3: Enterprise/Data Center Mode

High-availability deployment with multiple servers.

```
    ENTERPRISE DEPLOYMENT

    ┌─────────────────────────────────────────────────────────────┐
    │                     LOAD BALANCER                           │
    │                   (HAProxy/NGINX)                           │
    └───────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ CORAL-REEF #1 │ │ CORAL-REEF #2 │ │ CORAL-REEF #3 │
    │               │ │               │ │               │
    │  10GbE ────────────────────────────────── 10GbE   │
    │  (Cluster     │ │ (Cluster      │ │  Cluster     │
    │   Network)    │ │  Network)     │ │  Network)    │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   SHARED STORAGE  │
                    │   (NFS/iSCSI)     │
                    └───────────────────┘

    Latency: <1ms (local DC)
    Bandwidth: 10 Gbps per node
    Clients: 100+ concurrent
    HA: Active-active with failover
```

**Configuration:**
```yaml
# config/network.yaml - Enterprise Mode
mode: cluster
cluster:
  name: coral-reef-prod
  node_id: node-1
  discovery: etcd://10.0.0.5:2379
  nodes:
    - id: node-1
      ip: 10.0.1.10
    - id: node-2
      ip: 10.0.1.11
    - id: node-3
      ip: 10.0.1.12
interfaces:
  primary:
    type: ethernet
    ip: 10.0.1.10
    speed: 10gbps
  cluster:
    type: ethernet
    ip: 10.0.2.10
    speed: 10gbps
    mtu: 9000  # Jumbo frames
shared_storage:
  type: nfs
  server: 10.0.3.5
  path: /coral-reef/shared
```

### Mode 4: P2P Mesh Mode (Landseek Integration)

Distributed peer-to-peer network for Landseek mobile clients.

```
    P2P MESH DEPLOYMENT

                    ┌─────────────────────────────────────────┐
                    │              INTERNET                   │
                    └─────────────────┬───────────────────────┘
                                      │
                    ┌─────────────────┴───────────────────────┐
                    │           CORAL-REEF HUB                │
                    │  (Public IP / STUN/TURN Server)        │
                    └─────────────────┬───────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
    ┌─────────┐                 ┌─────────┐                 ┌─────────┐
    │ Phone A │◄───── P2P ─────►│ Phone B │◄───── P2P ─────►│ Phone C │
    │Landseek │     WebRTC      │Landseek │     WebRTC      │Landseek │
    └─────────┘                 └─────────┘                 └─────────┘
         │                           │                           │
         │     ┌─────────────────────┴─────────────────────┐    │
         │     │         SHARED CONVERSATION               │    │
         └────►│                                           │◄───┘
               │  All devices sync memories & messages     │
               │  Coral-Reef provides TPU inference        │
               └───────────────────────────────────────────┘

    Features:
    • Share codes for peer discovery
    • End-to-end encrypted P2P channels
    • Bidirectional memory sync
    • Coral-Reef as inference backend
```

**Configuration:**
```yaml
# config/network.yaml - P2P Mode
mode: p2p_hub
p2p:
  enabled: true
  stun_server: stun.coral-reef.local:3478
  turn_server: turn.coral-reef.local:3478
  turn_secret: ${TURN_SECRET}
  ice_servers:
    - url: stun:stun.l.google.com:19302
    - url: turn:turn.coral-reef.local:3478
      username: coral
      credential: ${TURN_CREDENTIAL}
share_codes:
  enabled: true
  expiry: 24h
  max_peers: 10
sync:
  memories: true
  conversations: true
  documents: false  # Opt-in for documents
encryption:
  protocol: noise_ik
  key_exchange: x25519
```

---

## Protocol Stack

### API Protocols

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROTOCOL STACK                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  APPLICATION LAYER                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  REST API (HTTP/2)  │  WebSocket  │  gRPC  │  GraphQL   │   │
│  │  - Chat endpoints   │  - Streaming│ - High │ - Complex  │   │
│  │  - CRUD operations  │  - Events   │   perf │   queries  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TRANSPORT SECURITY                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  TLS 1.3  │  mTLS (optional)  │  Noise Protocol (P2P)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TRANSPORT LAYER                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  TCP (primary)  │  QUIC (optional)  │  WebRTC (P2P)     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  NETWORK LAYER                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  IPv4 / IPv6  │  ICE/STUN/TURN (NAT traversal)          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### WebSocket Message Types

```
CLIENT → SERVER MESSAGES

┌────────────────────────────────────────────────────────────────┐
│ TYPE            │ PAYLOAD                                      │
├────────────────────────────────────────────────────────────────┤
│ chat            │ {persona_id, message, session_id, stream}   │
│ chat_group      │ {personas[], message, session_id}           │
│ typing_start    │ {session_id}                                │
│ typing_stop     │ {session_id}                                │
│ cancel          │ {request_id}                                │
│ ping            │ {}                                          │
│ subscribe       │ {channels[]}                                │
│ unsubscribe     │ {channels[]}                                │
└────────────────────────────────────────────────────────────────┘

SERVER → CLIENT MESSAGES

┌────────────────────────────────────────────────────────────────┐
│ TYPE            │ PAYLOAD                                      │
├────────────────────────────────────────────────────────────────┤
│ token           │ {content, request_id}                       │
│ done            │ {request_id, usage, finish_reason}          │
│ error           │ {code, message, request_id}                 │
│ persona_typing  │ {persona_id}                                │
│ persona_emotion │ {persona_id, emotion, intensity}            │
│ tool_start      │ {tool_name, request_id}                     │
│ tool_result     │ {tool_name, result, request_id}             │
│ memory_event    │ {type, persona_id, content}                 │
│ pong            │ {latency_ms}                                │
│ system          │ {event, data}                               │
└────────────────────────────────────────────────────────────────┘
```

### P2P Sync Protocol

```
    P2P SYNC MESSAGE FLOW

    DEVICE A                    CORAL-REEF                    DEVICE B
       │                            │                            │
       │──── share_code_create ────►│                            │
       │◄─── share_code: ABC123 ────│                            │
       │                            │                            │
       │                            │◄─── share_code_join ───────│
       │                            │         (ABC123)           │
       │                            │                            │
       │◄─────────────────── peer_connected ────────────────────►│
       │                            │                            │
       │◄═══════════ P2P DataChannel (WebRTC) ═════════════════►│
       │                            │                            │
       │────── sync_request ───────────────────────────────────►│
       │       (last_sync_time)     │                            │
       │                            │                            │
       │◄────── sync_response ─────────────────────────────────│
       │       (memories[], messages[])                          │
       │                            │                            │
       │──── inference_request ────►│                            │
       │     (message, persona)     │                            │
       │◄─── inference_response ────│                            │
       │     (tokens...)            │                            │
       │                            │                            │
       │──── broadcast_message ────────────────────────────────►│
       │                            │                            │
```

---

## Security Architecture

### Authentication Flow

```
    AUTHENTICATION METHODS

    ┌─────────────────────────────────────────────────────────────┐
    │  METHOD 1: API Key (Simple, for local/trusted networks)    │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Client ─── Authorization: Bearer <api_key> ───► Server    │
    │                                                             │
    │  • Single key per device/user                               │
    │  • Stored in config file or env var                         │
    │  • Suitable for: Local mode, home server                    │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  METHOD 2: JWT Token (Scalable, for multi-user)            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Client ─── POST /auth/login {user, pass} ───► Server      │
    │         ◄── {access_token, refresh_token} ───              │
    │                                                             │
    │  Client ─── Authorization: Bearer <jwt> ───► Server        │
    │                                                             │
    │  • Short-lived access tokens (15m)                          │
    │  • Refresh tokens for renewal (7d)                          │
    │  • Suitable for: Server mode, enterprise                    │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  METHOD 3: Device Keys (For P2P sync)                      │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Device generates Ed25519 keypair on first run             │
    │  Public key = Device ID                                     │
    │                                                             │
    │  Peer verification via share code + key exchange           │
    │                                                             │
    │  • No central authority required                            │
    │  • Keys stored in device secure enclave if available        │
    │  • Suitable for: P2P mode, Landseek mobile                  │
    └─────────────────────────────────────────────────────────────┘
```

### Authorization Model

```
    ROLE-BASED ACCESS CONTROL

    ┌─────────────────────────────────────────────────────────────┐
    │  ROLE           │ PERMISSIONS                               │
    ├─────────────────────────────────────────────────────────────┤
    │  admin          │ Full system access                        │
    │                 │ • Manage users, personas, models          │
    │                 │ • System configuration                    │
    │                 │ • View all conversations                  │
    ├─────────────────────────────────────────────────────────────┤
    │  user           │ Standard user access                      │
    │                 │ • Chat with assigned personas             │
    │                 │ • Upload documents to own KB              │
    │                 │ • Manage own conversations                │
    ├─────────────────────────────────────────────────────────────┤
    │  guest          │ Limited access                            │
    │                 │ • Chat with public personas               │
    │                 │ • Rate limited                            │
    │                 │ • No document upload                      │
    ├─────────────────────────────────────────────────────────────┤
    │  peer           │ P2P sync access                           │
    │                 │ • Sync specific shared data               │
    │                 │ • Use inference API                       │
    │                 │ • Time-limited via share code             │
    └─────────────────────────────────────────────────────────────┘
```

### Encryption

```
    ENCRYPTION AT REST & IN TRANSIT

    ┌─────────────────────────────────────────────────────────────┐
    │  IN TRANSIT                                                 │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Client ◄══════ TLS 1.3 (HTTPS/WSS) ═══════► Server        │
    │                                                             │
    │  Cipher suites (priority order):                            │
    │  1. TLS_AES_256_GCM_SHA384                                  │
    │  2. TLS_CHACHA20_POLY1305_SHA256                            │
    │  3. TLS_AES_128_GCM_SHA256                                  │
    │                                                             │
    │  P2P: Noise_IK pattern with X25519 + ChaCha20-Poly1305     │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  AT REST (Optional, for sensitive deployments)             │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Conversation DB: SQLCipher (AES-256)                       │
    │  Memory Store: Application-level encryption                 │
    │  Vector Index: Not encrypted (performance)                  │
    │  Models: Not encrypted (integrity verified)                 │
    │                                                             │
    │  Key derivation: Argon2id from master password             │
    │  Key storage: System keyring / HSM / TPM                   │
    └─────────────────────────────────────────────────────────────┘
```

---

## Rate Limiting & QoS

### Rate Limiting Tiers

```
    RATE LIMITING CONFIGURATION

    ┌─────────────────────────────────────────────────────────────┐
    │  TIER        │ REQUESTS/MIN │ TOKENS/MIN │ CONCURRENT      │
    ├─────────────────────────────────────────────────────────────┤
    │  Free/Guest  │     20       │   2,000    │      1          │
    │  Basic User  │     60       │  10,000    │      2          │
    │  Power User  │    120       │  50,000    │      4          │
    │  Admin       │    600       │ 200,000    │      8          │
    │  API Key     │  Custom      │  Custom    │   Custom        │
    └─────────────────────────────────────────────────────────────┘

    Rate limit headers in response:
    X-RateLimit-Limit: 60
    X-RateLimit-Remaining: 45
    X-RateLimit-Reset: 1706345678
```

### Quality of Service

```
    QoS PRIORITY QUEUES

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  HIGH PRIORITY (Process first)                              │
    │  ├── Admin requests                                         │
    │  ├── Active conversation continuations                      │
    │  └── Latency-sensitive streaming                            │
    │                                                             │
    │  NORMAL PRIORITY (Standard queue)                           │
    │  ├── New conversation starts                                │
    │  ├── Document queries                                       │
    │  └── Standard API requests                                  │
    │                                                             │
    │  LOW PRIORITY (Background processing)                       │
    │  ├── Document indexing                                      │
    │  ├── Memory consolidation                                   │
    │  └── Batch embedding generation                             │
    │                                                             │
    │  BULK PRIORITY (When system idle)                           │
    │  ├── Model preloading                                       │
    │  ├── Index optimization                                     │
    │  └── Backup operations                                      │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## Load Balancing

### Single-Node Load Balancing

```
    INTERNAL REQUEST DISTRIBUTION

    ┌─────────────────────────────────────────────────────────────┐
    │                    API GATEWAY                              │
    │                        │                                    │
    │         ┌──────────────┼──────────────┐                    │
    │         ▼              ▼              ▼                    │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
    │   │ Worker 1 │  │ Worker 2 │  │ Worker 3 │               │
    │   │ (CPU)    │  │ (CPU)    │  │ (CPU)    │               │
    │   └────┬─────┘  └────┬─────┘  └────┬─────┘               │
    │        │             │             │                       │
    │        └─────────────┴─────────────┘                       │
    │                      │                                     │
    │              ┌───────┴───────┐                             │
    │              │  TPU SCHEDULER │                            │
    │              └───────┬───────┘                             │
    │                      │                                     │
    │    ┌─────┬─────┬─────┼─────┬─────┬─────┐                  │
    │    ▼     ▼     ▼     ▼     ▼     ▼     ▼                  │
    │  [TPU] [TPU] [TPU] [TPU] [TPU] [TPU] [...]               │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    Scheduling algorithms:
    • Round-robin for equal distribution
    • Least-loaded for optimal utilization
    • Affinity for session stickiness (KV cache reuse)
```

### Multi-Node Load Balancing

```
    CLUSTER LOAD BALANCING

                    ┌─────────────────────────────────────┐
                    │         EXTERNAL LOAD BALANCER      │
                    │         (HAProxy / NGINX / AWS ALB) │
                    └─────────────────┬───────────────────┘
                                      │
                    Health checks: /health every 5s
                    Algorithm: Least connections
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
    ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
    │ CORAL-REEF #1 │        │ CORAL-REEF #2 │        │ CORAL-REEF #3 │
    │ Weight: 100   │        │ Weight: 100   │        │ Weight: 50    │
    │ TPUs: 96      │        │ TPUs: 96      │        │ TPUs: 48      │
    │ Status: ✓     │        │ Status: ✓     │        │ Status: ✓     │
    └───────────────┘        └───────────────┘        └───────────────┘

    Session affinity:
    • Cookie-based for web clients
    • Header-based for API clients
    • Ensures KV cache reuse
```

---

## Monitoring & Observability

### Network Metrics

```
    NETWORK MONITORING DASHBOARD

    ┌─────────────────────────────────────────────────────────────┐
    │  CONNECTIONS                                                │
    │  ├── Active HTTP:     124                                  │
    │  ├── Active WebSocket: 45                                  │
    │  ├── Active P2P:       12                                  │
    │  └── Total today:   12,456                                 │
    ├─────────────────────────────────────────────────────────────┤
    │  BANDWIDTH                                                  │
    │  ├── Inbound:   45 Mbps  ▓▓▓▓░░░░░░                       │
    │  ├── Outbound: 230 Mbps  ▓▓▓▓▓▓▓▓░░                       │
    │  └── Peak:     800 Mbps                                    │
    ├─────────────────────────────────────────────────────────────┤
    │  LATENCY (p50 / p95 / p99)                                 │
    │  ├── API:        5ms / 15ms / 45ms                         │
    │  ├── WebSocket:  2ms /  8ms / 20ms                         │
    │  └── P2P relay: 25ms / 80ms / 150ms                        │
    ├─────────────────────────────────────────────────────────────┤
    │  ERRORS (last hour)                                         │
    │  ├── 4xx:  23 (rate limited)                               │
    │  ├── 5xx:   2 (internal error)                             │
    │  └── Timeouts: 1                                           │
    └─────────────────────────────────────────────────────────────┘
```

### Prometheus Metrics

```
# Network metrics exported to Prometheus

# Connection counts
coral_reef_connections_active{type="http"} 124
coral_reef_connections_active{type="websocket"} 45
coral_reef_connections_active{type="p2p"} 12

# Bandwidth (bytes/sec)
coral_reef_network_bytes_total{direction="in"} 5625000
coral_reef_network_bytes_total{direction="out"} 28750000

# Latency histograms
coral_reef_request_duration_seconds_bucket{le="0.01"} 8500
coral_reef_request_duration_seconds_bucket{le="0.05"} 9200
coral_reef_request_duration_seconds_bucket{le="0.1"} 9450
coral_reef_request_duration_seconds_bucket{le="+Inf"} 9500

# Rate limiting
coral_reef_rate_limit_hits_total{reason="requests"} 156
coral_reef_rate_limit_hits_total{reason="tokens"} 23

# P2P metrics
coral_reef_p2p_peers_total 12
coral_reef_p2p_sync_bytes_total 125000000
```

---

## Firewall & Security Groups

### Recommended Firewall Rules

```
    FIREWALL CONFIGURATION

    ┌─────────────────────────────────────────────────────────────┐
    │  INBOUND RULES                                              │
    ├─────────────────────────────────────────────────────────────┤
    │  Port    │ Protocol │ Source        │ Purpose              │
    ├─────────────────────────────────────────────────────────────┤
    │  8080    │ TCP      │ LAN/VPN       │ API (HTTP/WS)        │
    │  8443    │ TCP      │ LAN/VPN       │ API (HTTPS/WSS)      │
    │  3478    │ UDP      │ Any           │ STUN (P2P)           │
    │  3478    │ TCP      │ Any           │ TURN (P2P relay)     │
    │  5349    │ TCP      │ Any           │ TURNS (TLS relay)    │
    │  22      │ TCP      │ Management    │ SSH (restricted)     │
    │  9090    │ TCP      │ Monitoring    │ Prometheus metrics   │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  OUTBOUND RULES                                             │
    ├─────────────────────────────────────────────────────────────┤
    │  Port    │ Protocol │ Dest          │ Purpose              │
    ├─────────────────────────────────────────────────────────────┤
    │  443     │ TCP      │ Any           │ HTTPS (updates, APIs)│
    │  53      │ UDP/TCP  │ DNS servers   │ DNS resolution       │
    │  123     │ UDP      │ NTP servers   │ Time sync            │
    │  *       │ UDP      │ Any           │ WebRTC (dynamic)     │
    └─────────────────────────────────────────────────────────────┘
```

### Network Segmentation

```
    VLAN ARCHITECTURE (Enterprise)

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  VLAN 10: Management (10.0.10.0/24)                        │
    │  ├── SSH access                                             │
    │  ├── Monitoring endpoints                                   │
    │  └── Admin web UI                                           │
    │                                                             │
    │  VLAN 20: API Traffic (10.0.20.0/24)                       │
    │  ├── Client API requests                                    │
    │  ├── WebSocket connections                                  │
    │  └── Load balancer frontend                                 │
    │                                                             │
    │  VLAN 30: Cluster (10.0.30.0/24)                           │
    │  ├── Inter-node communication                               │
    │  ├── Shared storage access                                  │
    │  └── Cluster sync traffic                                   │
    │                                                             │
    │  VLAN 40: Storage (10.0.40.0/24)                           │
    │  ├── NFS/iSCSI traffic                                      │
    │  └── Backup traffic                                         │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Common Network Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| High latency | Network congestion | Check bandwidth usage, enable QoS |
| Connection drops | Firewall timeout | Increase idle timeout, enable keepalive |
| P2P not connecting | NAT issues | Verify TURN server, check UDP ports |
| TLS errors | Certificate issues | Renew cert, check chain |
| Rate limit errors | Too many requests | Upgrade tier or implement backoff |

### Diagnostic Commands

```bash
# Check network interfaces
ip addr show

# Test connectivity to clients
ping -c 4 client_ip

# Check listening ports
ss -tlnp | grep coral

# Monitor bandwidth
iftop -i eth0

# Check WebSocket connections
ss -tn state established '( dport = :8080 )'

# Test TURN server
turnutils_uclient -T -u user -w pass turn_server:3478

# View connection stats
curl http://localhost:8080/api/v1/system/network/stats
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial network architecture |
