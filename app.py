import streamlit as st
import pandas as pd
import plotly.express as px

from playwright.sync_api import sync_playwright

#add image
st.image("envision.png")

st.set_page_config(
    page_title="ServiceNow Dashboard",
    layout="wide"
)

st.title("🎫 ServiceNow Ticket Dashboard")


@st.cache_data(ttl=300)
def fetch_data():

    tickets = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-setuid-sandbox",
                "--single-process"
           ]
        )

        context = browser.new_context(
            storage_state="auth.json"
        )

        api_url = "https://ee.envision-energy.com"

        response = context.request.get(api_url)

        print("Status:", response.status)

        if response.status != 200:
            raise Exception(f"API failed with status {response.status}")

        print("Status:", response.status)

        content_type = response.headers.get("content-type", "")

        print("Content-Type:", content_type)

        text = response.text()

        print(text[:1000])

        if "application/json" not in content_type:
             raise Exception(
                  f"Expected JSON but got: {content_type}"
             )

        data = response.json()

        for item in data["result"]:

            tickets.append({
                "Number": item.get("number"),
                "Short Description": item.get("short_description"),
                "Case State": item.get("case_state"),
                "Site": item.get("site"),
                "Register Time": item.get("register_time"),
                "Close Time": item.get("close_time", "")
            })

        browser.close()

    return pd.DataFrame(tickets)


try:

    df = fetch_data()

    st.success("Connected to ServiceNow")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Tickets", len(df))

    with col2:
        st.metric(
            "Open Tickets",
            len(df[df["Case State"] != "Closed"])
        )

    st.subheader("Tickets Table")

    st.dataframe(df, use_container_width=True)

    st.subheader("Tickets by Case State")

    
    fig1 = px.pie(
        df,
        names="Case State"
    )

    st.plotly_chart(fig2, use_container_width=True)

except Exception as e:

    st.error(f"Error: {e}")

    st.info(
        "Make sure auth.json exists and login session is valid."
    )
