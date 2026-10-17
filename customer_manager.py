from config import CUSTOMER_FILE
from storage import load_data, save_data, next_id
from utils import read_text, valid_email, print_table


def add_customer():
    customers = load_data(CUSTOMER_FILE)

    print("\n--- Register Electricity Customer ---")
    name = read_text("Customer name: ")
    phone = read_text("Phone number: ")

    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        print("Enter a phone number containing 10 to 15 digits.")
        return

    if any(c["phone"] == phone for c in customers):
        print("This phone number is already registered.")
        return

    email = read_text("Email address: ").lower()

    if not valid_email(email):
        print("Enter a valid email address.")
        return

    address = read_text("Address: ")
    meter_number = read_text("Meter number: ").upper()

    if any(
        c["meter_number"].upper() == meter_number
        for c in customers
    ):
        print("This meter number is already registered.")
        return

    customer = {
        "id": next_id(customers),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "meter_number": meter_number,
        "status": "Active"
    }

    customers.append(customer)
    save_data(CUSTOMER_FILE, customers)

    print(f"Customer registered. Customer ID: {customer['id']}")


def list_customers():
    customers = load_data(CUSTOMER_FILE)

    print_table(
        ["ID", "Name", "Phone", "Meter No.", "Address", "Status"],
        [
            [
                c["id"], c["name"], c["phone"],
                c["meter_number"], c["address"], c["status"]
            ]
            for c in customers
        ]
    )


def get_customer(customer_id):
    return next(
        (
            c for c in load_data(CUSTOMER_FILE)
            if c["id"] == customer_id
        ),
        None
    )


def customer_menu():
    while True:
        print("\n--- Customer Management ---")
        print("1. Register customer")
        print("2. View customers")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            list_customers()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
