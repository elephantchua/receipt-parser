import streamlit as st
import tempfile
from main import processing_receipt, calculating_receipt
import os


client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
username = st.secrets["username"]
api_key = st.secrets["api_key"]

@st.cache_data
def print_receipt(receipt_dict):
    description, quantity, total = st.columns(3)

    for i in range(len(receipt_dict['items'])):
        description.write(f"{i}: {receipt_dict['items'][i]['description']}")
        quantity.write(f"{receipt_dict['items'][i]['quantity']}")
        total.write(f"{receipt_dict['items'][i]['total']}")
        
    st.write("##")
    st.write(f"Subtotal: {receipt_dict['subtotal']}")
    st.write(f"Tax & other fees: {receipt_dict['tax & other fees']}")
    st.write(f"Tip: {receipt_dict['tip']}")
    st.write(f"Total: {receipt_dict['total']}")

def calculate_per_person(receipt_dict, person_number):
    st.write('######')
    st.write(f'### Person {person_number}')
    st.write('Select items to calculate total payment:')

    num_items = st.number_input(
        f'How many items does person {person_number} have?', 
        min_value=0,  # Set minimum value to 0
        max_value=len(receipt_dict['items']), 
        step=1, 
        value=0,  # Set default value to 0
        key=f'num_items_{person_number}'
    )
    
    selected_items = []
    for i in range(num_items):
        item = st.selectbox(
            f'Select item {i+1} for person {person_number}', 
            [item['description'] for item in receipt_dict['items']], 
            key=f'item_{person_number}_{i}'
        )
        selected_items.append(item)
    
    total_cost = 0
    fee_per_dollar = (receipt_dict['tax & other fees'] + receipt_dict['tip']) / receipt_dict['subtotal']

    for item in selected_items:
        for receipt_item in receipt_dict['items']:
            if receipt_item['description'] == item:
                total_cost += receipt_item['total'] / receipt_item['quantity']
                break

    st.write(f"Total cost for selected items before fee(s): {total_cost}")
    st.write(f"Fee(s): {round(total_cost * fee_per_dollar, 2)}")
    st.write(f"Total cost for selected items after fee(s): {round(total_cost * (fee_per_dollar + 1), 2)}")


def main():
    st.set_page_config(page_title="Receipt Parser", layout="centered")

    st.title("Welcome to Receipt Parser")
        
    file = st.file_uploader("Upload an image of your receipt", type=["jpg", "png", "jpeg", "HEIC"])

    if file is None:
        st.text("File Uploaded: None")
    else:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        response = processing_receipt(client_id, client_secret, username, api_key, file)

        receipt_dict = calculating_receipt(response)

        st.write('Item list:')
        print_receipt(receipt_dict)

        st.write('##')
        num_people = st.number_input('Number of people in the party:', min_value=0, step=1, value=0, key='num_people')
        for person_number in range(1, num_people + 1):
            calculate_per_person(receipt_dict, person_number)

if __name__ == '__main__':
    main()
