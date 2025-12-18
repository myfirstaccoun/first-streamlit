import streamlit as st

# دالة بسيطة
def say_hello():
    st.write("أهلا بيك! 👋")

st.title("مثال على زرار في Streamlit")

# زرار
if st.button("اضغط هنا"):
    say_hello()
