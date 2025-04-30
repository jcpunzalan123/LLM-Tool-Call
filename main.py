import ollama
import requests
import yfinance as yf


def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.info.get('regularMarketPrice') or ticker.fast_info.last_price


def get_current_weather(city):
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"


available_functions = {'get_stock_price': get_stock_price,
                       'get_current_weather': get_current_weather}


prompt = "what is the temperature in Manila?"

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{'role': 'user', 'content': prompt}],
    tools=[get_stock_price, get_current_weather]
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function: ', tool.function.name)
            print('Arguments: ', tool.function.arguments)
            print('Function output: ', function_to_call(**tool.function.arguments))

        else:
            print('Function', tool.function.name, 'not found')
