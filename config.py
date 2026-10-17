from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CUSTOMER_FILE = DATA_DIR / "customers.json"
READING_FILE = DATA_DIR / "readings.json"
BILL_FILE = DATA_DIR / "bills.json"
PAYMENT_FILE = DATA_DIR / "payments.json"

# Example residential tariff in rupees per unit.
# Change these rates to match the tariff you want to demonstrate.
TARIFF_SLABS = [
    (100, 3.00),
    (200, 5.00),
    (300, 7.00),
    (float("inf"), 9.00),
]

FIXED_MONTHLY_CHARGE = 100.00
LATE_FEE_RATE = 0.02
LATE_FEE_MAX = 500.00
