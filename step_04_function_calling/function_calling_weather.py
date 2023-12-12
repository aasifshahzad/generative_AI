from openai.types.chat.chat_completion import ChatCompletion,ChatCompletionMessage
from IPython.display import display  # Assuming you are using IPython
from typing import Optional, List, Tuple, Dict
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from openai import OpenAI
import requests
import json

_ : bool = load_dotenv("E:/Python/.env")
client: OpenAI = OpenAI()
#___________________________________________

# Get Latitude and Longitude of the City
def get_lat_long_from_city(city_name: str, count: int = 1, language: str = 'en', format: str = 'json') -> Optional[Tuple[float, float]]:
    api_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city_name,
        'count': count,
        'language': language,
        'format': format
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        result = response.json()
        if result:
            longitude = result['results'][0]['longitude']
            latitude = result['results'][0]['latitude']
            return float(longitude), float(latitude)
        else:
            print(f"Error: Unable to retrieve coordinates. API response: {result}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

#___________________________________________

#Get Weather Forecast and print results using API
def get_weather_forecast(latitude: float, longitude: float) -> Optional[dict]:
    api_url = "https://api.open-meteo.com/v1/forecast"
    
    # Define parameters for the API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
    }

    try:
        # Make a GET request to the API
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and return the JSON data from the response
            return response.json()
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        # Handle exceptions, e.g., network issues
        print(f"Exception: {e}")
        return None

#_______________________________________
#Get Current Weather using above two functions
def get_current_weather(city_name: str) -> str:
    Longitude , Latitude = get_lat_long_from_city(city_name)
    forecast_data = get_weather_forecast(Latitude, Longitude)
    # Prepare data for JSON dump
    result: Dict[str, Dict] = {}
    # Check if forecast_data is available
    if forecast_data:
        result["Location Data"] = {
            "Latitude": Latitude,
            "Longitude": Longitude,
            "Elevation": forecast_data.get('elevation'),
            "Timezone": forecast_data.get('timezone'),
            "Date": datetime.now().date().strftime("%d-%m-%Y"),
            "Time": datetime.now().time().strftime("%H:%M:%S")
        }
    else:
        print("Failed to retrieve Location Data.")

    current_data = forecast_data.get('current', {})
    if current_data:
        result["Current Weather Update"] = {
            "Temperature": current_data.get('temperature_2m'),
            "Relative Humidity": current_data.get('relative_humidity_2m'),
            "Is Day": 'Day' if current_data.get('is_day') else 'Night',
            "Surface Pressure": current_data.get('surface_pressure'),
            "Wind Speed": current_data.get('wind_speed_10m'),
            "Wind Direction": current_data.get('wind_direction_10m'),
            "Wind Gusts": current_data.get('wind_gusts_10m')
        }
    else:
        print("Failed to retrieve weather forecast.")

    # Dump the result as JSON
    return json.dumps(result, indent=4)

#_______________________________________________

