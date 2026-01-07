from colorama import Fore, Style, init
from textblob import TextBlob

init(autoreset = True)

print(f"{Fore.CYAN} Welcome to RRTD P or N!")

name= input(f"{Fore.MAGENTA} Enter your name: ").strip() or "Friend"
print(f"{Fore.CYAN} Hello, Agent {name}!")
print(f"Type a sentense to analize P or N or type {Fore.YELLOW}'exit'{Fore.CYAN} to quit.\n")

def detect_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.25:
        return "Posetive", Fore.GREEN
    elif polarity > -0.25:
        return "Negative", Fore.RED
    return "Neutral", Fore.YELLOW

while True:
    user_input = input(f"{Fore.GREEN}>>  ").strip()

    if not user_input:
        print(f"{Fore.RED} Please enter some text.")
        continue

    if user_input.lower() == "exit":
        print(f"{Fore.BLUE} Exiting RRTD P or N. Goodbye {name}!")
        break
    
    sentiment, color = detect_sentiment(user_input)
    polarity = TextBlob(user_input).sentiment.polarity


    print(f"{color}{sentiment} Sentiment detected (Polarity = {polarity : .2f})")