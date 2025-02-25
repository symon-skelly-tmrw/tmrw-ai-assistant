import os
import subprocess
import streamlit as st
import re
from typing import List, Optional

def get_test_files(directory: str) -> List[str]:
    """ Recursively fetch all .spec.ts files inside the tests directory and return them in a list. """
    test_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".spec.ts"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                test_files.append(relative_path)
    return test_files

def clean_log_line(line: str) -> str:
    """ Cleans and formats the log line by removing unwanted characters and adding a new line after every '›' """
    match = re.search(r'(\[chromium\].*)', line)
    if not match:
        return line.strip()
    
    log_text = match.group(1)
    formatted_log = "\n".join(log_text.split(" › "))
    return formatted_log

def run_playwright_test(test_path: str, base_url: str, email: str, password: str, log_container) -> None:
    """ Executes a Playwright test with the provided environment variables and updates logs in real-time. """
    try:
        if not base_url.strip():
            st.warning("⚠️ Please enter a valid Base URL in the sidebar before running the test.")
            return
        if not email.strip() or not password.strip():
            st.warning("⚠️ Please enter user Email and Password in the sidebar for the environment you wish to use.")
            return

        command = f"EMAIL={email} PASSWORD={password} BASE_URL={base_url} npx playwright test {test_path} --headed"

        # Keep the log title persistent
        with log_container:
            st.subheader("📡 Test Execution Logs")
            log_area = st.empty()

        # Run Playwright test and capture output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            cleaned_line = clean_log_line(line)
            log_area.text(cleaned_line)  # Update logs dynamically with formatted output

        process.stdout.close()
        process.wait()

        log_area.markdown(f"""
        ✅ **Test Execution Completed!**  
        **Base Url:** `{base_url}`  
        **Email:** `{email}`
        """)

    except Exception as e:
        log_area.error(f"❌ Failed to execute Playwright test: {e}")