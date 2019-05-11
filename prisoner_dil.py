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


def calculate_payoffs(wfn_array, r, t, s, p):
    for i in range(len(wfn_array)):
        curr = (np.absolute(wfn_array[i]))**2
        wfn_array[i] = np.around(curr, 5)
    player_1 = r * wfn_array[0] + t * wfn_array[1] + s * wfn_array[2] + p * wfn_array[3]
    player_2 = r * wfn_array[0] + s * wfn_array[1] + t * wfn_array[2] + p * wfn_array[3]
    return (player_1, player_2)

def normal_payoff_calc(p1, p2, r, t, s, p):
    if p1 == p2 == 0:
        player_1, player_2 = r, r

    elif p1 == p2 == 1:
        player_1, player_2 = p, p

    elif p1 == 0:
        player_1, player_2 = s, t

    elif p1 == 1:
        player_1, player_2 =  t, s  
    else:
        print("Error")

    return (player_1, player_2)


def cooperate():
    theta = 0
    phi = 0
    return theta, phi

def defect():
    theta = pi
    phi = 0
    return theta, phi

def magicQ():
    theta = 0
    phi = pi/2
    return theta, phi

def print_game(r, t, s, p, initial = False):
    if initial:
        print(
            "\n\n\n=========================================================================================================",
            "\n\nQuantum Prisoner's Dilemma\n\n"
            "========================================================================================================="
            "\n             C                             D                               \n",
            "C         (r,r)                        (s,t)                               \n",
            "D         (t,s)                        (p,p)                               \n",
        )
    else:
        print(
            "\n\n           C                             D                             \n",
            "C         (%s,%s)                        (%s,%s)                         \n" % (r,r,s,t),
            "D         (%s,%s)                        (%s,%s)                         \n\n" % (t,s, p, p),
        )



if __name__ == '__main__':
    r = 3.0
    t = 5.0
    s = 0.0
    p = 1.0

    print_game(r,t,s,p,initial = True)

    default = input("Play default? (y/n) = ")
    
    if default != "y":
        r = float(input("Please enter the reward value r = "))
        t = float(input("Please enter the temptation value t = "))
        s = float(input("Please enter the sucker value s = "))
        p = float(input("Please enter the punishment value p = "))
    print_game(r,t,s,p)

    qc = get_qc('2q-qvm')
    prog = Program()

    # Level of entanglement 
    y = pi/3

    if default != "y":
        temp = float(input("\nEnter number y and the level of entanglement will be pi/y \n(if y = 0, entanglement will be 0) y = "))
        if temp == 0.0 : y = 0
        else: y = pi/temp
    print("\nEntanglement Level is gamma = ", y, "\n\n")

    # Player 1
    theta_1 = 0
    phi_1 = pi/2

    theta_1, phi_1 = magicQ()

    # Player 2
    theta_2 =  pi
    phi_2 = pi/2

    theta_2, phi_2 = defect()




    if default != "y":
        temp = int(input("phi_1 = pi/"))
        if temp == 0: phi_1 = 0
        else: phi_1 = pi / temp

        temp = int(input("theta_1 = pi/"))
        if temp == 0: theta_1 = 0
        else: theta_1 = pi / temp

        temp = int(input("phi_2 = pi/"))
        if temp == 0: phi_2 = 0
        else: phi_2 = pi / temp

        temp = int(input("theta_2 = pi/"))
        if temp == 0: theta_2  = 0
        else: theta_2  = pi / temp


    wfn = WavefunctionSimulator().wavefunction(prog)
    print("\nInitial Wavefunction in |CC> =  ", wfn)

    if default != 'y': input("\nApply J?")
    else: print("\nApply J")
    
    # j matrix
    j = j_gate_matrix(y)
    j_def = DefGate("J",j)
    J = j_def.get_constructor()
    prog += j_def
    prog += J(0,1)

    print("Wavefunction: ", WavefunctionSimulator().wavefunction(prog))
    if default != 'y': input("\nApply U_A x U_B?")
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
    if default != 'y': input("\nApply J conjugate transpose?")
    else: print("\nApply J conjugate transpose")

    # j conj transose matrix
    jct = np.matrix.getH(j)
    jct_def = DefGate("JT",jct)
    JT = jct_def.get_constructor()
    prog += jct_def
    prog += JT(0,1)

    wfn = WavefunctionSimulator().wavefunction(prog)
    print("Final Wavefunction: ", wfn)
    wfn_array = wfn.probabilities()
    payoffs = calculate_payoffs(wfn_array,r,t,s,p)
    print("\nPayoffs\n------------------\nPlayer 1: ", payoffs[0], "\nPlayer 2: ",  payoffs[1])

    trials = int(input("\n\nHow many times play game? trials = "))
    result = qc.run_and_measure(prog, trials = trials)
    for i in range(trials):
        p1 = result[0][i]
        p2 = result[1][i]
        payoffs = normal_payoff_calc(p1,p2,r,t,s,p)
        print("\nGame", i + 1)
        print("\tPlayer 1 : ",p1, " payoff :", payoffs[0])
        print("\tPlayer 2 : ",p2, " payoff :",  payoffs[1])

    print("\n\n", result)




