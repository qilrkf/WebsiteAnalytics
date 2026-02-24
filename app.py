#!/usr/bin/env python3
"""
Website analytics console app.

Find users who:
1) visited product pages on both days (appear in both CSVs), AND
2) on the second day visited at least one product page that the same user did NOT visit on the first day.

Input CSV format (per line): user_id,product_id,timestamp
Duplicates may exist.

Usage:
  python app.py day1.csv day2.csv
  python app.py day1.csv day2.csv --output result.txt

Notes:
- Reads CSVs in a streaming manner (line by line).
- Stores (unique) products visited per user for day1 to compare with day2.
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, Set, Iterable, Optional, TextIO


def build_day1_index(path: Path, encoding: str = "utf-8") -> Dict[str, Set[str]]:
    """
    Build an index: user_id -> set(product_id) for day1.

    Complexity:
      Time:  O(N1) average (hash set insert), where N1 = number of rows in day1 file
      Space: O(U1 + P1) where U1 = unique users in day1, P1 = unique (user, product) pairs in day1
    """
    user_to_products: Dict[str, Set[str]] = {}

    with path.open("r", encoding=encoding, newline="") as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader, start=1):
            if len(row) != 3:
                raise ValueError(f"{path}: expected 3 columns at line {row_num}, got {len(row)}: {row}")
            user_id, product_id, _ts = row
            # Normalize to avoid accidental whitespace issues
            user_id = user_id.strip()
            product_id = product_id.strip()
            if not user_id or not product_id:
                # skip blank IDs (could also choose to error)
                continue
            s = user_to_products.get(user_id)
            if s is None:
                s = set()
                user_to_products[user_id] = s
            s.add(product_id)

    return user_to_products


def find_target_users(
    day1_index: Dict[str, Set[str]],
    day2_path: Path,
    encoding: str = "utf-8",
) -> Set[str]:
    """
    Stream day2 and find user IDs that:
      - exist in day1_index (visited both days), and
      - have at least one product_id in day2 that's not in their day1 set.

    Complexity:
      Time:  O(N2) average, where N2 = number of rows in day2 file
      Space: O(U*) where U* = number of matched users (results set)
    """
    result: Set[str] = set()

    with day2_path.open("r", encoding=encoding, newline="") as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader, start=1):
            if len(row) != 3:
                raise ValueError(f"{day2_path}: expected 3 columns at line {row_num}, got {len(row)}: {row}")
            user_id, product_id, _ts = row
            user_id = user_id.strip()
            product_id = product_id.strip()
            if not user_id or not product_id:
                continue

            day1_products = day1_index.get(user_id)
            if day1_products is None:
                # User did not appear on day1 => not eligible
                continue

            # If user already qualifies, we can skip further checks for that user
            if user_id in result:
                continue

            if product_id not in day1_products:
                result.add(user_id)

    return result


def write_output(user_ids: Iterable[str], out: Optional[TextIO]) -> None:
    """
    Write user IDs, one per line, sorted for stable output.
    """
    for uid in sorted(user_ids):
        out.write(uid + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find users who visited on both days and saw a new product on day2."
    )
    parser.add_argument("day1", type=Path, help="CSV file for day 1 (user_id,product_id,timestamp)")
    parser.add_argument("day2", type=Path, help="CSV file for day 2 (user_id,product_id,timestamp)")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Optional output file. Defaults to stdout.")
    args = parser.parse_args()

    if not args.day1.exists():
        parser.error(f"Day1 file not found: {args.day1}")
    if not args.day2.exists():
        parser.error(f"Day2 file not found: {args.day2}")

    day1_index = build_day1_index(args.day1, encoding=args.encoding)
    target_users = find_target_users(day1_index, args.day2, encoding=args.encoding)

    if args.output is None:
        import sys
        write_output(target_users, sys.stdout)
    else:
        with args.output.open("w", encoding="utf-8", newline="") as out:
            write_output(target_users, out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
