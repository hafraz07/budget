import calendar
import csv
from collections import defaultdict
from enum import Enum

import matplotlib.pyplot as plt

RULES = {
    "Biltpymts": "Rent",
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


def read_file(filename):
    with open(filename, "r") as csvfile:
        return csv.reader(csvfile)


def get_month_name(date_string):
    month_num = int(date_string.split("-")[1])
    return calendar.month_abbr[month_num]


def aggregate_by_category(data):
    """Return dict with key category and dollar amount
    spent on that category. Recategorizes categories according
    to recategorization rules."""
    categories = defaultdict(float)
    for date, account, transaction_name, category, tags, amount in data:
        # Recategorize if needed
        if transaction_name in RULES:
            category = RULES[transaction_name]
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


def plot_bar(categories, values):
    # Figure Size
    fig, ax = plt.subplots(figsize=(16, 9))
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

    ax.invert_yaxis()
    ax.set_title("Spending by Months", loc="left")
    plt.show()


def show_highest_categories(data):
    """Display a bar chart with the amount spent in categories in a given month. Only includes transactions from given month. Otherwise includes all transactions."""
    categories = aggregate_by_category(data)
    plot_bar(categories.keys(), categories.values())


def print_transactions(data, expected_category):
    print(expected_category)
    transactions = []
    for row in data:
        if expected_category == row[Fields.CATEGORY.value]:
            transactions.append(row)

    transactions = sorted(transactions, key=lambda item: float(item[-1]))
    for date, account, transaction_name, category, tags, amount in transactions:
        print_amount = (
            f"{bcolors.RED}${amount[1:]}"
            if float(amount) < 0
            else f"{bcolors.GREEN}+${amount}"
        )
        print(f"{date} {transaction_name} {print_amount}{bcolors.ENDC}")
    print()


def get_month(date: str) -> int:
    return int(date.split("-")[1])


def filter_by_month(transactions, month: int):
    """Return list of transactions for the given month"""
    return filter(
        lambda transaction: get_month(transaction[Fields.DATE.value]) == month,
        transactions,
    )


def main():
    filename = "transactions.csv"
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # extracting field names through first row
        _ = next(csvreader)

        filtered_transactions = list(filter_by_month(csvreader, 11))

        print_transactions(filtered_transactions, "General Merchandise")
        show_highest_categories(filtered_transactions)


if __name__ == "__main__":
    main()
