# Coral-Reef Storage Subsystem Design

## Overview

The storage subsystem is critical for AI workloads, handling:
- Model weights (fast loading)
- Vector databases (low-latency retrieval)
- Conversation history (persistent memory)
- Document corpus (RAG source data)

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE HIERARCHY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    TPU ON-CHIP MEMORY                    │   │
│  │                    (8MB SRAM per TPU)                    │   │
│  │                    Latency: <1μs                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    SYSTEM RAM (DDR4/DDR5)                │   │
│  │                    64-256GB                              │   │
│  │                    Latency: ~100ns                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PRIMARY NVMe SSD                      │   │
│  │                    1-4TB, Gen4/Gen5                      │   │
│  │                    Latency: ~10-50μs                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    SECONDARY STORAGE                     │   │
│  │                    HDD/NAS for archives                  │   │
│  │                    Latency: ~5-10ms                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Storage Requirements

### Capacity Planning

| Data Type | Per Persona | 10 Personas | Notes |
|-----------|-------------|-------------|-------|
| Base Models | - | 50-100GB | Shared across personas |
| LoRA Adapters | 128MB | 1.3GB | Personality fine-tuning |
| Vector Index | 40MB | 400MB | 10M tokens embedded |
| Document Corpus | 500MB | 5GB | Source documents |
| Conversation DB | 100MB | 1GB | Growing over time |
| Memory Store | 50MB | 500MB | Long-term memories |
| **Subtotal** | ~700MB | ~8GB | Per persona data |
| **Total System** | - | **~110GB** | With models |

### Recommended Configurations

**Minimal (48 TPU, 10 personas)**
```
┌─────────────────────────────────────────┐
│  Primary: 1TB NVMe Gen4                 │
│  ├── /models     500GB                  │
│  ├── /vectors    100GB                  │
│  ├── /data       300GB                  │
│  └── /system     100GB                  │
└─────────────────────────────────────────┘
```

**Standard (96 TPU, 20 personas)**
```
┌─────────────────────────────────────────┐
│  Primary: 2TB NVMe Gen4 (models + hot)  │
│  ├── /models     1TB                    │
│  ├── /vectors    200GB                  │
│  └── /cache      800GB                  │
│                                         │
│  Secondary: 2TB NVMe Gen4 (data)        │
│  ├── /data       1.5TB                  │
│  └── /backups    500GB                  │
└─────────────────────────────────────────┘
```

**Enterprise (96 TPU, 50+ personas)**
```
┌─────────────────────────────────────────┐
│  Primary: 2x 2TB NVMe Gen5 (RAID 0)     │
│  ├── /models     2TB                    │
│  ├── /vectors    500GB                  │
│  └── /cache      1.5TB                  │
│                                         │
│  Secondary: 4x 4TB NVMe (RAID 10)       │
│  ├── /data       8TB usable             │
│  └── Redundancy for reliability         │
│                                         │
│  Archive: NAS/SAN connection            │
│  └── Cold storage for old data          │
└─────────────────────────────────────────┘
```

---

## Physical Storage Layout

### Drive Bay Design

The Coral-Reef tower includes integrated storage bays:

```
    STORAGE MODULE (Base Section)

    ┌─────────────────────────────────────┐
    │           TOP PLATE                 │
    ├─────────────────────────────────────┤
    │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐│
    │  │NVMe │  │NVMe │  │NVMe │  │NVMe ││  ← 4x M.2 2280 slots
    │  │ #1  │  │ #2  │  │ #3  │  │ #4  ││    (vertical mount)
    │  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘│
    │     │       │       │       │     │
    │  ┌──┴───────┴───────┴───────┴──┐  │
    │  │      HEATSINK PLATE         │  │  ← Shared thermal mass
    │  │      (aluminum, finned)     │  │
    │  └─────────────────────────────┘  │
    │                                    │
    │  ┌──────────────────────────────┐ │
    │  │    2.5" SSD BAY (optional)   │ │  ← For SATA SSD
    │  └──────────────────────────────┘ │
    ├─────────────────────────────────────┤
    │          POWER DISTRIBUTION         │
    └─────────────────────────────────────┘

    Airflow: Intake air passes over NVMe heatsinks
             before entering main TPU section
```

### NVMe Thermal Management

