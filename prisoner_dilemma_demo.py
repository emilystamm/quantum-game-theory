# Prisoner's Dilemma
# A classic strategy game is the prisoner’s dilemma where two prisoners get the minimal penalty if they collaborate and stay silent, get zero penalty if one of them defects and the other collaborates (incurring maximum penalty) and get intermediate penalty if they both defect. This game has an equilibrium where both defect and incur intermediate penalty.
# However, things change dramatically when we allow for quantum strategies leading to the Quantum Prisoner’s Dilemma.
# Can you design a program that simulates this game?
from pyquil import *
from pyquil.gates import *
from pyquil.api import *
import numpy as np
import math
from pyquil.quil import DefGate
from numpy import cos, sin, pi
from math import e


def u_gate_matrix(phi, theta):
   u_matrix = np.array([
   [e**(complex(0,1)*phi)*cos(theta/2), sin(theta/2)],
      [sin(theta/2)*-1, e**(complex(0,-1)*phi)*cos(theta/2)]
   ])
   return u_matrix


# y = gamma
def j_gate_matrix(y):
   j_matrix = np.array([
      [cos(y/2), 0, 0, complex(0,sin(y/2))],
      [0, cos(y/2), complex(0,-sin(y/2)), 0],
      [0, complex(0,-sin(y/2)), cos(y/2), 0],
      [complex(0,sin(y/2)), 0, 0, cos(y/2)]
      ])
   return j_matrix


def calculate_payoffs(wfn_array, game):
   for i in range(len(wfn_array)):
      curr = wfn_array[i]
      wfn_array[i] = np.around(curr, 5)
   player_1 = game[0][0][0] * wfn_array[0] + game[0][1][0] * wfn_array[1] + game[1][0][0] * wfn_array[2] + game[1][1][0] * wfn_array[3]
   player_2 = game[0][0][1] * wfn_array[0] + game[0][1][1] * wfn_array[1] + game[1][0][1] * wfn_array[2] + game[1][1][1] * wfn_array[3]
   return (player_1, player_2)

def normal_payoff_calc(p1, p2, game):
   return game[p1][p2]


def deny():
   theta = 0
   phi = 0
   return theta, phi

def confess():
   theta = pi
   phi = 0
   return theta, phi

def magicQ():
   theta = 0
   phi = pi/2
   return theta, phi

def magicM():
   theta = pi/2
   phi = pi/2
   return theta, phi


def print_pd():
   print(
      "\n\n\n=========================================================================================================",
      "\n\nQuantum Prisoner's Dilemma\n\n"
      "========================================================================================================="
      "\n\t\t\tDeny\t\t\tConfess\n",
      "Deny\t\t\t(r,r)\t\t\t(s,t)\n",
      "Confess\t\t(t,s)\t\t\t(p,p)\n",
   )



def print_game(game):
   print(
   "\n\n\t\t\tDeny\t\t\tConfess\n",
   "Deny\t\t\t(%s,%s)\t\t(%s,%s)\n" % (game[0][0][0],game[0][0][1],game[0][1][0],game[0][1][1]),
   "Confess\t\t(%s,%s)\t\t(%s,%s)\n\n" % (game[1][0][0],game[1][0][1],game[1][1][0],game[1][1][1]),
   )




