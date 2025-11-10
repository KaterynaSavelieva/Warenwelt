from connection.storage import Storage
from pymysql import MySQLError
from tabulate import tabulate
from customer.validator import Validator
import pymysql

class CustomerMethods:
    #Methods for saving and loading customers.

    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

    # ---------------- Save ----------------
    def save_customer(
            self,
            *,
            name: str,
            email: str,
            kind: str,  # "private" | "company"
            address: str | None = None,
            phone: str | None = None,
            password: str = "",
            birthdate: str | None = None,
            company_number: str | None = None
    ) -> int | None:
        try:
            # 1. Валідація базових полів
            name = Validator.validate_name(name)
            email = Validator.validate_email(email)
            if address:
                address = Validator.validate_address(address)
            if phone:
                phone = Validator.validate_phone(phone)
            kind = Validator.validate_kind(kind)
            password = Validator.validate_password(password)

            # 2. Перевірка залежних полів ДО вставки в customers
            if kind == "private":
                if not birthdate:
                    print("Birthdate required for private customer (YYYY-MM-DD).")
                    return None
                birthdate = Validator.validate_birthdate(birthdate)
            elif kind == "company":
                if not company_number:
                    print("Company number required for company customer.")
                    return None
                company_number = Validator.validate_company_number(company_number)
                # 🔸 Перевіримо чи вже існує така company_number
                exists = self.storage.fetch_one(
                    "SELECT customer_id FROM company_customer WHERE company_number = %s",
                    (company_number,)
                )
                if exists:
                    print("This company number already exists. Please use another.")
                    return None

            #  3. Тільки тепер — транзакція та вставка
            self.storage.connection.begin()

            sql_cus = """
                INSERT INTO customers (name, email, address, phone, kind, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            new_id = self.storage.insert_and_get_id(sql_cus, (name, email, address, phone, kind, password))
            if not new_id:
                raise RuntimeError("Insert failed: no new ID returned.")

            # 4. Вставка підтаблиць
            if kind == "private":
                self.storage.execute(
                    "INSERT INTO private_customer (customer_id, birthdate) VALUES (%s, %s)",
                    (new_id, birthdate)
                )
            else:
                self.storage.execute(
                    "INSERT INTO company_customer (customer_id, company_number) VALUES (%s, %s)",
                    (new_id, company_number)
                )

            self.storage.connection.commit()
            print(f"Customer saved successfully with ID {new_id}.")
            return new_id

        except pymysql.err.IntegrityError as e:
            self.storage.connection.rollback()
            code = getattr(e, "args", [None])[0]
            msg = str(e).lower()
            if code == 1062:
                if "email" in msg:
                    print("This email already exists. Please use another email.")
                elif "company_number" in msg:
                    print("his company number already exists. Please use another number.")
                else:
                    print("Duplicate value violates a unique constraint.")
            else:
                print(f"Database integrity error: {e}")
            return None
        except ValueError as e:
            print("Validation error:", e)
            return None
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def save_customer2(
            self, *, name: str, email: str, kind: str,  # "private" | "company",
            address: str | None = None, phone: str | None = None, password: str = "", birthdate: str | None = None, company_number: str | None = None
    ) -> int | None:
        try:
            # 1) Валідація
            name = Validator.validate_name(name)
            email = Validator.validate_email(email)
            if address:
                address = Validator.validate_address(address)
            if phone:
                phone = Validator.validate_phone(phone)
            kind = Validator.validate_kind(kind)
            password = Validator.validate_password(password)

            if kind == "private":
                if not birthdate:
                    print("Birthdate required for private customer (YYYY-MM-DD).")
                    return None
                birthdate = Validator.validate_birthdate(birthdate)
            else:  # company
                if not company_number:
                    print("Company number required for company customer.")
                    return None
                company_number = Validator.validate_company_number(company_number)

            # 2) Транзакція
            self.storage.connection.begin()

            # customers
            sql_cus = """
                INSERT INTO customers (name, email, address, phone, kind, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            new_id = self.storage.insert_and_get_id(
                sql_cus, (name, email, address, phone, kind, password)
            )
            if not new_id:
                raise RuntimeError("Insert failed: no new ID returned.")

            # дочірня таблиця
            if kind == "private":
                self.storage.execute(
                    "INSERT INTO private_customer (customer_id, birthdate) VALUES (%s, %s)",
                    (new_id, birthdate)
                )
            else:
                self.storage.execute(
                    "INSERT INTO company_customer (customer_id, company_number) VALUES (%s, %s)",
                    (new_id, company_number)
                )

            # commit робиться всередині execute() (вдалий другий INSERT)
            print(f"✅ Customer saved successfully with ID {new_id}.")
            return new_id

        except pymysql.err.IntegrityError as e:
            # другий INSERT не закомітив — відкотимо перший
            self.storage.connection.rollback()
            code = getattr(e, "args", [None])[0]
            msg = str(e).lower()
            if code == 1062:
                if "email" in msg:
                    print("❌ This email already exists. Please use another email.")
                elif "company_number" in msg:
                    print("❌ This company number already exists. Please use another number.")
                else:
                    print("❌ Duplicate value violates a unique constraint.")
            else:
                print(f"❌ Database integrity error: {e}")
            return None
        except (ValueError, pymysql.MySQLError) as e:
            self.storage.connection.rollback()
            print(f"❌ Error: {e}")
            return None
        except Exception as e:
            self.storage.connection.rollback()
            print(f"❌ Unexpected error: {e}")
            return None


    # ---------------- Load one ----------------
    def get_customer(self, customer_id: int) -> dict | None:
        """Load one customer by id from the view v_cust."""
        try:
            sql = "SELECT * FROM v_cust WHERE customer_id = %s"
            row = self.storage.fetch_one(sql, (customer_id,))
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customer found with this ID.")
            return row
        except MySQLError as e:
            print("Error loading customer:", e)
            return None

    # ---------------- Load all ----------------
    def get_all_customers(self) -> list[dict]:
        """Load all customers from the view v_cust."""
        try:
            sql = "SELECT * FROM v_cust ORDER BY customer_id DESC"
            rows = self.storage.fetch_all(sql)
            if rows:
                print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customers found.")
            return rows
        except MySQLError as e:
            print("Error loading all customers:", e)
            return []

    def close(self):
        self.storage.disconnect()
