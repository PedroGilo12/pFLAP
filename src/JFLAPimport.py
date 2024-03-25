import xml.etree.ElementTree as ET
import src.StatesManager as sm
import re

def extract_state_id(string):
    # Expressão regular para encontrar o número após o 'q'
    padrao = r'q(\d+)'
    
    # Encontra todas as correspondências na string
    correspondencias = re.findall(padrao, string)
    
    # Se houver correspondências, retorna o primeiro número encontrado como inteiro
    if correspondencias:
        return str(correspondencias[0])
    else:
        return None

def parse_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    states_list = []

    # Itera sobre todos os elementos state no XML
    for state_elem in root.findall('./automaton/state'):
        state_id = int(state_elem.get('id'))
        state_name = state_elem.get('name')
        state_x = float(state_elem.find('x').text)
        state_y = float(state_elem.find('y').text)
        
        init = state_elem.find('initial')
        fin = state_elem.find('final')
        
        if init != None:
            is_initial = True
        else:
            is_initial = False
        
        if fin != None:
            is_final = True
        else:
            is_final = False
        
        # Cria um objeto StatesManager para representar o estado atual
        state_manager = sm.StatesManager(state_x, state_y, state_id, initial=is_initial, final=is_final)

        # Adiciona o objeto StatesManager à lista
        states_list.append(state_manager)

    # Itera sobre todos os elementos transition no XML
    for transition_elem in root.findall('./automaton/transition'):
        from_state = int(transition_elem.find('from').text)
        to_state = int(transition_elem.find('to').text)
        symbol = transition_elem.find('read').text

        # Adiciona a transição ao estado correspondente
        states_list[from_state].add_transition(states_list[to_state], symbol)  # Alteração nesta linha


    return states_list
def write_xml(automaton, output_file):
    # Cria o elemento raiz do XML
    structure_elem = ET.Element("structure")

    # Define o tipo de autômato
    type_elem = ET.SubElement(structure_elem, "type")
    type_elem.text = "fa"

    # Cria o elemento automaton
    automaton_elem = ET.SubElement(structure_elem, "automaton")

    # Itera sobre os estados e cria os elementos correspondentes no XML
    for e, state in enumerate(automaton):
        state_elem = ET.SubElement(automaton_elem, 'state', attrib={'id': extract_state_id(state.state_name), 'name': state.state_name})
        x_elem = ET.SubElement(state_elem, 'x')
        x_elem.text = str(state.x)
        y_elem = ET.SubElement(state_elem, 'y')
        y_elem.text = str(state.y)

        if state.initial:
            initial_elem = ET.SubElement(state_elem, 'initial')
        if state.final:
            final_elem = ET.SubElement(state_elem, 'final')

    # Itera sobre as transições e cria os elementos correspondentes no XML
    for state in automaton:
        for transition in state.transition_list:
            transition_elem = ET.SubElement(automaton_elem, 'transition')
            from_elem = ET.SubElement(transition_elem, 'from')
            from_elem.text = extract_state_id(state.state_name)
            to_elem = ET.SubElement(transition_elem, 'to')
            to_elem.text = extract_state_id(transition[0].state_name)
            read_elem = ET.SubElement(transition_elem, 'read')
            read_elem.text = str(transition[1])

    # Cria o objeto tree para escrever no arquivo
    tree = ET.ElementTree(structure_elem)

    # Escreve o XML no arquivo
    with open(output_file, "wb") as f:
        tree.write(f)