import os
import sys
import requests
import threading
from queue import Queue
from colorama import Fore, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Ensure result directory exists
os.makedirs("result", exist_ok=True)

# Global variables
q = Queue()
discovered_dirs = []
target_url = None
wordlist_file = None


def initialize_from_args():
    """Initialize variables from command-line arguments if provided."""
    global target_url, wordlist_file  

    # Ensure at least 1 argument (target URL) is provided
    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python dir_search.py <target_url> [wordlist]\n")
        sys.exit(1)

    target_url = sys.argv[1]
    
    if not target_url.startswith('http'):
        target_url = 'https://' + target_url

    # If a wordlist is provided, use it; otherwise, set a default wordlist
    wordlist_file = sys.argv[2] if len(sys.argv) > 2 else "wordlist/directory-list-2.3-small_edited.txt"

    # Validate wordlist file
    if not os.path.exists(wordlist_file):
        print(Fore.RED + f"Error: Wordlist file '{wordlist_file}' not found.\n")
        sys.exit(1)


def fill_queue():
    """Load directory names from the wordlist and add to the queue."""
    if wordlist_file is None:
        print(Fore.RED + "Error: No wordlist file specified.")
        sys.exit(1)

    try:
        with open(wordlist_file, "r", encoding="utf-8") as file:
            for line in file:
                directory = line.strip()
                if directory:
                    full_url = f"{target_url.rstrip('/')}/{directory}/"
                    q.put(full_url)
    except Exception as e:
        print(Fore.RED + f"Error reading wordlist: {e}")
        sys.exit(1)


def check_directory(url):
    """Check if a directory exists by sending an HTTP request."""
    try:
        response = requests.get(url, timeout=5)
        if 200 <= response.status_code < 400:  # Success codes
            print(Fore.GREEN + f"{url}       #{response.status_code}")
            discovered_dirs.append(f"{url}       #{response.status_code}")
    except requests.RequestException:
        pass


def worker():
    """Worker function to process URLs from the queue."""
    while not q.empty():
        url = q.get()
        check_directory(url)


def run_threads():
    """Run the directory enumeration using multiple threads."""
    print(Fore.YELLOW + f"Searching directories for {target_url} using {wordlist_file}\n")

    threads = []
    for _ in range(100):  # Adjust thread count as needed
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def save_results():
    """Save discovered directories to a result file."""
    result_file = "result/dirs.txt"
    with open(result_file, "w", encoding="utf-8") as file:
        for entry in discovered_dirs:
            file.write(entry + "\n")

    print(Fore.CYAN + f"\nResults saved to: {result_file}")


def run_directory_search(url, wordlist="wordlist/directory-list-2.3-small_edited.txt"):
    """Run directory search without command-line arguments (for GUI use)."""
    global target_url, wordlist_file
    target_url = url
    wordlist_file = wordlist

    if not os.path.exists(wordlist_file):
        print(Fore.RED + f"Error: Wordlist file '{wordlist_file}' not found.\n")
        return

    fill_queue()
    run_threads()

    print(Fore.CYAN + "\nDiscovered Directories:")
    if discovered_dirs:
        for entry in discovered_dirs:
            print(entry)
    else:
        print(Fore.RED + "No accessible directories found.")

    save_results()


def main():
    """Main execution function for CLI."""
    initialize_from_args()
    fill_queue()
    run_threads()

    print(Fore.CYAN + "\nDiscovered Directories:")
    if discovered_dirs:
        for entry in discovered_dirs:
            print(entry)
    else:
        print(Fore.RED + "No accessible directories found.")

    save_results()


# Ensure CLI execution only when run directly
if __name__ == "__main__":  # ✅ Fixed typo here
    main()
