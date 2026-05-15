# Title
st.title("My First Streamlit App")

# Text
st.write("Hello, Streamlit!")

# User input
name = st.text_input("Enter your name:")

# Button
if st.button("Submit"):
    st.success(f"Welcome, {name}!")

# Slider
age = st.slider("Select your age:", 1, 100, 25)

st.write(f"Your age is {age}")
