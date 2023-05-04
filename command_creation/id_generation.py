import random
import string

# given string length, generate id consisting of alphanumeric characters
# N^62 possible ids
def generate_random_id(string_length):
    possible_characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(possible_characters) for _ in range(string_length))
    return random_id

if __name__ == "__main__":
    # Example usage:
    random_id = generate_random_id(10)
    print(random_id)