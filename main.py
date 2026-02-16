import csv
import sys
from collections import defaultdict

def load_visits(filename):
    visits = defaultdict(set)
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for user_id, product_id, _ in reader:
            visits[user_id].add(product_id)
    return visits

def main(day1_file, day2_file):
    day1 = load_visits(day1_file)
    day2 = load_visits(day2_file)

    result_users = []

    for user in day1:
        if user in day2:
            if day2[user] - day1[user]:
                result_users.append(user)

    for user in result_users:
        print(user)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analytics.py day1.csv day2.csv")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])