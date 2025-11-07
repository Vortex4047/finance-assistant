#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Flask application
"""
import secrets

def generate_secret_key(length=64):
    """Generate a cryptographically secure secret key"""
    return secrets.token_hex(length)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 70)
    print("🔐 Generated SECRET_KEY for your Flask application")
    print("=" * 70)
    print(f"\n{secret_key}\n")
    print("=" * 70)
    print("\n📋 Add this to your Vercel Environment Variables:")
    print(f"   SECRET_KEY={secret_key}")
    print("\n⚠️  Keep this secret! Don't commit it to Git!")
    print("=" * 70)