```
    NVMe COOLING DETAIL

    Intake Air →→→→→→→→→→→→→→→→→→→→→→→→→→→
                     │ │ │ │
              ┌──────┼─┼─┼─┼──────┐
              │ ░░░░░│░│░│░│░░░░░ │  ← Thermal pad
              │ ┌────┴─┴─┴─┴────┐ │
              │ │   NVMe SSD    │ │
              │ │   Controller  │ │
              │ │      ●        │ │  ← Hottest point
              │ └───────────────┘ │
              │ ░░░░░░░░░░░░░░░░░ │  ← Thermal pad (bottom)
              └───────┬───────────┘
                      │
              ┌───────┴───────┐
              │   HEATSINK    │
              │  ┌─┬─┬─┬─┬─┐  │
              │  │ │ │ │ │ │  │  ← Vertical fins
              │  │ │ │ │ │ │  │
              └──┴─┴─┴─┴─┴─┴──┘
                     ↓ ↓ ↓
              Airflow continues to TPU layers

    Target: Keep NVMe controller <70°C
    Gen4/5 drives can throttle at 80°C+
```

---

## Data Organization

### Directory Structure

```
/coral-reef/
├── models/                      # AI model storage
│   ├── base/                    # Base model weights
│   │   ├── gemma-3-4b/
│   │   ├── gemma-3-27b/
│   │   └── embedding-e5/
│   ├── quantized/               # INT8/INT4 versions
│   │   ├── gemma-3-4b-int8/
│   │   └── gemma-3-27b-int4/
│   └── adapters/                # LoRA/fine-tuned weights
│       ├── persona-alice/
│       ├── persona-bob/
│       └── custom-lora-1/
│
├── vectors/                     # Vector database storage
│   ├── shared/                  # Shared knowledge base
│   │   ├── index.bin
│   │   └── metadata.db
│   └── personas/                # Per-persona vectors
│       ├── alice/
│       ├── bob/
│       └── .../
│
├── data/                        # Document and data storage
│   ├── documents/               # Uploaded documents
│   │   ├── raw/                 # Original files
│   │   └── processed/           # Extracted text/chunks
│   ├── conversations/           # Chat histories
│   │   └── {session_id}/
│   └── memories/                # Long-term memory store
│       └── {persona_id}/
│
├── cache/                       # Temporary/cache data
│   ├── model_cache/             # Loaded model cache
│   ├── embedding_cache/         # Recent embeddings
│   └── inference_cache/         # KV cache snapshots
│
└── config/                      # Configuration files
    ├── personas.yaml
    ├── models.yaml
    └── system.yaml
```

### File Format Specifications

**Model Files**
```
/models/quantized/gemma-3-4b-int8/
├── config.json              # Model configuration
├── tokenizer.json           # Tokenizer
├── model.safetensors        # Weights (SafeTensors format)
├── tpu_config.json          # TPU-specific settings
└── manifest.json            # Checksums, metadata
```

**Vector Index Files**
```
/vectors/personas/alice/
├── index.bin                # HNSW index binary
├── vectors.npy              # Raw vectors (numpy)
├── metadata.sqlite          # Document metadata
├── id_mapping.json          # Vector ID to doc mapping
└── config.json              # Index parameters
```

**Memory Store Files**
```
/data/memories/alice/
├── memories.sqlite          # SQLite database
├── embeddings.npy           # Memory embeddings
├── relationships.json       # Entity relationships
└── emotional_state.json     # Current emotional state
```

---

## Vector Database Design

### Index Configuration

```
VECTOR INDEX PARAMETERS

┌─────────────────────────────────────────────────────────────────┐
│  HNSW (Hierarchical Navigable Small World) Index               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Embedding Dimension:  1024 (E5-large) or 384 (MiniLM)         │
│  Distance Metric:      Cosine similarity                        │
│  M (connections):      32 (higher = better recall, more RAM)   │
│  EF Construction:      200 (build-time quality)                 │
│  EF Search:            64 (query-time accuracy)                 │
│                                                                 │
│  Memory Usage:         ~1.5KB per vector (1024-dim)            │
│  10M tokens (~20K vectors) = ~30MB index                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Query Flow

```
    RAG QUERY PIPELINE

    User Query: "What did we discuss about quantum computing?"
         │
         ▼
    ┌─────────────────┐
    │  EMBED QUERY    │──► 1024-dim vector
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  SEARCH LAYERS  │     │  Search order:  │
    │                 │     │  1. Memories    │
    │  ┌───────────┐  │     │  2. Persona KB  │
    │  │ Memories  │──┼────►│  3. Shared KB   │
    │  └───────────┘  │     │  4. Documents   │
    │  ┌───────────┐  │     └─────────────────┘
    │  │ Persona KB│  │
    │  └───────────┘  │
    │  ┌───────────┐  │
    │  │ Shared KB │  │
    │  └───────────┘  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  RERANK + FUSE  │──► Top 10 results, deduplicated
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  FORMAT CONTEXT │──► Structured context for LLM
    └─────────────────┘
