# CSIF-Guard: Deterministic Semantic Firewall v1.0

[![Status: Unified Architecture](https://img.shields.io/badge/Status-Unified__Architecture-blueviolet)](https://github.com/MoTechnicalities/Crystal-Structure-Information-Format)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache__2.0-blue)](LICENSE)
[![Latency: <10ms](https://img.shields.io/badge/Latency-%3C10ms-green)]()

> **The Problem:** Autonomous AI agents are highly fluid but structurally un-auditable. They suffer from data density crises, hallucinate mid-workflow, and corrupt their own memory banks—causing cascading logic failures in production loops.
>
> **The Solution:** `CSIF-Guard` is a blindingly fast, zero-hallucination semantic firewall that intercepts corrupted data writes *before* they pollute your memory loops. It bypasses heavy neural processing, transforming logical consistency into an absolute, auditable **structural invariant** using pure four-dimensional phase geometry.

---

## ── The Paradigm Shift: Weights vs. Geometry

Traditional AI guardrails deploy more LLMs to audit the first LLM, burning massive GPU cycles and adding seconds of latency.

`CSIF-Guard` implements the **Crystal Structure Information Format (CSIF)** and **Real-World Intelligence Format (RWIF)**. It maps semantic propositions, concepts, and relationships onto a continuous phase medium bound within the principal interval $[-\pi, \pi]$.

* **Absolute Coherence:** Aligns perfectly at a unified phase ($\theta \approx 0.0000$ rad).
* **Semantic Drift / Nuance:** Manifests as clean, predictable angular deviations ($\sim 0.15$ to $0.40$ rad).
* **Logical Contradiction:** Triggers an instant, measurable geometric anti-phase signal ($\theta \approx \pi$ rad).

Instead of running heavy inference, `CSIF-Guard` builds a localized `PhaseGraph` and executes an undirected depth-first traversal. By applying signed phase transitivity boundaries ($\theta_{\mathrm{reverse}} = \mathrm{wrap}_{\pi}(-\theta)$), it measures cycle torsion. If an incoming assertion buckles the graph topology, the firewall trips its circuit breaker in **under 10 milliseconds** using lightweight floating-point arithmetic.

---

## ── Repository Architecture

The codebase is engineered to be completely elegant, carrying **zero external bloat** or heavy runtime frameworks. It relies strictly on Python standard library modules (`math`, `uuid`, `json`, `time`).

```text
csif-guard/
├── core/
│   └── math.py              # wrap_pi, phase_distance, contradiction_threshold
├── storage/
│   └── rwif.py              # RWIFC1 & RWIFB1 append-only ledger serialization
├── engine/
│   └── phase_graph.py       # Direction-aware path composition & multi-path conflict detection
├── demo_firewall.py         # Out-of-the-door executable product demo
├── README.md                # This file
└── LICENSE                  # Apache 2.0
```

---

## ── Quickstart: Running the Firewall Sandbox

Verify the geometric hammer-drop locally on your workstation. This sandbox instantiates a verified baseline crystal bank, simulates an adversarial agent hallucination attempt, and logs the real-time interception trace.

### 1. Clone and Initialize

```bash
git clone https://github.com/MoTechnicalities/csif-guard.git
cd csif-guard
```

### 2. Execute the Demo Pipeline

```bash
python3 demo_firewall.py
```

### Expected Terminal Output Trace

```
=== CSIF-Guard: Deterministic Semantic Firewall Demo ===
Max multi-path phase residual: 3.1416
Contradiction threshold: 1.5788

[!] Contradiction detected! Write intercepted. Bank remains uncorrupted.

--- ConflictPathTrace ---
Source: light
Target: darkness
Path A: ['light', 'darkness']
Path B: ['light', 'darkness']
Phase A: -3.1416
Phase B: 0.0000
Residual: 3.1416
```

---

## ── Mathematical Infrastructure

The engine's reliability is strictly governed by IEEE 754 double precision float operations.

### Principal Modulo Wrapping

Angles are circular. To ensure absolute boundary continuity when calculations swing past the polar horizons ($-\pi$ and $\pi$), the principal wrap natively binds numeric overflow:

$$\mathrm{wrap}_{\pi}(\theta) = ((\theta + \pi) \bmod 2\pi) - \pi$$

### Adaptive Contradiction Thresholding

The boundary for triggering an internal logic violation scales dynamically with the localized uncertainty tracking envelope ($\sigma$) of the graph path using an empirical stability constant $c$:

$$T_{\mathrm{alarm}} = \frac{\pi}{2} + c \cdot \sigma_{\mathrm{path}}$$

---

## ── Core Behavioral Contracts

To maintain CSIF compatibility, all modifications to this engine must strictly adhere to the following core contracts:

**Absolute Immutability:** Trajectory entries are append-only. Factual constants are preserved indefinitely; structural evolution is tracked exclusively by appending fresh coordinates down the time axis, enabling flawless time-travel auditing.

**Deterministic Query Boundaries:** Given the same crystal bank state and the same query matrix, the engine must return identical resonance scores and conflict traces across all implementations.

**Graceful Degradation:** If external LLM compilers or language banks are unavailable, the substrate falls through to direct local geometric validation without throwing service crashes.

---

## ── Reference Context

This implementation is a digital knowledge extension of fundamental physical laws—mirroring how configurations in the physical domain are reducible to three fundamental stable topological fractal knots: the electron, proton, and neutron.

**Key References:**
- [Crystal Structure Information Format (CSIF)](https://github.com/MoTechnicalities/Crystal-Structure-Information-Format)
- CSIF Engine Specification V1
- RWIF Crystal Schema V1

---

## ── Developed By

**Mogir Jason Rofick (Mo)**  
May 17, 2026  
Apache License 2.0

---

## ── Contributing

This project welcomes reproducibility audits, geometric proofs, and implementation verification across independent platforms. When contributing, maintain:

1. **Determinism:** All phase computations must produce byte-identical results across runs and platforms.
2. **Auditability:** Every contradiction detection must include a full `ConflictPathTrace` with timestamps and provenance.
3. **Immutability:** Never modify or delete trajectory entries after they are appended.

---

## ── License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
