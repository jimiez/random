"""
Just silly little rock, paper, scissors game

-JPM 2020

"""

# Required modules
import random, time

# Let's initialize some variables, most pretty self explanatory
rounds = 0
wins = 0
playerChoices = []
computerChoices = []
winStats = [] # -1 computer wins, 0 tie, 1 player wins
aiRandomness = 5 # percentage chance that AI plays a completely random hand any given round
print_debug = False

# Let's do some color magic! Assign a color for each of the main choices, then assign them to numeric choices

normal_color = "\033[m" # reset terminal to the default color
t_rock = "\033[31m" + "Rock" + normal_color # Red Text, Rock
t_paper = "\033[32m" + "Paper" + normal_color # Green Text, Paper
t_scissors = "\033[34m" + "Scissors" + normal_color # Blue Text, Scissors

choiceToText = {1: t_rock, 
                2: t_paper, 
                3: t_scissors, 
                99: "Exit"}

# Make sure input is valid, reject both non-integer values and outside legal selections
def validateInput(playerInput):
    try:
        int(playerInput)
    except ValueError:
        return False

    if int(playerInput) in choiceToText.keys():
        return True
    else:
        return False
        
# Simple AI routine for the computer that looks at previous choices made by the player and tries to come up with a winning strategy
# Therefore, this is the best way to win at rock-paper-scissors: if you lose the first round, switch to the thing that beats the thing your opponent just played. 
# If you win, don't keep playing the same thing, but instead switch to the thing that would beat the thing that you just played. In other words, play the hand your losing opponent just played. 
# To wit: you win a round with rock against someone else's scissors. They are about to switch to paper. You should switch to scissors. Got it? Good.

def computerLogic():
    
    #First round, start random
    if rounds < 1:
        return random.randint(1,3)
       
    # A set probability that the AI plays a completely random hand in subsequent rounds
    if random.randint(1,100) < aiRandomness:
         return random.randint(1,3)
         
    # MAIN LOGIC
    # if computer lost previous round, play the winning action of previous round. People are much more likely to keep using a winning tactic.
    if winStats[-1] == 1:
        computerChoice = oppositeChoice(playerChoices[-1])
    # if computer won the previous round, switch to what wins what it played in the previous round
    elif winStats[-1] == -1:
        computerChoice = oppositeChoice(computerChoices[-1])
    # if last round was a draw, play a random hand
    else:
        computerChoice = random.randint(1,3)   
    return computerChoice

# Returns the option that WINS the chosen action
def oppositeChoice(choice):
    if choice == 1:
        return 2
    elif choice == 2:
        return 3
    elif choice == 3:
        return 1
    else: 
        return 000        
        
# Main game action
def playRound(playerChoice):
    
    # Resolve computer's choice 
    computerChoice = computerLogic()
    
    # Add the latest choices to action history
    playerChoices.append(playerChoice)
    computerChoices.append(computerChoice)
    
    #print("Player chose {} and the computer chose {}.".format(choiceToText[playerChoice], choiceToText[computerChoice]))    
    print("Player chose {}".format(choiceToText[playerChoice]))
    time.sleep(1)
    print("The computer chose {}".format(choiceToText[computerChoice]))
    time.sleep(1)

    if playerChoice == computerChoice:
        return 0    
    elif playerChoice == 3 and computerChoice == 2:
        return 1
    elif playerChoice == 2 and computerChoice == 1:
        return 1        
    elif playerChoice == 1 and computerChoice == 3:
        return 1
    else:
        return -1    
        
# Main game loop
while True:
    
    # To start off, we assume that input is NOT valid until proven otherwise
    inputOk = False
    
    print("Rock, paper, scissors! Rounds won: {}/{}".format(wins, rounds))
    print("Select (1) " + t_rock + ", (2) " + t_paper + ", (3) " + t_scissors + ". (99) to quit")
    
    # Let's take player input here and make sure it's valid
    while True:
        playerChoice = input()        
        if not validateInput(playerChoice):
            print("Please enter valid input")
        else:
            playerChoice = int(playerChoice)
            break
    
    # Shutdown
    if playerChoice == 99:
        print("Game shutting down, bye!")
        break

    # Play the actual round    
    result = playRound(playerChoice)
    
    # Announce the results... 
    if result == 0:
        print("Tie!")
    elif result > 0:
        print("Player wins!")
        wins += 1
    else:
        print("Player lost!")
        
    # and do the necessary bookkeeping
    winStats.append(result)
    rounds += 1
    time.sleep(1)
    print("")


if(print_debug):
# Debug stuff
    print(winStats)
    print(playerChoices)
    print(computerChoices)