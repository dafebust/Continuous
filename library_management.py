from datetime import datetime, timedelta
import unittest

class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity

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
            print(f"{i}. {book.title} by {book.author} - Available: {book.quantity}")

    def checkout_books(self, selections):
        for book, quantity in selections:
            if quantity <= 0 or quantity > book.quantity:
                return -1

        checkout_details = []
        for book, quantity in selections:
            book.quantity -= quantity
            due_date = datetime.now() + timedelta(days=14)
            late_fee = 0
            checkout_details.append((book, quantity, due_date, late_fee))

        self.checked_out_books.extend(checkout_details)
        return checkout_details

    def calculate_late_fee(self, due_date):
        days_late = (datetime.now() - due_date).days
        return max(0, days_late) * 1  # $1 late fee per day

    def return_books(self, return_details):
        for book, returned_quantity in return_details:
            if returned_quantity < 0 or returned_quantity > book.quantity:
                return -1

        total_late_fee = 0
        for book, returned_quantity in return_details:
            book.quantity += returned_quantity
            total_late_fee += self.calculate_late_fee(book.due_date)

        return total_late_fee

    def cancel_checkout(self, selections):
        for book, quantity in selections:
            book.quantity += quantity

    def run(self):
        while True:
            print("\n1. Checkout Books\n2. Return Books\n3. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                selections = self.checkout_books_interface()
                if selections == -1:
                    print("Checkout canceled.")
                    continue

                checkout_details = self.checkout_books(selections)
                if checkout_details != -1:
                    self.display_checkout_details(checkout_details)

            elif choice == '2':
                return_details = self.return_books_interface()
                if return_details == -1:
                    print("Return process canceled.")
                    continue

                total_late_fee = self.return_books(return_details)
                if total_late_fee != -1:
                    print(f"\nTotal late fees for returned books: ${total_late_fee}")

            elif choice == '3':
                break

    def display_checkout_details(self, checkout_details):
        print("\nCheckout Details:")
        for book, quantity, due_date, late_fee in checkout_details:
            print(f"{quantity}x '{book.title}' due on {due_date.strftime('%Y-%m-%d')}. Late fee: ${late_fee}")

    def checkout_books_interface(self):
        selections = []
        while True:
            self.display_catalog()
            book_index = int(input("Enter the book number to checkout (0 to finish): "))
            if book_index == 0:
                return selections

            book = self.books[book_index - 1]
            quantity = int(input(f"Enter the quantity for '{book.title}': "))

            if quantity <= 0 or quantity > book.quantity:
                print("Invalid quantity. Please enter a valid quantity.")
                cancel = input("Do you want to cancel the checkout? (y/n): ")
                if cancel.lower() == 'y':
                    self.cancel_checkout(selections)
                    return -1
                continue

            selections.append((book, quantity))

            if len(selections) > 10:
                print("Maximum books per checkout reached. Adjust your selection.")
                self.cancel_checkout(selections)
                return -1

    def return_books_interface(self):
        print("\nReturn Process:")
        return_details = []
        for book in self.checked_out_books:
            returned_quantity = int(input(f"Enter the quantity of '{book[0].title}' being returned: "))
            if returned_quantity < 0 or returned_quantity > book[1]:
                print("Invalid quantity. Please enter a valid quantity.")
                cancel = input("Do you want to cancel the return process? (y/n): ")
                if cancel.lower() == 'y':
                    return -1
                continue
            return_details.append((book[0], returned_quantity))
        return return_details

class TestLibrarySystem(unittest.TestCase):

    def test_cancel_checkout(self):
        selections = [(self.library_system.books[0], 2), (self.library_system.books[1], 1)]
        self.library_system.cancel_checkout(selections)
        self.assertEqual(self.library_system.books[0].quantity, 5)
        self.assertEqual(self.library_system.books[1].quantity, 8)

    def test_checkout_books_interface_cancel(self):
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', '0', 'y']):
            result = self.library_system.checkout_books_interface()
        self.assertIsNone(result)

    def test_return_books_interface_cancel(self):
        selections = [(self.library_system.books[0], 2), (self.library_system.books[1], 1)]
        self.library_system.checkout_books(selections)
        with unittest.mock.patch('builtins.input', side_effect=['1', '0', 'y']):
            result = self.library_system.return_books_interface()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
