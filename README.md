# Reproduced-AQEC-code-with-Qutip
# Kerr Parametric Oscillator Simulation with Autonomous Quantum Error Correction (AQEC)
This project simulates the time evolution of a Kerr Parametric Oscillator (KPO) coupled to an ancilla qubit by Hadis Salasi. It models the population dynamics between logical qubit states and demonstrates Autonomous quantum error correction using a driven-dissipative approach.
The link to the corresponding paper: Kwon, Sangil, Shohei Watabe, and Jaw-Shen Tsai. "Autonomous quantum error correction in a four-photon Kerr parametric oscillator." npj Quantum Information 8, no. 1 (2022): 40.
## 🧩 Features

- Constructs logical qubit states (`|0⟩_L` and `|1⟩_L`) in a 16-dimensional Fock space.
- Models the full Hamiltonian, including:
  - Kerr nonlinearity,
  - Four-photon driving,
  - Coupling to ancilla with time-dependent interaction.
- Solves the Lindblad master equation using QuTiP's `mesolve`.
- Calculates fidelities to track population transfer and error correction performance.
- Plots the populations over time.

## 🛠 Requirements

Install the following Python libraries:
```bash
pip install numpy matplotlib qutip pandas scipy



