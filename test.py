import itertools
import string

def sequential_string(start_len=5, end_len=8):
    for length in range(start_len, end_len + 1):
        # First, generate all numeric combinations for current length
        for s in itertools.product(string.digits, repeat=length):
            yield ''.join(s)
        # Then, generate all alphanumeric combinations for the same length
        for s in itertools.product(string.ascii_lowercase + string.digits, repeat=length):
            yield ''.join(s)

g = sequential_string()
for _ in range(999999):  # replace 50 with the amount needed
    print(next(g))