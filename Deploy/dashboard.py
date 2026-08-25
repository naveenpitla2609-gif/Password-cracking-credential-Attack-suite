import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Security Suite Dashboard", layout="wide")
st.title("🛡️ Password Cracking & Credential Attack Suite Dashboard")
st.write("---")

# Sidebar navigation menu create cheskodaniki
choice = st.sidebar.selectbox("Go to Module", [
    "1. Dictionary Generator",
    "2. Brute-Force Simulator",
    "3. Password Strength Analyzer"
])

if choice == "1. Dictionary Generator":
    st.header("📂 Dictionary Generator Module")
    st.write("Click below to run the wordlist script.")
    if st.button("Generate Wordlist"):
        with st.spinner("Running Dictionary Generator..."):
            # Folder dynamic path matching setup
            path = "Dictionary_Generator/dictionary_generator.py"
            if os.path.exists(path):
                res = subprocess.run(["python", path], capture_output=True, text=True)
                st.success("Execution Complete!")
                st.code(res.stdout if res.stdout else "Script executed successfully with local updates.")
            else:
                st.error(f"File not found at: {path}")

elif choice == "2. Brute-Force Simulator":
    st.header("⚡ Brute-Force Simulator Module")
    st.write("This initiates automated simulated structural attack logs.")
    if st.button("Start Brute Force Simulation"):
        with st.spinner("Analyzing parameters..."):
            path = "Bruite_Force_Simulator/brute_force.py"
            if os.path.exists(path):
                res = subprocess.run(["python", path], capture_output=True, text=True)
                st.success("Simulation Complete!")
                st.code(res.stdout)
            else:
                st.error(f"File not found at: {path}")

elif choice == "3. Password Strength Analyzer":
    st.header("🧠 Password Strength Evaluation")
    user_pass = st.text_input("Enter a password to test security strength:", "kali123@")
    if st.button("Analyze Password"):
        with st.spinner("Analyzing risk layers..."):
            path = "Password_Strength_Analyzer/compliance_engine.py"
            if os.path.exists(path):
                res = subprocess.run(["python", path], input=user_pass, capture_output=True, text=True)
                st.success("Analysis Complete!")
                st.code(res.stdout)
            else:
                st.error(f"Engine path missing: {path}")