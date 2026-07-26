import os
import pytest
from hq_bind.commitment import commit, verify, Commitment


def test_roundtrip():
    msg = b"Kerna-Ledger test vector 001"
    rnd = os.urandom(32)
    c = commit(msg, rnd)
    assert verify(c, msg)
    assert not verify(c, b"tampered")


def test_deterministic():
    msg = b"deterministic"
    rnd = b"\x00" * 32
    c1 = commit(msg, rnd)
    c2 = commit(msg, rnd)
    assert c1.binding == c2.binding


def test_domain_separation():
    msg = b"same message"
    rnd = b"\x01" * 32
    c1 = commit(msg, rnd, domain=b"DOMAIN-A")
    c2 = commit(msg, rnd, domain=b"DOMAIN-B")
    assert c1.binding != c2.binding
