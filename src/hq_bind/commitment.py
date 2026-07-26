"""Core commitment primitives for HQ-Bind.

This module provides a deterministic, pure-Python reference implementation
of the hybrid binding protocol. Production deployments should replace the
hash and reduction steps with the formally verified integer-ALU pipeline
from phi-boundary-commitments where appropriate.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from typing import Tuple


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _phi_reduce(x: int, modulus: int = 2**64 - 1) -> int:
    """Deterministic golden-ratio inspired reduction (placeholder for formal ALU)."""
    # phi ≈ 1.6180339887; use fixed-point approximation for determinism
    PHI_FIXED = 0x19E3779B97F4A7C1  # 64-bit fixed-point approximation
    return (x * PHI_FIXED) % modulus


@dataclass(frozen=True)
class Commitment:
    binding: bytes          # 32-byte commitment
    opening: bytes          # opening information
    tag: bytes              # domain separation tag


def commit(message: bytes, randomness: bytes, domain: bytes = b"HQ-BIND-v0") -> Commitment:
    """Produce a binding commitment.

    The construction is intentionally simple and fully deterministic so that
    independent verifiers can recompute it exactly. Cryptographic strength
    relies on the collision resistance of SHA-256 and the mixing properties
    of the phi-reduction step.
    """
    if len(randomness) < 16:
        raise ValueError("randomness must be at least 16 bytes")

    # Domain-separated hash of message
    h_msg = _sha256(domain + b"|msg|" + message)

    # Mix randomness through deterministic reduction
    r_int = int.from_bytes(randomness[:8], "big")
    mixed = _phi_reduce(r_int)
    h_rand = _sha256(domain + b"|rand|" + mixed.to_bytes(8, "big") + randomness)

    # Final binding
    binding = _sha256(h_msg + h_rand)
    opening = randomness + h_msg  # sufficient to recompute

    return Commitment(binding=binding, opening=opening, tag=domain)


def verify(commitment: Commitment, message: bytes) -> bool:
    """Recompute and check the binding."""
    try:
        randomness = commitment.opening[: len(commitment.opening) - 32]
        expected = commit(message, randomness, domain=commitment.tag)
        return expected.binding == commitment.binding
    except Exception:
        return False
