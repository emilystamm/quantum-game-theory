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

def magicM():
   theta = pi/2
   phi = pi/2
   return theta, phi


def print_pd():
   print(
      "\n\n\n=========================================================================================================",
      "\n\nQuantum Prisoner's Dilemma\n\n"
      "========================================================================================================="
      "\n             C                             D                               \n",
      "C         (r,r)                        (s,t)                               \n",
      "D         (t,s)                        (p,p)                               \n",
   )



def print_game(game):
   print(
   "\n\n           C                             D                             \n",
   "C         (%s,%s)                        (%s,%s)                         \n" % (game[0][0][0],game[0][0][1],game[0][1][0],game[0][1][1]),
   "D         (%s,%s)                        (%s,%s)                         \n\n" % (game[1][0][0],game[1][0][1],game[1][1][0],game[1][1][1]),
   )




if __name__ == '__main__':
   t = 5.0
   r = 3.0
   p = 1.0
   s = 0.0

   print_pd()

   default = input("Play default? (y/n) = ")
   
   if default != "y":
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

   if default != "y":
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
   payoffs = calculate_payoffs(wfn_array,game)
   print("\nPayoffs\n------------------\nPlayer 1: ", payoffs[0], "\nPlayer 2: ",  payoffs[1])

   trials = int(input("\n\nHow many times play game? trials = "))
   result = qc.run_and_measure(prog, trials = trials)
   for i in range(trials):
      p1 = result[0][i]
      p2 = result[1][i]
      payoffs = normal_payoff_calc(p1,p2,game)
      print("\nGame", i + 1)
      print("\tPlayer 1 : ",p1, " payoff :", payoffs[0])
      print("\tPlayer 2 : ",p2, " payoff :",  payoffs[1])

   print("\n\n", result)




