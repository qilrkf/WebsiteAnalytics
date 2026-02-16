# Website Analytics

## Task description
This program analyzes user activity on a website for two different days.
It finds users who:
- visited the website on both days
- visited at least one new product on the second day that they did not visit on the first day

## Input
Two CSV files with the following format:
user_id, product_id, timestamp

Duplicates are allowed.

## Output
User IDs that satisfy the conditions, printed to console.

## How to run
```bash
python analytics.py day1.csv day2.csv