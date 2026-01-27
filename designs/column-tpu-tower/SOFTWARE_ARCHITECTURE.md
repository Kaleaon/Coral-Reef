# Coral-Reef Software Architecture

## Overview

This document describes the software architecture for running distributed AI inference across 48-96 Edge TPUs, optimized for multi-agent conversational AI systems like Landseek.

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATIONS                        │
│        (Landseek Mobile, Web UI, API Consumers)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY                               │
│              (REST/WebSocket/gRPC endpoints)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Request    │  │   Session    │  │   Load       │          │
│  │   Router     │  │   Manager    │  │   Balancer   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  AI PERSONA   │     │  AI PERSONA   │     │  AI PERSONA   │
│   CLUSTER 1   │     │   CLUSTER 2   │     │   CLUSTER N   │
│  ┌─────────┐  │     │  ┌─────────┐  │     │  ┌─────────┐  │
│  │ Model   │  │     │  │ Model   │  │     │  │ Model   │  │
│  │ Engine  │  │     │  │ Engine  │  │     │  │ Engine  │  │
│  └─────────┘  │     │  └─────────┘  │     │  └─────────┘  │
│  ┌─────────┐  │     │  ┌─────────┐  │     │  ┌─────────┐  │
│  │   RAG   │  │     │  │   RAG   │  │     │  │   RAG   │  │
│  │ Engine  │  │     │  │ Engine  │  │     │  │ Engine  │  │
│  └─────────┘  │     └─────────┘  │     │  └─────────┘  │
│  ┌─────────┐  │     │  ┌─────────┐  │     │  ┌─────────┐  │
│  │ Memory  │  │     │  │ Memory  │  │     │  │ Memory  │  │
│  │  Store  │  │     │  │  Store  │  │     │  │  Store  │  │
│  └─────────┘  │     │  └─────────┘  │     │  └─────────┘  │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TPU DEVICE LAYER                           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │TPU 1│ │TPU 2│ │TPU 3│ │TPU 4│ │TPU 5│ │TPU 6│ │... │      │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## TPU Allocation Strategies

### Strategy 1: Dedicated Persona TPUs

Each AI persona gets dedicated TPU(s) for consistent low-latency responses.

```
┌─────────────────────────────────────────────────────────────────┐
│                    96 TPU ALLOCATION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PERSONA 1-10 (Primary Language Models)                        │
│  ├── 8 TPUs each × 10 personas = 80 TPUs                       │
│  │   └── Model sharding across 8 TPUs per persona              │
│  │                                                              │
│  SHARED SERVICES                                                │
│  ├── RAG/Embedding: 8 TPUs (pooled)                            │
│  ├── Vision/Audio: 4 TPUs (on-demand)                          │
│  └── Reserve: 4 TPUs (failover/burst)                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Strategy 2: Dynamic Pool

TPUs allocated dynamically based on demand, maximizing utilization.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DYNAMIC TPU POOL                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HOT POOL (Always loaded, instant response)                    │
│  ├── 32 TPUs with most-used models                             │
│  └── Serves 4 concurrent personas                              │
│                                                                 │
│  WARM POOL (Quick swap, <2s load time)                         │
│  ├── 48 TPUs with secondary models                             │
│  └── Context preserved in RAM                                  │
│                                                                 │
│  COLD POOL (Available for reallocation)                        │
│  ├── 16 TPUs for batch processing                              │
│  └── RAG indexing, model fine-tuning                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Strategy 3: Pipeline Parallel

Large models split across multiple TPUs in pipeline stages.

```
    REQUEST FLOW THROUGH PIPELINE

    Input → [TPU 1-8: Embed + Layers 1-8]
              ↓
            [TPU 9-16: Layers 9-16]
              ↓
            [TPU 17-24: Layers 17-24]
              ↓
            [TPU 25-32: Layers 25-32 + Output]
              ↓
            Response

    Benefit: Run 7B-27B parameter models
    Latency: ~50-200ms per token
    Throughput: 4 concurrent streams
