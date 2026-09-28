#!/usr/bin/env python3
"""Check kem-18-2: LoongKEM's reducible rings and quotient estimates."""

import math
import os
import random
import subprocess
import sys
from pathlib import Path


Q = 8191
ESTIMATOR_COMMIT = "53da5982597709ba0fdf94ea37a84d822310fd84"
SETS = (
    # name, N, k1, k2, eta, db, weak degree, resultant
    ("Loong128", 12, 48, 4, 5, 10, 4, 81),
    ("Loong384", 20, 72, 8, 3, 11, 4, 625),
    ("Loong512", 24, 80, 10, 2, 11, 8, 6561),
)
EXPECTED_WEAK = (73.0617, 103.3423, 203.7374)
EXPECTED_STRONG = (128.5918, 365.5144, 399.3088)


def reduction_matrix(matrix, ring, modulus, n):
    """Integer coefficient matrix for reduction modulo a monic factor."""
    x = ring.gen()
    d = modulus.degree()
    columns = []
    for j in range(n):
        r = (x**j).mod(modulus)
        columns.append([r[i] for i in range(d)])
    return matrix(ring.base_ring(), columns).transpose()


def main():
    root = Path(__file__).resolve().parents[2]
    estimator_path = Path(
        os.environ.get("LATTICE_ESTIMATOR_PATH", root / "lattice-estimator")
    ).resolve()
    try:
        revision = subprocess.check_output(
            ["git", "-C", str(estimator_path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(
            "LATTICE_ESTIMATOR_PATH must name a git checkout of malb/lattice-estimator"
        ) from exc
    if revision != ESTIMATOR_COMMIT:
        raise SystemExit(
            f"lattice-estimator must be at {ESTIMATOR_COMMIT}; found {revision}"
        )

    sys.path.insert(0, str(estimator_path))
    try:
        from estimator import LWE, ND
        from sage.all import GF, PolynomialRing, ZZ, log, matrix
    except ImportError as exc:
        raise SystemExit(
            "run with a Python interpreter that provides sage.all and set "
            "LATTICE_ESTIMATOR_PATH"
        ) from exc

    rz = PolynomialRing(ZZ, "x")
    rq = PolynomialRing(GF(Q), "x")
    x = rz.gen()
    rng = random.Random(18)
    weak_bits = []
    strong_bits = []

    for name, n_ring, k1, k2, eta, db, weak_degree, expected_resultant in SETS:
        whole = x**n_ring + 1
        factors = [factor for factor, multiplicity in whole.factor() for _ in range(multiplicity)]
        weak = next(factor for factor in factors if factor.degree() == weak_degree)
        strong = whole // weak
        resultant = abs(weak.resultant(strong))
        assert resultant == expected_resultant
        assert rq(weak).gcd(rq(strong)) == 1

        # Public reduction is a ring homomorphism, not just a dimension count.
        a = sum(rng.randrange(Q) * x**j for j in range(n_ring))
        b = sum(rng.randrange(Q) * x**j for j in range(n_ring))
        product = (rq(a) * rq(b)).mod(rq(whole))
        for factor in (weak, strong):
            assert product.mod(rq(factor)) == (
                rq(a).mod(rq(factor)) * rq(b).mod(rq(factor))
            ).mod(rq(factor))

        # The two quotient values reconstruct the original residue by CRT.
        fq_weak, fq_strong, fq_whole = rq(weak), rq(strong), rq(whole)
        gcd, u, v = fq_weak.xgcd(fq_strong)
        assert gcd == 1
        original = rq(a).mod(fq_whole)
        r_weak, r_strong = original.mod(fq_weak), original.mod(fq_strong)
        rebuilt = (r_weak * v * fq_strong + r_strong * u * fq_weak).mod(fq_whole)
        assert rebuilt == original

        weak_transform = reduction_matrix(matrix, rz, weak, n_ring)
        strong_transform = reduction_matrix(matrix, rz, strong, n_ring)
        weak_gram = weak_transform * weak_transform.transpose()
        strong_gram = strong_transform * strong_transform.transpose()
        weak_fold = int(weak_gram[0, 0])
        strong_fold = int(strong_gram[0, 0])
        assert weak_gram == weak_fold * weak_gram.parent().one()
        assert strong_fold == 2
        strong_degree = strong.degree()
        max_correlation = max(
            abs(float(strong_gram[i, j])) / strong_fold
            for i in range(strong_degree)
            for j in range(strong_degree)
            if i != j
        )
        assert abs(max_correlation - 0.5) < 1e-12

        def bdd_estimate(degree, fold):
            # Compression step is 2^(ceil(log2(q))-db). Its independent
            # uniform-rounding surrogate has variance step^2/12. Reduction
            # folds both CBD coefficients and rounding errors `fold` times.
            step = 2 ** (13 - db)
            sigma = math.sqrt(fold * (eta / 2 + step**2 / 12))
            params = LWE.Parameters(
                n=(k1 + k2) * degree,
                q=Q,
                Xs=ND.CenteredBinomial(fold * eta),
                Xe=ND.DiscreteGaussian(sigma),
                m=k1 * degree,
            )
            return float(log(LWE.primal_bdd(params)["rop"], 2))

        weak_cost = bdd_estimate(weak.degree(), weak_fold)
        strong_cost = bdd_estimate(strong.degree(), strong_fold)
        weak_bits.append(weak_cost)
        strong_bits.append(strong_cost)
        print(
            f"{name}: factors {weak} and {strong}; resultant={resultant}; "
            f"weak BDD={weak_cost:.2f} bits; complementary BDD={strong_cost:.2f} bits; "
            f"max complementary correlation={max_correlation:.2f}"
        )

    ok = all(abs(a - b) < 0.02 for a, b in zip(weak_bits, EXPECTED_WEAK))
    ok &= all(abs(a - b) < 0.02 for a, b in zip(strong_bits, EXPECTED_STRONG))
    if ok:
        print("CONFIRMED: ring projections and covariance-blind MATZOV BDD estimates reproduced")
        print("LIMITATION: complementary quotient coordinates have correlation magnitude 1/2")
        return 0
    print("NOT CONFIRMED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
