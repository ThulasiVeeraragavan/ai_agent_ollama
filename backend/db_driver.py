# import sqlite3
# from typing import Optional
# from dataclasses import dataclass
# from contextlib import contextmanager

# @dataclass
# class Loan:
#     loanid: str
#     amount: str
#     date: str
#     pending: int

# class DatabaseDriver:
#     def __init__(self, db_path: str = "auto_db.sqlite"):
#         self.db_path = db_path
#         self._init_db()

#     @contextmanager
#     def _get_connection(self):
#         conn = sqlite3.connect(self.db_path)
#         try:
#             yield conn
#         finally:
#             conn.close()

#     def _init_db(self):
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
            
#             # Create cars table
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS loan (
#                     loanid TEXT PRIMARY KEY,
#                     amount TEXT NOT NULL,
#                     date TEXT NOT NULL,
#                     pending INTEGER NOT NULL
#                 )
#             """)
#             conn.commit()

#     def create_loan(self, loanid: str, amount: str, date: str, pending: int) -> Loan:
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 "INSERT INTO loan (loanid, amount, date, pending) VALUES (?, ?, ?, ?)",
#                 (loanid, amount, date, pending)
#             )
#             conn.commit()
#             return Loan(loanid=loanid, amount=amount, date=date, pending=pending)

#     def get_loan_by_loanid(self, loanid: str) -> Optional[Loan]:
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM loan WHERE loanid = ?", (loanid,))
#             row = cursor.fetchone()
#             if not row:
#                 return None
            
#             return Loan(
#                 loanid=row[0],
#                 amount=row[1],
#                 date=row[2],
#                 pending=row[3]
#             )
import psycopg2
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Loan:
    loanid: str
    amount: str
    date: str
    pending: int

class DatabaseDriver:
    def __init__(self, dsn: str = "dbname=postgres user=postgres password=gitech123*gitech host=localhost"):
        self.dsn = dsn
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = psycopg2.connect(self.dsn)
        try:
            yield conn, conn.cursor()
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as (conn, cur):
            cur.execute("""
                CREATE TABLE IF NOT EXISTS loan (
                    loanid TEXT PRIMARY KEY,
                    amount TEXT NOT NULL,
                    date TEXT NOT NULL,
                    pending INTEGER NOT NULL
                )
            """)
            conn.commit()

    def create_loan(self, loanid: str, amount: str, date: str, pending: int) -> Loan:
        with self._get_connection() as (conn, cur):
            cur.execute(
                "INSERT INTO loan (loanid, amount, date, pending) VALUES (%s, %s, %s, %s)",
                (loanid, amount, date, pending)
            )
            conn.commit()
            return Loan(loanid=loanid, amount=amount, date=date, pending=pending)

    def get_loan_by_loanid(self, loanid: str) -> Optional[Loan]:
        with self._get_connection() as (conn, cur):
            cur.execute("SELECT * FROM loan WHERE loanid = %s", (loanid,))
            row = cur.fetchone()
            if not row:
                return None
            
            return Loan(
                loanid=row[0],
                amount=row[1],
                date=row[2],
                pending=row[3]
            )
