import StateMachine

# Automato finito Não Deterministico com Movimento Vazio para reconhecer sufixo A ou B
states = {
    "q0": StateMachine.State("q0", [("q0", "e", "q1"), ("q0", "e", "q2"), ("q0", "A", "q0"), ("q0", "B", "q0"), ("q0", "C", "q0")]),
    "q1": StateMachine.State("q1", [("q1", "A", "qf")]),
    "q2": StateMachine.State("q2", [("q2", "B", "qf")]),
    "qf": StateMachine.State("qf", [])
}

machine = StateMachine.FiniteStateMachine(states, states["q0"], ["qf"])

signals = list("CCCCACCCA")

for signal in signals:
    machine.process_symbol(signal)
    
print(machine.result())