```

---

## Model Deployment Architecture

### Supported Model Configurations

| Model Size | TPUs Required | Personas Possible | Use Case |
|------------|---------------|-------------------|----------|
| 1B params | 1 TPU | 96 concurrent | Fast chat, simple tasks |
| 2-4B params | 2-4 TPUs | 24-48 concurrent | Gemma 3 4B, balanced |
| 7B params | 8 TPUs | 12 concurrent | High quality responses |
| 13B params | 16 TPUs | 6 concurrent | Complex reasoning |
| 27B params | 32 TPUs | 3 concurrent | Maximum capability |

### Model Loading System

```
┌─────────────────────────────────────────────────────────────────┐
│                     MODEL MANAGER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   MODEL REGISTRY                         │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ gemma-3-4b-instruct    │ 4.2GB  │ INT8  │ READY │    │   │
│  │  │ gemma-3-4b-vision      │ 5.1GB  │ INT8  │ READY │    │   │
│  │  │ gemma-2-27b-instruct   │ 28GB   │ INT4  │ CACHED│    │   │
│  │  │ custom-persona-lora-1  │ 128MB  │ FP16  │ READY │    │   │
│  │  │ embedding-e5-large     │ 1.3GB  │ INT8  │ READY │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   QUANTIZATION ENGINE                    │   │
│  │  • INT8 quantization (default, 4 TOPS/TPU)              │   │
│  │  • INT4 quantization (experimental, larger models)      │   │
│  │  • Dynamic quantization for fine-tuned weights          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   HOT-SWAP CONTROLLER                    │   │
│  │  • Preload next-likely models                           │   │
│  │  • Graceful context migration                           │   │
│  │  • Zero-downtime model updates                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Multi-Agent Conversation System

### Conversation Router

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONVERSATION ROUTER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUT: "Hey everyone, what do you think about quantum physics?"│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 ROUTING DECISION                         │   │
│  │                                                          │   │
│  │  Mode: GROUP_CHAT                                        │   │
│  │  Active Personas: [Alice, Bob, Carol, Dave]              │   │
│  │                                                          │   │
│  │  Response Strategy: ROUND_ROBIN with RELEVANCE_BOOST     │   │
│  │                                                          │   │
│  │  Execution Plan:                                         │   │
│  │  1. Broadcast message to all 4 personas (parallel)       │   │
│  │  2. Score response relevance                             │   │
│  │  3. Select 2-3 most relevant to respond                  │   │
│  │  4. Sequence responses naturally                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Persona State Machine

```
    PERSONA LIFECYCLE

    ┌──────────┐
    │  IDLE    │◄─────────────────────────────┐
    └────┬─────┘                              │
         │ message_received                   │
         ▼                                    │
    ┌──────────┐                              │
    │ THINKING │──── timeout ────────────────►│
    └────┬─────┘                              │
         │ response_ready                     │
         ▼                                    │
    ┌──────────┐                              │
    │RESPONDING│                              │
    └────┬─────┘                              │
         │ response_complete                  │
         ▼                                    │
    ┌──────────┐                              │
    │ WAITING  │──── no_activity_timeout ────►│
    └────┬─────┘                              │
         │ follow_up_detected                 │
         └────────────────────────────────────┘

    States include:
    • Current emotional state
    • Conversation context window
    • Relationship scores with other personas
    • Active memory retrieval context
```

### Parallel Inference Execution

```
    PARALLEL MULTI-PERSONA INFERENCE

    Time ──────────────────────────────────────────────►

    User Message Arrives
         │
         ├──► Persona 1 (TPU 1-4)  ████████░░░░░░░ → Response 1
         │
         ├──► Persona 2 (TPU 5-8)  ████████████░░░ → Response 2
         │
         ├──► Persona 3 (TPU 9-12) ██████░░░░░░░░░ → Response 3
         │
         └──► Persona 4 (TPU 13-16)████████████████ → Response 4
                                   ↑
                                   All run simultaneously

    Total Latency = MAX(individual latencies)
    NOT SUM(individual latencies)
```

