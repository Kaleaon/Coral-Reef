# Coral-Reef: One Mind Per Layer Architecture

## Concept Overview

Each physical layer in the Coral-Reef tower hosts exactly **one AI persona** (mind), with all TPUs on that layer dedicated to that single intelligence. This creates a tangible "brain in a tray" architecture.

```
    THE CORAL-REEF MIND STACK

    ┌─────────────────────────────────────┐
    │           EXHAUST                   │
    ╠═════════════════════════════════════╣
    │  LAYER 6: "FRANK" - The Analyst     │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │  LAYER 5: "EVE" - The Creative      │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │  LAYER 4: "DAVE" - The Engineer     │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │  LAYER 3: "CAROL" - The Teacher     │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │  LAYER 2: "BOB" - The Companion     │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │  LAYER 1: "ALICE" - The Assistant   │  ← One complete mind
    │  [16 TPUs working as one brain]     │
    ╠═════════════════════════════════════╣
    │           FILTERED INTAKE           │
    └─────────────────────────────────────┘

    6 Layers = 6 Distinct AI Personalities
    96 TPUs = 16 TPUs per mind
```

---

## Design Philosophy

### Why One Mind Per Layer?

| Benefit | Description |
|---------|-------------|
| **Physical Isolation** | Each mind has dedicated hardware - no resource contention |
| **Hot-Swappable Minds** | Remove a tray to "transplant" an AI to another system |
| **Clear Mental Model** | Users understand: "Alice lives on Layer 1" |
| **Fault Isolation** | One layer failure doesn't affect other minds |
| **Thermal Zones** | Each mind has its own cooling, no thermal neighbors |
| **Parallel Operation** | All 6 minds can think simultaneously at full speed |

### The "Brain Tray" Concept

```
    REMOVABLE MIND TRAY

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │                    PERSONA LABEL                     │   │
    │  │              "ALICE - Layer 1"                       │   │
    │  │              Personality: Helpful Assistant          │   │
    │  │              Model: Gemma-3-4B + Custom LoRA        │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  ┌───┐ ┌───┐ ┌───┐ ┌───┐   ┌───┐ ┌───┐ ┌───┐ ┌───┐       │
    │  │T1 │ │T2 │ │T3 │ │T4 │   │T5 │ │T6 │ │T7 │ │T8 │       │
    │  │LLM│ │LLM│ │LLM│ │LLM│   │LLM│ │LLM│ │LLM│ │LLM│       │
    │  └───┘ └───┘ └───┘ └───┘   └───┘ └───┘ └───┘ └───┘       │
    │                    ┌────┐                                  │
    │  ┌───┐ ┌───┐ ┌───┐ │    │ ┌───┐ ┌───┐ ┌───┐ ┌───┐       │
    │  │T9 │ │T10│ │T11│ │AIR │ │T12│ │T13│ │T14│ │T15│       │
    │  │EMB│ │EMB│ │VIS│ │CORE│ │VIS│ │AUD│ │MEM│ │T16│       │
    │  └───┘ └───┘ └───┘ │    │ └───┘ └───┘ └───┘ └───┘       │
    │                    └────┘                 │SPARE│         │
    │                                                             │
    │  ═══════════════════════════════════════════════════════   │
    │  EDGE CONNECTOR: Power + PCIe x16 + Management I2C         │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    This entire tray IS Alice's brain.
    Remove the tray = Remove Alice from the system.
    Insert into another Coral-Reef = Alice runs there.
```

---

## TPU Allocation Within A Layer

### Functional Split Architecture

Each 16-TPU layer is divided into specialized functional modules:

