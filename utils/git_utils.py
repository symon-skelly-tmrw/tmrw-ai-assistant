# utils/git_utils.py
import subprocess
import streamlit as st

def fetch_and_pull_master() -> None:
    """ Fetches and pulls the latest changes from the master branch. """
    try:
        status_placeholder = st.empty()
        status_placeholder.info("Fetching latest updates from the repository...")

        # Run git fetch
        fetch_process = subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
        st.text(fetch_process.stdout)

        # Run git pull
        pull_process = subprocess.run(["git", "pull", "origin", "master"], capture_output=True, text=True)
        st.text(pull_process.stdout)

        status_placeholder.empty()
        st.success("✅ Successfully pulled the latest changes from master!")

    except Exception as e:
        status_placeholder.empty()
        st.error(f"❌ Failed to fetch & pull master: {e}")