```

### Sharding Strategy

For large deployments (50+ personas):

```
    VECTOR DATABASE SHARDING

    ┌─────────────────────────────────────────────────────────────┐
    │                    SHARD COORDINATOR                        │
    │                                                             │
    │  Query → Hash(persona_id) → Route to shard                 │
    └─────────────────────────────────────────────────────────────┘
                    │           │           │
         ┌──────────┴───┐ ┌─────┴─────┐ ┌───┴──────────┐
         ▼              ▼ ▼           ▼ ▼              ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Shard 0 │    │ Shard 1 │    │ Shard 2 │    │ Shard 3 │
    │ NVMe #1 │    │ NVMe #1 │    │ NVMe #2 │    │ NVMe #2 │
    │         │    │         │    │         │    │         │
    │ P: 0-12 │    │ P: 13-24│    │ P: 25-37│    │ P: 38-50│
    └─────────┘    └─────────┘    └─────────┘    └─────────┘

    P = Persona IDs assigned to shard
    Each shard: Separate HNSW index file
    Parallel search across shards for shared knowledge
```

---

## Model Loading Optimization

### Memory-Mapped Loading

```
    MODEL LOADING STRATEGIES

    STRATEGY 1: Full Load (Small models <8GB)
    ┌─────────────────────────────────────────────────────────────┐
    │  NVMe → Read entire model → RAM → Transfer to TPU          │
    │  Time: ~2-5 seconds for 4GB model                          │
    │  RAM Usage: Full model size                                 │
    └─────────────────────────────────────────────────────────────┘

    STRATEGY 2: Memory-Mapped (Large models 8-32GB)
    ┌─────────────────────────────────────────────────────────────┐
    │  NVMe ←→ Virtual Memory (mmap) → Stream to TPU on demand   │
    │  Time: ~500ms initial, pages loaded as needed              │
    │  RAM Usage: Only active pages (~4-8GB)                     │
    └─────────────────────────────────────────────────────────────┘

    STRATEGY 3: Streaming Load (Very large models >32GB)
    ┌─────────────────────────────────────────────────────────────┐
    │  NVMe → Stream layers sequentially → TPU pipeline          │
    │  Time: ~10-30 seconds total                                │
    │  RAM Usage: One layer at a time (~1-2GB)                   │
    └─────────────────────────────────────────────────────────────┘
```

### Model Cache Management

```
    MODEL CACHE LRU POLICY

    Cache Size: 32GB RAM allocated

    ┌─────────────────────────────────────────────────────────────┐
    │                    MODEL CACHE                              │
    ├─────────────────────────────────────────────────────────────┤
    │  [HOT]    gemma-3-4b-alice     4.2GB   Last: 0s ago        │
    │  [HOT]    gemma-3-4b-bob       4.2GB   Last: 5s ago        │
    │  [WARM]   gemma-3-4b-carol     4.2GB   Last: 2m ago        │
    │  [WARM]   embedding-e5         1.3GB   Last: 10s ago       │
    │  [COLD]   gemma-3-4b-dave      4.2GB   Last: 15m ago       │
    │  [COLD]   vision-encoder       2.1GB   Last: 1h ago        │
    │  ─────────────────────────────────────────────────────     │
    │  Total Cached: 20.2GB / 32GB                               │
    │  Free: 11.8GB                                              │
    └─────────────────────────────────────────────────────────────┘

    Eviction Policy:
    1. Never evict HOT models (used in last 60s)
    2. Prefer evicting COLD over WARM
    3. LRU within temperature tier
    4. Keep embedding models loaded (shared resource)
