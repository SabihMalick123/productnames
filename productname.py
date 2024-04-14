import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
import random

# Configure Gemini with API key
genai.configure(api_key="AIzaSyBy0nEMHwDwImc0ySdDRIZfVVGkuzzgX9E")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def generate_product_names_and_description(input_text):
    # Prompt for Gemini model
    prompt = f"""
        Welcome to the innovation lab of the future! 🚀✨

        Imagine you're about to unveil the next big thing - a product so groundbreaking, it defies imagination.
        Picture a world where innovation knows no bounds and creativity reigns supreme.

        Now, tell us about your visionary creation. What sets it apart from the ordinary? What makes it a game-changer?

        Describe your product in vivid detail, from its functionality to its design, and even the emotions it evokes in its users.
        Let your imagination run wild, and together, we'll craft a name and description that captivates the world!

        Product Details:
        "{input_text}"
        
        Output Format:
        Product Name
        
        Product Description
        """
    # prompt = f"""
    #     Welcome to the future of e-commerce innovation! 🛍️✨

    #     Imagine you're on the cutting edge of online retail, introducing a revolutionary new product to the world.
    #     Your product is not just an item on a shelf; it's an experience, a lifestyle, a must-have for every digital shopper.

    #     Describe your e-commerce masterpiece in detail - from its features and benefits to its unique selling points.
    #     What makes it stand out in the crowded e-commerce landscape? How does it delight and inspire your customers?

    #     Product Details:
    #     "{input_text}"
    #     Output Format:
    #     Product Name
    #    
    #     Product Description
    #     """

    # Use Gemini to generate product names and descriptions
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit App
st.set_page_config(page_title="Product Name & Description Generator")

# Define a function to handle user input and generate responses
def chat():
    st.title("Product Name & Description Generator")
    st.write("Welcome to the innovation lab of the future! Let's create something extraordinary together.")

    # User input for product details
    input_text = st.text_area("Tell us about your visionary creation:", height=150, max_chars=500, key="input_text")

    # Generate product names and descriptions when user sends a message
    if st.button("Unleash Creativity"):
        if input_text:
            # Save the user's message to chat history
            st.session_state.chat_history.append(("User", input_text))

            # Display user's message
            key = f"user_message_{random.randint(1, 1000000)}"
            message(input_text, is_user=True, key=key)

            # Generate product names and descriptions based on user's input
            try:
                with st.spinner("Firing up the imagination engine..."):
                    product_info = generate_product_names_and_description(input_text)
                # Save the generated product names and descriptions to chat history
                st.session_state.chat_history.append(("Bot", product_info))
                # Display generated product names and descriptions
                key = f"bot_message_{random.randint(1, 1000000)}"
                message(product_info, key=key)
            except Exception as e:
                st.error("An error occurred while igniting creativity. Please try again later.")
                print("An error occurred while igniting",e)
        else:
            st.warning("Please share the essence of your visionary creation.")

# Display the chat interface
chat()

# Button to toggle chat history visibility
show_chat_history = st.button("Show Innovation Log")

# Display chat history only if the button is clicked
if show_chat_history:
    st.subheader("Innovation Log")
    for idx, (sender, msg) in enumerate(st.session_state.chat_history):
        key = f"message_{random.randint(1, 1000000)}"
        message(msg, is_user=(sender == "User"), key=key)