#Calling OpenAI run_conversation in Function calling process
def run_conversation(main_request: str)->str:
    #Step 1 send the conversation and available function to the model
    messages = [
        {
            "role": "user",
            "content": main_request,
        }
    ]
    
    tools = [
        #Function description for "get_lat_long_from_city" :
        {
            "type": "function",
            "function": {
                "name": "get_lat_long_from_city",
                "description": "Get the latitude and longitude coordinates for a given city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The name of the city for which coordinates are requested."
                        },
                        "count": {
                            "type": "integer",
                            "description": "The number of results to retrieve (default is 1)."
                        },
                        "language": {
                            "type": "string",
                            "description": "The language for the response (default is 'en')."
                        },
                        "format": {
                            "type": "string",
                            "description": "The format of the response (default is 'json')."
                        }
                    },
                    "required": ["city_name"]
                },
                "return": {
                    "type": "tuple",
                    "items": [
                        {"type": "float", "description": "Longitude coordinate."},
                        {"type": "float", "description": "Latitude coordinate."}
                    ],
                    "description": "Returns a tuple containing the longitude and latitude coordinates. Returns None in case of an error."
                }
            }
        },
        #Function description for "get_weather_forecast" :
        {
            "type": "function",
            "function": {
                "name": "get_weather_forecast",
                "description": "Get the weather forecast for a given location based on latitude and longitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        # "latitude": {
                        #     "type": "float",
                        #     "description": "The latitude coordinate of the location."
                        # },
                        # "longitude": {
                        #     "type": "float",
                        #     "description": "The longitude coordinate of the location."
                        # }
                        "latitude": {
                            "type": "string",
                            "format": "float",  # Use "format" to specify the type
                            "description": "The latitude coordinate of the location."
                        },
                        "longitude": {
                            "type": "string",
                            "format": "float",  # Use "format" to specify the type
                            "description": "The longitude coordinate of the location."
                        }
                    },
                    "required": ["latitude", "longitude"]
                },
                "return": {
                    "type": "object",
                    "description": "Returns a dictionary containing various weather forecast parameters. Returns None in case of an error.",
                    "example": {
                        "temperature_2m": 25.0,
                        "relative_humidity_2m": 60,
                        "apparent_temperature": 26.5,
                        "is_day": True,
                        "weather_code": "partly_cloudy_day",
                        "pressure_msl": 1013.2,
                        "surface_pressure": 1011.5,
                        "wind_speed_10m": 5.0,
                        "wind_direction_10m": 120,
                        "wind_gusts_10m": 8.0
                    }
                }
            }
        },
        #Function description for "get_current_weather" :
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather data for a given city, including location details and weather updates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The name of the city for which weather data is requested."
                        }
                    },
                    "required": ["city_name"]
                },
                "return": {
                    "type": "string",
                    "description": "Returns a JSON-formatted string containing location details and current weather updates. Returns an empty string if data retrieval fails.",
                    "example": """
                        {
                            "Location Data": {
                                "Latitude": 37.7749,
                                "Longitude": -122.4194,
                                "Elevation": 60.0,
                                "Timezone": "America/Los_Angeles",
                                "Date": "12-02-2023",
                                "Time": "14:30:00"
                            },
                            "Current Weather Update": {
                                "Temperature": 20.5,
                                "Relative Humidity": 75,
                                "Is Day": "Day",
                                "Surface Pressure": 1012.3,
                                "Wind Speed": 5.0,
                                "Wind Direction": 150,
                                "Wind Gusts": 8.0
                            }
                        }
                        """
                }
            }
        }
    ]
    
    # First Request
    response: ChatCompletion = client.chat.completions.create(
        model= "gpt-3.5-turbo-1106",
        messages= messages,
        tools= tools,
        tool_choice= "auto", # auto is default, but we'll be explicit
    )
    response_message: ChatCompletion = response.choices[0].message
    display(" *First Response: ", dict(response_message))
    
    tool_calls = response_message.tool_calls
    display("* First Response Tool Calls: ", list(tool_calls))
    
    #Step 2 Check if the model want to call a function
    if tool_calls:
        #Step 3 Call the function
        #Note: The JSON response may not always be valid, be sure to handle errors
        available_functions = {
            "get_lat_long_from_city": get_lat_long_from_city,
            "get_weather_forecast": get_weather_forecast,
            "get_current_weather": get_current_weather,
        }
        
    #Step 4 Send the info for each function call and function response to the model
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # Mapping function arguments dynamically

            function_args_mapping = {
                "get_lat_long_from_city": {
                    "city_name": None,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
                "get_weather_forecast": {
                    "latitude": None,
                    "longitude": None,
                },
                "get_current_weather": {
                    "city_name": None,
                },
            }

            # Get the corresponding function_args
            function_args = function_args_mapping.get(function_name, {})

            # Check if tool_call.function.arguments is a JSON-formatted string
            try:
                parsed_arguments = json.loads(tool_call.function.arguments)
                # Update function_args with parsed arguments
                function_args.update(parsed_arguments)
            except json.JSONDecodeError:
                print("Error parsing JSON from tool_call.function.arguments")
                        
            # Call the function with dynamically obtained arguments
            function_response = function_to_call(**function_args)
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
    display("* Second Request Message: ", list(messages))
            
    print("Messages before second API call:", messages)
            
    second_response: ChatCompletion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )
            
    print("* Second Response: ", dict(second_response))
    return second_response.choices[0].message.content
    #Step 1 send the conversation and available function to the model
    messages = [
        {
            "role": "user",
            "content": main_request,
        }
    ]
    
    tools = [
        #Function description for "get_lat_long_from_city" :
        {
            "type": "function",
            "function": {
                "name": "get_lat_long_from_city",
                "description": "Get the latitude and longitude coordinates for a given city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The name of the city for which coordinates are requested."
                        },
                        "count": {
                            "type": "integer",
                            "description": "The number of results to retrieve (default is 1)."
                        },
                        "language": {
                            "type": "string",
                            "description": "The language for the response (default is 'en')."
                        },
                        "format": {
                            "type": "string",
                            "description": "The format of the response (default is 'json')."
                        }
                    },
                    "required": ["city_name"]
                },
                "return": {
                    "type": "tuple",
                    "items": [
                        {"type": "float", "description": "Longitude coordinate."},
                        {"type": "float", "description": "Latitude coordinate."}
                    ],
                    "description": "Returns a tuple containing the longitude and latitude coordinates. Returns None in case of an error."
                }
            }
        },
        #Function description for "get_weather_forecast" :
        {
            "type": "function",
            "function": {
                "name": "get_weather_forecast",
                "description": "Get the weather forecast for a given location based on latitude and longitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "float",
                            "description": "The latitude coordinate of the location."
                        },
                        "longitude": {
                            "type": "float",
                            "description": "The longitude coordinate of the location."
                        }
                    },
                    "required": ["latitude", "longitude"]
                },
                "return": {
                    "type": "object",
                    "description": "Returns a dictionary containing various weather forecast parameters. Returns None in case of an error.",
                    "example": {
                        "temperature_2m": 25.0,
                        "relative_humidity_2m": 60,
                        "apparent_temperature": 26.5,
                        "is_day": True,
                        "weather_code": "partly_cloudy_day",
                        "pressure_msl": 1013.2,
                        "surface_pressure": 1011.5,
                        "wind_speed_10m": 5.0,
                        "wind_direction_10m": 120,
                        "wind_gusts_10m": 8.0
                    }
                }
            }
        },
        #Function description for "get_current_weather" :
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather data for a given city, including location details and weather updates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The name of the city for which weather data is requested."
                        }
                    },
                    "required": ["city_name"]
                },
                "return": {
                    "type": "string",
                    "description": "Returns a JSON-formatted string containing location details and current weather updates. Returns an empty string if data retrieval fails.",
                    "example": """
                        {
                            "Location Data": {
                                "Latitude": 37.7749,
                                "Longitude": -122.4194,
                                "Elevation": 60.0,
                                "Timezone": "America/Los_Angeles",
                                "Date": "12-02-2023",
                                "Time": "14:30:00"
                            },
                            "Current Weather Update": {
                                "Temperature": 20.5,
                                "Relative Humidity": 75,
                                "Is Day": "Day",
                                "Surface Pressure": 1012.3,
                                "Wind Speed": 5.0,
                                "Wind Direction": 150,
                                "Wind Gusts": 8.0
                            }
                        }
                        """
                }
            }
        }
    ]
    
    # First Request
    response: ChatCompletion = client.chat.completions.create(
        model= "gpt-3.5-turbo-1106",
        messages= messages,
        tools= tools,
        tool_choice= "auto", # auto is default, but we'll be explicit
    )
    response_message: ChatCompletion = response.choices[0].message
    display(" *First Response: ", dict(response_message))
    
    tool_calls = response_message.tool_calls
    display("* First Response Tool Calls: ", list(tool_calls))
    
    #Step 2 Check if the model want to call a function
    if tool_calls:
        #Step 3 Call the function
        #Note: The JSON response may not always be valid, be sure to handle errors
        available_functions = {
            "get_lat_long_from_city": get_lat_long_from_city,
            "get_weather_forecast": get_weather_forecast,
            "get_current_weather": get_current_weather,
        }
        
    #Step 4 Send the info for each function call and function response to the model
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # Mapping function arguments dynamically
            function_args_mapping = {
                "get_lat_long_from_city": {
                    "city_name": tool_call.function.arguments.get("city_name"),
                    "count": tool_call.function.arguments.get("count", 1),
                    "language": tool_call.function.arguments.get("language", "en"),
                    "format": tool_call.function.arguments.get("format", "json"),
                },
                "get_weather_forecast": {
                    "latitude": tool_call.function.arguments.get("latitude"),
                    "longitude": tool_call.function.arguments.get("longitude"),
                },
                "get_current_weather": {
                    "city_name": tool_call.function.arguments.get("city_name"),
                },
            }

            # Get the corresponding function_args
            function_args = function_args_mapping.get(function_name, {})

            # Call the function with dynamically obtained arguments
            function_response = function_to_call(**function_args)
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
    display("* Second Request Message: ", list(messages))
            
    print("Messages before second API call:", messages)
            
    second_response: ChatCompletion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )
            
    print("* Second Response: ", dict(second_response))
    return second_response.choices[0].message.content

#_______________________________________________
run_conversation("What's the weather like in Islamabad?")
run_conversation("What's the weather like in new york?")
run_conversation("What is current temperature in karachi?")
run_conversation("what is uv index in karachi?")