```

---

## Conversation & Memory Persistence

### SQLite Schema for Conversations

```sql
-- conversations.sqlite

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    persona_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    summary TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id),
    role TEXT NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tokens INTEGER,
    metadata JSON  -- tool calls, emotions, etc.
);

CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding BLOB,  -- 1024-dim float32
    importance REAL DEFAULT 0.5,
    recency REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    source_session TEXT,
    source_message INTEGER,
    tags JSON
);

CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_memories_persona ON memories(persona_id);
CREATE INDEX idx_memories_importance ON memories(persona_id, importance DESC);
```

### Memory Consolidation Process

```
    MEMORY LIFECYCLE

    New Information (conversation)
         │
         ▼
    ┌─────────────────┐
    │ IMPORTANCE      │
    │ SCORING         │
    │                 │
    │ • Emotional     │
    │   intensity     │
    │ • User explicit │
    │   request       │
    │ • Novel info    │
    │ • References    │
    │   past context  │
    └────────┬────────┘
             │
             ├─── Score < 0.3 ───► DISCARD
             │
             ├─── Score 0.3-0.7 ─► SHORT-TERM BUFFER
             │                          │
             │                     After 24h, re-score
             │                          │
             │                     ┌────┴────┐
             │                     │         │
             │                   <0.5      ≥0.5
             │                     │         │
             │                  DISCARD   CONSOLIDATE
             │                              │
             └─── Score > 0.7 ─────────────►│
                                            ▼
                                    ┌───────────────┐
                                    │  LONG-TERM    │
                                    │  MEMORY       │
                                    │               │
                                    │  • Embed      │
                                    │  • Index      │
                                    │  • Link to    │
                                    │    related    │
                                    │    memories   │
                                    └───────────────┘
```

---

## Backup & Recovery

### Backup Strategy

```
    BACKUP TIERS

    ┌─────────────────────────────────────────────────────────────┐
    │  TIER 1: Hot Backup (Every 15 minutes)                      │
    │                                                             │
    │  • SQLite WAL checkpoints                                   │
    │  • Vector index snapshots (incremental)                     │
    │  • Memory state snapshots                                   │
    │  • Location: Secondary NVMe                                 │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  TIER 2: Daily Backup (Every 24 hours)                      │
    │                                                             │
    │  • Full database dumps                                      │
    │  • Vector database export                                   │
    │  • Configuration backup                                     │
    │  • Location: External storage / NAS                         │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  TIER 3: Archive Backup (Weekly)                            │
    │                                                             │
    │  • Compressed full system backup                            │
    │  • Model weights (if modified)                              │
    │  • Retain 4 weekly snapshots                                │
    │  • Location: Cloud storage (optional)                       │
    └─────────────────────────────────────────────────────────────┘
```

### Recovery Procedures

```
    RECOVERY SCENARIOS

    ┌─────────────────────────────────────────────────────────────┐
    │  SCENARIO: Single persona data corruption                   │
    ├─────────────────────────────────────────────────────────────┤
    │  1. Stop persona service                                    │
    │  2. Restore from Tier 1 backup (15 min data loss max)      │
    │  3. Rebuild vector index from documents                     │
    │  4. Restart persona                                         │
    │  Time: ~5 minutes                                           │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  SCENARIO: Primary NVMe failure                             │
    ├─────────────────────────────────────────────────────────────┤
    │  1. System boots from secondary NVMe (if RAID)             │
    │  2. OR: Restore Tier 2 backup to replacement drive         │
    │  3. Re-download models from cache/repository               │
    │  4. Rebuild indexes                                         │
    │  Time: ~30 minutes to 2 hours                              │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  SCENARIO: Full system recovery                             │
    ├─────────────────────────────────────────────────────────────┤
    │  1. Install base OS                                         │
    │  2. Restore Tier 3 backup                                   │
    │  3. Download models                                         │
    │  4. Rebuild all indexes                                     │
    │  5. Verify data integrity                                   │
    │  Time: ~2-4 hours                                           │
    └─────────────────────────────────────────────────────────────┘
```

---

## Performance Optimization

### I/O Optimization Settings

```bash
# /etc/sysctl.conf optimizations for AI workloads

# Increase dirty page limits for large writes
vm.dirty_ratio = 40
vm.dirty_background_ratio = 10

# Optimize for SSD
vm.swappiness = 10

# Increase file handle limits
fs.file-max = 2097152