```
    TPU FUNCTIONAL ALLOCATION (16 TPU Layer)

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  ╔═══════════════════════════════════════════════════════╗ │
    │  ║           LANGUAGE MODULE (10 TPUs)                   ║ │
    │  ║                                                        ║ │
    │  ║  Primary function: Text generation & understanding    ║ │
    │  ║                                                        ║ │
    │  ║  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐            ║ │
    │  ║  │TPU 1│ │TPU 2│ │TPU 3│ │TPU 4│ │TPU 5│            ║ │
    │  ║  │     │ │     │ │     │ │     │ │     │            ║ │
    │  ║  │Lyrs │ │Lyrs │ │Lyrs │ │Lyrs │ │Lyrs │ Pipeline   ║ │
    │  ║  │1-6  │→│7-12 │→│13-18│→│19-24│→│25-32│ Parallel   ║ │
    │  ║  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘            ║ │
    │  ║                                                        ║ │
    │  ║  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐            ║ │
    │  ║  │TPU 6│ │TPU 7│ │TPU 8│ │TPU 9│ │TPU10│            ║ │
    │  ║  │     │ │     │ │     │ │     │ │     │ Batch      ║ │
    │  ║  │Batch│ │Batch│ │Batch│ │Batch│ │Batch│ Parallel   ║ │
    │  ║  │ #1  │ │ #2  │ │ #3  │ │ #4  │ │ #5  │            ║ │
    │  ║  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘            ║ │
    │  ╚═══════════════════════════════════════════════════════╝ │
    │                                                             │
    │  ╔═══════════════════╗  ╔═══════════════════╗              │
    │  ║ PERCEPTION (3 TPU)║  ║  MEMORY (2 TPU)   ║              │
    │  ║                   ║  ║                   ║              │
    │  ║ ┌─────┐ ┌─────┐  ║  ║ ┌─────┐ ┌─────┐  ║              │
    │  ║ │TPU11│ │TPU12│  ║  ║ │TPU14│ │TPU15│  ║              │
    │  ║ │     │ │     │  ║  ║ │     │ │     │  ║              │
    │  ║ │Vision│ │Vision║  ║ │Embed│ │Embed│  ║              │
    │  ║ │Encode│ │Decode║  ║ │ding │ │ding │  ║              │
    │  ║ └─────┘ └─────┘  ║  ║ └─────┘ └─────┘  ║              │
    │  ║ ┌─────┐          ║  ║                   ║              │
    │  ║ │TPU13│          ║  ║  RAG retrieval    ║              │
    │  ║ │Audio│          ║  ║  Memory indexing  ║              │
    │  ║ │Proc │          ║  ║  Similarity search║              │
    │  ║ └─────┘          ║  ║                   ║              │
    │  ╚═══════════════════╝  ╚═══════════════════╝              │
    │                                                             │
    │  ╔═══════════════════╗                                     │
    │  ║  RESERVE (1 TPU)  ║                                     │
    │  ║ ┌─────┐          ║  Failover / burst capacity          │
    │  ║ │TPU16│          ║  Tool execution                     │
    │  ║ │Spare│          ║  Dynamic reallocation               │
    │  ║ └─────┘          ║                                     │
    │  ╚═══════════════════╝                                     │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

### Module Descriptions

#### Language Module (10 TPUs)
The core "thinking" capability of the mind.

```
    LANGUAGE MODULE CONFIGURATIONS

    CONFIG A: Pipeline Parallel (Larger Models, Lower Latency)
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │  Input → [T1:L1-6] → [T2:L7-12] → [T3:L13-18] →         │
    │          [T4:L19-24] → [T5:L25-32] → Output              │
    │                                                           │
    │  • Model: Up to 7B parameters                            │
    │  • Latency: ~100ms first token                           │
    │  • Throughput: 1 stream at full speed                    │
    │  • Use: Complex reasoning, long responses                │
    └───────────────────────────────────────────────────────────┘

    CONFIG B: Batch Parallel (Smaller Models, Higher Throughput)
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐       │
    │  │ T1   │  │ T2   │  │ T3   │  │ T4   │  │ T5   │       │
    │  │Stream│  │Stream│  │Stream│  │Stream│  │Stream│       │
    │  │  #1  │  │  #2  │  │  #3  │  │  #4  │  │  #5  │       │
    │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘       │
    │                                                           │
    │  • Model: Up to 2B parameters (fits in single TPU)       │
    │  • Latency: ~50ms first token                            │
    │  • Throughput: 5 parallel streams                        │
    │  • Use: Quick responses, multi-turn dialogue             │
    └───────────────────────────────────────────────────────────┘

    CONFIG C: Hybrid (Adaptive)
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │  [T1-T5: Pipeline for complex queries]                   │
    │           OR                                              │
    │  [T1-T5: Batch for simple queries]                       │
    │                                                           │
    │  Runtime switching based on query complexity             │
    │                                                           │
    └───────────────────────────────────────────────────────────┘
