from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, available_quantity):
        self.title = title
        self.author = author
        self.available_quantity = available_quantity

class LibrarySystem:
    def __init__(self):
        self.books = [
            Book("Book1", "Author1", 5),
            Book("Book2", "Author2", 8),
            # Add more books as needed
        ]
        self.checked_out_books = []

    def display_catalog(self):
        print("Library Catalog:")
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book.title} by {book.author} - Available: {book.available_quantity}")

    def checkout_books(self):
        selected_books = []
        while True:
            self.display_catalog()
            book_index = int(input("Enter the book number to checkout (0 to finish): "))
            if book_index == 0:
                break

            book = self.books[book_index - 1]
            quantity = int(input(f"Enter the quantity for '{book.title}': "))
            
            if quantity <= 0 or quantity > book.available_quantity:
                print("Invalid quantity. Please enter a valid quantity.")
                continue

            selected_books.append((book, quantity))
            book.available_quantity -= quantity

        if not selected_books:
            return -1

        return selected_books

    def calculate_due_date(self):
        return datetime.now() + timedelta(days=14)

    def calculate_late_fee(self, due_date):
        days_late = (datetime.now() - due_date).days
        return max(0, days_late) * 1  # $1 late fee per day

    def display_checkout_details(self, checkout_details):
        print("\nCheckout Details:")
        for book, quantity, due_date, late_fee in checkout_details:
            print(f"{quantity}x '{book.title}' due on {due_date.strftime('%Y-%m-%d')}. Late fee: ${late_fee}")

    def return_books(self):
        print("\nReturn Process:")
        return_details = []
        for book in self.checked_out_books:
            returned_quantity = int(input(f"Enter the quantity of '{book.title}' being returned: "))
            if returned_quantity < 0 or returned_quantity > book[1]:
                print("Invalid quantity. Please enter a valid quantity.")
                return -1
            return_details.append((book[0], returned_quantity))
            book[1] -= returned_quantity

        return return_details

    def run(self):
        while True:
            print("\n1. Checkout Books\n2. Return Books\n3. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                checkout_details = self.checkout_books()
                if checkout_details != -1:
                    for book, quantity in checkout_details:
                        due_date = self.calculate_due_date()
                        late_fee = self.calculate_late_fee(due_date)
                        self.checked_out_books.append((book, quantity, due_date, late_fee))
                    self.display_checkout_details(checkout_details)

            elif choice == '2':
                return_details = self.return_books()
                if return_details != -1:
                    total_late_fee = sum(self.calculate_late_fee(book[2]) for book in return_details)
                    print(f"\nTotal late fees for returned books: ${total_late_fee}")
                    self.checked_out_books = [book for book in self.checked_out_books if book not in return_details]

            elif choice == '3':
                break

if __name__ == "__main__":
    library_system = LibrarySystem()
    library_system.run()
