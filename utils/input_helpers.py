def optional_input(prompt: str) -> str | None:
    value = input(prompt).strip()
    return value or None


def get_int_input(prompt: str) -> int:
    """
    Reads input and converts to int.
    Repeats until input is a valid integer.
    """
    while True:
        value_str = input(prompt).strip()
        try:
            return int(value_str)
        except ValueError:
            print("Value must be a number. Try again.")


def get_optional_int_input(prompt: str) -> int | None:
    """
    Запитує число, але дозволяє порожній ввід:
    - ""  → повертає None (означає 'пропустити')
    - інакше повторює запит, поки користувач не введе коректне число.
    """
    while True:
        value_str = input(prompt).strip()
        if value_str == "":
            return None
        try:
            return int(value_str)
        except ValueError:
            print("Value must be a number or blank to skip. Try again.")


def pause(message: str = "Press ENTER to continue..."):
    input(f"\n{message}")

def get_optional_float_input(prompt: str) -> float | None:
    """
    Питає число з плаваючою комою, але дозволяє пустий ввід.
    Якщо користувач просто натиснув Enter – повертає None.
    Якщо ввів щось некоректне – виводимо повідомлення і теж повертаємо None.
    """
    value_str = input(prompt).strip().replace(",", ".")

    if not value_str:
        # користувач нічого не ввів → пропускаємо поле
        return None

    try:
        return float(value_str)
    except ValueError:
        print("Value must be a number (e.g. 19.99). Skipping this field.")
        return None

def get_float_input(prompt: str) -> float:
    """
    Ask for a floating-point number (e.g. rating or max price).
    Accepts both '3.5' and '3,5'.
    """
    while True:
        value_str = input(prompt).strip().replace(",", ".")
        try:
            return float(value_str)
        except ValueError:
            print("Value must be a number (e.g. 4.5). Try again.")

