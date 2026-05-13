import random

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def random_enum(enum_class):
    return random.choice(list(enum_class))