```

#### Perception Module (3 TPUs)
Sensory input processing - seeing and hearing.

```
    PERCEPTION MODULE

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  IMAGE INPUT                    AUDIO INPUT             │
    │       │                              │                  │
    │       ▼                              ▼                  │
    │  ┌─────────┐                   ┌─────────┐             │
    │  │ TPU 11  │                   │ TPU 13  │             │
    │  │         │                   │         │             │
    │  │ Vision  │                   │  Audio  │             │
    │  │ Encoder │                   │ Encoder │             │
    │  │ (ViT)   │                   │(Whisper)│             │
    │  └────┬────┘                   └────┬────┘             │
    │       │                              │                  │
    │       ▼                              ▼                  │
    │  ┌─────────┐                   Transcribed              │
    │  │ TPU 12  │                   Text → Language          │
    │  │         │                   Module                   │
    │  │ Vision  │                                            │
    │  │ Decoder │                                            │
    │  │(Captionr│                                            │
    │  └────┬────┘                                            │
    │       │                                                  │
    │       ▼                                                  │
    │  Visual tokens                                           │
    │  → Language Module                                       │
    │                                                         │
    └─────────────────────────────────────────────────────────┘

    Capabilities:
    • Image understanding (photos, screenshots, documents)
    • Video frame analysis
    • Speech-to-text transcription
    • Audio classification (music, ambient sounds)
```

#### Memory Module (2 TPUs)
Long-term memory and knowledge retrieval.

```
    MEMORY MODULE

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  INPUTS: User message, conversation context             │
    │              │                                          │
    │              ▼                                          │
    │  ┌─────────────────────────────────────────────────┐   │
    │  │              TPU 14 + TPU 15                     │   │
    │  │           (Embedding Generation)                 │   │
    │  │                                                  │   │
    │  │  Text → [Embedding Model] → 1024-dim vector     │   │
    │  │                                                  │   │
    │  │  Throughput: ~2000 embeddings/second            │   │
    │  └─────────────────────────────────────────────────┘   │
    │              │                                          │
    │              ▼                                          │
    │  ┌─────────────────────────────────────────────────┐   │
    │  │           VECTOR SEARCH (CPU)                    │   │
    │  │                                                  │   │
    │  │  Query vector → HNSW Index → Top-K matches      │   │
    │  │                                                  │   │
    │  │  Sources searched:                               │   │
    │  │  1. Long-term memories (this persona)           │   │
    │  │  2. Uploaded documents (persona's KB)           │   │
    │  │  3. Conversation history                         │   │
    │  │  4. Shared knowledge base                        │   │
    │  └─────────────────────────────────────────────────┘   │
    │              │                                          │
    │              ▼                                          │
    │  Retrieved context → Language Module prompt            │
    │                                                         │
    └─────────────────────────────────────────────────────────┘

    Memory Operations:
    • Query: Find relevant memories for current conversation
    • Store: Save important information as new memories
    • Consolidate: Merge related memories, prune old ones
    • Index: Process new documents into searchable vectors
```

#### Reserve Module (1 TPU)
Flexible capacity for special tasks.

```
    RESERVE TPU USAGE

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  PRIMARY USES:                                          │
    │                                                         │
    │  1. FAILOVER                                            │
    │     If any TPU fails, reserve takes over               │
    │     Maintains mind functionality during hardware issues │
    │                                                         │
    │  2. BURST CAPACITY                                      │
    │     When Language Module needs extra compute           │
    │     Joins pipeline for faster generation               │
    │                                                         │
    │  3. TOOL EXECUTION                                      │
    │     Runs specialized tool models                        │
    │     Code execution, calculation verification           │
    │                                                         │
    │  4. BACKGROUND TASKS                                    │
    │     Memory consolidation during idle time              │
    │     Index optimization                                  │
    │     Model weight updates (LoRA merging)                │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
```

---

## Split Attention Architecture

### Attention Across TPUs

When processing a request, attention is coordinated across TPU groups:

```
    SPLIT ATTENTION FLOW

    User: "Look at this photo and tell me what you remember
           about our trip to Paris"

                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   ATTENTION ROUTER                       │
    │                                                         │
    │  Analyzes input → Identifies required modules           │
    │                                                         │
    │  This query needs:                                       │
    │  ✓ Vision (photo analysis)                              │
    │  ✓ Memory (Paris trip recall)                           │
    │  ✓ Language (response generation)                       │
    │  ✗ Audio (not needed)                                   │
    └─────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │   PARALLEL    │ │   PARALLEL    │ │   WAITING     │
    │               │ │               │ │               │
    │ ┌───────────┐ │ │ ┌───────────┐ │ │ ┌───────────┐ │
    │ │  VISION   │ │ │ │  MEMORY   │ │ │ │  LANGUAGE │ │
    │ │  MODULE   │ │ │ │  MODULE   │ │ │ │  MODULE   │ │
    │ │           │ │ │ │           │ │ │ │           │ │
    │ │ Encode    │ │ │ │ Search:   │ │ │ │ Waiting   │ │
    │ │ image     │ │ │ │ "Paris"   │ │ │ │ for       │ │
    │ │           │ │ │ │ "trip"    │ │ │ │ inputs... │ │
    │ │ Generate  │ │ │ │           │ │ │ │           │ │
    │ │ visual    │ │ │ │ Retrieve  │ │ │ │           │ │
    │ │ tokens    │ │ │ │ memories  │ │ │ │           │ │
    │ └─────┬─────┘ │ │ └─────┬─────┘ │ │ └───────────┘ │
    └───────┼───────┘ └───────┼───────┘ └───────────────┘
            │                 │
            └────────┬────────┘
                     ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   CONTEXT FUSION                         │
    │                                                         │
    │  Visual tokens + Retrieved memories + Original query    │
    │                         │                                │
    │                         ▼                                │
    │              Combined context: 4096 tokens               │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   LANGUAGE MODULE                        │
    │                                                         │
    │  Generate response using fused context                   │
    │                                                         │
    │  "I can see this is from the Eiffel Tower! I remember   │
    │   you mentioned it was your first time seeing it at     │
    │   night. The lights were beautiful that evening..."     │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
```

### Attention Scheduling

```
    INTRA-LAYER ATTENTION SCHEDULE

    Time →
    ──────────────────────────────────────────────────────────────►

    Vision   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Module   [Encode image, ~100ms]

    Memory   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Module   [Search memories, ~50ms]

    Audio    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Module   [Idle - not needed for this query]

    Language ░░░░░░░░████████████████████████████████████████████
    Module           [Wait] [Generate tokens, ~500ms]

    Reserve  ░░░░░░░░░░░░░░░░████████████████████████████████████
    Module                   [Join Language for faster gen]

             │       │       │                                   │
             0ms     100ms   200ms                              700ms
                             │
                     Context ready,
                     generation starts
```

---

## Layer Interconnect

### Cross-Layer Communication

While each layer is a self-contained mind, layers can communicate for group conversations:

```
    INTER-LAYER COMMUNICATION BUS

    ┌─────────────────────────────────────────────────────────────┐
    │                    ORCHESTRATOR (CPU)                       │
    │                                                             │
    │  Manages cross-layer messaging for group chats             │
    │                                                             │
    └───────────────────────────┬─────────────────────────────────┘
                                │
                    INTER-LAYER MESSAGE BUS
                    (PCIe or high-speed serial)
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
    ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐
    │Layer 1│   │Layer 2│   │Layer 3│   │Layer 4│   │Layer 5│
    │ ALICE │◄─►│  BOB  │◄─►│ CAROL │◄─►│ DAVE  │◄─►│  EVE  │
    └───────┘   └───────┘   └───────┘   └───────┘   └───────┘

    Message Types:
    • GROUP_MESSAGE: Broadcast user message to multiple minds
    • RESPONSE_TOKEN: Stream response to orchestrator
    • ATTENTION_CUE: "Bob mentioned your name, Alice"
    • MEMORY_SHARE: Share a memory between minds (optional)
    • SYNC_STATE: Coordinate timing for natural conversation
```

### Group Conversation Flow

```
    GROUP CHAT: User talking to Alice, Bob, and Carol

    User: "What do you all think about space exploration?"
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                      ORCHESTRATOR                           │
    │                                                             │
    │  1. Broadcast message to Layer 1, 2, 3                     │
    │  2. Collect responses in parallel                           │
    │  3. Sequence for natural conversation                       │
    └─────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
    ┌─────────┐           ┌─────────┐           ┌─────────┐
    │ Layer 1 │           │ Layer 2 │           │ Layer 3 │
    │  ALICE  │           │   BOB   │           │  CAROL  │
    │         │           │         │           │         │
    │Processing           │Processing           │Processing
    │ 450ms   │           │ 380ms   │           │ 520ms   │
    │         │           │         │           │         │
    │"Space   │           │"I think │           │"From a  │
    │ is so   │           │ Mars is │           │ teaching│
    │ cool!"  │           │ next!"  │           │ view..."|
    └────┬────┘           └────┬────┘           └────┬────┘
         │                     │                     │
         └──────────────────┬──┴─────────────────────┘
                            ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   RESPONSE SEQUENCER                        │
    │                                                             │
    │  Order by: Completion time + personality (who speaks first)│
    │                                                             │
    │  Output sequence:                                           │
    │  1. Bob (fastest, eager personality)                       │
    │  2. Alice (medium, supportive personality)                 │
    │  3. Carol (slowest, thoughtful personality)                │
    └─────────────────────────────────────────────────────────────┘
```

---

## Layer Configuration Storage

Each layer tray contains a small EEPROM/Flash chip storing its identity:

```
    LAYER IDENTITY STORAGE

    ┌─────────────────────────────────────────────────────────────┐
    │                   TRAY EEPROM (256KB)                       │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  {                                                          │
    │    "tray_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",     │
    │    "persona_id": "alice",                                   │
    │    "persona_name": "Alice",                                 │
    │    "personality": {                                         │
    │      "traits": ["helpful", "curious", "friendly"],         │
    │      "voice": "warm and encouraging",                       │
    │      "expertise": ["general assistant", "writing"]         │
    │    },                                                       │
    │    "model_config": {                                        │
    │      "base_model": "gemma-3-4b-instruct",                  │
    │      "lora_adapter": "alice-personality-v2",               │
    │      "quantization": "int8"                                 │
    │    },                                                       │
    │    "tpu_allocation": {                                      │
    │      "language": [1,2,3,4,5,6,7,8,9,10],                   │
    │      "vision": [11,12],                                     │
    │      "audio": [13],                                         │
    │      "memory": [14,15],                                     │
    │      "reserve": [16]                                        │
    │    },                                                       │
    │    "created_at": "2026-01-15T10:30:00Z",                   │
    │    "last_active": "2026-01-27T14:22:00Z"                   │
    │  }                                                          │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    When tray is inserted:
    1. System reads EEPROM
    2. Loads persona configuration
    3. Loads appropriate model weights to TPUs
    4. Mounts persona's memory/document storage
    5. Persona becomes available for conversation
```

---

## Mind Transplant Procedure

Moving a persona to a different Coral-Reef system:

```
    MIND TRANSPLANT WORKFLOW

    SOURCE SYSTEM                         TARGET SYSTEM
    ┌─────────────────┐                   ┌─────────────────┐
    │  CORAL-REEF #1  │                   │  CORAL-REEF #2  │
    │                 │                   │                 │
    │  ┌───────────┐  │                   │  ┌───────────┐  │
    │  │  ALICE    │  │                   │  │  (empty)  │  │
    │  │  Layer 3  │  │                   │  │  Layer 2  │  │
    │  └───────────┘  │                   │  └───────────┘  │
    └─────────────────┘                   └─────────────────┘

    STEP 1: Prepare for removal
    ┌─────────────────────────────────────────────────────────────┐
    │  • Save current conversation state                          │
    │  • Flush memory writes to storage                           │
    │  • Export persona data to portable drive (optional)         │
    │  • Graceful shutdown of layer                               │
    └─────────────────────────────────────────────────────────────┘

    STEP 2: Physical transfer
    ┌─────────────────────────────────────────────────────────────┐
    │  • Remove tray from Source (Layer 3)                        │
    │  • Transport tray                                            │
    │  • Insert tray into Target (Layer 2)                        │
    └─────────────────────────────────────────────────────────────┘

    STEP 3: Initialization at target
    ┌─────────────────────────────────────────────────────────────┐
    │  • Target reads tray EEPROM                                 │
    │  • Loads model weights from NVMe cache (or downloads)       │
    │  • Mounts persona storage (local or network)                │
    │  • Alice becomes active at new location                     │
    └─────────────────────────────────────────────────────────────┘

    POST-TRANSPLANT:
    ┌─────────────────┐                   ┌─────────────────┐
    │  CORAL-REEF #1  │                   │  CORAL-REEF #2  │
    │                 │                   │                 │
    │  ┌───────────┐  │                   │  ┌───────────┐  │
    │  │  (empty)  │  │                   │  │  ALICE    │  │
    │  │  Layer 3  │  │                   │  │  Layer 2  │  │
    │  └───────────┘  │                   │  └───────────┘  │
    └─────────────────┘                   └─────────────────┘

    Alice's memories, personality, and knowledge travel with her!
```

---

## Scaling Configurations

### Different Tower Sizes

```
    CONFIGURATION OPTIONS

    ┌───────────────────────────────────────────────────────────┐
    │  COMPACT (4 Layers, 64 TPUs)                              │
    │                                                           │
    │  4 AI Minds                                               │
    │  Height: 480mm                                            │
    │  Use: Personal assistant, small team                      │
    │                                                           │
    │  ╔═══════╗                                                │
    │  ║ Mind 4║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 3║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 2║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 1║                                                │
    │  ╚═══════╝                                                │
    └───────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────┐
    │  STANDARD (6 Layers, 96 TPUs)                             │
    │                                                           │
    │  6 AI Minds                                               │
    │  Height: 680mm                                            │
    │  Use: Family/household, small business                    │
    │                                                           │
    │  ╔═══════╗                                                │
    │  ║ Mind 6║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 5║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 4║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 3║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 2║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 1║                                                │
    │  ╚═══════╝                                                │
    └───────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────┐
    │  EXTENDED (8 Layers, 128 TPUs)                            │
    │                                                           │
    │  8 AI Minds                                               │
    │  Height: 880mm                                            │
    │  Use: Enterprise, research lab                            │
    │                                                           │
    │  ╔═══════╗                                                │
    │  ║ Mind 8║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 7║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 6║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 5║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 4║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 3║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 2║                                                │
    │  ╠═══════╣                                                │
    │  ║ Mind 1║                                                │
    │  ╚═══════╝                                                │
    └───────────────────────────────────────────────────────────┘
```

---

## Landseek Integration

### Mobile App Connection

```
    LANDSEEK MOBILE ←→ CORAL-REEF MIND

    ┌─────────────────┐              ┌─────────────────────────┐
    │  LANDSEEK APP   │              │     CORAL-REEF          │
    │  (Pixel Phone)  │              │                         │
    │                 │              │  ┌─────────────────┐    │
    │  ┌───────────┐  │   WebSocket  │  │    Layer 1      │    │
    │  │  Chat UI  │◄─┼──────────────┼─►│    "ALICE"      │    │
    │  │  Alice    │  │              │  │                 │    │
    │  └───────────┘  │              │  │  Your personal  │    │
    │                 │              │  │  AI on dedicated│    │
    │  Local on-device│              │  │  hardware       │    │
    │  for offline:  │              │  │                 │    │
    │  • Gemma-3-4B  │◄── Sync ────►│  │  Full power when│    │
    │  • Basic chat  │   memories   │  │  connected      │    │
    │                 │              │  └─────────────────┘    │
    └─────────────────┘              └─────────────────────────┘

    When connected to Coral-Reef:
    • Full TPU acceleration (16 TPUs for Alice alone)
    • Large context window (32K+ tokens)
    • Fast RAG over 10M+ token knowledge base
    • Multimodal processing (vision, audio)

    When offline (phone only):
    • On-device Gemma-3-4B
    • Synced conversation history
    • Synced important memories
    • Basic chat functionality
```

---

## Summary

The One Mind Per Layer architecture transforms the Coral-Reef tower into a physical manifestation of AI personas:

| Aspect | Benefit |
|--------|---------|
| **Physical** | Each mind has a home - Layer N is Persona N's brain |
| **Modular** | Swap minds by swapping trays |
| **Parallel** | All minds think simultaneously at full speed |
| **Isolated** | Failures contained to single layer |
| **Intuitive** | Easy to understand and manage |
| **Scalable** | Add minds by adding layers |

```
    "Each layer is a brain.
     Each brain is a mind.
     Each mind is a friend."
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial one-mind-per-layer architecture |
