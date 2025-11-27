from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from utils.cart_helpers import  check_password
from models.customers.customer_methods import CustomerMethods
from models.customers.validator import Validator
from pydantic import ValidationError

customers_bp = Blueprint("customers", __name__)
cm = CustomerMethods()

@customers_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page:
      - GET: show empty form
      - POST: validate, save customer, handle errors with flash messages.
    """
    if request.method == "POST":
        form = request.form.to_dict()

        name = form.get("name", "").strip().title()
        email = form.get("email", "").strip().title()
        address = form.get("address") or None
        phone = form.get("phone") or None
        kind = form.get("kind", "private").lower()
        password = form.get("password", "")
        password2 = form.get("password2", "")
        birthdate = form.get("birthdate") or None
        company_number = form.get("company_number") or None

        try:
            # 1) Check if passwords match
            if password != password2:
                raise ValueError("Passwords do not match.")

            # 2) Try to save customer using CustomerMethods (with Pydantic inside)
            try:
                new_id = cm.save_customer(
                    name=name,
                    email=email,
                    address=address,
                    phone=phone,
                    kind=kind,
                    password=password,
                    birthdate=birthdate,
                    company_number=company_number,
                )
            except ValidationError as err:
                # extract field name from Pydantic error
                field = err.errors()[0].get("loc", ["?"])[0]
                field_map = {
                    "name": "Name",
                    "email": "Email",
                    "address": "Address",
                    "phone": "Phone",
                    "birthdate": "Birthdate",
                    "company_number": "Company number",
                    "password": "Password",
                    "kind": "Kind",
                }
                label = field_map.get(field, str(field).capitalize())
                # raise ValueError with short readable message
                Validator.f_short_err(err, label)

            # 3) If save_customer returned None → generic failure
            if not new_id:
                flash("Registration failed. Please try again later.", "error")
                return render_template("register.html", form=form)

            # 4) Success
            flash(
                f"Registration successful, {name}!\n"
                f"Your customer number is {new_id}.\n"
                "Please save your customer number and password.\n"
                "You can now log in.",
                "success",
            )
            return redirect(url_for("customers.login"))

        except ValueError as e:
            # All our "nice" messages arrive here
            flash(str(e), "error")
            return render_template("register.html", form=form)

        except Exception as e:
            print("Unexpected error in /register:", e)
            flash("Unexpected error. Please try again later.", "error")
            return render_template("register.html", form=form)

    return render_template("register.html", form={})


@customers_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page:
      - GET: show form
      - POST: check email/password, set session and redirect to products.
    """
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # 1) Simple check for empty fields
        if not email or not password:
            error = "Please enter your email address and password."
        else:
            # 2) Load user from DB
            user = cm.get_customer_by_email(email)

            # 3) Validate user and password
            if not user or not check_password(user, password):
                error = "Incorrect email or password."
            else:
                # 4) Login successful → store session data
                session.clear()

                session["customer_id"] = user["customer_id"]
                session["user_email"] = user["email"]
                session["user_name"] = user["name"]
                session["customer_name"] = user["name"]
                session["customer_kind"] = user["kind"]          # 'private' or 'company'
                session["is_company"] = (user["kind"] == "company")

                flash(f"Logged in as {user['name']}.", "success")
                return redirect(url_for("products.product_list"))

    return render_template("login.html", error=error)

@customers_bp.route("/logout")
def logout():
    """
    Clear all user-related session keys and redirect to products page.
    """
    session.pop("user_email", None)
    session.pop("customer_id", None)
    session.pop("user_name", None)
    session.pop("customer_kind", None)
    session.pop("is_company", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@customers_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Profile page:
      - GET: show user data
      - POST: update name, email, address, phone using Validator and CustomerMethods.
    """
    customer_id = session.get("customer_id")
    if not customer_id:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for("customers.login"))

    # load current customer from DB
    user = cm.get_customer_by_id(customer_id)
    if not user:
        flash("Customer not found.", "error")
        return redirect(url_for("products.product_list"))

    error = None
    success = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()

        try:
            # example validation via your Validator class
            name = Validator.validate_name(name)
            email = Validator.validate_email(email)
            address = Validator.validate_address(address)
            phone = Validator.validate_phone(phone)

            ok = cm.update_customer(
                customer_id=customer_id,
                name=name,
                email=email,
                address=address,
                phone=phone,
            )

            if not ok:
                error = "Could not update profile. Please try again."
            else:
                # update session so navbar shows new name/email
                session["user_name"] = name
                session["user_email"] = email
                success = "Profile updated successfully."

                # reload user from DB to show fresh data in the form
                user = cm.get_customer_by_id(customer_id)

        except ValueError as e:
            error = str(e)

    return render_template(
        "profile.html",
        user=user,
        error=error,
        success=success,
    )
