import hashlib
import binascii

def test_verify(password, salt_hex, expected_hash_hex):
    salt = binascii.unhexlify(salt_hex)
    
    # Try different combinations just in case
    # 1. Standard
    derived = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=64)
    res = binascii.hexlify(derived).decode()
    print(f"Standard Scrypt: {res == expected_hash_hex}")
    if res == expected_hash_hex: return True
    
    # 2. Maybe salt is also password encoded? (Unlikely)
    # 3. Maybe dklen is 32? (The hash I saw was 128 chars = 64 bytes, so dklen=64)
    
    return False

# From DB for abub96891@gmail.com
salt_hex = "bf90c26fe12cef042a8171ceecea5578"
hash_hex = "083c8ef1c6583e2cbbb550a9ec4b9f32b2e03c3ef835ce9ea8c4c619489c22c75c23db040962e705642db0f5d0b95a2a73c525a53cb9315ed6f1652201fec5e9"

# I don't know the user's password, but I can try common ones or just inform the user.
# Wait, I'll add a tool to the backend that allows me to log the comparison results.

if __name__ == "__main__":
    # Test with a dummy to see if hex formatting is correct
    test_verify("password", "abcde12345", "ffff")
