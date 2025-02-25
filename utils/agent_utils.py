import asyncio
import json
from openai import OpenAI
import requests
import time
from pathlib import Path
from browser_use import Agent, Browser, BrowserContextConfig
from langchain_openai import ChatOpenAI
from browser_use.browser.context import BrowserContext
import config
from utils.auth_utils import get_api_url

# Define the path for cookies.json
COOKIES_FILE = Path("cookies.json")

with open(config.ROOM3D_AUTH_PATH, "r") as file:
    auth_prompt = file.read()

def authenticate_via_api() -> str:
    """Logs in via API and returns an authentication token."""
    
    API_URL = get_api_url(config.DEFAULT_BASE_URL)
    payload = {
        "msgType": 1719641397,
        "cmd": "login",
        "password": config.DEFAULT_PASSWORD,
        "username": config.DEFAULT_EMAIL,
        "keepMeLoggedIn": True,
        "date": int(time.time() * 1000)
    }

    api_url = f"{API_URL}/user"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Extract authToken from response
        data = response.json()
        auth_token = data.get("loggedInUser", {}).get("authToken")

        if not auth_token:
            raise Exception("Authentication token not found in response.")

        # Save cookies to file
        save_cookies_to_file(auth_token)

        return auth_token

    except requests.exceptions.RequestException as e:
        raise Exception(f"Authentication failed: {e}")

def save_cookies_to_file(auth_token: str) -> None:
    """Saves the auth token in a JSON file for persistent authentication."""
        
    import time

    # Calculate expiration time (1 year from now)
    expires = int(time.time()) + (365 * 24 * 60 * 60)  # 1 year in seconds

    cookies = [{
        "name": "authToken",
        "value": auth_token,
        "domain": config.DEFAULT_BASE_URL.replace("https://", ""),
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "None",
        "date": 1727647200000
    }]

    with open(COOKIES_FILE, "w") as file:
        json.dump(cookies, file, indent=4)

def run_ai_agent(user_prompt: str, openai_api_key: str) -> str:
    """Runs the AI Agent to generate a test script based on the user prompt."""
    
    authenticate_via_api()

    # Load cookies from file
    browser_config = BrowserContextConfig(
        cookies_file=str(COOKIES_FILE)  # ✅ Load cookies from saved file
    )

    # Create browser and context
    browser = Browser()
    context = BrowserContext(browser=browser, config=browser_config)

    agent = Agent(
        task=f"{user_prompt}{auth_prompt}",
        llm=ChatOpenAI(
            model='gpt-4o',
            api_key=openai_api_key
        ),
        use_vision=False,
        max_failures=2,
        max_actions_per_step=5,
        save_conversation_path="logs/conversation.json",
        browser_context=context
    )

    # Use asyncio to run the agent
    return str(asyncio.run(agent.run()))

def get_llm_response(user_prompt: str, openai_api_key: str):

    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        stream=False
    )

    return str(response.choices[0].message.content)
