from auth import hash_password

try:
    # Try a long password
    long_pwd = "a" * 80
    print(f"Hashing password of length {len(long_pwd)}...")
    hash_password(long_pwd)
    print("Success!")
except Exception as e:
    print(f"Caught expected error: {e}")
