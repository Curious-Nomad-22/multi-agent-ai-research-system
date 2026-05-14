import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔍",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stTextInput input {
    border-radius: 10px;
    padding: 12px;
}

.report-box {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.2);
    margin-top: 20px;
    line-height: 1.8;
    background-color: transparent;
}

.title-style {
    font-size: 42px;
    font-weight: bold;
}

.subtitle-style {
    opacity: 0.7;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    '<p class="title-style">🔍 Multi-Agent AI Research System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle-style">AI-powered startup and market intelligence dashboard</p>',
    unsafe_allow_html=True
)

# =========================
# INPUT SECTION
# =========================

query = st.text_input(
    "Enter your research topic",
    placeholder="Example: Top AI healthcare startups in India"
)

# =========================
# BUTTON
# =========================

if st.button("🚀 Start Research"):

    if query.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    # =========================
    # LOADING
    # =========================

    with st.spinner("Research agents are analyzing data..."):

        try:

            # =========================
            # API REQUEST
            # =========================

            response = requests.get(
                "http://127.0.0.1:8000/research",
                params={"query": query}
            )

            # =========================
            # CHECK STATUS
            # =========================

            if response.status_code != 200:
                st.error(f"Backend Error: {response.status_code}")
                st.stop()

            data = response.json()

            # =========================
            # PLAN
            # =========================

            st.subheader("📌 Research Plan")

            st.markdown(data["plan"])

            # =========================
            # REPORT
            # =========================

            st.subheader("📊 Final Research Report")

            report = data["report"]

            st.markdown(
                f"""
                <div class="report-box">
                {report}
                </div>
                """,
                unsafe_allow_html=True
            )

            # =========================
            # SUCCESS MESSAGE
            # =========================

            st.success("Research completed successfully.")

        except Exception as e:

            st.error(f"Error: {e}")