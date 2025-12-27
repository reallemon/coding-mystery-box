import streamlit as st
import json
import random

def main(): 
    st.set_page_config(page_title='Coding Mystery Box')
    
    if 'random' not in st.session_state:
        st.session_state['random'] = []
    
    if 'data' not in st.session_state:
        st.session_state['data'] = {}
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.button(label='Generate Option', on_click=add_random_choice)
        
    with col_2:
        st.button(label='Reset', on_click=clear_session_state)
    
    if st.session_state.random != []:
        for i in range(len(st.session_state.random) -1, -1, -1):
            option = st.session_state.random[i]
            
            
            with st.container(border=True):
                d_col_1, d_col_2 = st.columns([6,1])
                
                with d_col_2:
                    st.button('🗑️', key=f'delete_{i}', on_click=delete_index, args=(i,))
                
                c1, c2 = st.columns([1, 5])
                
                with c1:
                    st.write("")
                    st.write("")
                    st.button('🔄', key=f'reroll_inputs_{i}', on_click=reroll_idea, args=(i, 'inputs',))
                
                with c2:
                    st.write('## Input')
                    st.write(f"{option['inputs']['name']}: {option['inputs']['description']}")
                
                c1, c2 = st.columns([1, 5])
                
                with c1:
                    st.write("")
                    st.write("")
                    st.button('🔄', key=f'reroll_constraints_{i}', on_click=reroll_idea, args=(i, 'constraints',))
                
                with c2:
                    st.write('## Constraint')
                    st.write(f"{option['constraints']['name']}: {option['constraints']['description']}")
                    
                c1, c2 = st.columns([1, 5])
                
                with c1:
                    st.write("")
                    st.write("")
                    st.button('🔄', key=f'reroll_outputs_{i}', on_click=reroll_idea, args=(i, 'outputs',))
                
                with c2:
                    st.write('## Output')
                    st.write(f"{option['outputs']['name']}: {option['outputs']['description']}")

def reroll_idea(index, category_key):
    st.session_state.random[index][category_key] = random.choice(st.session_state['data'][category_key])

def delete_index(index):
    del st.session_state.random[index]

def clear_session_state():
    if 'random' in st.session_state:
        st.session_state['random'] = []

def add_random_choice():
    data = st.session_state['data']
            
    rand_input = random.choice(data['inputs'])
    rand_constraint = random.choice(data['constraints'])
    rand_output = random.choice(data['outputs'])
    
    rand_choice = {
        "inputs": rand_input,
        "constraints": rand_constraint,
        "outputs": rand_output
    }
    
    st.session_state.random.append(rand_choice)
        
if __name__ == "__main__":
    try:
        with open('data.json', 'r') as file:
            raw_data = json.load(file)
        # List of dicts
        inputs = raw_data['tables']['fabric_inputs']
        constraints = raw_data['tables']['logic_constraints']
        outputs = raw_data['tables']['output_mediums']
        
        data = {
            "inputs": inputs,
            "constraints": constraints,
            "outputs": outputs
        }
        
        st.session_state['data'] = data
        
    except:
        print("Something went wrong")
    
    main()
