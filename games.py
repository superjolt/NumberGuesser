import random
import palette as p
import helperkit as hk

def main():
    hk.set_theme("TOKYO_NIGHT")
    options = ['Number Guessing', 'Blackjack', 'Dice Roller', 'Rock Paper Scissors', 'Hangman', 'Exit this :(']

    while True:
        choice = hk.get_input_option("\nWhat do you wanna play?", options)

        if choice == 'Number Guessing':
            numberGuesserSelect()
        elif choice == 'Blackjack':
            blackjack()
        elif choice == 'Dice Roller':
            diceRoller()
        elif choice == 'Rock Paper Scissors':
            rockPaperScissors()
        elif choice == 'Hangman':
            hangman()
        elif choice == 'Exit this :(':
            break

    hk.print_message("Aight. Have a nice day!")

def numberGuesserSelect():

    options = ['Try To Guess My Number!', 'Let Me Guess Your Number!']
    hk.print_message("Try to guess my number is a game where the computer picks a secret number, you try to guess it.")
    hk.print_message("The other is where YOU create a secret number, and the computer tries to guess it!\n")
    choice = hk.get_input_option("Which game do you want to play?", options)

    if choice == 'Try To Guess My Number!':
        humanGuessingGame()
        return
    elif choice == 'Let Me Guess Your Number!':
        computerGuessingGame()
        return

def blackjack():

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

def rockPaperScissors():
    
    computerWin = 0
    playerWin = 0

    gameLength = hk.get_input_number("How many times do you wanna play?", int) # You can only iterate over an int 
    
    for i in range(gameLength):
        myChoice = random.choice(["rock", "paper", "scissors"])
        input = hk.get_input_string("Rock, Paper, or Scissors?")

        hk.print_message(f"You picked {input}, and I picked {myChoice}.")

        if input == "rock" and myChoice == "paper":
            hk.error("You lose! I win!")
            computerWin += 1

        elif input == "paper" and myChoice == "scissors":
            hk.error("You lose! I win!")
            computerWin += 1

        elif input == "scissors" and myChoice == "rock":
            hk.error("You lose! I win!")
            computerWin += 1

        elif input == myChoice:
            hk.note("We tied!")

        else:
            hk.success("You won! I lost!")
            playerWin += 1

        hk.print_message(f"You vs Computer: {playerWin} | {computerWin}")

def hangman():
    
    words = []

    # cool check, basically takes words that dont have special chars and have a length from 3 to 8, and makes it lower case
    
    with open('/usr/share/dict/words', 'r') as f:
        for word in f:
            word = word.strip()
            if word.isalpha() and 3 <= len(word) <= 8:
                words.append(word)
    
    secretWord = random.choice(words).lower()

    visibleWord = "_" * len(secretWord) # fill it up
    
    while visibleWord != secretWord:

        hk.print_message(f"Word: {visibleWord}")
        guess = hk.get_input_string("Guess a letter", max_len=1) # we only accept letters

        guess.lower()

        visibleList = list(visibleWord) # make it a list

        for i in range(len(secretWord)): # is that guess right
            if secretWord[i] == guess:
                print("You guessed a letter!")
                visibleList[i] = guess

        visibleWord = "".join(visibleList) # make it a string again

    hk.success("\nYou guessed the word!\nGGs!\n")

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