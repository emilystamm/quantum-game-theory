
# Quantum Fourier Transform
# -------------------------------------

from pyquil import *
from pyquil.gates import *
from pyquil.api import *

import numpy as np
import math
from math import e, floor
from numpy import pi
from numpy.fft import ifft


# QFT
# -------------------------------------
# Input: n (number of qubits), prog (quantum program)
# Output: QFT_n(prog) (quantum program) - quantum fourier transform applied to program

def QFT(n, prog):
   # Swap qubits to get correct order
   for k in range(floor(n/2)):
      prog += SWAP(k, n-k-1)
   # For each qubit, apply H and a series of CPhase gates
   for i in range(n):
      prog += H(i)
      m = 2
      # For each qubit j > i, Apply Control-R_m to qubits j (control), i (target)
      for j in range(i+1, n):
         prog += CPHASE(pi * (2**(-m+1)), j, i)
         m += 1
   # Return QFT_n(prog)
   return prog


# Rest of the functions for testing QFT 
# -------------------------------------

def QFT_Test(n, prog, classic_array):
   # Initial Wave Function
   wfn = WavefunctionSimulator().wavefunction(prog)
   print("\n\nInitial Wavefunction:", wfn)

   # Final Wave Function (after apply QFT)
   wfn = WavefunctionSimulator().wavefunction(QFT(n,prog))
   wfn_array = wfn.amplitudes
   print("\nFinal Wavefunction:", wfn)

   # Classically compute IFFT
   IFFT_Array = ifft(classic_array, norm="ortho")
   
   # Compare classical and quantum
   for x in range(2**n):
      if not (abs(IFFT_Array[x] - wfn_array[x])< .001): return False
   return True


def Run_Tests():
   number_of_tests = 0
   number_of_successes = 0

   # Test 
   n = 5
   prog = Program()
   # Initial State
   prog.inst(I(0), I(1), I(2), I(3), I(4))
   # Representative Array of initial state
   array  = [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
   test_success = QFT_Test(n,prog, array)
   print(test_success)
   # Counter
   if test_success: number_of_successes += 1
   number_of_tests += 1


   # Test 
   n = 4
   prog = Program()
   # Initial State
   prog.inst(H(0), H(1), I(2), I(3))
   # Representative Array of initial state
   array  = [.5,.5,.5,.5,0,0,0,0,0,0,0,0,0,0,0,0]
   test_success = QFT_Test(n,prog, array)
   print(test_success)
   # Counter
   if test_success: number_of_successes += 1
   number_of_tests += 1


   # Test 
   n = 3
   prog = Program()
   # Initial State
   prog.inst(X(0), I(1), I(2))
   # Representative Array of initial state
   array  = [0,1,0,0,0,0,0,0]
   test_success = QFT_Test(n,prog, array)
   print(test_success)
   # Counter
   if test_success: number_of_successes += 1
   number_of_tests += 1

   print("\nFinished.", number_of_successes, "/", number_of_tests, "Tests Correct\n")




if __name__ == "__main__":
   Run_Tests()