if __name__ == '__main__':
    t = -1.0
    r = -3.0
    p = -10.0
    s = -25.0

    print_pd()

    default = input("Play default? (y/n) = ")

    if default == "n":
        payoffs = input("Use default payoffs? (y/n) = ")
        if payoffs == "n":
            t = float(input("Please enter the temptation value t = "))
            r = float(input("Please enter the reward value r = "))
            p = float(input("Please enter the punishment value p = "))
            s = float(input("Please enter the sucker value s = "))


    game = [
    [(r,r), (s,t)],
    [(t,s), (p,p)]
    ] 

    print_game(game)

    qc = get_qc('2q-qvm')
    prog = Program()

    # Level of entanglement 
    y = pi/2

    if default == "n":
        temp = float(input("\nEnter number y and the level of entanglement will be pi/y \n(if y = 0, entanglement will be 0) y = "))
        if temp == 0.0 : y = 0
        else: y = pi/temp
    print("\nEntanglement Level is gamma = ", y, "\n\n")

    # Player 1
    theta_1 = 0
    phi_1 = pi/4

    # Player 2
    theta_2 = 0
    phi_2 = pi/2



    if default != "y":
        choice = input("Mighty Joe : (D)eny, (C)onfess, Magic(Q) or (O)ther? ").strip()
        if choice == "D" or choice == "Deny":
            theta_1, phi_1 = deny()
        if choice == "C" or choice == "Confess":
            theta_1, phi_1 = confess()
        if choice == "Q" or choice == "MagicQ":
            theta_1, phi_1 = magicQ()
        if choice == "O" or choice == "Other":
            temp = int(input("phi_1 = pi/"))
            if temp == 0: phi_1 = 0
            else: phi_1 = pi / temp

            temp = int(input("theta_1 = pi/"))
            if temp == 0: theta_1 = 0
            else: theta_1 = pi / temp
    
        choice = input("Mighty Joe : (D)eny, (C)onfess, Magic(Q) or (O)ther? ").strip()
        if choice == "D" or choice == "Deny":
            theta_2, phi_2 = deny()
        if choice == "C" or choice == "Confess":
            theta_2, phi_2 = confess()
        if choice == "Q" or choice == "MagicQ":
            theta_2, phi_2 = magicQ()
        if choice == "O" or choice == "Other":
            temp = int(input("phi_2 = pi/"))
            if temp == 0: phi_2 = 0
            else: phi_2 = pi / temp

            temp = int(input("theta_2 = pi/"))
            if temp == 0: theta_2  = 0
            else: theta_2  = pi / temp


    wfn = WavefunctionSimulator().wavefunction(prog)
    print("\nInitial Wavefunction in |DenyDeny> =  ", wfn)

    if default == 'n': input("\nApply J?")
    else: print("\nApply J")

    # j matrix
    j = j_gate_matrix(y)
    j_def = DefGate("J",j)
    J = j_def.get_constructor()
    prog += j_def
    prog += J(0,1)

    print("Wavefunction: ", WavefunctionSimulator().wavefunction(prog))
    if default == 'n2': input("\nApply U_A x U_B?")
    else: print("\nApply U_A x U_B")


    # U matrices 
    u1 = u_gate_matrix(phi_1,theta_1)
    u2 = u_gate_matrix(phi_2,theta_2)
    u = np.kron(u1, u2)
    u_def = DefGate("U", u)
    U = u_def.get_constructor()
    prog += u_def
    prog += U(0,1)

    print("Wavefunction: ", WavefunctionSimulator().wavefunction(prog))
    if default == 'n': input("\nApply J conjugate transpose?")
    else: print("\nApply J conjugate transpose")

    # j conj transose matrix
    jct = np.matrix.getH(j)
    jct_def = DefGate("JCT",jct)
    JCT = jct_def.get_constructor()
    prog += jct_def
    prog += JCT(0,1)

    wfn = WavefunctionSimulator().wavefunction(prog)
    print("Final Wavefunction: ", wfn)
    wfn_array = wfn.probabilities()
    payoffs = calculate_payoffs(wfn_array,game)
    print("\nAverage Payoffs\n------------------\nCrazy Crow : ", -1 * payoffs[0], " years\nMighty Joe : ", -1 * payoffs[1], " years")

    trials = int(input("\n\nHow many times play game? trials = "))
    result = qc.run_and_measure(prog, trials = trials)
    for i in range(trials):
        p1 = result[0][i]
        p2 = result[1][i]
        payoffs = normal_payoff_calc(p1,p2,game)
        print("\nGame", i + 1)
        print("\tCrazy Crow:\t",p1, "\tpayoff :", -1 * payoffs[0], " years")
        print("\tMighty Joe:\t",p2, "\tpayoff :",  -1 * payoffs[1], " years")

    print("\n\n", result)


