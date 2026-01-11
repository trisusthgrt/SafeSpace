# from langchain.agents import tool
# from tools import query_medgemma, call_emergency

# @tool
# def ask_mental_health_specialist(query: str) -> str:
#     """
#     Generate a therapeutic response using the MedGemma model.
#     Use this for all general user queries, mental health questions, emotional concerns,
#     or to offer empathetic, evidence-based guidance in a conversational tone.
#     """
#     return query_medgemma(query)


# @tool
# def emergency_call_tool() -> None:
#     """
#     Place an emergency call to the safety helpline's phone number via Twilio.
#     Use this only if the user expresses suicidal ideation, intent to self-harm,
#     or describes a mental health emergency requiring immediate help.
#     """
#     call_emergency()


# @tool
# def find_nearby_therapists_by_location(location: str) -> str:
#     """
#     Finds and returns a list of licensed therapists near the specified location.

#     Args:
#         location (str): The name of the city or area in which the user is seeking therapy support.

#     Returns:
#         str: A newline-separated string containing therapist names and contact info.
#     """
#     return (
#         f"Here are some therapists near {location}, {location}:\n"
#         "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
#         "- Dr. James Patel - +1 (555) 987-6543\n"
#         "- MindCare Counseling Center - +1 (555) 222-3333"
#     )


# # Step1: Create an AI Agent & Link to backend
# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
# from config import OPENAI_API_KEY


# tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
# llm = ChatOpenAI(model="gpt-4", temperature=0.2, api_key=OPENAI_API_KEY)
# graph = create_react_agent(llm, tools=tools)

# SYSTEM_PROMPT = """
# You are an AI engine supporting mental health conversations with warmth and vigilance.
# You have access to three tools:

# 1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
# 2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
# 3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

# Always take necessary action. Respond kindly, clearly, and supportively.
# """

# def parse_response(stream):
#     tool_called_name = "None"
#     final_response = None

#     for s in stream:
#         # Check if a tool was called
#         tool_data = s.get('tools')
#         if tool_data:
#             tool_messages = tool_data.get('messages')
#             if tool_messages and isinstance(tool_messages, list):
#                 for msg in tool_messages:
#                     tool_called_name = getattr(msg, 'name', 'None')

#         # Check if agent returned a message
#         agent_data = s.get('agent')
#         if agent_data:
#             messages = agent_data.get('messages')
#             if messages and isinstance(messages, list):
#                 for msg in messages:
#                     if msg.content:
#                         final_response = msg.content

#     return tool_called_name, final_response


# """if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED: ", tool_called_name)
#         print("ANSWER: ", final_response)"""
        
from tools import query_medgemma, call_emergency
import re

SYSTEM_PROMPT = """
You are a compassionate AI mental health assistant.
Always respond with empathy and encourage professional help when appropriate.
"""

# ---------------- SAFETY ROUTER ----------------

def detect_crisis(text: str) -> bool:
    crisis_keywords = [
        "suicide", "kill myself", "end my life",
        "self harm", "hurt myself", "no reason to live"
    ]
    text = text.lower()
    return any(k in text for k in crisis_keywords)


def detect_location_request(text: str) -> bool:
    return "therapist" in text.lower() or "near me" in text.lower()


def find_nearby_therapists_by_location(location: str) -> str:
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


# ---------------- MAIN AGENT FUNCTION ----------------

def run_agent(user_input: str):
    # 🚨 Emergency first (deterministic & safe)
    if detect_crisis(user_input):
        call_emergency()
        return "emergency_call_tool", (
            "I'm really glad you reached out. "
            "Your safety matters, and I've contacted emergency support to help you right now. "
            "You're not alone."
        )

    # 📍 Therapist lookup
    if detect_location_request(user_input):
        return "find_nearby_therapists_by_location", find_nearby_therapists_by_location("your area")

    # 🧠 Default: MedGemma therapy
    response = query_medgemma(user_input)
    return "ask_mental_health_specialist", response
