import os
import random
from datetime import datetime, timedelta

import pandas as pd


def generate_mock_transactions(num_days=365):
    """Generates realistic mock bank transactions."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)

    current_date = start_date
    transactions = []

    # Starting balance
    balance = random.uniform(5000, 15000)

    # Establish some recurring rules
    salary_day = 10
    rent_day = 1
    subscriptions = {
        'Netflix': (15, 60.0),
        'Spotify': (20, 19.99),
        'Gym': (5, 120.0)
    }

    # Common stores for random expenses
    groceries = ['Biedronka', 'Lidl', 'Auchan', 'Kaufland', 'Zabka']
    dining = ['McDonalds', 'KFC', 'Starbucks', 'Pyszne.pl', 'Local Restaurant']
    transport = ['Orlen', 'BP', 'Uber', 'Bolt', 'Jakdojade']
    shopping = ['Allegro', 'Zalando', 'Amazon', 'Media Expert', 'IKEA']

    while current_date <= end_date:
        daily_transactions = []
        is_weekend = current_date.weekday() >= 5

        # 1. Monthly Salary (Income)
        if current_date.day == salary_day and current_date.weekday() < 5:
            # If salary day is weekday
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': 'WYNAGRODZENIE Z TYTULU UMOWY O PRACE - ACME CORP',
                'Amount': round(random.uniform(8000, 9500), 2),
                'Type': 'Income'
            })
        elif current_date.day == salary_day - 1 and current_date.weekday() == 4:
           # If salary falls on weekend, paid on Friday
           daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': 'WYNAGRODZENIE Z TYTULU UMOWY O PRACE - ACME CORP',
                'Amount': round(random.uniform(8000, 9500), 2),
                'Type': 'Income'
            })

        # 2. Fixed Expenses
        if current_date.day == rent_day:
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': 'PRZELEW - WYNAJEM MIESZKANIA',
                'Amount': -3500.00,
                'Type': 'Expense'
            })

        for sub_name, (sub_day, sub_amount) in subscriptions.items():
            if current_date.day == sub_day:
                daily_transactions.append({
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Description': f'PLATNOSC KARTA - {sub_name.upper()} COMP',
                    'Amount': -sub_amount,
                    'Type': 'Expense'
                })

        # 3. Variable Expenses (Groceries) - More frequent
        if random.random() < (0.6 if is_weekend else 0.3):
            store = random.choice(groceries)
            amount = round(random.uniform(30.0, 350.0), 2)
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': f'PLATNOSC KARTA - {store} WAW',
                'Amount': -amount,
                'Type': 'Expense'
            })

        # 4. Variable Expenses (Dining out) - Heavy on weekends
        if random.random() < (0.5 if is_weekend else 0.1):
            restaurant = random.choice(dining)
            amount = round(random.uniform(40.0, 180.0), 2)
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': f'PLATNOSC KARTA - {restaurant}',
                'Amount': -amount,
                'Type': 'Expense'
            })

        # 5. Transport (Gas, taxis)
        if random.random() < 0.2:
            vendor = random.choice(transport)
            amount = round(random.uniform(15.0, 300.0), 2)
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': f'PLATNOSC KARTA - {vendor}',
                'Amount': -amount,
                'Type': 'Expense'
            })

        # 6. Random Shopping / Anomalies
        if random.random() < 0.05:
            store = random.choice(shopping)
            # Occasional large purchase
            amount = round(random.uniform(100.0, 2500.0), 2)
            daily_transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': f'PLATNOSC WWW - {store}',
                'Amount': -amount,
                'Type': 'Expense'
            })

        # Process transactions for the day, update balance
        # Randomize order within the day
        random.shuffle(daily_transactions)
        for t in daily_transactions:
            balance += t['Amount']
            t['Balance'] = round(balance, 2)
            transactions.append(t)

        current_date += timedelta(days=1)

    # Introduce some noise/errors for realism (empty rows, corrupted lines)
    df = pd.DataFrame(transactions)

    # Sort descending (newest first, typical for bank exports)
    df = df.sort_values('Date', ascending=False).reset_index(drop=True)

    return df

if __name__ == "__main__":
    print("Generating mock transactions data...")
    df = generate_mock_transactions(num_days=400) # Generating slightly more than a year

    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    output_path = os.path.join('data', 'transactions.csv')
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} transactions.")
    print(f"Saved to: {output_path}")

    print("\nSample Data:")
    print(df.head())

