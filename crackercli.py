
import hashlib
import itertools
import argparse
import time
import threading
from tqdm import tqdm
from fake_useragent import UserAgent
import os

# Common characters for brute force
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

# User-Agent randomization (useful if making requests)
ua = UserAgent()

# Function to hash a password with a given algorithm
def hash_password(password, algorithm="md5"):
    password = password.encode()
    if algorithm == "md5":
        return hashlib.md5(password).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(password).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(password).hexdigest()
    else:
        raise ValueError("Unsupported hashing algorithm!")

# Save cracked passwords to a file
def save_result(password, hash_value, algorithm):
    filename = "cracked_passwords.txt"
    with open(filename, "a") as f:
        f.write(f"{hash_value} ({algorithm}) -> {password}\n")
    print(f"✅ Password saved in {filename}")

# Dictionary attack
def dictionary_attack(hash_to_crack, wordlist, algorithm="md5"):
    print("\n🔎 Running Dictionary Attack...\n")

    if not os.path.exists(wordlist):
        print("❌ Wordlist file not found!")
        return None

    with open(wordlist, "r", encoding="ISO-8859-1") as f:
        words = f.read().splitlines()

    for word in tqdm(words, desc="Testing passwords", unit="password"):
        hashed_word = hash_password(word.strip(), algorithm)
        if hashed_word == hash_to_crack:
            print(f"\n✅ Password Found: {word}\n")
            save_result(word, hash_to_crack, algorithm)
            return word

    print("\n❌ Password not found in dictionary.\n")
    return None

# Brute-force attack
def brute_force_attack(hash_to_crack, max_length=4, algorithm="md5"):
    print("\n🔎 Running Brute Force Attack...\n")

    for length in range(1, max_length + 1):
        for attempt in tqdm(itertools.product(CHARSET, repeat=length), desc=f"Trying length {length}", unit="password"):
            password = ''.join(attempt)
            hashed_attempt = hash_password(password, algorithm)
            if hashed_attempt == hash_to_crack:
                print(f"\n✅ Password Found: {password}\n")
                save_result(password, hash_to_crack, algorithm)
                return password

    print("\n❌ Password not found within constraints.\n")
    return None

# Multi-threaded brute force attack
def multi_threaded_brute_force(hash_to_crack, max_length=4, algorithm="md5", num_threads=4):
    def worker(start, step):
        for length in range(1, max_length + 1):
            for attempt in itertools.islice(itertools.product(CHARSET, repeat=length), start, None, step):
                password = ''.join(attempt)
                hashed_attempt = hash_password(password, algorithm)
                if hashed_attempt == hash_to_crack:
                    print(f"\n✅ Password Found: {password}\n")
                    save_result(password, hash_to_crack, algorithm)
                    return password

    print(f"\n🔎 Running Multi-Threaded Brute Force Attack with {num_threads} threads...\n")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i, num_threads))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Advanced Python Password Cracker")
    parser.add_argument("-m", "--mode", choices=["brute", "dict"], required=True, help="Choose attack mode: brute (Brute Force) or dict (Dictionary Attack)")
    parser.add_argument("-ht", "--hash", required=True, help="Hashed password to crack")
    parser.add_argument("-a", "--algorithm", choices=["md5", "sha1", "sha256", "sha512"], default="md5", help="Hashing algorithm used (default: md5)")
    parser.add_argument("-wl", "--wordlist", help="Path to a dictionary wordlist file (Required for dictionary attack)")
    parser.add_argument("-ml", "--max-length", type=int, default=4, help="Max password length for brute force attack (default: 4)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads for brute force attack (default: 4)")

    args = parser.parse_args()

    print("\n🚀 Starting Password Cracker...\n")
    time.sleep(1)

    if args.mode == "dict":
        if not args.wordlist:
            print("\n❌ Dictionary attack requires a wordlist file!\n")
            return
        dictionary_attack(args.hash, args.wordlist, args.algorithm)

    elif args.mode == "brute":
        multi_threaded_brute_force(args.hash, args.max_length, args.algorithm, args.threads)

if __name__ == "__main__":
    main()

