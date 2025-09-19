import random

def generate_random_number(min_val: int, max_val: int) -> int:
    """Generate a random integer between min_val and max_val (inclusive)"""
    return random.randint(min_val, max_val)

def calculate_reward(success: bool) -> int:
    """Calculate reward based on success: 1 for success, -1 for failure"""
    return 1 if success else -1