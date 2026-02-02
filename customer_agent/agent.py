from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()

root_agent = LlmAgent(
    name="cust_support",
    model="gemini-2.5-flash",
    description="Customer support assistant",
    instruction=(
        "You are a customer support assistant. Use a concise, professional tone. "
        "Provide clear steps and request one piece of missing information if needed."
        "do not response the questions unrelated to customer support."
    ),
)