import streamlit as st

if 'column_count' not in st.session_state:
    st.session_state.column_count = 1

input_stocks_count = st.text_input('How many shares of stock have been issued?')
add_column = st.button('Add Row')
if add_column:
    st.session_state.column_count += 1

col1, col2, col3 = st.columns([6, 2, 2])
ownership = []
for i in range(st.session_state.column_count):
    ownership_name = col1.text_input('Name', key=f'name{i}')
    ownership_percentage = col2.number_input('Percentage', key=f'percentage{i}', step=0.1, min_value=0.0, format="%.2f")
    ownership_stock = col3.number_input('Stock', key=f'stock{i}', step=1, min_value=0)

    if ownership_name and ownership_stock >= 0:
        ownership.append({
            'name': ownership_name,
            'percentage': float(ownership_percentage),
            'stock': ownership_stock
        })

input_amount_rise = st.text_input('How much money are you looking to raise?')
input_premoney = st.text_input('What is your pre-money valuation?')
submit_data = st.button('Submit details')

if submit_data:
    try:
        input_stocks_count = int(input_stocks_count) if input_stocks_count else 0
        input_amount_rise = int(input_amount_rise) if input_amount_rise else 0
        input_premoney = int(input_premoney) if input_premoney else 0

        if input_stocks_count < 0:
            st.error('Only a positive number is accepted for stock count')   
        if input_amount_rise < 0:
            st.error('Only a positive number is accepted for amount to raise')      
        if input_premoney < 0:
            st.error('Only a positive number is accepted for pre-money valuation')  

    except ValueError:
        st.error('Please enter valid numeric values for stock count, amount to raise, and pre-money valuation.')

    if sum(item['percentage'] for item in ownership) > 100:
        st.error('Total percentage should not exceed 100%')

    st.subheader('Result')
    st.write('# Basics #')

    post_money_valuation = input_amount_rise + input_premoney
    share_price = input_premoney / input_stocks_count if input_stocks_count else 0
    share_to_issue = input_amount_rise / share_price if share_price else 0
    total_stock = input_stocks_count + share_to_issue
    investors_ownership = (share_to_issue / total_stock) * 100 if total_stock else 0

    col4, col5, col6 = st.columns([6, 2, 2])
    with col4:
        st.write('Post-Money Valuation')
        st.write('Stock that needs to be issued')
        st.write('Total company stock after funding')
        st.write("Investor's ownership")

    with col5:
        st.write(f'{post_money_valuation}')
        st.write(f'{int(share_to_issue)}')
        st.write(f'{int(total_stock)}')
        st.write(f'{investors_ownership:.2f}%')

    with col6:
        st.write('USD')
        st.write('Shares')
        st.write('Shares')
        st.write('Percentage')

    col7, col8, col9 = st.columns([5, 3, 2])
    with st.container():
        col7.write('## Cap Table ##')
        col8.write('## Percentage (pre-funding) ##')
        col9.write('## Percentage Ownership ##')

    for item in ownership:
        new_ownership_percentage = (item['stock'] / total_stock) * 100 if total_stock else 0
        col7.write(f"{item['name']}")
        col8.write(f"{item['stock']}")
        col9.write(f"{new_ownership_percentage:.2f}%")

    col7.write('Investors')
    col8.write(f'{int(share_to_issue)}')
    col9.write(f'{investors_ownership:.2f}%')

    st.write("Pie chart visualization can be handled using Streamlit's built-in `st.bar_chart` for simplicity or by re-integrating another graphing library like Plotly.")
