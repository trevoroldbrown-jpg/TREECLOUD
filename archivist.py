import requests
import json
import os
from datetime import datetime

# Configuration
BOOKS_FILE = "books.json"

def search_books_by_author(author_name, limit=50):
    """Searches Open Library for ebooks by a specific author."""
    print(f"[INFO] The Archivist is performing a deep search for: {author_name} (Limit: {limit})...")
    url = f"https://openlibrary.org/search.json?author={requests.utils.quote(author_name)}&limit={limit}"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        books = []
        for doc in data.get("docs", []):
            ia_ids = doc.get("ia", [])
            ia_link = f"https://archive.org/details/{ia_ids[0]}" if ia_ids else None
            
            books.append({
                "title": doc.get("title"),
                "first_publish_year": doc.get("first_publish_year"),
                "author": author_name,
                "ia_id": ia_ids[0] if ia_ids else None,
                "link": ia_link,
                "has_fulltext": doc.get("has_fulltext", False),
                "why_interesting": "Archival Research",
                "source": "Open Library / Internet Archive"
            })
        return books
        
    except Exception as e:
        print(f"[ERROR] The Archivist encountered an error: {e}")
        return []

def save_books(books):
    if not books:
        return
        
    # Append to existing books if file exists
    existing_books = []
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            try:
                existing_books = json.load(f)
            except:
                existing_books = []
                
    # Avoid duplicates by title
    titles = {b['title'] for b in existing_books}
    new_books = [b for b in books if b['title'] not in titles]
    
    existing_books.extend(new_books)
    
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_books, f, indent=4)
    print(f"[OK] The Archivist has cataloged {len(new_books)} new works.")

def main(author="Karl Marx", limit=50):
    results = search_books_by_author(author, limit=limit)
    if results:
        save_books(results)
        print(f"[OK] Found {len(results)} works. Displaying top 10:")
        for b in results[:10]:
            link_status = "Available" if b['link'] else "No Direct Link"
            # Sanitize for safe console printing
            safe_title = b['title'].encode('ascii', 'ignore').decode('ascii')
            print(f"- {safe_title} ({b['first_publish_year']}) [{link_status}]")
    else:
        print("[WARNING] No digital works found in the archives for this search.")

if __name__ == "__main__":
    import sys
    search_term = "Karl Marx"
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
    main(search_term)
