# invoices/utils.py
import hashlib


def compute_file_hash(file_content: bytes) -> str:
    """Generate SHA256 hash from file content bytes."""
    sha256 = hashlib.sha256()
    sha256.update(file_content)
    return sha256.hexdigest()