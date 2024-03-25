# Index

1. [PFLAP: Python Formal Language and Automata Package](#pflap-python-formal-language-and-automata-package)
2. [Developers](#developers)
3. [How To Run a Python Script](#how-to-run-a-python-script)
    - [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
    - [Running The Project](#running-the-project)
4. [Generating an Executable](#generating-an-executable)

# PFLAP: Python Formal Language and Automata Package

pFlap is a Python implementation inspired by JFLAP, an educational tool for theory of computation. It provides a graphical interface for creating, simulating, and testing deterministic finite automata.

Currently, it is not possible to simulate nondeterministic finite automata due to limitations of the interface, but the underlying code is prepared for this type of simulation.

The only supported operating system for pFlap is Windows.

# Developers:
- Pedro Henrique Vieira Giló: [phvg@ic.ufal.br](mailto:phvg@ic.ufal.br)
- Caio Oliveira França dos Anjos: [cofa@ic.ufal.br](mailto:cofa@ic.ufal.br)
- Plácido Augustus de Oliveira Cordeiro: [paoc@ic.ufal.br](mailto:paoc@ic.ufal.br)

# How To Run a Python Script

## Setting up the Virtual Environment

It is recommended to use a virtual environment to isolate the project's dependencies from the global Python system. Follow the steps below to set up the virtual environment:

1. Make sure you have Python installed on your system. If not, download and install it from the official Python website.

2. Open the terminal and navigate to the project's root directory.

3. Execute the following command to create a new virtual environment (we'll use venv in this example):

```bash
    python -m venv venv
```

4. To activate the virtual environment on Windows, run:

```bash
    venv\Scripts\activate
```

After activating the virtual environment, the terminal prompt should change to indicate the active virtual environment.

## Installing Dependencies

The project's dependencies are listed in the requirements.txt file. To install them, follow the steps below:

1. Ensure the virtual environment is activated.

2. In the terminal, execute the following command:

```bash
    pip install -r requirements.txt
```
This will install all the necessary dependencies listed in the requirements.txt file.

## Running The Project

After performing the steps above, type the following command in the terminal within the project's root folder:
```bash
    python main.py
```

# Generating an Executable

1. Install a PyInstaller Library:

```bash
    pip install pyinstaller
```

2. Navigate to the project's root folder and run the following command:
```bash
    pyinstaller --onefile --windowed --add-data="src/assets/:src/assets/" --icon "src/assets/img/icon.ico" .\main.py --name pFLAP-UFAL
```