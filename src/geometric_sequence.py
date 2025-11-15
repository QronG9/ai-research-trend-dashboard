"""Generates and prints the first N terms of a geometric sequence."""

def geometric_sequence(first_term, common_ratio, n):
    """Generates and prints the first N terms of a geometric sequence.

    Args:
        first_term (float): The first term of the sequence.
        common_ratio (float): The common ratio of the sequence.
        n (int): The number of terms to generate.
    """
    if n <= 0:
        print("Number of terms must be positive.")
        return

    for i in range(n):
        term = first_term * (common_ratio ** i)
        print(term)

if __name__ == "__main__":
    try:
        first_term = float(input("Enter the first term: "))
        common_ratio = float(input("Enter the common ratio: "))
        n = int(input("Enter the number of terms: "))
        geometric_sequence(first_term, common_ratio, n)
    except ValueError:
        print("Invalid input. Please enter numeric values.")