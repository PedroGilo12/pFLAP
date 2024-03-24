import pySub
import queue
import time

final_states = []

class State:
    name = ""
    elements : list[tuple[str, str]] = []

    def __init__(self, name, elements):
        self.name = name
        self.elements = elements
        
    def get_name(self):
        return self.name

    def get_elements(self):
        return self.elements
    
    def process(self, signal):
        output_states = []
        
        for element in self.elements:
            if element[1] == signal:
                output_states.append(element[2])

        return output_states

class StateMachine:
    _undefined_state = State("undefined", [])
    _states: dict[str, State] = {}
    _initial_state: State = None
    _current_state: State = None
    _final_states = []
    
    def __init__(self, states, initial_state, final_states, topic, end: list):
        self._states = states
        self._initial_state = initial_state
        self._final_states = final_states
        self._current_state = self._initial_state
        self._end = end
        self.topic = topic
        self.subscriber = pySub.Subscriber("", topic)
        self.subscriber.set_run(self.run)
        topic.subscribe(self.subscriber)
        self.subscriber.start()
    
    def _empty_moves(self, state_elements):
        return [state[2] for state in state_elements if state[1] == "e"]
    
    def set_state(self, state):
        self._current_state = state
        
    def get_state(self):
        return self._current_state
    
    def run(self):

        while True:
            signal = self.subscriber.queue.get()
            if signal == "exit":
                self._end.append(self.final())
                break
            if not self.process(signal):
                break
    
    def process(self, signal: str): 
        
        next_states = self._current_state.process(signal)
        
        if len(next_states) == 0:
            print(f"{self._current_state.get_name()} -> {signal} -> {self._undefined_state.get_name()}")
            self.set_state(self._undefined_state)
            return False
        
        for n, next_state in enumerate(next_states):
            print(f"{self._current_state.get_name()} -> {signal} -> {next_state}")
            empty_moves = self._empty_moves(self._states[next_state].get_elements())
            for sstate in empty_moves:
                self.__class__(self._states, self._states[sstate], self._final_states, self.topic, self._end)
                
            if n == len(next_states) - 1:
                self.set_state(self._states[next_state])
            else:
                self.__class__(self._states, self._states[next_state], self._final_states, self.topic, self._end)           
        
        return True 
            
    def final(self):
        return self._current_state.get_name() in self._final_states
    
class FiniteStateMachine:
    
    def __init__(self, states, initial_state, final_states):
        self._states = states
        self._initial_state = initial_state
        self._final_states = final_states
        self._end = []
        
        self._topic = pySub.Topic()
        self.machine = StateMachine(self._states, self._initial_state, self._final_states, self._topic, self._end)

    def process_symbol(self, symbol):
        print(f"Symbol: {symbol}")
        self._topic.publish(symbol)
        time.sleep(0.5)
        
    def result(self):
        self._topic.stop_all_subscribers()
        return self._end