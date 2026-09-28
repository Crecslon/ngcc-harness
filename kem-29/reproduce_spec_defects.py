#!/usr/bin/env python3
"""Certify Polar-KEM findings kem-29-3 and kem-29-4."""

from math import comb, log2
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
SPEC_TEX = ROOT / "Submission_Package" / "Algorithm_Text" / "polarkem-spec.tex"
SPEC_PDF = ROOT / "kem-29-spec.pdf"


def binomial_cdf_half(n: int, bound: int) -> float:
    return sum(comb(n, k) for k in range(bound + 1)) / (1 << n)


def signed_unit_safe_probability(n: int, norm_squared_bound: int) -> float:
    """Probability a random signed unit shift remains an accepted honest error.

    By symmetry fix the + sign.  An original coefficient -1 becomes 0 with
    probability 1/4, and 0 becomes +1 with probability 1/2.  The +1 case
    leaves the specified ternary alphabet and is excluded.
    """
    return (
        0.25 * binomial_cdf_half(n - 1, norm_squared_bound)
        + 0.5 * binomial_cdf_half(n - 1, norm_squared_bound - 1)
    )


def main() -> None:
    if SPEC_TEX.is_file():
        text = SPEC_TEX.read_text()
        source_tex = True
    else:
        text = subprocess.check_output(
            ["pdftotext", "-layout", str(SPEC_PDF), "-"], text=True
        )
        source_tex = False

    # Normative structure and parameters used by both certificates.
    if source_tex:
        assert r"R_\ell = 2^{-\ell}" in text
        assert r"C_0 + 2C_1 + 4C_2" in text
        assert r"\rho < \lambda_1(\Lambda) / 2" in text
        assert "Decoding radius & 15.0 & 31.0 & 63.0" in text
        assert r"$\delta$ (decryption failure prob.) & $< 2^{-128}$ & $< 2^{-256}$ & $< 2^{-512}$" in text
        assert r"4^5 = 1024 > 3844" in text
        assert r"4^6 = 4096 > 15876" in text
    else:
        assert "Rℓ = 2−ℓ" in text
        assert "Λpolar = C0 + 2C1 + 4C2" in text
        assert "ρ satisfies ρ < λ1 (Λ)/2" in text
        assert re.search(r"Decoding radius\s+15\.0\s+31\.0\s+63\.0", text)
        assert re.search(r"δ \(decryption failure prob\.\)\s+< 2−128\s+< 2−256\s+< 2−512", text)
        assert "45 = 1024 > 3844" in text
        assert "46 = 4096 > 15876" in text

    # R_0=1 means C_0 is the full binary space.  Since C_0 is included
    # unscaled, every unit vector is a lattice vector: lambda_1=1.
    assert 2 ** 0 == 1
    lambda1 = 1

    honest_accept_128 = binomial_cdf_half(512, 15 * 15)
    honest_failure_128 = 1.0 - honest_accept_128
    assert abs(honest_failure_128 - 0.996518496182011) < 1e-15

    # Algorithm 7 accepts solely on the residual norm and returns Extract(m).
    if source_tex:
        decaps = text[text.index(r"\caption{$\polarKem.\mathsf{Decaps}") :]
        decaps = decaps[: decaps.index(r"\end{algorithm}")]
        assert r"\norm{\widehat{\mathbf{e}}} > \rho" in decaps
        assert r"K \gets \Extract(\widehat{\mathbf{m}})" in decaps
    else:
        decaps = text[text.index("Algorithm 7 Polar-KEM.Decaps") :]
        decaps = decaps[: decaps.index("5     Security Analysis")]
        assert "e∥ > ρ" in decaps
        assert "K ← Extract(" in decaps
    assert "re-encrypt" not in decaps.lower()

    # This certificate does not assume the contradicted minimum-distance
    # guarantee.  A random signed unit perturbation stays in the honest
    # ternary-error alphabet with probability 3/4.  Its point probabilities
    # are at most twice those of the honest distribution, so a decoder with
    # claimed honest failure delta fails on these shifted inputs with
    # probability at most 2*delta.  The values below additionally impose the
    # public residual-norm check.
    alias_128 = signed_unit_safe_probability(512, 15 * 15)
    alias_256 = signed_unit_safe_probability(1024, 31 * 31)
    alias_512 = signed_unit_safe_probability(2048, 63 * 63)

    assert abs(alias_128 - 0.002495639076518277) < 1e-18
    assert alias_256 == 0.75
    assert alias_512 == 0.75

    print(f"PolarKEM-128 honest rejection probability: {honest_failure_128:.15f}")
    print(f"normative R_0=1 gives lambda_1={lambda1}")
    print(
        "signed-unit alias lower bound before decoder failures: "
        f"128={alias_128:.16g} (2^{log2(alias_128):.4f}); "
        f"256={alias_256:.2f}; 512={alias_512:.2f}"
    )
    print("POLARKEM_SPEC_DEFECTS_CONFIRMED")


if __name__ == "__main__":
    main()
