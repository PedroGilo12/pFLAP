import StateMachine

# Automato finito para reconhecer AA ou BB como subpalavra
states = {
    "q0": StateMachine.State("q0", [("q0", "A", "q1"), ("q0", "B", "q2")]),
    "q1": StateMachine.State("q1", [("q1", "B", "q2"), ("q1", "A", "qf")]),
    "q2": StateMachine.State("q2", [("q2", "A", "q1"), ("q2", "B", "qf")]),
    "qf": StateMachine.State("qf", [("qf", "A", "qf"), ("qf", "B", "qf")])
}

stateMachine = StateMachine.StateMachine(states, states["q0"], ["qf"])

# Fita de entrada
input_row = 'ABABABABABABABABABABA'
signals = list(input_row)

print(f"fita de entrada: {input_row}")

for signal in signals:
    stateMachine.process(signal)
    
print(stateMachine.final())