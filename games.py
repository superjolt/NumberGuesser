import random
import hashlib
import os

import palette as p
import helperkit as hk

jolt_currency = 0
signed_in = False
current_user = None

def main():
    hk.set_theme("TOKYO_NIGHT")
    setup()
    setup_credentials()

    while True:
        hk.menu(f"What do you wanna play? (Points: {jolt_currency})", games)

def setup():
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()

    global games
    games = {
        'Number Guessing': number_guesser_select,
        'Blackjack': blackjack,
        'Dice Roller': dice_roller,
        'Rock Paper Scissors': rock_paper_scissors,
        'Hangman': hangman,
        'Wordchain': word_chain,
        'Save and exit': save_and_exit
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_credentials():
    global jolt_currency
    choice = hk.get_input_option("Sign in, or sign up?", ["Sign in", "Sign up"] )
    if choice == "Sign up":
        sign_up()
    else:
        sign_in()

    jolt_currency = get_points()


def sign_up():
    global current_user, signed_in
    while True:
        uname = hk.get_input_string("Select your username")
        if user_exists(uname):
            hk.print_message("That username is already taken!")
        else:
            current_user = uname
            break

    pwd = hk.get_input_password("Create your password")
    hashed = hash_password(pwd)

    with open("users.txt","a") as f:
        f.write(f"{current_user}:{hashed}:0\n")

    signed_in = True
    hk.success(f"User {current_user} created and signed in!")


def sign_in():
    global current_user, signed_in
    uname = hk.get_input_string("Enter your username")
    pwd = hk.get_input_password("Enter your password")
    hashed = hash_password(pwd)

    with open("users.txt","r") as f:
        for line in f:
            user, hpwd, pts = line.strip().split(":")
            if user == uname and hpwd == hashed:
                current_user = user
                signed_in = True
                hk.success(f"Logged in as {current_user}")
                return
    hk.print_message("Invalid credentials.")


def user_exists(uname):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt","r") as f:
        for line in f:
            if line.startswith(uname + ":"):
                return True
    return False


def get_points():
    global current_user, signed_in
    if not signed_in:
        return 0
    with open("users.txt","r") as f:
        for line in f:
            user, _, pts = line.strip().split(":")
            if user == current_user:
                return int(pts)
    return 0


def set_points(value):
    global current_user, signed_in, jolt_currency
    if not signed_in:
        hk.print_message("Sign in first.")
        return

    lines = []
    with open("users.txt","r") as f:
        for line in f:
            user, hpwd, pts = line.strip().split(":")
            if user == current_user:
                lines.append(f"{user}:{hpwd}:{value}\n")
            else:
                lines.append(line)

    with open("users.txt","w") as f:
        f.writelines(lines)

    jolt_currency = value

def update_currency_on_result(result):
    global jolt_currency
    if result == "win":
        jolt_currency += 1
        hk.success("You earned 1 point!")
    elif result == "lose":
        jolt_currency -= 1
        hk.error("You lost 1 point!")
    set_points(jolt_currency)

# === Game functions ===
def number_guesser_select():
    opts = ['Try To Guess My Number!', 'Let Me Guess Your Number!']
    hk.print_message("Try to guess my number is a game where the computer picks a secret number, you try to guess it.")
    hk.print_message("The other is where YOU create a secret number, and the computer tries to guess it!\n")
    choice = hk.get_input_option("Which game do you want to play?", opts)
    if choice == opts[0]:
        human_guessing_game()
    else:
        computer_guessing_game()

def human_guessing_game():
    hk.print_message("Welcome to the Human Guessing Game! Try to guess the secret number chosen by the computer.")

    secretNumber = random.randint(1, 100)  # New secret number every game
    guess = None
    guessesTaken = 0

    while True:
        guess = hk.get_input_number("Enter your guess", num_type=int)

        if guess > secretNumber:
            hk.warn("Too big!")
        elif guess < secretNumber:
            hk.warn("Too small!")
        else:
            hk.success(f"Yay! You won in {guessesTaken} guesses!")
            break
        
        guessesTaken += 1

def computer_guessing_game():
    hk.print_message("Welcome to the Computer Guessing Game! Think of a number, and the computer will try to guess it.")

    guess = None
    guessesTaken = 0
    high = 100
    low = 1

    while True:

        guess = (low + high) // 2
        
        options = ["<", ">", "="]
        msg = f"Compared to your secret number, what is {guess}?"
        choice = hk.get_input_option(msg, options)

        if choice == "=":
            hk.success(f"Yay! I found your number! In {guessesTaken} guesses!")
            break
        
        elif choice == ">": # we guessed too small
            low = guess # so we raise the bar
        
        elif choice == "<": # we guessed too big
            high = guess # so we lower the bar
        
        guessesTaken +=1

def blackjack():
    hk.print_message("Welcome to Blackjack! Try to get as close to 21 as possible without going over.")

    player = [random.choice([2,3,4,5,6,7,8,9,10,11]) for _ in range(2)]
    dealer = [random.choice([2,3,4,5,6,7,8,9,10,11]) for _ in range(2)]

    def adjust_hand(hand):
        total = sum(hand)
        if total > 21 and 11 in hand:
            total -= 10
        return total

    while True:
        p_tot = adjust_hand(player)
        d_vis = dealer[0]
        hk.print_message(f"Your cards: {player} | Total: {p_tot}\nDealer: {d_vis}+?")
        choice = hk.get_input_string("Hit or Stand?")
        if choice.lower() == "hit":
            player.append(random.choice([2,3,4,5,6,7,8,9,10,11]))
        else:
            while adjust_hand(dealer) < 17:
                dealer.append(random.choice([2,3,4,5,6,7,8,9,10,11]))

        p_tot = adjust_hand(player)
        d_tot = adjust_hand(dealer)

        if p_tot > 21:
            hk.warn("You busted! You lost!")
            update_currency_on_result("lose")
            return
        if d_tot > 21:
            hk.success("Dealer busted! You win.")
            update_currency_on_result("win")
            return
        if p_tot > d_tot:
            hk.success("You have a greater total! You win!")
            update_currency_on_result("win")
            return
        if p_tot < d_tot:
            hk.warn("The dealer has a greater total! You lose!")
            update_currency_on_result("lose")
            return
        hk.info("Bro.. you've TIED!! GGs!")
        return


def dice_roller():
    hk.print_message("Welcome to Dice Roller! Roll the dice and see what number you get.")
    roll = random.randint(1,6)
    hk.success(f"You rolled a {roll}!")
    update_currency_on_result("win" if roll >=4 else "lose")


def rock_paper_scissors():
    hk.print_message("Welcome to Rock Paper Scissors! Choose rock, paper, or scissors.")
    wins = {'win':0,'lose':0}
    rounds = hk.get_input_number("How many times?", int)
    for _ in range(rounds):
        comp = random.choice(["rock","paper","scissors"])
        usr = hk.get_input_string("Rock, Paper, or Scissors?")
        if usr == comp:
            hk.note("Tie!")
        elif (usr,comp) in [("rock","scissors"),("scissors","paper"),("paper","rock")]:
            hk.success("You won!")
            update_currency_on_result("win")
        else:
            hk.error("You lose!")
            update_currency_on_result("lose")
        hk.print_message(f"Score - You: {wins['win']} | Dealer: {wins['lose']}")


def hangman():
    hk.print_message("Welcome to Hangman!")
    words = []
    with open('/usr/share/dict/words') as f:
        for w in f:
            w=w.strip()
            if w.isalpha() and 3<=len(w)<=8:
                words.append(w.lower())
    secret = random.choice(words)
    visible = ['_']*len(secret)
    attempts = len(secret)+3
    while attempts>0 and '_' in visible:
        hk.print_message(f"Word: {''.join(visible)}")
        guess = hk.get_input_string("Guess a letter", max_len=1).lower()
        for i,ch in enumerate(secret):
            if ch==guess: visible[i]=guess
        attempts-=1
    if '_' not in visible:
        hk.success("You guessed it! GGs!")
        update_currency_on_result("win")
    else:
        hk.error(f"Out of attempts! The word was: {secret}")
        update_currency_on_result("lose")


def word_chain():
    hk.print_message("Welcome to Word Chain!")
    words = []
    with open('/usr/share/dict/words') as f:
        for w in f:
            w=w.strip()
            if w.isalpha() and 3<=len(w)<=8:
                words.append(w.lower())
    last = random.choice(words)
    hk.print_message(f"Starting word: {last}")
    while True:
        nxt = hk.get_input_string(f"Give a word that starts with '{last[-1]}'")
        if nxt[0].lower()==last[-1]: last=nxt.lower()
        else: hk.print_message(f"Invalid! Must start with '{last[-1]}'")


def save_and_exit():
    global current_user, jolt_currency
    if not signed_in:
        hk.print_message("No user signed in. Nothing to save.")
        exit()
    lines=[]
    with open("users.txt") as f:
        for line in f:
            user,hpwd,pts=line.strip().split(":")
            if user==current_user:
                lines.append(f"{user}:{hpwd}:{jolt_currency}\n")
            else:
                lines.append(line)
    with open("users.txt","w") as f:
        f.writelines(lines)
    hk.success(f"Saved {jolt_currency} points for {current_user}. Bye!")
    exit()

if __name__ == "__main__":
    main()
