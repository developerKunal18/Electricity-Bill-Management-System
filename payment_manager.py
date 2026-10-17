from datetime import date

from config import BILL_FILE, PAYMENT_FILE, CUSTOMER_FILE, LATE_FEE_RATE, LATE_FEE_MAX
from storage import load_data, save_data, next_id
from utils import read_positive_int, print_table, money, timestamp


def pay_bill():
    print("\n--- Pay Electricity Bill ---")

    bill_id = read_positive_int("Bill ID: ")
    bills = load_data(BILL_FILE)

    bill = next(
        (
            b for b in bills
            if b["id"] == bill_id and b["status"] == "Unpaid"
        ),
        None
    )

    if not bill:
        print("Unpaid bill not found.")
        return

    payment_date = date.today()
    due_date = date.fromisoformat(bill["due_date"])
    late_fee = 0.0

    if payment_date > due_date:
        late_fee = min(
            round(float(bill["total_amount"]) * LATE_FEE_RATE, 2),
            LATE_FEE_MAX
        )

    amount_due = round(float(bill["total_amount"]) + late_fee, 2)

    print(f"Bill amount: {money(bill['total_amount'])}")
    print(f"Late fee:    {money(late_fee)}")
    print(f"Amount due:  {money(amount_due)}")

    method = input(
        "Payment method (Cash/UPI/Card/Bank Transfer): "
    ).strip().title()

    allowed_methods = ["Cash", "UPI", "Card", "Bank Transfer"]

    if method not in allowed_methods:
        print("Invalid payment method.")
        return

    reference = input("Transaction reference (optional): ").strip()

    payments = load_data(PAYMENT_FILE)

    payment = {
        "id": next_id(payments),
        "bill_id": bill_id,
        "customer_id": bill["customer_id"],
        "amount": amount_due,
        "late_fee": late_fee,
        "method": method,
        "reference": reference,
        "status": "Paid",
        "paid_at": timestamp()
    }

    # Save payment before marking the bill paid.
    payments.append(payment)
    save_data(PAYMENT_FILE, payments)

    bill["late_fee"] = late_fee
    bill["total_amount"] = amount_due
    bill["status"] = "Paid"
    bill["paid_at"] = payment["paid_at"]
    save_data(BILL_FILE, bills)

    customers = load_data(CUSTOMER_FILE)
    customer = next(
        (c for c in customers if c["id"] == bill["customer_id"]),
        None
    )

    print("\n========== PAYMENT RECEIPT ==========")
    print(f"Receipt ID:     {payment['id']}")
    print(f"Bill ID:        {bill_id}")
    print(f"Customer:       {customer['name'] if customer else 'Unknown'}")
    print(f"Payment method: {method}")
    print(f"Bill amount:    {money(bill['total_amount'] - late_fee)}")
    print(f"Late fee:       {money(late_fee)}")
    print(f"Amount paid:    {money(amount_due)}")
    print(f"Date:           {payment['paid_at']}")
    print("Status:         PAID")
    print("======================================")


def list_payments():
    payments = load_data(PAYMENT_FILE)

    print_table(
        ["Payment ID", "Bill ID", "Customer ID", "Amount",
         "Method", "Status", "Paid At"],
        [
            [
                p["id"], p["bill_id"], p["customer_id"],
                money(p["amount"]), p["method"],
                p["status"], p["paid_at"]
            ]
            for p in payments
        ]
    )


def payment_menu():
    while True:
        print("\n--- Payment Management ---")
        print("1. Pay bill")
        print("2. View payment history")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            pay_bill()
        elif choice == "2":
            list_payments()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
