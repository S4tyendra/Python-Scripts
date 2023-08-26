from chatterbot import ChatBot
from chatterbot.logic import MathematicalEvaluation
from chatterbot.storage import SQLStorageAdapter

# Create a ChatBot instance for the calculator
calculator_bot = ChatBot(
    'Calculator',
    logic_adapters=[MathematicalEvaluation()],
    storage_adapter=SQLStorageAdapter()  # You can set the database path here
)

# Clear the screen and start the calculator
print('\033c')
print("Hello, I am a calculator. How may I help you? Type 'quit' to exit.")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'quit':
        print("Exiting")
        break

    try:
        response = calculator_bot.get_response(user_input)
        print("Calculator:", response)
    except Exception as e:
        print("Calculator: An error occurred. Please enter valid input.")
