# B-VQE: Exceptional-Point-Anchored Variational Quantum Eigensolver

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Qiskit 2.4](https://img.shields.io/badge/qiskit-2.4.1-6929C4.svg)](https://qiskit.org/)
[![IBM Heron r2](https://img.shields.io/badge/IBM%20QPU-Heron%20r2-0f62fe.svg)](https://quantum.ibm.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![IOP QST](https://img.shields.io/badge/Journal-IOP%20QST-orange.svg)](https://iopscience.iop.org/journal/2058-9565)

> **Paper:** *Exceptional-Point-Anchored Variational Quantum Eigensolver for  
> Non-Hermitian Many-Body Phase Diagrams*  
> A. B., S. B. & X. C. — *IOP Quantum Science & Technology* (submitted)

---

## Overview

B-VQE is a complete NISQ methodology for non-Hermitian (NH) many-body physics.
It simultaneously optimises **two independent parameterised quantum circuits** —
one for the right eigenstate |ψ_R⟩ and one for the left eigenstate |ψ_L⟩ — via
the **biorthogonal Rayleigh quotient** cost function:

```
L(θ, φ) = Re[E_bio(θ, φ)] + λ · Im[E_bio(θ, φ)]²

where  E_bio = ⟨ψ_L|H_NH|ψ_R⟩ / ⟨ψ_L|ψ_R⟩
```

### Key modules

| Module | File | Description |
|--------|------|-------------|
| **B-VQE core** | `bvqe/core.py` | Dual-circuit ansatz, cost function, COBYLA optimiser |
| **EPD** | `bvqe/epd.py` | Exceptional-Point Detector via coalescence metric C(γ) |
| **NH-QGT** | `bvqe/nhqgt.py` | Non-Hermitian Quantum Geometric Tensor |
| **IS Mitigation** | `bvqe/is_mitigation.py` | Importance-Sampling error mitigation |
| **Hamiltonians** | `hamiltonians/` | NH-Hubbard, NH-XXZ, 2D NH t-J models |
| **IBM backend** | `circuits/backend.py` | Heron r2 noise model + real-hardware session |
| **Experiments** | `experiments/` | Reproduce all paper results (Exp A–D) |
| **Figures** | `figures/` | Publication-quality panels B, C, E, F |
| **QASM** | `qasm/` | IBM Quantum Composer-ready circuits |

---

## Hardware

Tested on three **IBM Heron r2** QPUs (156 qubits, us-east, QAS):

| QPU | p₂q (median) | Readout error | CLOPS |
|-----|-------------|---------------|-------|
| ibm_kingston | 2.08 × 10⁻³ | 1.44 × 10⁻² | 340 K |
| ibm_fez | 2.73 × 10⁻³ | 1.44 × 10⁻² | 320 K |
| ibm_marrakesh | 2.62 × 10⁻³ | 1.172 × 10⁻² | 300 K |

---

## Installation

```bash
git clone https://github.com/QAMP-Group14/NH-VQE.git
cd NH-VQE
pip install -e ".[dev]"
```

**Requirements:** Python ≥ 3.10, Qiskit ≥ 2.4.1, qiskit-ibm-runtime ≥ 0.47,
qiskit-aer, numpy, scipy, matplotlib.

---

## Quick Start

```python
from bvqe import BVQE
from hamiltonians import H_PT

# Build PT-symmetric Hamiltonian H = J·Z + iγ·X
H = H_PT(J=1.0, gamma=0.5)

# Run B-VQE on local Heron r2 simulation
result = BVQE(H, n_qubits=1, depth=3).run(mode="fake", qpu="ibm_kingston")

print(f"E_bio = {result.E_bio:.5f}")   # ≈ -0.86603
print(f"C(γ)  = {result.C:.4f}")       # ≈ 0.0 (PT-unbroken)
```

---

## Repository Structure

```
NH-VQE/
├── bvqe/                    # Core B-VQE library
│   ├── __init__.py
│   ├── core.py              # BVQE class, E_bio, cost function
│   ├── epd.py               # EPD module, coalescence metric
│   ├── nhqgt.py             # NH-QGT, Berry curvature, quantum metric
│   └── is_mitigation.py     # IS weights, variance bound
├── hamiltonians/            # Model Hamiltonians
│   ├── __init__.py
│   ├── nh_pt.py             # H = J·Z + iγ·X  (PT-symmetric)
│   ├── nh_hubbard.py        # Non-Hermitian Hubbard chain
│   ├── nh_xxz.py            # Non-Hermitian XXZ spin chain
│   └── nh_tj_2d.py          # 2D NH t-J model (Fermi skin)
├── circuits/                # Qiskit circuit builders
│   ├── __init__.py
│   ├── hea.py               # Hardware-Efficient Ansatz
│   ├── hadamard_test.py     # Hadamard test for overlap
│   ├── backend.py           # IBM Heron r2 backends + noise models
│   └── transpiler.py        # ISA transpilation utilities
├── experiments/             # Reproduce paper experiments
│   ├── exp_A_pt_transition.py
│   ├── exp_B_ep_detection.py
│   ├── exp_C_size_scaling.py
│   └── exp_D_fidelity.py
├── figures/                 # Publication figures
│   └── panels_bcef.py       # Panels B, C, E, F (Nature style)
├── notebooks/               # Jupyter notebooks
│   └── bvqe_panels_bcef.ipynb
├── qasm/                    # IBM Quantum Composer circuits
│   ├── right/               # U_R(θ) circuits
│   ├── left/                # U_L(φ) circuits
│   └── hadamard/            # EPD Hadamard test circuits
├── tests/                   # Unit + integration tests
│   ├── test_core.py
│   ├── test_epd.py
│   ├── test_hamiltonians.py
│   └── test_circuits.py
├── scripts/
│   ├── run_all_experiments.sh
│   └── generate_qasm.py
├── docs/
│   └── theory.md
├── setup.py
├── requirements.txt
└── README.md
```

---

## Reproducing Paper Results

```bash
# All four experiments (fake Heron r2 backends)
bash scripts/run_all_experiments.sh

# Or individually
python experiments/exp_A_pt_transition.py
python experiments/exp_B_ep_detection.py
python experiments/exp_C_size_scaling.py
python experiments/exp_D_fidelity.py

# Generate publication figures
python figures/panels_bcef.py
# → ./output/panel_B_pt_transition.png etc.

# Generate QASM files for IBM Quantum Composer
python scripts/generate_qasm.py
```

---

## Running on Real IBM Quantum Hardware

```python
import os
from bvqe import BVQE
from hamiltonians import H_PT

H = H_PT(J=1.0, gamma=0.5)
result = BVQE(H, n_qubits=1, depth=3).run(
    mode="real",
    qpu="ibm_kingston",
    ibm_token=os.environ["IBM_QUANTUM_TOKEN"],
    shots=8192,
)
print(result)
```

Set your IBM Quantum API token:
```bash
export IBM_QUANTUM_TOKEN="your_token_from_quantum.ibm.com"
```

---

## Citation

```bibtex
@article{bvqe2026,
  title   = {Exceptional-Point-Anchored Variational Quantum Eigensolver
             for Non-Hermitian Many-Body Phase Diagrams},
  author  = {B., A. and B., S. and C., X.},
  journal = {IOP Quantum Science \& Technology},
  year    = {2026},
  note    = {submitted}
}
```

---

## License

MIT License — see [LICENSE](LICENSE).
