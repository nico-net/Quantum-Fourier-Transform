"""
Gallucci Nicola
Garzoni Stefano
"""

#qiskit is a software development kit that gives the opportunity 
#to work with real quantum computers provided by IBM.
#Through quiskit SDK we can implement and simulate/process circuits, 
#pulses and quantum algorithms
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import math
import matplotlib.pyplot as plt

#Let's now define the registers we will need for the circuit, 
#this step is important to define the basic components 
#for the quantum calculation of the Quantum Fourier Transform

nQubits = 5  #number of qubits

#The qubits in this register will be used to represent 
#the quantum state on which the QFT will be applied
qReg = QuantumRegister(nQubits, name='q')

#This register will contain the results of the qubit measurement
# after the QFT has been performed
cReg = ClassicalRegister(nQubits, name='c')

#Creation of the quantum circuit with the registers created above
circuit = QuantumCircuit(qReg, cReg)

#Hadamard transform:
#The Hadamard transform plays a crucial role in enabling superposition computation.
#It is a key component for many quantum algorithms, especially Fourier sampling.
#Also called Hadamard Gate, it operates on a single qubit represented by the well-known Hadamard matrix,
# which acts on the quantum state of the latter.
#When the Hadamard transform is applied to a qubit in the computational basis (|0⟩ and |1⟩), 
#it transforms the basis states into superposition states.
#In practice, the Hadamard transform allows the qubit to exist simultaneously 
#in the |0> and |1> states with relative probabilities associated with each of the states.
#Therefore, thanks to the Hadamard transform we can, 
#through quantum computers, process information in parallel, 
#developing an exponential acceleration compared to a classic computer that works with bits.
#For Fourier sampling we will use a series of Hadamard transforms 
#on a set of qubits and then perform the Fourier transform 
#on their collective state.
#This allows us to read information about the frequency of the input state.
for i in range(nQubits):
    circuit.h(qReg[i])

#QFT phase:
#The QFT step is applied using the CU gate specifically to generate the Fourier transform 
#of the initial quantum state.
#The CU gates add phases dependent on the controlled qubits, modulating the Fourier transform.
#The combination of these operations, repeated specifically for all qubits, leads to the implementation of QFT.
#ctrl = control qubit
#tar = target qubit
#(math.pi / 4) * (2**(i - j)) = phase theta angle
#0 = phase phi, lam, gamma angle
for i in range(nQubits):
    for j in range(i):
        ctrl = qReg[i]
        tar = qReg[j]
        phase_angle = (math.pi / 4) * (2**(i - j))
        circuit.cu(phase_angle, 0, 0, 0, ctrl, tar)
        

#Qubit measurement
circuit.measure(qReg, cReg)

#Once the circuit has been created and prepared, we are now going to execute it
#A AerSimulator object is created, i.e. a virtual quantum simulator, on which the circuit will be executed.
#This is a common practice to simulate a real quantum device in order to test circuits 
#before running them on a real quantum computer.
#Through the AerSimulator object, and the circuit, a simulator.run is created with an arbitrary number of shots. 
#They represent the number of times the circuit will be executed and consequently the 
#execution results are averaged. The greater the number of shots, 
#the greater the precision of the results and the execution time.
#Once the object for execution is created, we start the execution and save it in result.
#The result variable is a dictionary of which each key represents a binary string 
#that corresponds to a possible state of the measured qubits, 
#and the value associated with the key represents the number of times 
#that state has been measured.
simulator = AerSimulator()
exe = simulator.run(circuit, shots=4096).result()
result = exe.get_counts(circuit)

#In the end we just have to print the circuit, the results and observe the histogram based on them
print(circuit)
print(result)
plot_histogram(result)
plt.show()

"""
Fonti:
https://docs.quantum.ibm.com/
https://www.wikiwand.com/it/Trasformata_di_Hadamard
https://www.nexsoft.it/quantum-computing-qiskit-part3/
"""