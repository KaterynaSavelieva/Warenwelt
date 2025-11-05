import sys
sys.tracebacklimit = 0

from kunde import Kunde
from privatkunde import Privatkunde
from firmenkunde import Firmenkunde

def make_and_print(label, factory):
    #Створити об'єкт і красивенько його показати, або вивести причину помилки.
    try:
        obj = factory()
        print(obj)
    except Exception as e:
        print(f"{label}: {e}")

print("test")

make_and_print("k1", lambda: Kunde(
    "Anna Schmidt", "Hauptstraße 5", "anna@mail.at", "+436601234567", "StrongPass1"
))
make_and_print("p1", lambda: Privatkunde(
    "Lena", "Ring 2", "lena@mail.at", "+43660111222", "Passwort9", "1990-05-20"
))
make_and_print("f1", lambda: Firmenkunde(
    "ACME GmbH", "Industriestr. 10", "info@acme.at", "+43720123456", "Secret12", "123456789"
))

# — свідомо поганий кейс — тут буде зрозуміла помилка, але тест не зупиниться
make_and_print("f2", lambda: Firmenkunde(
    "ACME GmbH", "Industriestr. 10", "info@acme.at", "+43720123456", "Secret12", "$$$$$$$"
))

# наступні теж виконаються
make_and_print("k2", lambda: Kunde(
    "Anna Schmidt", "Hauptstraße 5", "annamail.at", "+436601234567", "StrongPass1"
))
make_and_print("p2", lambda: Privatkunde(
    "Lena", "Ring 2", "lena@mail.at", "+43662222w0111222", "Passwort9", "1990-05-20"
))
