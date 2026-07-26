# HQ-Bind

**Hybrid Quantum Binding Protocol — Verifiable Quantum-Inspired Commitments**

Even The Odds Foundry / Kerna-Ledger · 2026

## Overview

HQ-Bind explores deterministic, hybrid classical/quantum-inspired binding commitments that aim to challenge classical Message-Locked Commitment (MLC) impossibility results under the reduction assumptions used throughout the Kerna-Ledger stack.

This repository currently provides a pure-Python reference implementation that is fully deterministic and independently verifiable. It is intended as a research scaffold that will later integrate the formally verified integer-ALU pipeline from `phi-boundary-commitments`.

## Quick Start

```bash
pip install -e .
pytest
```

```python
from hq_bind.commitment import commit, verify
import os

msg = b"SB 253 compliance event"
rnd = os.urandom(32)
c = commit(msg, rnd)
assert verify(c, msg)
```

## Design Principles

- Fully deterministic (no OS entropy in the critical path after randomness is supplied)
- Domain-separated hashing
- Transparent reduction step (phi-inspired fixed-point) that can be replaced by the verified ALU from phi-boundary-commitments
- Compatible with the broader Kerna-Ledger sealing and Merkle pipeline

## Status

- v0.1.0 reference implementation
- Research track — not yet production-hardened
- Continuous health automation monitors this repository

## Related Work

- [phi-boundary-commitments](https://github.com/jabrahns-source/phi-boundary-commitments)
- [Q-Reg](https://github.com/jabrahns-source/Q-Reg)
- [kerna-ledger](https://github.com/jabrahns-source/kerna-ledger)

## License

MIT
