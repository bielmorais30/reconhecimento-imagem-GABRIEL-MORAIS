from typing import Sequence, Tuple


def calculate_statistics(numbers: Sequence[float]) -> Tuple[float, float, float, float]:
    """Return (total, mean, maximum, minimum) for ``numbers``.

    Raises ``ValueError`` if ``numbers`` is empty.
    """
    if not numbers:
        raise ValueError("`numbers` must contain at least one value")

    total = sum(numbers)
    count = len(numbers)
    mean = total / count
    maximum = max(numbers)
    minimum = min(numbers)

    return total, mean, maximum, minimum


if __name__ == "__main__":
    sample = [23, 7, 45, 2, 67, 12, 89, 34, 56, 11]
    total, mean, maximum, minimum = calculate_statistics(sample)
    print("total:", total)
    print("media:", mean)
    print("maior:", maximum)
    print("menor:", minimum)