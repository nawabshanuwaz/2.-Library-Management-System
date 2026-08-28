import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("library_data.json")


def load_books():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read the saved data. Starting with an empty library.")
        return []


def save_books(books):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)


def add_book(books):
    title = input("Book title: ").strip()
    author = input("Author: ").strip()

    if not title or not author:
        print("Title and author cannot be empty.")
        return

    book = {
        "id": max((item["id"] for item in books), default=0) + 1,
        "title": title,
        "author": author,
        "available": True,
        "borrower": ""
    }
    books.append(book)
    save_books(books)
    print("Book added successfully.")


def show_books(books):
    print("\nALL BOOKS")
    print("-" * 72)
    if not books:
        print("No books are available.")
        return

    print(f"{'ID':<5}{'Title':<28}{'Author':<22}{'Status'}")
    print("-" * 72)
    for book in books:
        status = "Available" if book["available"] else f"Borrowed by {book['borrower']}"
        print(f"{book['id']:<5}{book['title'][:26]:<28}{book['author'][:20]:<22}{status}")


def search_books(books):
    keyword = input("Enter title or author keyword: ").strip().lower()
    matches = [
        book for book in books
        if keyword in book["title"].lower() or keyword in book["author"].lower()
    ]
    show_books(matches)


def get_book_by_id(books):
    try:
        book_id = int(input("Enter book ID: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return None

    for book in books:
        if book["id"] == book_id:
            return book
    print("Book not found.")
    return None


def borrow_book(books):
    show_books(books)
    if not books:
        return

    book = get_book_by_id(books)
    if book is None:
        return
    if not book["available"]:
        print(f"This book is already borrowed by {book['borrower']}.")
        return

    borrower = input("Borrower's name: ").strip()
    if not borrower:
        print("Borrower name cannot be empty.")
        return

    book["available"] = False
    book["borrower"] = borrower
    save_books(books)
    print("Book borrowed successfully.")


def return_book(books):
    borrowed = [book for book in books if not book["available"]]
    show_books(borrowed)
    if not borrowed:
        print("There are no borrowed books to return.")
        return

    book = get_book_by_id(books)
    if book is None:
        return
    if book["available"]:
        print("This book is already available.")
        return

    book["available"] = True
    book["borrower"] = ""
    save_books(books)
    print("Book returned successfully.")


def delete_book(books):
    show_books(books)
    if not books:
        return

    book = get_book_by_id(books)
    if book is None:
        return
    books.remove(book)
    save_books(books)
    print("Book deleted successfully.")


def main():
    books = load_books()

    while True:
        print("\n" + "=" * 42)
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=" * 42)
        print("1. Add book")
        print("2. View all books")
        print("3. Search books")
        print("4. Borrow book")
        print("5. Return book")
        print("6. Delete book")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            show_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            borrow_book(books)
        elif choice == "5":
            return_book(books)
        elif choice == "6":
            delete_book(books)
        elif choice == "7":
            print("Library data saved. Goodbye!")
            break
        else:
            print("Invalid selection. Choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
