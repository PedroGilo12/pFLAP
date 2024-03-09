class State:
    _name = ""
    _elements : list[tuple[str, str]] = []

    def __init__(self, name, elements):
        self._name = name
        self._elements = elements
        
    def get_name(self):
        return self._name

    def get_elements(self):
        return self._elements
    
    def process(self, signal):
        output_states = []
        
        for element in self._elements:
            if element[1] == signal:
                output_states.append(element[2])

        return output_states

class StateMachine:
    _undefined_state = State("undefined", [])
    _states: dict[str, State] = {}
    _initial_state: State = None
    _current_state: State = None
    _final_states = []
    
    def __init__(self, states, initial_state, final_states):
        self._states = states
        self._initial_state = initial_state
        self._final_states = final_states
        self._current_state = self._initial_state
        
    def set_state(self, state):
        self._current_state = state
        
    def get_state(self):
        return self._current_state
    
    def process(self, signal: str): 
        next_state = self._current_state.process(signal)
        
        if len(next_state) > 0:
            
            if len(next_state) == 1:
                for next_state in next_state:
                    print(f"{self._current_state.get_name()} -> {signal} -> {next_state}")
                    self.set_state(self._states[next_state])
            else:
                print(f'AFN is not suported')
        else:
            self.set_state(self._undefined_state)
            print(f"State '{next_state}' not found in the dictionary.")
            
    def final(self):
        return self._current_state.get_name() in self._final_states

states = {
    "q0": State("q0", [("q0", "A", "q1"), ("q0", "B", "q2")]),
    "q1": State("q1", [("q1", "B", "q2"), ("q1", "A", "qf")]),
    "q2": State("q2", [("q2", "A", "q1"), ("q2", "B", "qf")]),
    "qf": State("qf", [("qf", "A", "qf"), ("qf", "B", "qf")])
}

stateMachine = StateMachine(states, states["q0"], ["qf"])

input_row = 'ABABABBABABABABABABABA'
signals = list(input_row)

print(f"fita de entrada: {input_row}")

for signal in signals:
    stateMachine.process(signal)
    
print(stateMachine.final())