# PFLAP: Python Formal Language and Automata Package

O pFlap é uma implementação em Python inspirada no JFLAP, uma ferramenta educacional para teoria da computação. Ele fornece uma interface gráfica para criar, simular e testar autômatos finitos, máquinas de Turing, gramáticas e expressões regulares.

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