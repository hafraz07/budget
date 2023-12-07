import calendar
import csv
from collections import defaultdict
from enum import Enum
from functools import reduce

import matplotlib.pyplot as plt

RULES = {
    "Biltpymts": "Rent",
    "American Express": "Restaurants",
    "Verizon": "Internet",
    "Mint Mobile": "Telephone",
    "Shake Shack": "Restaurants",
}


class bcolors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    ENDC = "\033[0m"


class Fields(Enum):
    DATE = 0
    ACCOUNT = 1
    DESCRIPTION = 2
    CATEGORY = 3
    TAGS = 4
    AMOUNT = 5


def get_month_name(date_string):
    month_num = int(date_string.split("-")[1])
    return calendar.month_abbr[month_num]


def aggregate_by_category(data):
    """Return dict with key category and dollar amount
    spent on that category. Recategorizes categories according
    to recategorization rules."""
    categories = defaultdict(float)
    for date, account, transaction_name, category, tags, amount in data:
        categories[category] += float(amount)

    # Sort by amount
    return dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))


def aggregate_by_month(data):
    return _aggregate_by_key(data, Fields.DATE.value)


def aggregate_by_account(data):
    return _aggregate_by_key(data, Fields.ACCOUNT.value)


def aggregate_by_transaction(data):
    return _aggregate_by_key(data, Fields.DESCRIPTION.value)


def aggregate_by_tags(data):
    return _aggregate_by_key(data, Fields.TAGS.value)


def _aggregate_by_key(data, index):
    aggregated = defaultdict(float)
    for row in data:
        field = row[index]
        amount = row[Fields.AMOUNT.value]
        if index == Fields.DATE.value:
            field = get_month_name(field)
        aggregated[field] += float(amount)
    return aggregated


def plot_bar(categories, values, **kwargs):
    # Figure Size
    _, ax = plt.subplots(figsize=(16, 9))
    ax.barh(
        list(categories),
        values,
        color=["purple", "maroon", "orange", "green", "salmon"],
    )

    # Add annotation to bars
    for bar in ax.patches:
        ax.annotate(
            f"${bar.get_width():,.0f}",
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            ha="center",
            va="center",
            size=15,
            xytext=(30, 0),
            textcoords="offset points",
        )

    if "invert" in kwargs and kwargs["invert"] is True:
        ax.invert_yaxis()
    ax.set_title("Spending by Category", loc="left")
    plt.show()


def show_highest_categories(data):
    """Display a bar chart with the amount spent in categories in a given month. Only includes transactions from given month. Otherwise includes all transactions."""
    categories = aggregate_by_category(data)
    plot_bar(categories.keys(), categories.values(), invert=True)


def print_transactions(transactions, categories: list):
    for category in categories:
        filtered_transactions = filter(
            lambda transaction: transaction[Fields.CATEGORY.value] == category,
            transactions,
        )
        sorted_by_amount = sorted(
            filtered_transactions, key=lambda item: float(item[-1])
        )

        print(category)
        for date, _, transaction_name, _, _, amount in sorted_by_amount:
            print_amount = (
                f"{bcolors.RED}${amount[1:]}"
                if float(amount) < 0
                else f"{bcolors.GREEN}+${amount}"
            )
            print(f"{date} {transaction_name} {print_amount}{bcolors.ENDC}")
        print()


def get_month(date: str) -> int:
    return int(date.split("-")[1])


def apply_rules(transactions):
    def _apply_rules(transaction):
        transaction_name = transaction[Fields.DESCRIPTION.value]
        if transaction_name in RULES:
            transaction[Fields.CATEGORY.value] = RULES[transaction_name]
        return transaction

    return map(_apply_rules, transactions)


def filter_by_month(transactions, month: int):
    """Return list of transactions for the given month"""
    return filter(
        lambda transaction: get_month(transaction[Fields.DATE.value]) == month,
        transactions,
    )


def calculate_summary_data(transactions):
    total_income, total_expenses = 0, 0
    for transaction in transactions:
        amount = float(transaction[Fields.AMOUNT.value])
        if amount < 0:
            total_expenses += amount
        else:
            total_income += amount

    net_cash_flow = total_income - abs(total_expenses)
    return total_income, total_expenses, net_cash_flow


def show_summary(transactions, categories=[]):
    """
    Given transactions and categories(optional),
    1. Print Cash Flow Information
    2. Print Transactions for provided categories
    3. Display Bar chart with category breakdown
    """
    transactions = list(apply_rules(transactions))

    total_income, total_expenses, net_cash_flow = calculate_summary_data(transactions)
    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expenses: {total_expenses:.2f}")
    print(f"Net Cash Flow: {net_cash_flow:.2f}")
    print()
    print_transactions(transactions, categories)
    show_highest_categories(transactions)


def show_cash_flow(transactions):
    cash_flow = defaultdict(list)
    transactions = list(transactions)
    for month in range(1, 13):
        filtered_transactions = filter_by_month(transactions, month)
        total_income, total_expenses, net_cash_flow = calculate_summary_data(
            filtered_transactions
        )
        cash_flow["Income"].append(total_income)
        cash_flow["Expense"].append(total_expenses)

    fig, ax = plt.subplots(figsize=(16, 9))
    for cash_flow_type, values in cash_flow.items():
        ax.bar(list(calendar.month_abbr[1:]), values, 0.5, label=cash_flow_type)
        # Add annotation to bars
        for bar in ax.patches:
            ax.annotate(
                f"${abs(bar.get_height()):,.0f}",
                (bar.get_x() + 0.2, bar.get_height()),
                ha="center",
                va="center",
                size=13,
                xytext=(0, 8),
                textcoords="offset points",
            )

    ax.set_title("Cash flow over months")
    ax.legend(loc="upper right")

    plt.show()


def show_net_cash_flow(transactions):
    """Display bar chart with net cash flow
    by month"""
    months = aggregate_by_month(transactions)
    plot_bar(months.keys(), months.values())


def main():
    filename = "transactions.csv"
    with open(filename, "r") as csvfile:
        transactions = csv.reader(csvfile)
        # extracting field names through first row
        _ = next(transactions)

        # transactions = filter_by_month(csvreader, 11)
        # show_summary(transactions, ["Rent"])
        show_net_cash_flow(transactions)


if __name__ == "__main__":
    main()
