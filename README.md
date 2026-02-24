# Website Analytics (Distributed Lab Challenge — Task #3)

## Problem
You have two CSV files with product page visits (each file represents one day).  
CSV format: `user_id,product_id,timestamp` (duplicates are possible).

Find all users who:
1. Visited some product pages on **both** days (appear in both CSVs), and
2. On the **second day** visited **at least one** product page that this user **did not** visit on the first day.

Output: print all matching `user_id`s to the console (one per line).

---

## Solution idea (efficient & simple)
### Key observation
To decide whether a user visited a *new* product on day 2, we only need to know which products that user visited on day 1.

### Algorithm
1. **Index day 1**: build a mapping `user_id -> set(product_id)` using a hash set per user.
2. **Stream day 2** line-by-line:
   - if `user_id` is not in day 1 index → user didn’t visit both days → ignore
   - else if `product_id` is not in the user’s day 1 set → user qualifies → add to result set

Duplicates do not matter because sets remove duplicates automatically.

### Complexity (Big-O)
Let:
- `N1` = number of rows in day1 CSV
- `N2` = number of rows in day2 CSV  
Average-case (hash table / hash set operations):

- **Time**: `O(N1 + N2)`
- **Memory**: `O(U1 + P1)` where  
  - `U1` = number of unique users in day1  
  - `P1` = number of unique `(user, product)` pairs in day1

This is efficient because:
- each file is processed in a **single pass**
- day2 is processed in **streaming mode** (no need to store it in memory)
- membership checks are `O(1)` average

---

## How to run

### Requirements
- Python 3.9+ (works on 3.8+ too)

### Run (stdout)
```bash
python app.py day1.csv day2.csv
```

### Run (save to file)
```bash
python app.py day1.csv day2.csv --output result.txt
```

### Optional encoding
```bash
python app.py day1.csv day2.csv --encoding utf-8
```

---

## Input example

**day1.csv**
```
u1,p1,1700000000
u1,p2,1700000100
u2,p5,1700000200
```

**day2.csv**
```
u1,p2,1700086400
u1,p3,1700086500
u3,p9,1700086600
```

Output:
```
u1
```
Explanation:
- `u1` appears in both days and visited `p3` on day2 which was not visited on day1.
- `u3` appears only on day2 → not eligible.

---

## Time spent (example)
- Understanding the task & planning: ~0.5h  
- Implementation: ~1.0h  
- Testing + README: ~0.5h  
**Total:** ~2.0h

(You can adjust these numbers to your actual time.)

---

## Notes
- The script validates the CSV format (expects exactly 3 columns per line).
- Whitespace around IDs is trimmed.
