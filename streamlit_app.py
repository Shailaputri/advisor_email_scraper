import streamlit as st
from scraper.scrape_MFD_project import main
import pandas as pd
import os

st.set_page_config(page_title="Advisor Email Scraper", layout="centered")

st.title("📧 Scrape Advisor Emails")
city = st.text_input("Enter City Name:")
if st.button("Scrape Emails"):
    if city.strip() == "":
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Scraping emails..."):
            emails = main(city)

        if emails:
            df = pd.DataFrame({"Email": list(emails)})
            # ✅ Save in current directory or static folder
            os.makedirs("static", exist_ok=True)
            csv_filename = f"advisor_emails_{city}.csv"
            csv_path = os.path.join("static", csv_filename)
            df.to_csv(csv_path, index=False)

            st.success(f"✅ Found {len(emails)} emails for {city.title()}")
            with open(csv_path, "rb") as f:
                st.download_button("Download CSV", f, file_name=csv_filename)
        else:
            st.error("No emails found.")