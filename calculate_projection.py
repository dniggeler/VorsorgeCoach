import datetime

# --- Constants ---
DOB = datetime.date(1969, 3, 17)
RETIREMENT_AGE = 65
RETIREMENT_YEAR = DOB.year + RETIREMENT_AGE
# Retirement date is typically end of the month after reaching 65
RETIREMENT_DATE = datetime.date(RETIREMENT_YEAR, DOB.month, 31) 
CURRENT_YEAR = 2026

# Remaining years (assuming beginning of 2026 for simplicity, or just full years remaining)
YEARS_TO_RETIREMENT = RETIREMENT_YEAR - CURRENT_YEAR # 2034 - 2026 = 8

# --- Existing Accounts ---
# From context:
# Baloise: 38000 @ 0%
# UBS: 67000 @ 1%
# Frankly: 10000 @ 2.5%
# Swisslife: 10000 @ 0%

existing_accounts = [
    {"name": "Baloise", "principal": 38000, "rate": 0.00},
    {"name": "UBS", "principal": 67000, "rate": 0.01},
    {"name": "Frankly", "principal": 10000, "rate": 0.025},
    {"name": "Swisslife", "principal": 10000, "rate": 0.00}
]

print(f"Projection Period: {YEARS_TO_RETIREMENT} years (2026 to {RETIREMENT_YEAR})")

total_existing_fv = 0
print("\n--- Existing 3a Capital Growth ---")
for acc in existing_accounts:
    fv = acc["principal"] * ((1 + acc["rate"]) ** YEARS_TO_RETIREMENT)
    total_existing_fv += fv
    print(f"{acc['name']}: Start {acc['principal']} -> End {fv:.2f} (Rate: {acc['rate']*100}%)")

print(f"Total Future Value of Existing Accounts: {total_existing_fv:.2f}")

# --- New Annual Savings ---
ANNUAL_SAVINGS = 7000
SAVINGS_RATE = 0.03 # User selected Balanced

# Future Value of an Annuity Due (assuming payment at start of year)
# FV = P * [ ((1 + r)^n - 1) / r ] * (1 + r)
n = YEARS_TO_RETIREMENT
r = SAVINGS_RATE
p = ANNUAL_SAVINGS

fv_savings = p * (((1 + r) ** n - 1) / r) * (1 + r)

print("\n--- New Annual Savings Growth ---")
print(f"Annual Savings: {ANNUAL_SAVINGS}")
print(f"Interest Rate: {SAVINGS_RATE*100}%")
print(f"Future Value of New Savings: {fv_savings:.2f}")

# --- Total ---
total_capital = total_existing_fv + fv_savings
print(f"\n=== Total Expected 3a Capital at Retirement ({RETIREMENT_YEAR}) ===")
print(f"CHF {total_capital:,.2f}")
