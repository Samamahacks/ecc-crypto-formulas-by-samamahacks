"""
Educational ECDH Key Exchange

- p: Field prime, entered as Hexadecimal or Decimal
- a, b: Elliptic curve parameters
- G: Generator point (X, Y), entered as Hexadecimal or Decimal
- Server Public Key: X, Y, entered as Hexadecimal or Decimal
- Client Private Key: Cryptographically random value
- Client Public Key: A = aG
- Shared Secret: S = aB

IMPORTANT:
This is an educational implementation.

For production cryptography, use a well-tested and audited
cryptographic library instead of implementing ECC manually.
"""

import secrets


class ECCError(Exception):
    """Custom exception for ECC-related errors."""
    pass


class ECC:
    def __init__(self, p, a, b, G):
        self.p = p
        self.a = a
        self.b = b
        self.G = G

    # ---------------------------------------------------------
    # Parse an integer from Hexadecimal or Decimal input
    # ---------------------------------------------------------
    @staticmethod
    def parse_int(value, name="Value"):
        value = value.strip()

        if not value:
            raise ECCError(
                f"{name} cannot be empty."
            )

        try:
            # Explicit hexadecimal format
            if value.lower().startswith("0x"):
                return int(value, 16)

            # Automatically detect hexadecimal characters
            if any(c in "abcdefABCDEF" for c in value):
                return int(value, 16)

            # Otherwise treat the input as decimal
            return int(value, 10)

        except ValueError:
            raise ECCError(
                f"{name} is invalid. Enter a valid decimal or hexadecimal value."
            )

    # ---------------------------------------------------------
    # Validate whether a point belongs to the elliptic curve
    # ---------------------------------------------------------
    def is_on_curve(self, P):

        if P is None:
            return True

        x, y = P

        # Coordinates must be inside the finite field
        if not (0 <= x < self.p and 0 <= y < self.p):
            return False

        # Check:
        # y^2 = x^3 + ax + b (mod p)
        return (
            (y * y - (x * x * x + self.a * x + self.b))
            % self.p
            == 0
        )

    # ---------------------------------------------------------
    # Calculate modular inverse
    # ---------------------------------------------------------
    def mod_inverse(self, value):

        value %= self.p

        if value == 0:
            raise ECCError(
                "The modular inverse of zero does not exist."
            )

        # Requires Python 3.8 or newer
        return pow(value, -1, self.p)

    # ---------------------------------------------------------
    # Elliptic curve point addition
    # ---------------------------------------------------------
    def point_add(self, P, Q):

        # Point at infinity acts as the identity element
        if P is None:
            return Q

        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        # P + (-P) = Point at Infinity
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # Point doubling
        if P == Q:

            if y1 % self.p == 0:
                return None

            numerator = (
                3 * x1 * x1 + self.a
            ) % self.p

            denominator = (
                2 * y1
            ) % self.p

        # Normal point addition
        else:

            numerator = (
                y2 - y1
            ) % self.p

            denominator = (
                x2 - x1
            ) % self.p

        inverse = self.mod_inverse(
            denominator
        )

        lam = (
            numerator * inverse
        ) % self.p

        x3 = (
            lam * lam - x1 - x2
        ) % self.p

        y3 = (
            lam * (x1 - x3) - y1
        ) % self.p

        return x3, y3

    # ---------------------------------------------------------
    # Scalar multiplication: kP
    # Uses the Double-and-Add algorithm
    # ---------------------------------------------------------
    def scalar_mult(self, k, P):

        if k < 0:
            raise ECCError(
                "The scalar value cannot be negative."
            )

        if P is None:
            return None

        if not self.is_on_curve(P):
            raise ECCError(
                "The supplied point is not on the elliptic curve."
            )

        result = None
        current = P

        while k > 0:

            if k & 1:
                result = self.point_add(
                    result,
                    current
                )

            current = self.point_add(
                current,
                current
            )

            k >>= 1

        return result


# =============================================================
# INPUT HELPERS
# =============================================================

def read_number(prompt, name):

    while True:

        try:
            raw = input(prompt)

            return ECC.parse_int(
                raw,
                name
            )

        except ECCError as e:

            print(f"\n[ERROR] {e}")
            print("Please enter the value again.\n")


def read_point(point_name):

    print(f"\n--- {point_name} ---")

    x = read_number(
        f"{point_name} X (Hex/Decimal): ",
        f"{point_name} X"
    )

    y = read_number(
        f"{point_name} Y (Hex/Decimal): ",
        f"{point_name} Y"
    )

    return x, y


def print_point(name, P):

    if P is None:

        print(
            f"{name}: Point at Infinity"
        )

        return

    x, y = P

    print(f"\n{name}")
    print("-" * 60)

    print(
        f"X (Decimal)     : {x}"
    )

    print(
        f"X (Hexadecimal) : {hex(x)}"
    )

    print(
        f"Y (Decimal)     : {y}"
    )

    print(
        f"Y (Hexadecimal) : {hex(y)}"
    )


