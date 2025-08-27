import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write("Choose the fruits you want in your custom smoothie.")

# User input: Name
name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your Smoothie will be:", name_on_order)

# Get Snowflake session and fruit options
cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Multiselect for fruits
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list and name_on_order:
    # Create ingredient string
    ingredients_string = " ".join(ingredients_list)

    # Correct insert with both columns
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)  # For debugging

    # Button to submit order
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
import requests
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


