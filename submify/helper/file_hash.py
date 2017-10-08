import hashlib


def generate_hash_string(string):
    return int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16) % 10**8