# =============================================================
# MAIN PROGRAM
# =============================================================

def main():

    print("=" * 65)
    print("              ECDH CLIENT KEY EXCHANGE")
    print("=" * 65)

    try:

        # -----------------------------------------------------
        # 1. Read field prime p
        # -----------------------------------------------------

        p = read_number(
            "\nField Prime p (Hex/Decimal): ",
            "p"
        )

        if p <= 2:
            raise ECCError(
                "The field prime p must be greater than 2."
            )

        # -----------------------------------------------------
        # 2. Read curve parameters
        # -----------------------------------------------------

        print("\nEnter the elliptic curve parameters.")

        a = read_number(
            "Curve parameter a (Hex/Decimal): ",
            "a"
        )

        b = read_number(
            "Curve parameter b (Hex/Decimal): ",
            "b"
        )

        # -----------------------------------------------------
        # 3. Read generator point G
        # -----------------------------------------------------

        G = read_point(
            "Generator Point G"
        )

        # Create ECC instance
        ecc = ECC(
            p=p,
            a=a,
            b=b,
            G=G
        )

        # Validate generator point
        if not ecc.is_on_curve(G):

            raise ECCError(
                "The generator point G is not on the specified curve."
            )

        print(
            "\n[OK] Field prime, curve parameters, and generator "
            "point have been validated."
        )

        # -----------------------------------------------------
        # 4. Read server public key
        # -----------------------------------------------------

        server_public = read_point(
            "Server Public Key"
        )

        # Validate server public key
        if not ecc.is_on_curve(server_public):

            raise ECCError(
                "The server public key is not on the specified curve."
            )

        print(
            "\n[OK] Server public key is a valid curve point."
        )

        # -----------------------------------------------------
        # 5. Generate client private key
        # -----------------------------------------------------

        # Generate a cryptographically secure random value.
        client_private = (
            secrets.randbelow(p - 1) + 1
        )

        # -----------------------------------------------------
        # 6. Calculate client public key
        # -----------------------------------------------------

        print(
            "\n[+] Calculating client public key..."
        )

        client_public = ecc.scalar_mult(
            client_private,
            G
        )

        if client_public is None:

            raise ECCError(
                "The client public key resulted in the point at infinity."
            )

        # -----------------------------------------------------
        # 7. Calculate shared secret
        # -----------------------------------------------------

        print(
            "[+] Calculating shared secret..."
        )

        shared_secret = ecc.scalar_mult(
            client_private,
            server_public
        )

        if shared_secret is None:

            raise ECCError(
                "The shared secret resulted in the point at infinity."
            )

        # =====================================================
        # OUTPUT
        # =====================================================

        print("\n")
        print("=" * 65)
        print("                         SUCCESS")
        print("=" * 65)

        # -----------------------------------------------------
        # Client private key
        # -----------------------------------------------------

        print("\nCLIENT PRIVATE KEY")
        print("-" * 60)

        print(
            f"Decimal : {client_private}"
        )

        print(
            f"Hex     : {hex(client_private)}"
        )

        # -----------------------------------------------------
        # Client public key
        # -----------------------------------------------------

        print_point(
            "CLIENT PUBLIC KEY",
            client_public
        )

        # -----------------------------------------------------
        # Shared secret
        # -----------------------------------------------------

        print_point(
            "SHARED SECRET POINT",
            shared_secret
        )

        # -----------------------------------------------------
        # Shared secret values
        # -----------------------------------------------------

        print("\n" + "=" * 65)
        print("                 SHARED SECRET VALUES")
        print("=" * 65)

        print(
            f"\nShared X (Decimal): "
            f"{shared_secret[0]}"
        )

        print(
            f"Shared X (Hex)    : "
            f"{hex(shared_secret[0])}"
        )

        print(
            f"\nShared Y (Decimal): "
            f"{shared_secret[1]}"
        )

        print(
            f"Shared Y (Hex)    : "
            f"{hex(shared_secret[1])}"
        )

        print("\n" + "=" * 65)
        print("               ECDH CALCULATION COMPLETE")
        print("=" * 65)

    # ---------------------------------------------------------
    # Expected ECC errors
    # ---------------------------------------------------------

    except ECCError as e:

        print("\n" + "=" * 65)
        print("                           ERROR")
        print("=" * 65)

        print(
            f"\nReason: {e}"
        )

        print("-" * 65)

    # ---------------------------------------------------------
    # User interruption
    # ---------------------------------------------------------

    except KeyboardInterrupt:

        print(
            "\n\nProgram terminated by the user."
        )

    # ---------------------------------------------------------
    # Unexpected errors
    # ---------------------------------------------------------

    except Exception as e:

        print(
            "\nUnexpected error:"
        )

        print(e)


# =============================================================
# PROGRAM ENTRY POINT
# =============================================================

if __name__ == "__main__":
    main()
