from sqlalchemy import text
from core.database import engine


def check_pair(lender_company: str, borrower_company: str, month: str, year: int) -> None:
    sql_rows = text(
        """
        SELECT COUNT(*) AS cnt
        FROM tally_data t1
        WHERE t1.matched_with IS NOT NULL
          AND t1.match_status = 'user_verified'
          AND ((t1.lender = :l AND t1.borrower = :b) OR (t1.lender = :b AND t1.borrower = :l))
          AND t1.statement_month = :m AND t1.statement_year = :y
        """
    )

    sql_pairs = text(
        """
        SELECT COUNT(*) AS cnt
        FROM (
            SELECT LEAST(t1.uid, t1.matched_with) AS a,
                   GREATEST(t1.uid, t1.matched_with) AS b
            FROM tally_data t1
            WHERE t1.matched_with IS NOT NULL
              AND t1.match_status = 'user_verified'
              AND ((t1.lender = :l AND t1.borrower = :b) OR (t1.lender = :b AND t1.borrower = :l))
              AND t1.statement_month = :m AND t1.statement_year = :y
            GROUP BY a, b
        ) x
        """
    )

    sql_dupes = text(
        """
        SELECT LEAST(t1.uid, t1.matched_with) AS a,
               GREATEST(t1.uid, t1.matched_with) AS b,
               COUNT(*) AS rows_per_pair
        FROM tally_data t1
        WHERE t1.matched_with IS NOT NULL
          AND t1.match_status = 'user_verified'
          AND ((t1.lender = :l AND t1.borrower = :b) OR (t1.lender = :b AND t1.borrower = :l))
          AND t1.statement_month = :m AND t1.statement_year = :y
        GROUP BY a, b
        HAVING COUNT(*) > 1
        ORDER BY rows_per_pair DESC
        """
    )

    params = {"l": lender_company, "b": borrower_company, "m": month, "y": year}
    with engine.connect() as conn:
        rows = conn.execute(sql_rows, params).scalar() or 0
        pairs = conn.execute(sql_pairs, params).scalar() or 0
        dupes = conn.execute(sql_dupes, params).fetchall()

    print(f"Confirmed rows: {rows}")
    print(f"Unique confirmed pairs: {pairs}")
    if dupes:
        print("Pairs with duplicate rows (should be 2 rows per pair in raw table):")
        for a, b, c in dupes:
            print(f"  pair=({a}, {b}) rows={c}")
    else:
        print("No duplicate confirmed pairs beyond the expected two raw rows.")


if __name__ == "__main__":
    # Default to the pair shown in your screenshot
    check_pair("GeoTex", "Steel", "January", 2025)


