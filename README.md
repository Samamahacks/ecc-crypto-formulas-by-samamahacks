# ecc-crypto-formulas-by-samamahacks
# Elliptic Curve Cryptography (ECC) Math Engine

A lightweight, zero-dependency Python implementation of fundamental **Elliptic Curve Cryptography (ECC)** operations. This project demonstrates the core mathematical mechanics behind public-key cryptography, including point addition, point doubling, and scalar multiplication.

##  Features

*   **Point Addition:** Computes $P + Q$ on an elliptic curve.
*   **Point Doubling:** Computes $2P$ efficiently using curve tangents.
*   **Scalar Multiplication:** Computes $kP$ using the efficient Double-and-Add algorithm.
*   **Custom Curve Support:** Define your own curve parameters $(a, b, p)$.

##  The Math Behind It

This engine solves equations over a finite field $\mathbb{F}_p$ in the form:
$$y^2 \equiv x^3 + ax + b \pmod p$$

Where the algebraic operations prevent fractional values by utilizing the **Extended Euclidean Algorithm** for modular inverse calculations.

##  How to Use

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd YOUR-REPO-NAME
   ```

2. **Run the script:**
   ```bash
   python ecc.py
   ```

##  Requirements
* Python 3.6 or higher (No external libraries required).
