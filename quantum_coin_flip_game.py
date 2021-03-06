# ============================= 
# Quantum Coin Flip
# ============================= 

from pyquil import Program, get_qc 
from pyquil.gates import H, X
from pyquil.api import WavefunctionSimulator
import time
import random
from random_num_gen import random_bit

def game_rules():
    print(
        "\n\nQuantum Coin Flip!\n\n"
        "A qubit represents the quantum coin, initially at HEADS (superposition |0>)\n"
        "First the quantum computer can flip the coin by applying a gate\n"
        "Second you can decide to either flip the coin or not\n"
        "Third the quantum computer can flip the coin by applying a gate\n"
        "Then we measure the qubit, and if we measure HEADS (|0>) then the computer wins\n"
        "If we measure TAILS (|1>) then we win!\n\n"
    )

def classic_flip(coin, flip, view):
    if flip == 1:
        if view: print("Flip")
        coin = coin + 1 % 2
    return coin

def classic_coin_flip(your_move = False, view = True):
    coin = 0
    # Cpu moves 
    coin = classic_flip(coin, random.randrange(0,2,1), view) # pseudo ranom int 0 or 1 
    # You move
    if your_move: 
        coin = classic_flip(coin, int(input("Flip = ")), view)
    else:
        coin = classic_flip(coin, random.randrange(0,2,1), view) # pseudo ranom int 0 or 1 
    # Cpu moves 
    coin = classic_flip(coin, random.randrange(0,2,1), view) # pseudo ranom int 0 or 1 
    return coin 

def classic_coin_flip_game(n = 1, your_move = False, view = True):
    print("Flip  == 1; Not flip == 0.\n")
    cpu_wins, you_wins = 0, 0 
    for i in range(n):
        coin = classic_coin_flip(your_move, view)
        if coin == 0:
            print("Computer Wins!\n")
            cpu_wins += 1
        else:
            print("You Win!\n")
            you_wins += 1
    print("\nYour wins:", you_wins, "Computer wins", cpu_wins)
    



def q_cpu_move(p, view = False, t = False, randy = False):
    p += H(0) 
    if view: 
        print("Quantum Computer Move: H")
        print_prog(p)
    elif not randy: 
        print("Quantum Computer Moves")
    if t: time.sleep(1)
    
    return p




def your_move(p, view = True, t = False):
    flip = input("\nYour Move - flip? (y/n)")
    if flip == "y":
        print("Flip Coin")
        p += X(0)
    else:
        print("...")
    if t: time.sleep(1)
    if view: print_prog(p)
    if t: time.sleep(1)
    
    return p

def random_move(p, view = False, t = False):
    flip = random.randrange(0,2,1) # pseudo ranom int 0 or 1 
    if flip == 1:
        print("Flip Coin")
        p += X(0)
    else:
        print("...")
    if t: time.sleep(1)
    if view: print_prog(p)
    if t: time.sleep(1)
    
    return p

def random_game():
    # Get Quantum Computer qc with 1 qubit
    qc = get_qc('1q-qvm')

    # Initialize Program
    p = Program()
    # 1. qc moves
    p = q_cpu_move(p, False, False, True)

    # 2. you have the option to flip or not
    p = random_move(p, False, False)
 
    # 3. qc moves again 
    p = q_cpu_move(p, False, False, True)
    result = qc.run_and_measure(p, trials = 1)
    r = result[0][0]
    return r

def print_prog(p):
    print("The program is:", p)
    wfn = WavefunctionSimulator().wavefunction(p)
    print("The wave function is:", wfn)


if __name__ == '__main__':
    game_rules()
    t = False
    start = input("Ready to play?(c = classic) ")
    view = input("View Everything (y/n)")
    if view == "y":view = True
    else: view = False
    if start ==  "c":
        print("\n\nClassical Game\n")
        classic = int(input("How many classical games? n = "))
        classic_coin_flip_game(classic, True, view)

    else:
        # Get Quantum Computer qc with 1 qubit
        print("\n\nQuantum Game\n")

        randy = input("Play random game? (y/n) ")
        if randy == "y":
            trials = int(input("How many rounds? "))
            for i in range(trials):
                r = random_game()
                if r == 0: print("Round ", i, " : Quantum Computer Wins!\n")
                else: print("Round ", i, " : You win!\n")
        qc = get_qc('1q-qvm')

        # Initialize Program
        p = Program()

        # 1. qc moves
        p = q_cpu_move(p, view, t)

        # 2. you have the option to flip or not
        p = your_move(p, view, t)
    
        # 3. qc moves again 
        p = q_cpu_move(p, view, t)


        # Print Results
        result = qc.run_and_measure(p, trials = 1)
        r = result[0][0]

        if t: time.sleep(1)

        print("\n\nMeasure:", r)

        if r == 0: 
            print("HEADS")
            print("\nQuantum Computer Wins!\n")
        elif r == 1: 
            print("TAILS")
            print("\nYou Win!\n")
        else:
            print("\n\nError", r)
    
   

    