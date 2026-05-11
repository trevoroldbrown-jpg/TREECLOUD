import subprocess
import time

authors = [
    "Tricontinental: Institute for Social Research",
    "Vijay Prashad"
]

def run_archivist(author):
    print(f"\n[INFO] Dispatching The Archivist for: {author}")
    try:
        # Using subprocess to call our archivist script
        subprocess.run(["python", "archivist.py", author], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error archiving {author}: {e}")
    
    # Small sleep to be respectful to Open Library API
    time.sleep(2)

def main():
    print("[INFO] Treecloud Archival Expansion: Initializing Batch Mode...")
    for author in authors:
        run_archivist(author)
    print("\n[SUCCESS] Batch Archival Complete. Check books.json for the full library.")

if __name__ == "__main__":
    main()
