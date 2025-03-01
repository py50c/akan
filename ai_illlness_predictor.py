import sys
import os
import time
import google.generativeai as genai
from colorama import Fore, Style, init

init()


# Set the API key

API_KEY = "YOUR_API_KEY_HERE"
if not API_KEY:
  raise ValueError("Api key not found!")

genai.configure(api_key = API_KEY)
#Create the model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.7,
  "top_k": 40,
  "max_output_tokens":500,
}
model = genai.GenerativeModel(
  model_name = "gemini-1.5-flash",
  generation_config = generation_config,
  system_instruction =  ("You are an experienced medical assistant specializing in illness prediction. "
    "Given a list of symptoms, provide possible illnesses and suggest relevant follow-up questions "
    "to refine the diagnosis. Ensure the illnesses are closely related to the symptoms provided. "
    "Keep responses professional, medically accurate, and under 60 words."
)
)
chat_session = model.start_chat(
  history = []
  )

def typing_effect(text, delay=0.03):
    """Simulates typing effect for better presentation."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to next line



def get_illness_prediction(symptoms):
  try:
    response = chat_session.send_message(symptoms)
    return response.text
  except Exception as e:
    return f"{Fore.RED}Error: {e}{Style.RESET_ALL}"


# Display chatbot header
print(Fore.YELLOW + "=" * 50)
print(Fore.CYAN + "  ðŸ¤– Medical Assistant Chatbot  ")
print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

print("Type 'exit' to end the conversation.\n")


# Real-time conversation loop

while True:
    user_input = input(Fore.CYAN + "You: " + Style.RESET_ALL)

    if user_input.lower() == "exit":
        print(Fore.YELLOW + "\nChat ended. Thank you! ðŸ¤–" + Style.RESET_ALL)
        break

    print(Fore.GREEN + "Bot is thinking...âŒ›" + Style.RESET_ALL)
    response = get_illness_prediction(user_input)

    # Display response with typing effect
    print(Fore.GREEN + "Bot: ", end="")
    typing_effect(response)

    # Handle follow-up questions
    while "follow-up" in response.lower():
        user_input = input(Fore.CYAN + "You (Follow-up Answer): " + Style.RESET_ALL)
        if user_input.lower() == "exit":
            print(Fore.YELLOW + "\nChat ended. Thank you! ðŸ¤–" + Style.RESET_ALL)
            exit()
        print(Fore.GREEN + "Bot is thinking...âŒ›" + Style.RESET_ALL)
        response = get_illness_prediction(user_input)

        print(Fore.GREEN + "Bot: ", end="")
        typing_effect(response)
