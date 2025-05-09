import random
import palette as p
import helperkit as hk

def main():
    hk.set_theme("DRACULA")
    options = ['Number Guessing', 'Blackjack', 'Dice Roller', 'Exit this :(']

    while True:
        choice = hk.get_input_option("\nWhat do you wanna play?", options)

        if choice == 'Number Guessing':
            computerGuessingGame()
        elif choice == 'Blackjack':
            blackjack()
        elif choice == 'Dice Roller':
            diceRoller()
        elif choice == 'Exit this :(':
            break

    hk.print_message("Aight. Have a nice day!")

def numberGuesserSelect():

    options = ['Try To Guess My Number!', 'Let Me Guess Your Number!']
    hk.print_message("Try to guess my number is a game where the computer picks a secret number, you try to guess it.")
    hk.print_message("The other is where YOU create a secret number, and the computer tries to guess it!\n")
    choice = hk.get_input_option("Which game do you want to play?", options)

    if choice == 'Human Guessing Game':
        humanGuessingGame()
        return
    elif choice == 'Computer Guessing Game':
        computerGuessingGame()
        return

def blackjack():
    """Blackjack"""

    hk.print_message("") # blank message in python already has a \n! (newline)

    playerCards = [random.choice([2,3,4,5,6,7,8,9,10,11]) for _ in range(2)]
    playerTotal = sum(playerCards)

    dealerVisible = random.choice([2,3,4,5,6,7,8,9,10,11])
    dealerHidden = random.choice([2,3,4,5,6,7,8,9,10,11])
    dealerCards = [dealerVisible, dealerHidden]
    dealerTotal = sum(dealerCards)

    if playerTotal > 21 and 11 in playerCards:
        playerTotal -= 10

    while True:
        hk.print_message(f"Your cards: {playerCards} | Total: {sum(playerCards)}\nDealer: {dealerVisible}+?")
        choice = hk.get_input_string("Hit or Stand?")

        if choice.lower() == "hit":
            playerCards.append(random.randint(1, 11))
            playerTotal = sum(playerCards)

            if playerTotal > 21 and 11 in playerCards:
                playerTotal -= 10

            hk.print_message(f"Your cards: {playerCards} | Total: {sum(playerCards)}\nDealer: {dealerVisible}+?")
        
        elif choice.lower() == "stand":
            while dealerTotal < 17:
                card = random.choice([2,3,4,5,6,7,8,9,10,11])
                dealerCards.append(card)
                dealerTotal = sum(dealerCards)
                if dealerTotal > 21 and 11 in dealerCards:
                    dealerTotal -= 10

        if playerTotal > 21:
            hk.warn("You busted! You lost!")
            return
        elif dealerTotal > 21:
            hk.success("Dealer busted! You win.")
            return
        elif playerTotal > dealerTotal:
            hk.success("You have a greater total! You win!")
            return
        elif playerTotal < dealerTotal:
            hk.warn("The dealer has a greater total! You lose!")
            return
        elif playerTotal == dealerTotal:
            hk.info("Bro.. you've TIED!! GGs!")
            return
        
def diceRoller():
    hk.print_message("Rolling the dice...")
    roll = random.randint(1, 6)
    hk.success(f"You rolled a {roll}!")

def humanGuessingGame():

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

def computerGuessingGame():

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

if __name__ == "__main__":
    main()