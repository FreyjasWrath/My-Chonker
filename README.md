# My Chonker
**An append-only context stack for lossless aggregation**

---

## What is My Chonker?

My Chonker is a system for collecting, preserving, and aggregating context **without deciding what it means**.

It is designed to safely extract information from conversations or documents, store that information verbatim, and stack it in a way that is **lossless, reversible, and non-authoritative**.

My Chonker exists *before* memory, *before* interpretation, and *before* canon.

---

## What Problem Does This Solve?

When working across many conversations, documents, or systems, context is often:
- summarized too early
- merged irreversibly
- treated as authoritative by accident
- or silently rewritten

My Chonker avoids all of that.

Instead of **merging meaning**, it **stacks context**.

---

## 🧠 Conceptual Overview (Mind Map)

This diagram answers: **“What exists in My Chonker?”**

```mermaid
mindmap
  root((My Chonker))
    Identity
      Title["My Chonker"]
      Bio["Append-only context stack"]
    Core_Principles
      AppendOnly["Append-only"]
      Lossless["Lossless"]
      Reversible["Reversible"]
      NonCanonical["Non-canonical"]
      HumanAuthority["Human-authorized interpretation"]
    Artifacts
      Paper["Paper (per-source JSON)"]
      Archive["Archive (folder of papers)"]
      Container["Container (append-only aggregation)"]
    Controls
      ThreadLens["Thread Lens"]
      BiasMode["Soft / Hard Bias"]
    NonGoals
      NotMemory["Not memory"]
      NotTruth["Not truth"]
      NotAgent["Not an agent"]
      NotAuthority["Not authoritative"]

This is a structural map, not a workflow.
It defines what exists, not what is true.


---

🔁 How My Chonker Works (System Flow)

This diagram answers: “What happens when I run it?”

flowchart LR
    A[Thread / Source] --> B[Chonker Autorun JSON]
    B --> C[Paper JSON]
    C --> D[Raw Archive Folder]
    D --> E[Append-Only Container]
    E -->|optional| F[Filtered / Derived Views]

    C:::safe
    D:::safe
    E:::safe
    F:::derived

    classDef safe fill:#e6f3ff,stroke:#333,stroke-width:1px;
    classDef derived fill:#fce5cd,stroke:#333,stroke-width:1px;

Key properties of this flow:

No step overwrites a previous step

No step decides meaning

No step assigns truth

Interpretation happens only downstream, by humans or other systems



---

Core Artifacts

Paper

A Paper is a single, immutable JSON artifact produced from one source (e.g., one thread).

Verbatim extraction

Dated and sourced

Never edited after creation



---

Archive

An Archive is a folder containing many Papers.

No transformations

No reordering

No deduplication

Pure storage



---

Container

A Container is an append-only aggregation of Papers.

Papers are wrapped, not merged

Fully reversible

Informationally equivalent to the Archive folder


If the container can reproduce all original Papers verbatim, it is valid.


---

What My Chonker Is

An append-only context stack

A lossless aggregation mechanism

A pre-memory, pre-canon pipeline

A portable specification with multiple runtimes



---

What My Chonker Is Not

❌ Not memory

❌ Not truth

❌ Not an agent

❌ Not authoritative

❌ Not a decision-maker


Any system that uses My Chonker may do those things —
My Chonker itself never does.


---

Design Guarantees

Append-only: nothing is overwritten

Lossless: no information is discarded

Reversible: originals can always be recovered

Non-canonical: no implicit truth is created

Human-authorized interpretation only



---

Typical Use Cases

Multi-thread research

Large conversational archives

AI system handoff and alignment

Pre-ingestion filtering for memory systems

Long-running design or architecture projects



---

Status

My Chonker is stable at v1.0.x.

The architecture is locked.
Future changes are additive, not corrective.


---

Philosophy (One Sentence)

> My Chonker stacks context so humans can decide meaning later. 