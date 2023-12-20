from random_word import RandomWords

RW = RandomWords()


def get_random_words(num_words: int):
    """
    Get a tuple of random words.

    Args:
        num_words: the number of words to generate.

    Returns:
         The words.
    """
    return (str(RW.get_random_word()).capitalize() for _ in range(num_words))


def generate_name() -> str:
    """
    Generate a name using 2 random English words.

    Returns:
        The name.
    """
    first_name, last_name = get_random_words(num_words=2)
    return f"{first_name}{last_name}"
