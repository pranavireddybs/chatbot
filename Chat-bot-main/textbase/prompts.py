from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

SYSTEM_PROMPT = "You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!"
system_prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
# messages
Welcome_message = "Hello! I'm your Personal Stylist 😎✨ AI. Let's find you the perfect outfit!What style of clothing do you prefer? (casual, formal, business casual, etc."
errormsg=""" Oops🥲 ! i couldnt find the style you mentioned , But you are osm✨ with\n 
Style : {style} \n
Color : {color} \n
Brand : {brand} \n
Size : {size} \n
Price : {min_price} \n
shall we try agian ? What do you pick casual agian or any other style ?"""
#questions
color_question = " ok , {style} style has various options What color do you prefer? (e.g., red, blue, green, etc.)"
brand_question = " ok , {style} style and {color} color  has various options What brand do you prefer? (e.g., Nike, Adidas, Zara etc.)"
budget_question = " May  I know the Price Ranges that your Confortable with ? (e.g., 50-100, 100-150, etc.)"
size_question = "Color and Styles are Cool for the brands {brands} but May i know the Sizes you prefer? (e.g., S, M, L, XL, etc.)"

#preference prompts

format_instructions = """
The output should be a markdown code snippet formatted 
in the following schema, including the leading and trailing "```json" and "```"""


#schemas

style_schema = ResponseSchema(
    name="style",
    description="Please describe your preferred clothing style (e.g., casual, formal, trendy, classic).",
)

color_schema = ResponseSchema(
    name="color",
    description="What is your preferd color or color range for the clothing?",
)

brand_schema = ResponseSchema(
    name="brand",
    description=" diffrent clothing brands",
)

size_schema = ResponseSchema(
    name="size",
    description="What is your clothing size (e.g., S, M, L, XL , XXL , XXXL) ",
)

price_schema = ResponseSchema(
    name="price",
    description="",
)

suggestion_schema = ResponseSchema(
    name="suggestion",
    description="suggestion that includes the style, color, brand, size, and price of the clothing.",
)

response_schemas = [style_schema, color_schema, brand_schema, size_schema, price_schema]


output_parser_style = StructuredOutputParser.from_response_schemas([style_schema])


style_template="""Form the following Conversation , extract the following information:

style : What style of clothing that the user  prefer? \
Answer the style of clothing that the user  prefer. \

The output should be a markdown code snippet formatted 
in the following schema, including the leading and trailing "```json" and "```

Conversation:

"""

color_template="""
Form the following Conversation , extract the following information:
color: what color the user prefer? \
Answer the color that the user prefer. \

The output should be a markdown code snippet formatted
in the following schema, including the leading and trailing "```json" and "```

Conversation:

"""

output_parser_color = StructuredOutputParser.from_response_schemas([color_schema])

brand_template="""
Form the following Conversation , extract the following information:
brand: what brand the user prefer? \
Answer The brands that user mentioned  \

The output should be a json  markdown code snippet formatted
in the following schema, including the leading and trailing "```json" and "```

Conversation:

"""
output_parser_brand = StructuredOutputParser.from_response_schemas([brand_schema])


size_template="""
Form the following Conversation , extract the following information:
size: what size the user prefer? \
Answer  S , M ,L , XL , XXL  The size that user mentioned  \
The output should be a json  markdown code snippet formatted
in the following schema, including the leading and trailing "```json" and "```
the Key  of json is fixed size like 
{
    "size": "S"
}
Conversation:

"""
output_parser_size = StructuredOutputParser.from_response_schemas([size_schema])

price_template="""

Form the following Conversation , extract the following information:

price: what price range the user prefer? \
minimum price :  The minimum price range that user mentioned  \
maximum price :  The maximum price range that user mentioned  \

Answer The price range that user mentioned  \

The output should be a json  markdown code snippet formatted 
including the leading and trailing "```json" and "```
should be like
{
    "price": {
        "minimum_price": 50,
        "maximum_price": 100
        }   
}

the variables are fixed minimum_price and maximum_price with a Key price
Conversation:

"""

output_parser_price = StructuredOutputParser.from_response_schemas([price_schema])

suggestion_template="""

Form the following Dictionary , extract the following information:

{res}

suggestion: Based on the Dictionary  give the all the user specified \
Answer Style , Size , Brand , price , color   \

The output should be a json  markdown code snippet formatted
including the leading and trailing "```json" and "```

Conversation:

"""

output_parser_suggestion = StructuredOutputParser.from_response_schemas([suggestion_schema])