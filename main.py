
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate


_ = load_dotenv(find_dotenv())

# Initialize the OpenAI GPT-4 language model
# OpenAIGPT4 = ChatOpenAI(
#     model="gpt-4"
# )

LLM = ChatGroq(temperature=0.7, model="llama3-70b-8192")

delimiter = "####"
system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
    'category': <one of Computers and Laptops, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, 
    Audio Equipment, Cameras and Camcorders>,
OR
    'products': <a list of products that must \
    be found in the allowed products below>

Where the categories and products must be found in \
the customer service query.
If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list.

Allowed products: 

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

Only output the list of objects, with nothing else.
"""
user_message_1 = f"""
 tell me about the smartx pro phone and \
 the fotosnap camera, the dslr one. \
 Also tell me about your tvs """


def get_input() -> str:
 print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
 contents = []
 while True:
  try:
   line = input()
  except EOFError:
   break
  if line == "q":
   break
  contents.append(line)
 return "\n".join(contents)

def get_completion_from_messages(system_message, user_message):
 messages = [
  ("system", system_message),
  ('human', f"{delimiter}{user_message}{delimiter}"),
 ]
 prompt = ChatPromptTemplate.from_messages(messages)

 chain = prompt | LLM
 response = chain.invoke({})
 return response.content


user_input = get_input() #"tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
response = get_completion_from_messages(system_message, user_input)
print(response)

