# Ecc-crypto-formulas-by-samamahacks
ecdh-key-exchange-python
Educational ECDH Key Exchange

A lightweight, zero-dependency Python implementation of Elliptic Curve Diffie-Hellman (ECDH) for educational and experimental purposes.

This project demonstrates the fundamental mathematics behind Elliptic Curve Cryptography (ECC), including point addition, point doubling, scalar multiplication, public-key generation, and shared-secret calculation.

# Features

**Hexadecimal / Decimal Input:** Accepts numeric values in both Hexadecimal and Decimal formats.
**Custom Curve Parameters:** Allows the user to provide p, a, and b.
**Custom Generator Point:** Accepts the generator point G = (X, Y).
**Server Public Key:** Accepts and validates the server's public key.
**Secure Random Private Key:** Generates the client private key using Python's secrets module.
**Public Key Generation:** Calculates the client public key using scalar multiplication.
**Shared Secret Calculation:** Calculates the ECDH shared secret from the client private key and server public key.
**Point Validation:** Verifies that supplied points belong to the specified curve.
**Error Handling:** Provides clear errors for invalid input and invalid ECC points.
**Dual Output:** Displays important values in both Decimal and Hexadecimal formats.
Zero External Dependencies: Uses Python's standard library only.

The Math Behind It
The elliptic curve is represented by the equation:

𝑦<pow>2 ≡ 𝑥<pow>3 + 𝑎𝑥 + 𝑏 (mod𝑝)

Where:

p = Field prime
a = Curve parameter
b = Curve parameter
G = Generator point

(x, y) = A point on the elliptic curve

ECDH Key Exchange

The client generates a private key a and calculates its public key:

A = aG

The server has its own private key b and corresponding public key:

B = bG

The client calculates the shared secret:

S = aB

The server independently calculates:

S = bA

Because:

aB = a(bG) = b(aG) = bA

both parties obtain the same shared secret.

# ECC Operations

Point Addition: Calculates P + Q.
Point Doubling: Calculates 2P.
Scalar Multiplication: Calculates kP using the Double-and-Add algorithm.
Modular Inverse: Calculates the multiplicative inverse modulo p.
Point Validation: Checks whether a point satisfies the elliptic-curve equation.
Point-at-Infinity Handling: Handles the identity element of the elliptic-curve group.

# Input Format

The program accepts both Decimal and Hexadecimal values.

Decimal
123456789

Hexadecimal
0x75BCD15


The program also supports hexadecimal values containing characters from A-F.

# Program Inputs

The program asks the user for:

Field Prime p
Curve Parameter a
Curve Parameter b
Generator Point G
Server Public Key

The generator point is entered as:

G X
G Y


The server public key is entered as:

Server Public Key X
Server Public Key Y

Validation and Error Handling

Before performing ECC calculations, the program verifies that the supplied points satisfy:

y² ≡ x³ + ax + b (mod p)

# The program handles:

Empty input
Invalid Decimal input
Invalid Hexadecimal input
Invalid generator point
Invalid server public key
Invalid curve points
Modular inverse errors
Point-at-Infinity results
Unexpected runtime errors

# Output

After a successful calculation, the program displays:

# CLIENT PRIVATE KEY

# CLIENT PUBLIC KEY
X (Decimal)
X (Hexadecimal)
Y (Decimal)
Y (Hexadecimal)

# SHARED SECRET POINT
X (Decimal)
X (Hexadecimal)
Y (Decimal)
Y (Hexadecimal)

# How to Run

Save the Python script:

python ecc.py


# Run the script:

python eccdh.py

Enter the requested curve parameters and server public key.

# Requirements

Python 3.8 or higher
No external libraries required
Uses Python's built-in secrets module.

# Security Notes

This project is intended for educational and experimental purposes only.
The ECC operations are implemented manually to demonstrate the underlying mathematics. For production cryptographic applications, use a well-tested and professionally audited cryptographic library.
Never expose private keys or shared secrets in public logs, screenshots, repositories, or other publicly accessible locations.
The client does not calculate, recover, or derive the server's private key. The server private key must remain secret on the server, while only the server public key is shared with the client.

# Educational Purpose

This project can be used to understand:

Elliptic Curve Cryptography
Finite Field Arithmetic
Point Addition
Point Doubling
Scalar Multiplication
Double-and-Add Algorithm
Public-Key Cryptography
ECDH Key Exchange
Shared Secret Calculation
Hexadecimal and Decimal Representation

# Project Structure
.
├── eccdh.py
└── README.md

# License

This project is provided for educational and experimental purposes. It should not be considered a replacement for professionally audited cryptographic software in production environments.
