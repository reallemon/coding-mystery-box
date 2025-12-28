import streamlit as st
import json
import random
from typing import TypedDict, Literal, cast
    
class Input(TypedDict):
    name: str
    description: str    

class Constraint(TypedDict):
    name: str
    description: str
    
class Architecture(TypedDict):
    name: str
    description: str

class Option(TypedDict):
    inputs: Input
    constraints: Constraint
    architectures: Architecture

class Data(TypedDict):
    inputs: list[Input]
    constraints: list[Constraint]
    architectures: list[Architecture]

CategoryKey = Literal['inputs', 'constraints', 'architectures']

def main() -> None: 
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
            option: Option = st.session_state.random[i]
            
            
            with st.container(border=True):
                d_col_1, d_col_2 = st.columns([6,1]) # type: ignore
                
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
                    st.button('🔄', key=f'reroll_architectures_{i}', on_click=reroll_idea, args=(i, 'architectures',))
                
                with c2:
                    st.write('## Architecture')
                    st.write(f"{option['architectures']['name']}: {option['architectures']['description']}")

def reroll_idea(index: int, category_key: CategoryKey) -> None:
    st.session_state.random[index][category_key] = random.choice(st.session_state['data'][category_key])

def delete_index(index: int) -> None:
    del st.session_state.random[index]

def clear_session_state() -> None:
    if 'random' in st.session_state:
        st.session_state['random'] = []

def add_random_choice() -> None:
    data = cast(Data, st.session_state['data'])
            
    rand_input: Input = random.choice(data['inputs'])
    rand_constraint: Constraint = random.choice(data['constraints'])
    rand_architecture: Architecture = random.choice(data['architectures'])
    
    rand_choice: Option = {
        "inputs": rand_input,
        "constraints": rand_constraint,
        "architectures": rand_architecture
    }
    
    st.session_state.random.append(rand_choice)
        
if __name__ == "__main__":
    try:
        with open('data.json', 'r') as file:
            raw_data = json.load(file)
        # List of dicts
        inputs: list[Input] = raw_data['tables']['fabric_inputs']
        constraints: list[Constraint] = raw_data['tables']['notions_constraints']
        architectures: list[Architecture] = raw_data['tables']['architecture_scenarios']
        
        data: Data = {
            "inputs": inputs,
            "constraints": constraints,
            "architectures": architectures
        }
        
        st.session_state['data'] = data
        
    except:
        print("Something went wrong")
    
    main()