---

## RAG System Architecture

### Vector Database Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG SUBSYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               DOCUMENT INGESTION PIPELINE                │   │
│  │                                                          │   │
│  │  Documents → Parse → Chunk → Embed → Index → Store      │   │
│  │      │         │       │       │        │       │        │   │
│  │      ▼         ▼       ▼       ▼        ▼       ▼        │   │
│  │  70+ formats  Text   512-2048  TPU    HNSW   Vector     │   │
│  │  supported    Extract tokens   Embed  Index   DB        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               PER-PERSONA KNOWLEDGE STORES               │   │
│  │                                                          │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │  Persona 1   │  │  Persona 2   │  │  Persona N   │   │   │
│  │  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │   │   │
│  │  │  │10M+ tok│  │  │  │10M+ tok│  │  │  │10M+ tok│  │   │   │
│  │  │  │vectors │  │  │  │vectors │  │  │  │vectors │  │   │   │
│  │  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │   │   │
│  │  │  Custom docs │  │  Custom docs │  │  Custom docs │   │   │
│  │  │  + memories  │  │  + memories  │  │  + memories  │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  SHARED KNOWLEDGE BASE                   │   │
│  │                                                          │   │
│  │  • Common reference materials                            │   │
│  │  • Shared conversation history                           │   │
│  │  • Cross-persona relationship graph                      │   │
│  │  • World knowledge corpus                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Embedding Pipeline (TPU Accelerated)

```
    EMBEDDING THROUGHPUT

    Dedicated Embedding TPUs: 8
    Model: E5-large-v2 or similar (INT8 quantized)

    Performance:
    ┌─────────────────────────────────────────┐
    │  Single TPU:    ~1,000 embeddings/sec   │
    │  8 TPU Pool:    ~8,000 embeddings/sec   │
    │  Batch size:    32-64 optimal           │
    │  Latency:       <10ms per batch         │
    └─────────────────────────────────────────┘

    Capacity:
    ┌─────────────────────────────────────────┐
    │  10M tokens = ~20,000 chunks            │
    │  Index time: ~2.5 seconds per persona   │
    │  Storage: ~40MB vectors per persona     │
    └─────────────────────────────────────────┘
```

### Memory Reinforcement Learning (MemRL)

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  SHORT-TERM     │  │  WORKING        │  │  LONG-TERM      │ │
│  │  MEMORY         │  │  MEMORY         │  │  MEMORY         │ │
│  │                 │  │                 │  │                 │ │
│  │  Current        │  │  Active         │  │  Consolidated   │ │
│  │  conversation   │  │  context from   │  │  memories with  │ │
│  │  (4K-8K tokens) │  │  RAG retrieval  │  │  importance     │ │
│  │                 │  │  (8K-16K tokens)│  │  scores         │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │          │
│           └────────────────────┼────────────────────┘          │
│                                ▼                               │
│                    ┌─────────────────────┐                     │
│                    │  MEMORY CONTROLLER  │                     │
│                    │                     │                     │
│                    │  • Importance score │                     │
│                    │  • Recency decay    │                     │
│                    │  • Emotional weight │                     │
│                    │  • Retrieval boost  │                     │
│                    └─────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

    Memory Flow:

    New Information → Score Importance → Buffer in STM
                                              │
                           ┌──────────────────┴──────────────────┐
                           │                                     │
                      High Importance                    Low Importance
                           │                                     │
                           ▼                                     ▼
                    Consolidate to LTM                    Decay & Forget
```

---

## Multimodal Processing Pipeline

### Vision Processing

```
┌─────────────────────────────────────────────────────────────────┐
│                   VISION PIPELINE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Image Input                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │ Preprocessor│──► Resize, normalize, tile large images       │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐      ┌─────────────┐                          │
│  │ Vision      │      │ Vision TPU  │                          │
│  │ Encoder     │◄────►│ (dedicated) │                          │
│  │ (ViT/CLIP)  │      │ 2-4 units   │                          │
│  └──────┬──────┘      └─────────────┘                          │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                               │
│  │ Visual      │──► Patch embeddings + position encoding       │
│  │ Tokens      │                                               │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                               │
│  │ Cross-Modal │──► Fuse with text embeddings                  │
│  │ Attention   │                                               │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  Language Model Inference                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Audio Processing

