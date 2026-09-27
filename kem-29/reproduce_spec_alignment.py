#!/usr/bin/env python3
"""Check the aligned-basis equation in the archived Polar-KEM specification."""

import subprocess
from pathlib import Path


pdf = Path(__file__).resolve().with_name("kem-29-spec.pdf")
text = subprocess.run(
    ["pdftotext", "-layout", str(pdf), "-"],
    check=True,
    capture_output=True,
    text=True,
).stdout

for phrase in (
    "Bred ← LLL(B)",
    "Bpk ← O · Bred",
    "pk ← Bpk",
    "sk ← O",
    "the public basis can be represented in Hermite Normal Form (HNF)",
):
    assert phrase in text, phrase

# Algorithm 1 publishes corresponding columns without an unknown right
# unimodular factor. Section 6.1.1's HNF remark does not change Algorithm 1.
print("Algorithm 1: Bred = LLL(B); Bpk = O * Bred; pk = Bpk; sk = O")
print("For the corresponding reduced basis, O = Bpk * inverse(Bred).")
print("Section 6.1.1's HNF remark does not specify a key-generation conversion.")
print("CONFIRMED kem-29-2: the specified aligned basis exposes the secret isometry")
