import xml.etree.ElementTree as ET

def parse_xml(file_path):
    automaton = {}
    tree = ET.parse(file_path)
    root = tree.getroot()

    states = root.findall('.//state')
    for state in states:
        state_id = state.get('id')
        state_name = state.get('name')
        initial = state.find('initial') is not None
        final = state.find('final') is not None
        x = float(state.find('x').text)
        y = float(state.find('y').text)
        automaton[state_id] = {'name': state_name, 'initial': initial, 'final': final, 'x': x, 'y': y}

    transitions = root.findall('.//transition')
    for transition in transitions:
        from_state = transition.find('from').text
        to_state = transition.find('to').text
        read = transition.find('read').text
        if from_state in automaton:
            if 'transitions' not in automaton[from_state]:
                automaton[from_state]['transitions'] = []
            automaton[from_state]['transitions'].append({'to': to_state, 'read': read})

    return automaton

def write_xml(automaton, output_file):
    root = ET.Element('structure')
    
    type_element = ET.SubElement(root, 'type')
    type_element.text = 'fa'
    
    automaton_element = ET.SubElement(root, 'automaton')
    
    for state_id, state_data in automaton.items():
        state = ET.SubElement(automaton_element, 'state', id=str(state_id), name=state_data['name'])
        x_element = ET.SubElement(state, 'x')
        x_element.text = str(state_data['x'])
        y_element = ET.SubElement(state, 'y')
        y_element.text = str(state_data['y'])
        if state_data['initial']:
            initial_element = ET.SubElement(state, 'initial')
        if state_data['final']:
            final_element = ET.SubElement(state, 'final')
    
    for state_id, state_data in automaton.items():
        if 'transitions' in state_data:
            for transition in state_data['transitions']:
                transition_element = ET.SubElement(automaton_element, 'transition')
                from_element = ET.SubElement(transition_element, 'from')
                from_element.text = state_id
                to_element = ET.SubElement(transition_element, 'to')
                to_element.text = transition['to']
                read_element = ET.SubElement(transition_element, 'read')
                read_element.text = transition['read']
    
    tree = ET.ElementTree(root)
    
    tree.write(output_file)