from datetime import date, timedelta

from config import (
    BILL_FILE,
    READING_FILE,
    CUSTOMER_FILE,
    TARIFF_SLABS,
    FIXED_MONTHLY_CHARGE
)
from storage import load_data, save_data, next_id
from utils import read_positive_int, read_month, money, print_table


def calculate_energy_charge(units):
    remaining = units
    lower_limit = 0
    charge = 0.0

    for upper_limit, rate in TARIFF_SLABS:
        slab_size = upper_limit - lower_limit
        slab_units = min(remaining, slab_size)

        if slab_units > 0:
            charge += slab_units * rate
            remaining -= slab_units

        if remaining <= 0:
            break

        lower_limit = upper_limit

    return round(charge, 2)


def generate_bill():
    print("\n--- Generate Electricity Bill ---")

    customer_id = read_positive_int("Customer ID: ")
    month = read_month("Billing month (YYYY-MM): ")

    customers = load_data(CUSTOMER_FILE)
    customer = next(
        (
            c for c in customers
            if c["id"] == customer_id and c["status"] == "Active"
        ),
        None
    )

    if not customer:
        print("Active customer not found.")
        return

    readings = load_data(READING_FILE)

    reading = next(
        (
            r for r in readings
            if r["customer_id"] == customer_id
            and r["month"] == month
        ),
        None
    )

    if not reading:
        print("No meter reading found for this customer and month.")
        return

    bills = load_data(BILL_FILE)

    if any(
        b["customer_id"] == customer_id and b["month"] == month
        for b in bills
    ):
        print("A bill already exists for this customer and month.")
        return

    units = int(reading["units_consumed"])
    energy_charge = calculate_energy_charge(units)
    fixed_charge = float(FIXED_MONTHLY_CHARGE)
    total = round(energy_charge + fixed_charge, 2)

    due_date = date.fromisoformat(month + "-01") + timedelta(days=14)

    bill = {
        "id": next_id(bills),
        "customer_id": customer_id,
        "reading_id": reading["id"],
        "month": month,
        "units_consumed": units,
        "energy_charge": energy_charge,
        "fixed_charge": fixed_charge,
        "late_fee": 0.0,
        "total_amount": total,
        "due_date": due_date.isoformat(),
        "status": "Unpaid"
    }

    bills.append(bill)
    save_data(BILL_FILE, bills)

    print("\n========== ELECTRICITY BILL ==========")
    print(f"Bill ID:         {bill['id']}")
    print(f"Customer:        {customer['name']}")
    print(f"Meter number:    {customer['meter_number']}")
    print(f"Billing month:   {month}")
    print(f"Units consumed:  {units}")
    print(f"Energy charge:   {money(energy_charge)}")
    print(f"Fixed charge:    {money(fixed_charge)}")
    print(f"Total amount:    {money(total)}")
    print(f"Due date:        {bill['due_date']}")
    print("======================================")


def list_bills():
    bills = load_data(BILL_FILE)
    customers = {
        c["id"]: c["name"]
        for c in load_data(CUSTOMER_FILE)
    }

    print_table(
        [
            "Bill ID", "Customer", "Month", "Units",
            "Amount", "Due Date", "Status"
        ],
        [
            [
                b["id"],
                customers.get(b["customer_id"], "Unknown"),
                b["month"],
                b["units_consumed"],
                money(b["total_amount"]),
                b["due_date"],
                b["status"]
            ]
            for b in sorted(bills, key=lambda item: item["month"])
        ]
    )


def billing_menu():
    while True:
        print("\n--- Billing Management ---")
        print("1. Generate bill")
        print("2. View all bills")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            generate_bill()
        elif choice == "2":
            list_bills()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
