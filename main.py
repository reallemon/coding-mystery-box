import streamlit as st
import json
import random

def main(): 
    st.title('Coding Mystery Box')
    
    if 'random' not in st.session_state:
        st.session_state['random'] = []
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.button(label='Generate Option', on_click=add_random_choice)
        
    with col_2:
        st.button(label='Reset', on_click=clear_session_state)
    
    if st.session_state.random != []:
        for option in reversed(st.session_state.random):
            st.write('## Input')
            st.write(f"{option['input']['name']}: {option['input']['description']}")
            
            st.write('## Constraint')
            st.write(f"{option['constraint']['name']}: {option['constraint']['description']}")
            
            st.write('## Output')
            st.write(f"{option['output']['name']}: {option['output']['description']}")
            st.write('---')


def clear_session_state():
    if 'random' in st.session_state:
        st.session_state['random'] = []

def add_random_choice():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        # List of dicts
        inputs = data['tables']['fabric_inputs']
        constraints = data['tables']['logic_constraints']
        outputs = data['tables']['output_mediums']
        
        rand_input = random.choice(inputs)
        rand_constraint = random.choice(constraints)
        rand_output = random.choice(outputs)
        
        rand_choice = {
            "input": rand_input,
            "constraint": rand_constraint,
            "output": rand_output
        }
        
        st.session_state.random.append(rand_choice)
    except:
        print("Something went wrong")
        
if __name__ == "__main__":
    main()
