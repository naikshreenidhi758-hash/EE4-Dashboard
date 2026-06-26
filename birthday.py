import time
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def type_text(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

def birthday_wish():
    name = input("NEELA ")

    clear_screen()

    print("🎁 Preparing your birthday surprise...")
    time.sleep(2)
    clear_screen()

    cake = f"""
              🕯️   🕯️   🕯️
             ─────────────
            |   HAPPY    |
            |  BIRTHDAY  |
            |   {name.upper():^10} |
            |____________|
           /##############\\
          /################\\
         |##################|
         |##################|
         |__________________|
    """

    print(cake)

    message = (
        f"\n🎉 Happy Birthday, {name}! 🎉\n"
        "🎂 May your day be filled with happiness,\n"
        "💖 laughter, love, and unforgettable memories.\n"
        "🌟 Wishing you success, good health,\n"
        "and endless joy in the year ahead!\n\n"
        "🎁 Have a fantastic birthday! 🎈🎊\n"
    )

    type_text(message)

if __name__ == "__main__":
    birthday_wish()
