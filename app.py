import streamlit as st
import os
import config
from utils.test_generator import extract_typescript_block, write_new_test_spec_file
from utils.agent_utils import get_llm_response, run_ai_agent
from utils.git_utils import fetch_and_pull_master
from utils.playwright_utils import get_test_files, run_playwright_test
from utils.ui_helpers import apply_custom_styles, render_title, render_footer

# Page Configuration
st.set_page_config(
    page_title="TMRW QA AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Apply Custom Styles
apply_custom_styles()

# Render Title
render_title()

# Sidebar Configuration
st.sidebar.header("🔑 API Key Configuration")
openai_api_key: str = st.sidebar.text_input("Enter OpenAI API Key", type="password", value=config.OPENAI_API_KEY)

st.sidebar.header("🌍 Test Environment")
base_url: str = st.sidebar.text_input("Base URL", value=config.DEFAULT_BASE_URL)

st.sidebar.header("🔐 Room3D / Aired.tv Credentials")
room3d_email: str = st.sidebar.text_input("Room3D / Aired.tv Email", value=config.DEFAULT_EMAIL)
room3d_password: str = st.sidebar.text_input("Room3D / Aired.tv Password", type="password", value=config.DEFAULT_PASSWORD)

st.sidebar.header("🛠 AI Assistant Config")
generate_test = st.sidebar.checkbox('Generate Playwright Test')

# Tabs
tab1, tab2 = st.tabs(["🔍 AI Assistant", "📂 Playwright Test Explorer"])

# ---- TAB 1: AI Assistant ----
with tab1:
    autogen_complete = False
    st.markdown("<p class='subheader'>📌 Enter Your Test Scenario</p>", unsafe_allow_html=True)
    user_prompt = f"BASE_URL={base_url}\n"
    user_prompt = user_prompt + st.text_area(
        "Describe your test scenario in detail:", 
        height=150, 
        placeholder="e.g:\nGiven a logged-in user is on the meet page of Room3D\nWhen they schedule a meeting for tomorrow in the Art Library Room\nThen the scheduled meeting card will be displayed with the correct information."
    )

    if st.button("🚀 Initiate Test!"):
        with st.spinner(text="AI Browser Test In progress...", show_time=False):
            result: str = run_ai_agent(user_prompt, openai_api_key)

        with open(config.POM_CODE_PATH, "r") as file:
            pomCode = file.read()

        with open(config.PLAYWRIGHT_TS_CODE_GEN, "r") as file:
            playwright_code_gen = file.read()
        
        updated_content = playwright_code_gen.replace("{json_file_content}", result)
        updated_content = updated_content.replace("{pom_code}", pomCode)

        if generate_test:
            with st.spinner(text="Generating Playwright Test Case...", show_time=False):
                response = get_llm_response(updated_content, openai_api_key)
                complete_playwright_test = extract_typescript_block(response)

            write_new_test_spec_file(response)

            generate = st.subheader("✅ AI-Generated Test Output")
            st.code(complete_playwright_test, "typescript")

# ---- TAB 2: Playwright Test Explorer ----
with tab2:
    st.subheader("📂 Select a Playwright Test File to Run")

    test_directory = os.path.join(config.TESTS_DIR)
    
    if os.path.exists(test_directory):
        test_files = get_test_files(test_directory)

        if test_files:
            selected_test: str = st.selectbox("Choose a test file to execute:", test_files)
            
            # Create two columns for buttons (side-by-side)
            col1, col2 = st.columns([1, 1])

            # Persistent log container
            log_container = st.container()

            with col1:
                if st.button("▶️ Run Selected Test"):
                    run_playwright_test(os.path.join(test_directory, selected_test), base_url, room3d_email, room3d_password, log_container)

            with col2:
                if st.button("▶️ Run All Tests"):
                    run_playwright_test(test_directory, base_url, room3d_email, room3d_password, log_container)

        else:
            st.warning("⚠️ No Playwright test files found in the 'tests' directory.")
    else:
        st.warning("⚠️ The `tests` directory does not exist.")

    # Add Git Fetch & Pull Button
    st.markdown("<p class='subheader'>🔄 Sync your repo with master to get updates</p>", unsafe_allow_html=True)
    if st.button("🔄 Fetch & Pull Master"):
        fetch_and_pull_master()

# Render Footer
render_footer()
