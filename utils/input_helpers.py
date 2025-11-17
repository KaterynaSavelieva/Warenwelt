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
