from config import CUSTOMER_FILE, READING_FILE
from storage import load_data, save_data, next_id
from customer_manager import get_customer
from utils import (
    read_positive_int,
    read_non_negative_int,
    read_month,
    print_table,
    timestamp
)


def record_reading():
    print("\n--- Record Meter Reading ---")

    customer_id = read_positive_int("Customer ID: ")
    customer = get_customer(customer_id)

    if not customer:
        print("Customer not found.")
        return

    if customer["status"] != "Active":
        print("This customer account is inactive.")
        return

    month = read_month("Billing month (YYYY-MM): ")
    readings = load_data(READING_FILE)

    if any(
        r["customer_id"] == customer_id and r["month"] == month
        for r in readings
    ):
        print("A meter reading already exists for this customer and month.")
        return

    previous_readings = [
        r for r in readings
        if r["customer_id"] == customer_id and r["month"] < month
    ]

    previous_readings.sort(key=lambda r: r["month"])

    previous_value = (
        previous_readings[-1]["current_reading"]
        if previous_readings
        else 0
    )

    print(f"Previous recorded reading: {previous_value} units")
    current_value = read_non_negative_int("Current meter reading: ")

    if current_value < previous_value:
        print("Current reading cannot be lower than the previous reading.")
        return

    reading = {
        "id": next_id(readings),
        "customer_id": customer_id,
        "month": month,
        "previous_reading": previous_value,
        "current_reading": current_value,
        "units_consumed": current_value - previous_value,
        "recorded_at": timestamp()
    }

    readings.append(reading)
    save_data(READING_FILE, readings)

    print("Meter reading saved successfully.")
    print(f"Units consumed: {reading['units_consumed']}")


def list_readings():
    readings = load_data(READING_FILE)
    customers = {
        c["id"]: c["name"]
        for c in load_data(CUSTOMER_FILE)
    }

    rows = [
        [
            r["id"],
            customers.get(r["customer_id"], "Unknown"),
            r["month"],
            r["previous_reading"],
            r["current_reading"],
            r["units_consumed"]
        ]
        for r in sorted(
            readings,
            key=lambda item: (item["month"], item["customer_id"])
        )
    ]

    print_table(
        [
            "Reading ID", "Customer", "Month",
            "Previous", "Current", "Units"
        ],
        rows
    )


def meter_menu():
    while True:
        print("\n--- Meter Reading Management ---")
        print("1. Record monthly reading")
        print("2. View meter readings")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            record_reading()
        elif choice == "2":
            list_readings()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
