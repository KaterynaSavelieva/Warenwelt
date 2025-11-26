from connection.storage import Storage
from pymysql import MySQLError
from tabulate import tabulate
from customers.validator import Validator
import pymysql


class CustomerMethods:
    # Methods for saving and loading customers.

    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

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
                    raise ValueError("Birthdate: required for private customers (format: YYYY-MM-DD).")
                birthdate = Validator.validate_birthdate(birthdate)

            elif kind == "company":
                if not company_number:
                    raise ValueError("Company number: required for company customers.")
                company_number = Validator.validate_company_number(company_number)

                exists = self.storage.fetch_one(
                    "SELECT customer_id FROM company_customer WHERE company_number = %s",
                    (company_number,)
                )
                if exists:
                    raise ValueError("Company number: this company number already exists. Please use another.")

            # 3. Транзакція + вставка
            self.storage.connection.begin()

            sql_cus = """
                INSERT INTO customers (name, email, address, phone, kind, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            new_id = self.storage.insert_and_get_id(
                sql_cus, (name, email, address, phone, kind, password)
            )
            if not new_id:
                # якщо insert не повернув id – це вже технічна помилка
                raise RuntimeError("Insert failed: no new ID returned.")

            # 4. Підтаблиці
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
            #  дублікати email/номер компанії → теж як помилка введення
            self.storage.connection.rollback()
            code = getattr(e, "args", [None])[0]
            msg = str(e).lower()
            if code == 1062 and "email" in msg:
                raise ValueError("Email: this email already exists. Please use another email.") from None
            if code == 1062 and "company_number" in msg:
                raise ValueError(
                    "Company number: this company number already exists. Please use another number."
                ) from None
            # усе інше нехай летить далі
            raise

        except pymysql.MySQLError as e:
            # «серйозні» помилки БД
            self.storage.connection.rollback()
            print(f"Database error: {e}")
            return None

        # НІЯКОГО `except Exception` тут – інакше ми знову з’їмо ValueError!

    def get_customer(self, customer_id: int) -> dict | None:
        """Load one customers by id from the cli v_cust."""
        try:
            sql = "SELECT * FROM v_customers WHERE customer_id = %s"
            row = self.storage.fetch_one(sql, (customer_id,))
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customers found with this ID.")
            return row
        except MySQLError as e:
            print("Error loading customers:", e)
            return None

    def get_customer_name(self, customer_id: int) -> str | None:
        row = self.storage.fetch_one(
            "SELECT name FROM v_cust WHERE customer_id = %s",
            (customer_id,)
        )
        if row:
            return row["name"]
        return None

    def get_customer_by_email (self, email: str) -> dict | None:
        try:
            sql = "SELECT * FROM v_cust WHERE email = %s"
            row = self.storage.fetch_one(sql, (email,)) #tuple
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customers found with this email.")
            return row
        except MySQLError as e:
            print("Error loading customers:", e)
            return None

    def get_customer_by_id(self, customer_id: int) -> dict | None:
        sql = "SELECT * FROM v_customers WHERE customer_id = %s"
        row = self.storage.fetch_one(sql, (customer_id,))
        return row

    def get_all_customers(self) -> list[dict]:
        """Load all customers from the cli v_customers."""
        try:
            sql = "SELECT * FROM v_customers ORDER BY customer_id DESC"
            rows = self.storage.fetch_all(sql)
            if rows:
                print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customers found.")
            return rows
        except MySQLError as e:
            print("Error loading all customers:", e)
            return []

    def update_customer(
            self,
            customer_id: int,
            *,
            name: str | None = None,
            email: str | None = None,
            address: str | None = None,
            phone: str | None = None,
    ) -> bool:
        """
        Updates basic customer data in 'customers' table.
        """
        fields = []
        params: list[object] = []

        if name is not None:
            fields.append("name = %s")
            params.append(name)
        if email is not None:
            fields.append("email = %s")
            params.append(email)
        if address is not None:
            fields.append("address = %s")
            params.append(address)
        if phone is not None:
            fields.append("phone = %s")
            params.append(phone)

        if not fields:
            return True  # nothing to update

        params.append(customer_id)
        sql = "UPDATE customers SET " + ", ".join(fields) + " WHERE customer_id = %s"
        ok = self.storage.execute(sql, tuple(params))
        return bool(ok)

    def update_customer2(self, customer_id: int, *,
                        name: str | None = None,
                        address: str | None = None,
                        phone: str | None = None,
                        password: str | None = None) -> bool:
        try:
            sets, vals = [], []
            if name:
                sets.append("name=%s")
                vals.append(Validator.validate_name(name))
            if address:
                sets.append("address=%s")
                vals.append(Validator.validate_address(address))
            if phone:
                sets.append("phone=%s")
                vals.append(Validator.validate_phone(phone))
            if password:
                sets.append("password=%s")
                vals.append(Validator.validate_password(password))

            if not sets:
                print("Nothing to update.")
                return False

            sql = f"UPDATE customers SET {', '.join(sets)} WHERE customer_id=%s"
            vals.append(customer_id)
            ok = self.storage.execute(sql, tuple(vals))
            self.storage.connection.commit()
            print(f"Customer {customer_id} updated.") if ok else print("No changes.")
            return bool(ok)
        except MySQLError as e:
            self.storage.connection.rollback()
            print("Update error:", e)
            return False
        # ValueError від Validator нехай летить нагору → побачиш нормальне повідомлення в UI/меню

    def delete_customer(self, customer_id: int) -> bool:
        try:
            ok = self.storage.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
            self.storage.connection.commit()
            return bool(ok)
        except MySQLError as e:
            self.storage.connection.rollback()
            print("Delete error:", e)
            return False

    def find_customers_by_kind(self, kind: str) -> list[dict]:
        # якщо передадуть "privat" → тут одразу ValueError, і це добре
        kind = Validator.validate_kind(kind)
        try:
            rows = self.storage.fetch_all(
                "SELECT * FROM v_customers WHERE kind=%s ORDER BY customer_id",
                (kind,)
            )
            if rows:
                print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            else:
                print("No customers for this kind.")
            return rows or []
        except MySQLError as e:
            print("Find error:", e)
            return []

    def close(self):
        self.storage.disconnect()
