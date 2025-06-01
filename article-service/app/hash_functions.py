import hashlib


def hash_file(file):
    hash_func = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_func.update(chunk)
    file.seek(0)
    return hash_func.hexdigest()