```
┌─────────────────────────────────────────────────────────────────┐
│                   AUDIO PIPELINE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Audio Input (speech, music, ambient)                          │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │ Audio       │──► Resample to 16kHz, mono                    │
│  │ Preprocessor│                                               │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ├──────────────────┬──────────────────┐                │
│         ▼                  ▼                  ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ Speech-to-  │    │ Audio       │    │ Music       │        │
│  │ Text (STT)  │    │ Classifier  │    │ Analysis    │        │
│  │ Whisper-like│    │             │    │             │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                │
│                            │                                    │
│                            ▼                                    │
│                    Text/Features for LLM                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tool Execution Framework

### Tool Registry

```
┌─────────────────────────────────────────────────────────────────┐
│                     TOOL REGISTRY                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  BUILT-IN TOOLS                                          │   │
│  │                                                          │   │
│  │  calculator      │ Math expressions, unit conversion     │   │
│  │  web_search      │ Internet search (if connected)        │   │
│  │  file_reader     │ Read uploaded documents               │   │
│  │  code_executor   │ Python sandbox for computations       │   │
│  │  image_generator │ Generate images (if model available)  │   │
│  │  rag_query       │ Search knowledge base                 │   │
│  │  memory_store    │ Save important information            │   │
│  │  memory_recall   │ Retrieve past memories                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CUSTOM TOOLS (Plugin API)                               │   │
│  │                                                          │   │
│  │  home_automation │ Control smart home devices            │   │
│  │  calendar        │ Schedule management                   │   │
│  │  email           │ Send/read emails                      │   │
│  │  database        │ Query external databases              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Execution Flow

```
    TOOL CALL SEQUENCE

    LLM Output: "I'll calculate that for you."
                <tool_call name="calculator">2^32 * 1.5</tool_call>
         │
         ▼
    ┌─────────────────┐
    │  TOOL PARSER    │──► Extract tool name + arguments
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  SAFETY CHECK   │──► Validate permissions, sanitize input
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  TOOL EXECUTOR  │──► Run in sandboxed environment
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  RESULT FORMAT  │──► Convert output to text
    └────────┬────────┘
             │
             ▼
    LLM Continuation: "The result is 6,442,450,944"
```

---

## API Layer

### REST Endpoints

```
API ENDPOINT REFERENCE

Base URL: http://coral-reef.local:8080/api/v1

┌──────────────────────────────────────────────────────────────────┐
│  CHAT ENDPOINTS                                                  │
├──────────────────────────────────────────────────────────────────┤
│  POST /chat                      Send message, get response      │
│  POST /chat/stream               Stream response tokens          │
│  POST /chat/group                Multi-persona group chat        │
│  GET  /chat/history/{session}    Get conversation history        │
│  DELETE /chat/history/{session}  Clear conversation              │
├──────────────────────────────────────────────────────────────────┤
│  PERSONA ENDPOINTS                                               │
├──────────────────────────────────────────────────────────────────┤
│  GET  /personas                  List all personas               │
│  POST /personas                  Create new persona              │
│  GET  /personas/{id}             Get persona details             │
│  PUT  /personas/{id}             Update persona config           │
│  DELETE /personas/{id}           Delete persona                  │
│  POST /personas/{id}/memory      Add to persona memory           │
├──────────────────────────────────────────────────────────────────┤
│  DOCUMENT ENDPOINTS                                              │
├──────────────────────────────────────────────────────────────────┤
│  POST /documents/upload          Upload document for RAG         │
│  GET  /documents                 List indexed documents          │
│  DELETE /documents/{id}          Remove document                 │
│  POST /documents/query           Search documents                │
├──────────────────────────────────────────────────────────────────┤
│  SYSTEM ENDPOINTS                                                │
├──────────────────────────────────────────────────────────────────┤
│  GET  /system/status             TPU status, temps, load         │
│  GET  /system/models             Available models                │
│  POST /system/models/load        Load model to TPUs              │
│  GET  /metrics                   Prometheus metrics              │
└──────────────────────────────────────────────────────────────────┘
```

