from config import (
    CUSTOMER_FILE,
    READING_FILE,
    BILL_FILE,
    PAYMENT_FILE
)
from storage import ensure_file

from customer_manager import customer_menu
from meter_manager import meter_menu
from billing_manager import billing_menu
from payment_manager import payment_menu
from report_manager import report_menu


def initialize():
    for file_path in [
        CUSTOMER_FILE,
        READING_FILE,
        BILL_FILE,
        PAYMENT_FILE
    ]:
        ensure_file(file_path)


def main():
    initialize()

    while True:
        print("\n========================================")
        print("    ELECTRICITY BILL MANAGEMENT")
        print("========================================")
        print("1. Customer management")
        print("2. Meter reading management")
        print("3. Billing management")
        print("4. Payment management")
        print("5. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                customer_menu()
            elif choice == "2":
                meter_menu()
            elif choice == "3":
                billing_menu()
            elif choice == "4":
                payment_menu()
            elif choice == "5":
                report_menu()
            elif choice == "0":
                print("Thank you for using Electricity Bill Management.")
                break
            else:
                print("Invalid choice. Please try again.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Operation failed: {error}")
            print("Check your input and JSON data files before retrying.")


if __name__ == "__main__":
    main()
