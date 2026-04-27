"""Utility to check prime numbers.

This module provides `is_prime(n)` using trial division optimized
with the 6k±1 wheel. The script also includes a small command-line
interface for quick checks.
"""

import argparse
import math
from typing import Any


def is_prime(n: int) -> bool:
	"""Return True if ``n`` is a prime number, else False.

	Behavior notes:
	- Non-integers return ``False`` (the function does not coerce types).
	- Uses trial division: tests 2 and 3, then checks candidates of the
	  form 6k ± 1 up to ``isqrt(n)``. This is faster than testing every odd.
	- Suitable for small-to-moderate integers; for very large numbers,
	  probabilistic tests (e.g., Miller–Rabin) are recommended.
	"""
	if not isinstance(n, int):
		return False
	if n < 2:
		return False
	if n <= 3:
		return True
	if n % 2 == 0 or n % 3 == 0:
		return False

	limit = math.isqrt(n)
	i = 5
	while i <= limit:
		if n % i == 0 or n % (i + 2) == 0:
			return False
		i += 6
	return True


def _main(argv: Any = None) -> None:
	parser = argparse.ArgumentParser(description="Cheque se números são primos")
	parser.add_argument("numbers", nargs="*", type=int, help="Números a testar")
	args = parser.parse_args(argv)
	tests = args.numbers or [-5, 0, 1, 2, 3, 4, 17, 18, 19, 7919]
	for t in tests:
		print(f"{t}: {'prime' if is_prime(t) else 'not prime'}")


if __name__ == "__main__":
	_main()
