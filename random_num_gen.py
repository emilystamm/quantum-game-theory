# ============================= 
# Random Number Generator
# ============================= 

from pyquil import Program, get_qc 
from pyquil.gates import H

def random_bit(trials):
   # Get quantum computer
   qc = get_qc('1q-qvm')
   # Initialize Program
   p = Program(H(0))

   # Result
   result = qc.run_and_measure(p, trials = trials)
   r = result[0]
   if trials == 1: return r[0]
   else: return r

if __name__ == '__main__':
    trials = int(input("Number of Random Bits: "))
    print(random_bit(trials))
