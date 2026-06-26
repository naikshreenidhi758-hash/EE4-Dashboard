import time
import os

def clear_screen():
    # Clears the terminal screen for a clean animation feel
    os.system('cls' if os.name == 'nt' else 'clear')

def birthday_wish():
    name = input("NEELA Heart")
    clear_screen()
    
    # Simple candle lighting animation
    print("Preparing your surprise...")
    time.sleep(1)
    clear_screen()

    print(f"""
       |||||||||||||
      {|  H-A-P-P-Y  |}
     @@{| B-I-R-T-H |}@@
    @@@@{|   D-A-Y   |}@@@@
   @@@@@@{|   {name.upper().center(5)}   |}@@@@@@
  @@@@@@@@============@@@@@@@@
    """)
    
    # Animated typing effect for the message
    message = f"\n🎉 Wishing you a fantastic year ahead, {name}! May all your dreams come true! 🎂✨\n"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)

if __name__ == "__main__":
    birthday_wish()