### WebSocket Protocol

```
WEBSOCKET MESSAGES

Connection: ws://coral-reef.local:8080/ws

┌──────────────────────────────────────────────────────────────────┐
│  CLIENT → SERVER                                                 │
├──────────────────────────────────────────────────────────────────┤
│  {                                                               │
│    "type": "chat",                                               │
│    "persona_id": "alice",                                        │
│    "message": "Hello!",                                          │
│    "session_id": "abc123",                                       │
│    "stream": true                                                │
│  }                                                               │
├──────────────────────────────────────────────────────────────────┤
│  SERVER → CLIENT (streaming)                                     │
├──────────────────────────────────────────────────────────────────┤
│  {"type": "token", "content": "Hi"}                              │
│  {"type": "token", "content": " there"}                          │
│  {"type": "token", "content": "!"}                               │
│  {"type": "done", "usage": {"prompt": 15, "completion": 3}}      │
├──────────────────────────────────────────────────────────────────┤
│  SERVER → CLIENT (events)                                        │
├──────────────────────────────────────────────────────────────────┤
│  {"type": "typing", "persona_id": "bob"}                         │
│  {"type": "emotion", "persona_id": "alice", "state": "happy"}    │
│  {"type": "tool_call", "tool": "calculator", "status": "running"}│
└──────────────────────────────────────────────────────────────────┘
```

---

## Deployment Configuration

### Docker Compose Stack

```yaml
# docker-compose.yml (conceptual)

services:
  coral-orchestrator:
    image: coral-reef/orchestrator:latest
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
      - ./data:/data
    environment:
      - TPU_VISIBLE_DEVICES=all
      - MODEL_CACHE_SIZE=32GB
    depends_on:
      - vector-db
      - redis

  vector-db:
    image: qdrant/qdrant:latest
    volumes:
      - ./vectors:/qdrant/storage
    ports:
      - "6333:6333"

  redis:
    image: redis:7-alpine
    volumes:
      - ./redis:/data

  monitoring:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

### System Requirements

```
MINIMUM REQUIREMENTS (48 TPU config)

┌─────────────────────────────────────────────────────────────────┐
│  CPU:     8+ cores (Intel/AMD x64)                              │
│  RAM:     64GB DDR4 (128GB recommended)                         │
│  Storage: 1TB NVMe SSD (models + vectors)                       │
│  Network: 1GbE minimum, 10GbE recommended                       │
│  OS:      Linux (Ubuntu 22.04+, Debian 12+)                     │
└─────────────────────────────────────────────────────────────────┘

RECOMMENDED REQUIREMENTS (96 TPU config)

┌─────────────────────────────────────────────────────────────────┐
│  CPU:     16+ cores (Intel Xeon / AMD EPYC)                     │
│  RAM:     256GB DDR4 ECC                                        │
│  Storage: 4TB NVMe RAID (2x 2TB)                                │
│  Network: 10GbE + 1GbE management                               │
│  OS:      Linux with real-time kernel patches                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Performance Targets

### Latency Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Time to first token | <200ms | Single persona |
| Token generation | 30-50 tok/s | Per TPU cluster |
| RAG retrieval | <50ms | Top-10 results |
| Embedding generation | <10ms | Per batch of 32 |
| Tool execution | <100ms | Most tools |
| Model hot-swap | <2s | Warm cache |

### Throughput Targets

| Metric | 48 TPU | 96 TPU |
|--------|--------|--------|
| Concurrent conversations | 12 | 24 |
| Tokens/second (aggregate) | 400 | 800 |
| Embeddings/second | 4,000 | 8,000 |
| Documents indexed/hour | 10,000 | 20,000 |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial software architecture |
