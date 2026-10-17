
# Electricity Bill Management System

## Overview

A command-line Python application for managing electricity customers, meter readings, monthly bills, payments, and billing reports. All records are stored locally in JSON files.

## Features

- Register electricity customers
- Maintain unique customer and meter IDs
- Record monthly meter readings
- Calculate consumed electricity units
- Generate slab-based electricity bills
- Add fixed monthly charges
- Calculate late-payment fees
- Record payments and print receipts in the terminal
- View customer billing history
- Generate monthly reports and a dashboard

## Technologies

- Python 3.10+
- JSON file storage
- Python standard library

## Project Structure

```text
day357_electricity_billing/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── customer_manager.py
├── meter_manager.py
├── billing_manager.py
├── payment_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
└── data/
    ├── customers.json
    ├── readings.json
    ├── bills.json
    └── payments.json
```

## Installation

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run the application:

   ```bash
   python main.py
   ```

No external packages are required.

## How Billing Works

The sample tariff is configured in `config.py`:

- First 100 units: ₹3 per unit
- Next 100 units: ₹5 per unit
- Next 100 units: ₹7 per unit
- Units above 300: ₹9 per unit
- Fixed monthly charge: ₹100

The energy charge is calculated progressively across the slabs. The fixed charge is then added to calculate the bill total.

A late fee of 2% of the unpaid bill, capped at ₹500, is applied when payment is made after the configured due date.

**Note:** These are illustrative project rates, not official electricity tariffs. Actual tariffs vary by electricity provider, location, consumer category, and applicable rules.

## Recommended Testing Workflow

1. Register a customer.
2. Record a meter reading for a billing month.
3. Generate a bill for that customer and month.
4. View the generated bill.
5. Record payment using the bill ID.
6. Review the receipt and customer billing history.
7. Generate a monthly billing report.
8. Test duplicate readings, duplicate bills, and duplicate payments.

## Data Storage

The `data` folder stores customer profiles, readings, bills, and payment records. Back up these files regularly. Do not delete bills or payments independently because reports depend on their relationships.

## Limitations

- This is a learning project, not a production billing system.
- The tariff and late-fee rules are examples.
- Payments are manually recorded; no payment gateway is connected.
- JSON storage is not designed for simultaneous multi-user access.
- Authentication, auditing, and automatic payment reconciliation are not included.
- Meter-reading corrections and refunds require additional functionality.

## Future Improvements

- Add a graphical interface using Tkinter.
- Add PDF bill generation.
- Add search and CSV export.
- Add email or SMS notifications.
- Use SQLite or MySQL for persistent database storage.
- Add automated tests with `unittest`.
