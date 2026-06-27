import streamlit as st

st.set_page_config(page_title="Happy Birthday", page_icon="🎂")

with open("nastelbom-happy-birthday-471481.mp3", "rb") as audio_file:
    st.audio(audio_file.read(), format="audio/mp3")

st.balloons()

st.markdown("""
# ❤️ Happy Birthday NEELA ❤️

## 🎂 Wishing You On your birthday,
May joy fill your heart and love surround your soul, reminding you of the countless blessings your friendship brings into every life you touch.

💖 Happiness
🌟 Success

### 🎉 Have an Amazing Birthday! 🎉
""")

st.image(
    "https://resize.indiatvnews.com/en/resize/newbucket/1200_-/2022/10/jimin-1665636114.jpg",
    caption="Happy Birthday My Girl ❤️🎂"
)

st.success("May all your dreams come true! ❤️")

st.image(
    "https://wallpaperaccess.com/full/1627574.jpg",
    caption="Always Keep Smiling My Girl ❤️"
)

with st.expander("💌 Click Here ❤️"):

    left_col, right_col = st.columns([1, 2])

    # LEFT SIDE
    with left_col:
        st.image(
            "https://i.pinimg.com/originals/46/c6/b0/46c6b01da21acbdac9941cb3a0cc6601.jpg",
            width=250
        )

    # RIGHT SIDE
    with right_col:
        st.markdown("""
# ❤️ Dear Neela ❤️

## ❤️ YOU WILL BE ALWAYS MY GIRL ❤️
""")

    # Letter starts below the image
    st.markdown("""
---

### 💌 My Letter To You

Happy Birthday to the most amazing person! 🎂

May every dream of yours come true. 🌸

May your smile never fade. 😊

May you always stay happy, healthy, and successful. 🌟

Thank you for being such a wonderful person.

Your kindness, your smile, and your presence make every moment brighter.

No matter where life takes us, I wish you endless happiness and countless beautiful memories.

🎉 Have the Best Birthday Ever! 🎉

❤️ Always Keep Smiling ❤️
""")
