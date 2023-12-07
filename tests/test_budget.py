import csv

import budget


def test_filter_by_month():
    transactions = [
        ["2023-11-01", "Capital One", "Chipotle", "Restaurants", "", "-12.63"],
        ["2023-10-01", "Chase", "CVS", "Drugs", "", "-5.00"],
    ]

    # Filter October transactions
    filtered = list(budget.filter_by_month(transactions, 10))
    assert len(filtered) == 1
    assert filtered[0] == transactions[1]


def test_apply_rules():
    transactions = [
        ["2023-11-01", "Capital One", "American Express", "Food", "", "-12.63"],
    ]
    rules_applied = list(budget.apply_rules(transactions))
    assert len(rules_applied) == 1
    assert rules_applied[0][3] == "Restaurants"


def test_summary_data():
    transactions = [
        ["2023-11-01", "Capital One", "Chipotle", "Restaurants", "", "-15.0"],
        ["2023-10-01", "Chase", "CVS", "Drugs", "", "-5.00"],
        ["2023-10-01", "Chase", "Paycheck", "Income", "", "10.0"],
    ]
    total_income, total_expenses, net_cash_flow = budget.calculate_summary_data(
        transactions
    )
    assert total_income == 10.0
    assert total_expenses == -20.0
    assert net_cash_flow == -10.0


# def test_aggregation_by_month():
#     with open("transactions.csv", 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         aggregated = budget.aggregate_by_month(csvreader)
#         print_aggregated(aggregated)
#
# def test_aggregation_by_category():
#     with open("transactions.csv", 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         aggregated = budget.aggregate_by_category(csvreader)
#         print_aggregated(aggregated)
#
# def test_aggregation_by_account():
#     with open("transactions.csv", 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         aggregated = budget.aggregate_by_account(csvreader)
#         print_aggregated(aggregated)
#
# def print_aggregated(aggregated):
#     for key, amount in aggregated.items():
#         print(f"{key}: ${amount:.2f}")
#     print()
