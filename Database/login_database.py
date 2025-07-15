import sqlite3
import os
from Time_And_Config.time_and_config import DateTimeUtils
from CTkMessagebox import CTkMessagebox

datebase_path = os.path.join(os.path.dirname(__file__), "bank_account.db")

class _data_base:
    def __init__(self):
        self.db_name = datebase_path
        self.datetime_util = DateTimeUtils()
        self._initialize_database()
        with sqlite3.connect(self.db_name) as self.conn:
            self.cursor = self.conn.cursor()
    
    def _initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # check
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
            if cursor.fetchone() is None:
                # create
                cursor.execute('''
                CREATE TABLE employees (
                    employee_id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    branch_code TEXT NOT NULL
                )
                ''')
                print("employees table created")
            
            # check
            cursor.execute("SELECT COUNT(*) FROM employee WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                # insert
                cursor.execute('''
                INSERT INTO employee (username, password, full_name, position, branch_code)
                VALUES (?, ?, ?, ?, ?)
                ''', ('admin', 'admin', 'Administrator', 'System Admin', 'HQS'))
                conn.commit()
                print("default admin created")
            else:
                print("admin exists")

    def verify_user(self, username, password):
        """Auth"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT password FROM employee WHERE username = ?",
                    (username,)
                )
                result = cursor.fetchone()
                if not result:
                    return False
                stored_password = result[0]
                return password == stored_password
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return False

    def get_all_employees(self) -> list:
        """Fetch"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        employee_id,
                        username,
                        old,
                        full_name,
                        position,
                        branch_code,
                        password
                    FROM employees
                """)
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    def search_employees(self, term: str) -> list:
        """Search"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                wildcard = f"%{term}%"
                cursor.execute("""
                    SELECT
                        employee_id,
                        username,
                        old,
                        full_name,
                        position,
                        branch_code,
                        password
                    FROM employees
                    WHERE username LIKE ?
                       OR full_name LIKE ?
                       OR position LIKE ?
                """, (wildcard, wildcard, wildcard))
                rows = cursor.fetchall()
                return [ (r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows ]
        except Exception:
            return []

    def save_customer(self, nationalcode, full_name, opening_date, state='ACTIVE', balance=0.0):
        """Insert"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO customers (nationalcode, full_name, opening_date, state, balance)
            VALUES (?, ?, ?, ?, ?)
            ''', (nationalcode, full_name, opening_date, state, balance))
            conn.commit()

    def add_employee(self, username: str, old: str, full_name: str, position: str, branch_code: str,
                     password: str) -> bool:
        """Insert"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username FROM employee WHERE username = ?",
                    (username,)
                )
                if cursor.fetchone():
                    return False
                cursor.execute("""
                    INSERT INTO employee (
                        username,
                        old,
                        full_name,
                        position,
                        branch_code,
                        password
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (username, old, full_name, position, branch_code, password))
                conn.commit()
                return True
        except Exception:
            return False

    def create_account(self, account_id: str, full_name: str, nationalcode: str, balance: float) -> bool:
        """Create"""
        try:
            if self.get_account_by_number(account_id):
                CTkMessagebox(icon="cancel", title='Account ID', message="Exists") 
                return False
            query = """
            INSERT INTO customers (account_id, nationalcode, full_name, opening_date, state, balance)
            VALUES (?, ?, ?, datetime('now'), 'active', ?)
            """
            self.cursor.execute(query, (account_id, nationalcode, full_name, balance))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            CTkMessagebox(icon="cancel", title='Cancel', message=f"{e}")
            return False

    def get_account_by_number(self, account_id: str):
        """Fetch"""
        try:
            query = """
            SELECT account_id, nationalcode, full_name, opening_date, state, balance
            FROM customers 
            WHERE account_id = ?
            """
            self.cursor.execute(query, (account_id,))
            result = self.cursor.fetchone()
            if result:
                return {
                    'account_id': result[0],
                    'nationalcode': result[1],
                    'full_name': result[2],
                    'opening_date': result[3],
                    'state': result[4],
                    'balance': result[5]
                }
            return None
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return None

    def get_all_customers(self):
        """Fetch"""
        try:
            query = """
            SELECT account_id, nationalcode, full_name, opening_date, state, balance
            FROM customers
            ORDER BY account_id
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results 
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return

    def get_all_employees(self) -> list:
        """Fetch"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        employee_id,
                        username,
                        old,
                        full_name,
                        position,
                        branch_code,
                        password
                    FROM employee
                """)
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

    def update_account(self, account_number: str, account_name: str, account_nationalcode: str, account_balance: str) -> bool:
        """Update"""
        try:
            existing = self.get_account_by_number(account_number)
            if not existing:
                CTkMessagebox(
                    title="Error",
                    message=f"No account '{account_number}'",
                    icon="cancel",
                    option_1="OK"
                )
                return False
            query = """
                UPDATE customers
                SET full_name      = ?,
                    nationalcode   = ?,
                    balance        = ?
                WHERE account_id  = ?
            """
            self.cursor.execute(query, (account_name, account_nationalcode, account_balance, account_number))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return False

    def deactivate_account(self, account_id: int) -> bool:
        """Toggle"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT state FROM customers WHERE account_id = ?",
                    (account_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return False
                current_state = row[0].strip().lower()
                new_state = "inactive" if current_state == "active" else "active"
                cursor.execute(
                    "UPDATE customers SET state = ? WHERE account_id = ?",
                    (new_state, account_id)
                )
                conn.commit()
                return True
        except Exception:
            return False

    def withdraw_account(self, account_id: int, amount: str) -> bool:
        """Withdraw"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT balance FROM customers WHERE account_id = ?",
                    (account_id,)
                )
                row = cursor.fetchone()
                if not row:
                    CTkMessagebox(
                        title="Error",
                        message=f"No account '{account_id}'",
                        icon="cancel",
                        option_1="OK"
                    )
                    return False
                current_balance = str(row[0])
                if amount <= 0:
                    CTkMessagebox(
                        title="Error",
                        message="Must be positive",
                        icon="cancel",
                        option_1="OK"
                    )
                    return False
                if amount > int(current_balance.replace(',', '')):
                    CTkMessagebox(
                        title="Error",
                        message="Insufficient",
                        icon="cancel",
                        option_1="OK"
                    )
                    return False
                new_balance = int(current_balance.replace(',', '')) - amount
                cursor.execute(
                    "UPDATE customers SET balance = ? WHERE account_id = ?",
                    (new_balance, account_id)
                )
                conn.commit()
                return True
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return False

    def deposit_account(self, account_id: int, amount: float) -> bool:
        """Deposit"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT balance FROM customers WHERE account_id = ?",
                    (account_id,)
                )
                row = cursor.fetchone()
                if not row:
                    CTkMessagebox(
                        title="Error",
                        message=f"No account '{account_id}'",
                        icon="cancel",
                        option_1="OK"
                    )
                    return False
                current_balance = float(row[0])
                if amount <= 0:
                    CTkMessagebox(
                        title="Error",
                        message="Must be positive",
                        icon="cancel",
                        option_1="OK"
                    )
                    return False
                new_balance = current_balance + amount
                cursor.execute(
                    "UPDATE customers SET balance = ? WHERE account_id = ?",
                    (new_balance, account_id)
                )
                conn.commit()
                return True
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"{e}",
                icon="cancel",
                option_1="OK"
            )
            return False

    def delete_account(self, account_id: str) -> bool:
        """Delete"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT account_id FROM customers WHERE account_id = ?",
                    (account_id,)
                )
                if not cursor.fetchone():
                    return False
                cursor.execute(
                    "DELETE FROM customers WHERE account_id = ?",
                    (account_id,)
                )
                conn.commit()
                return True
        except Exception:
            return False
    
    def delete_user(self, username: str) -> bool:
        """Delete"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username FROM employee WHERE username = ?",
                    (username,)
                )
                if not cursor.fetchone():
                    return False
                cursor.execute(
                    "DELETE FROM employee WHERE username = ?",
                    (username,)
                )
                conn.commit()
                return True
        except Exception:
            return False

    def search_accounts(self, term: str) -> list:
        """Search"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                wildcard = f"%{term}%"
                query = """
                    SELECT
                        account_id,
                        nationalcode,
                        full_name,
                        "opening date",
                        state,
                        balance
                    FROM customers
                    WHERE CAST(account_id AS TEXT) LIKE ?
                       OR CAST(nationalcode AS TEXT) LIKE ?
                """
                cursor.execute(query, (wildcard, wildcard))
                rows = cursor.fetchall()
                return rows
        except Exception:
            return []

class _Login:
    def __init__(self):
        self.db = _data_base()
        self.login_status = False
        self.username = None
        self.login_problem = None

    def login_btn(self, username, password):
        """Login"""
        if not username or not password:
            self.login_problem = "Empty"
            return False
        if self.db.verify_user(username, password):
            self.login_status = True
            self.username = username
            return True
        self.login_problem = "Failed"
        return False

    def get_login_status(self):
        return self.login_status

    def get_username(self):
        return self.username

    def get_login_problem(self):
        return self.login_problem
