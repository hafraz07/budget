import calendar
import csv
from collections import defaultdict
from enum import Enum

import matplotlib.pyplot as plt

FILENAME = "transactions.csv"


class Fields(Enum):
    DATE = 0
    ACCOUNT = 1
    DESCRIPTION = 2
    CATEGORY = 3
    TAGS = 4


def read_file(filename):
    with open(filename, "r") as csvfile:
        return csv.reader(csvfile)


def get_month_name(date_string):
    month_num = int(date_string.split("-")[1])
    return calendar.month_abbr[month_num]


def aggregate_by_category(csvreader):
    aggregated = _aggregate_by_key(csvreader, Fields.CATEGORY.value)
    return dict(sorted(aggregated.items(), key=lambda item: item[1], reverse=True))


def aggregate_by_month(csvreader):
    return _aggregate_by_key(csvreader, Fields.DATE.value)


def aggregate_by_account(csvreader):
    return _aggregate_by_key(csvreader, Fields.ACCOUNT.value)


def aggregate_by_transaction(csvreader):
    return _aggregate_by_key(csvreader, Fields.DESCRIPTION.value)


def aggregate_by_tags(csvreader):
    return _aggregate_by_key(csvreader, Fields.TAGS.value)


def _aggregate_by_key(csvreader, index):
    aggregated = defaultdict(float)
    # extracting field names through first row
    fields = next(csvreader)
    for row in csvreader:
        field = row[index]
        amount = row[-1]
        if index == Fields.DATE.value:
            field = get_month_name(field)
        aggregated[field] += abs(float(amount))
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
    ax.xaxis.set_label("Months")
    ax.yaxis.set_label("Amount")
    ax.set_title("Spending by Months", loc="left")
    plt.show()


def main():
    filename = "transactions.csv"
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        aggregated = aggregate_by_category(csvreader)
        plot_bar(aggregated.keys(), aggregated.values())


if __name__ == "__main__":
    main()
