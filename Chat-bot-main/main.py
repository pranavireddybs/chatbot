import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
from textbase import prompts
import random


# Load your OpenAI API key

models.OpenAI.api_key = "API_KEY"



# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. 
There are no specific prefixes for responses,
 so you can ask or talk about anything you like.
   The AI will respond in a natural, conversational manner.
     Feel free to start the conversation with any question or topic, 
     and let's have a pleasant chat!
"""
DATABASE = [
    {"name": "Blue Jeans", "style": "casual", "color": "blue", "brand": "Levi's", "price": 50.0},
    {"name": "White Dress Shirt", "style": "formal", "color": "white", "brand": "Calvin Klein", "price": 60.0},
    # Add more clothing items here...
]

def search_database(style, color,  brand, size,max_price, min_price):

    sizes = ["S", "M", "L", "XL", "XXL"]

    # Sample Vector database for clothing items
    vector_database = []
    for i in range(1, 101):
        item = {
            "id": i,
            "name": f"Clothing {i}",
            "info" : random.choice(["Jeans ", "Shirts", "Phants", "Dresses", "Skirts"]),
            "style": random.choice(["casual", "formal", "trendy"]),
            "description": "Cool clothing item with a nice style",
            "color": random.choice(["blue", "red", "black", "white", "green"]),
            "brand": random.choice(["Zara", "Levies", "H&M", "Calvin Klein"]),
            "size": random.choice(sizes),
            "price": random.randint(20, 10000),
        }
        vector_database.append(item)

    # Print the first 5 items in the database for demonstration purposes
    print(vector_database[:5])

    filtered_items = [
        item
        for item in vector_database
        if item["style"].lower() == style.lower()
        and item["color"].lower()== color.lower()
        and item["size"].lower()== size.lower()
        and item["price"] <= int(max_price) 
        and item["price"] >= int(min_price)
    ]
    if len(filtered_items) > 0: 
        return filtered_items
    else:
        filtered_items = vector_database[random.randint(0, len(vector_database) - 1)]


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "preferences" not in state:
        # Initial message, ask for user preferences
        bot_response = prompts.Welcome_message
        state = {"preferences": {}}
    else:
        # Extract user preferences from the state
        preferences = state["preferences"]
        if "style" not in preferences:
            res= models.OpenAI.generate(
                system_prompt=prompts.style_template,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
            bot_response = res
            bot_response = prompts.output_parser_style.parse(bot_response)
            preferences["style"] = bot_response["style"]
            bot_response = prompts.color_question.format(style=preferences["style"])
        elif "color" not in preferences:
            res= models.OpenAI.generate(
                system_prompt=prompts.color_template,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
            bot_response = prompts.output_parser_color.parse(res)
            preferences["color"] = bot_response["color"]
            bot_response = prompts.brand_question.format(style=preferences["style"], color=preferences["color"])
        elif "brand" not in preferences:
            res= models.OpenAI.generate(
                system_prompt=prompts.brand_template,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
            bot_response = prompts.output_parser_brand.parse(res)
            print(bot_response)
            preferences["brand"] = bot_response['brand']
            brand_str= ",".join(preferences["brand"])
            bot_response = prompts.size_question.format(style=preferences["style"], color=preferences["color"], brands=brand_str)
        elif "size" not in preferences:
            res= models.OpenAI.generate(
                system_prompt=prompts.size_template,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
            bot_response = prompts.output_parser_size.parse(res)
            preferences["size"] = bot_response["size"]
            bot_response = prompts.budget_question.format(style=preferences["style"], color=preferences["color"], brand=preferences["brand"])
        else:
            # All preferences collected, now search the database for recommendations
            res= models.OpenAI.generate(
                system_prompt=prompts.price_template,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
            bot_response = prompts.output_parser_price.parse(res)
            print(bot_response)
            preferences["price"] = bot_response["price"]
            recommendations = search_database(
                preferences["style"],
                preferences["color"],
                preferences["brand"],
                preferences["size"],
                preferences["price"]["minimum_price"],
                preferences["price"]["maximum_price"],
            )
            if recommendations:
                bot_response = "Based on your preferences, here are some recommendations:\n"
                print(recommendations)
                for key, value in recommendations.items():
                    if key == 'id':  # Skip the 'id' key
                        continue
                    bot_response += (
                        f"{key.capitalize()}: {value}, "  # Use key.capitalize() for style information
                    )
            else:
                res = prompts.errormsg.format(style= preferences['style'], color= preferences['color'], brand= preferences['brand'][0], size= preferences['size'], min_price= preferences['price']['minimum_price'], max_price= preferences['price']['maximum_price'])
                print(res)
                # bot_response= models.OpenAI.generate(
                #     system_prompt=prompts.suggestion_template.format(res= preferences),
                #     message_history=message_history,
                #     model="gpt-3.5-turbo",
                # )
                # bot_response = prompts.output_parser_suggestion.parse(res)

                # for key, value in preferences.items():
                #     if key == 'id':  # Skip the 'id' key
                #         continue
                #     bot_response += (
                #         f"{key.capitalize()}: {value}, "  # Use key.capitalize() for style information
                #     )

                bot_response = res
            # Clear the state to restart the conversation
            state = {"preferences": {}}

    # # Generate GPT-3.5 Turbo response
    # bot_response = models.OpenAI.generate(
    #     # system_prompt=prompts.system_prompt.messages[0].prompt.template,
    #     system_prompt=prompts.SYSTEM_PROMPT,
    #     message_history=message_history,
    #     model="gpt-3.5-turbo",
    # )

    return bot_response, state


