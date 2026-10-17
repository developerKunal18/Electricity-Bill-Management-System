from datetime import date

from config import (
    CUSTOMER_FILE,
    READING_FILE,
    BILL_FILE,
    PAYMENT_FILE
)
from storage import load_data
from utils import read_month, money, print_table


def dashboard():
    customers = load_data(CUSTOMER_FILE)
    readings = load_data(READING_FILE)
    bills = load_data(BILL_FILE)
    payments = load_data(PAYMENT_FILE)

    total_collected = sum(
        float(p["amount"])
        for p in payments
        if p["status"] == "Paid"
    )

    outstanding = sum(
        float(b["total_amount"])
        for b in bills
        if b["status"] == "Unpaid"
    )

    print("\n======= ELECTRICITY BILLING DASHBOARD =======")
    print(f"Total customers:       {len(customers)}")
    print(f"Active customers:      {sum(c['status'] == 'Active' for c in customers)}")
    print(f"Meter readings:        {len(readings)}")
    print(f"Total bills:           {len(bills)}")
    print(f"Paid bills:            {sum(b['status'] == 'Paid' for b in bills)}")
    print(f"Unpaid bills:          {sum(b['status'] == 'Unpaid' for b in bills)}")
    print(f"Total collected:       {money(total_collected)}")
    print(f"Outstanding amount:    {money(outstanding)}")
    print("=============================================")


def monthly_report():
    month = read_month("Enter billing month (YYYY-MM): ")

    customers = {
        c["id"]: c["name"]
        for c in load_data(CUSTOMER_FILE)
    }

    bills = [
        b for b in load_data(BILL_FILE)
        if b["month"] == month
    ]

    rows = [
        [
            b["id"],
            customers.get(b["customer_id"], "Unknown"),
            b["units_consumed"],
            money(b["total_amount"]),
            b["status"]
        ]
        for b in bills
    ]

    print(f"\nMonthly Bill Report: {month}")

    print_table(
        ["Bill ID", "Customer", "Units", "Amount", "Status"],
        rows
    )

    paid_total = sum(
        float(b["total_amount"])
        for b in bills
        if b["status"] == "Paid"
    )

    unpaid_total = sum(
        float(b["total_amount"])
        for b in bills
        if b["status"] == "Unpaid"
    )

    print(f"\nPaid bill total:   {money(paid_total)}")
    print(f"Unpaid bill total: {money(unpaid_total)}")


def customer_history():
    customer_id_text = input("Enter customer ID: ").strip()

    try:
        customer_id = int(customer_id_text)

        if customer_id <= 0:
            raise ValueError

    except ValueError:
        print("Enter a valid positive customer ID.")
        return

    customer = next(
        (
            c for c in load_data(CUSTOMER_FILE)
            if c["id"] == customer_id
        ),
        None
    )

    if not customer:
        print("Customer not found.")
        return

    readings = [
        r for r in load_data(READING_FILE)
        if r["customer_id"] == customer_id
    ]

    bills = [
        b for b in load_data(BILL_FILE)
        if b["customer_id"] == customer_id
    ]

    print(f"\nBilling history for {customer['name']}")
    print(f"Meter number: {customer['meter_number']}")

    print("\nMeter readings:")
    print_table(
        ["Month", "Previous", "Current", "Units"],
        [
            [
                r["month"], r["previous_reading"],
                r["current_reading"], r["units_consumed"]
            ]
            for r in sorted(readings, key=lambda item: item["month"])
        ]
    )

    print("\nBills:")
    print_table(
        ["Bill ID", "Month", "Units", "Amount", "Due Date", "Status"],
        [
            [
                b["id"], b["month"], b["units_consumed"],
                money(b["total_amount"]), b["due_date"], b["status"]
            ]
            for b in sorted(bills, key=lambda item: item["month"])
        ]
    )


def report_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Dashboard")
        print("2. Monthly billing report")
        print("3. Customer billing history")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            monthly_report()
        elif choice == "3":
            customer_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