# Network buffers for P2P
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
```

### NVMe Tuning

```bash
# Optimal NVMe scheduler for AI workloads
echo "none" > /sys/block/nvme0n1/queue/scheduler

# Increase read-ahead for sequential model loads
blockdev --setra 4096 /dev/nvme0n1

# Enable write caching (if battery backup available)
hdparm -W1 /dev/nvme0n1
```

### Filesystem Recommendations

```
FILESYSTEM COMPARISON

┌───────────────┬─────────────┬─────────────┬─────────────┐
│ Use Case      │ Recommended │ Alternative │ Avoid       │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ Models        │ XFS         │ ext4        │ btrfs       │
│ (large files) │ (best seq)  │ (good)      │ (overhead)  │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ Vectors/DB    │ ext4        │ XFS         │ ZFS*        │
│ (random I/O)  │ (low lat)   │ (good)      │ (RAM heavy) │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ Documents     │ btrfs       │ ext4        │ -           │
│ (snapshots)   │ (CoW snap)  │ (manual)    │             │
└───────────────┴─────────────┴─────────────┴─────────────┘

* ZFS is excellent but requires significant RAM for ARC
```

---

## Hardware Recommendations

### NVMe Drive Selection

| Tier | Model Examples | Specs | Use Case |
|------|----------------|-------|----------|
| Enterprise | Samsung PM9A3, Intel D7-P5520 | 7GB/s, 1M IOPS, 1 DWPD | 24/7 operation |
| Prosumer | Samsung 990 Pro, WD SN850X | 7GB/s, 1M IOPS | Heavy workloads |
| Consumer | Samsung 980 Pro, SK Hynix P41 | 5GB/s, 700K IOPS | Budget builds |

### Recommended Configurations

**Budget Build (~$200 storage)**
```
1x Samsung 980 Pro 2TB ($150)
- Models + all data on single drive
- External backup drive
```

**Standard Build (~$500 storage)**
```
1x Samsung 990 Pro 2TB ($200) - Models + cache
1x Samsung 990 Pro 2TB ($200) - Data + vectors
1x External 4TB HDD ($100) - Backups
```

**Enterprise Build (~$2000 storage)**
```
2x Intel D7-P5520 3.84TB ($800 each) - RAID 1
2x Samsung PM9A3 1.92TB ($300 each) - Data RAID 1
NAS connection for archives
```

---

## Monitoring & Alerts

### Storage Metrics to Monitor

```
STORAGE DASHBOARD

┌─────────────────────────────────────────────────────────────────┐
│  NVMe #1 (Models)                                               │
│  ├── Capacity: 1.8TB / 2TB (90%)        ▓▓▓▓▓▓▓▓▓░ WARNING    │
│  ├── Read: 2.1 GB/s                     ▓▓▓▓▓░░░░░            │
│  ├── Write: 450 MB/s                    ▓▓░░░░░░░░            │
│  ├── Temperature: 52°C                  ▓▓▓▓▓░░░░░ OK         │
│  └── Health: 98% (23TB written)         ▓▓▓▓▓▓▓▓▓░            │
├─────────────────────────────────────────────────────────────────┤
│  NVMe #2 (Data)                                                 │
│  ├── Capacity: 850GB / 2TB (42%)        ▓▓▓▓░░░░░░ OK         │
│  ├── Read: 1.8 GB/s                     ▓▓▓▓░░░░░░            │
│  ├── Write: 1.2 GB/s                    ▓▓▓░░░░░░░            │
│  ├── Temperature: 48°C                  ▓▓▓▓░░░░░░ OK         │
│  └── Health: 99% (12TB written)         ▓▓▓▓▓▓▓▓▓░            │
├─────────────────────────────────────────────────────────────────┤
│  Vector DB Performance                                          │
│  ├── Query Latency (p50): 12ms          ▓▓░░░░░░░░ GOOD       │
│  ├── Query Latency (p99): 45ms          ▓▓▓░░░░░░░ OK         │
│  ├── Index Size: 2.4GB                                         │
│  └── Documents Indexed: 125,000                                │
└─────────────────────────────────────────────────────────────────┘

ALERTS:
• Capacity >85%: Warning
• Capacity >95%: Critical
• Temperature >70°C: Warning
• Health <90%: Warning (plan replacement)
• Query latency p99 >100ms: Warning
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial storage subsystem design |
