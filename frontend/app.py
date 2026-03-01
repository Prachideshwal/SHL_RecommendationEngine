import streamlit as st
import requests

st.title("SHL Assessment Recommendation Engine")

query = st.text_input("Enter job role or skills:")

if st.button("Get Recommendations"):

    response = requests.post(
        "phttps://recommendationengine-backend.onrender.com/recommend",
        json={"query": query}
    )

    if response.status_code == 200:

        data = response.json()

        st.subheader("Recommended Assessments")

        for r in data["recommendations"]:

            st.write("Assessment:", r["assessment_name"])
            st.write("URL:", r["assessment_url"])
            st.write("Confidence:", f"{r['confidence_percentage']}%")
            st.write("Explanation:", r["explanation"])
            st.write("---")

    else:
        st.error("API Error")