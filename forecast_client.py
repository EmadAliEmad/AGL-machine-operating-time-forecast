import requests
import json
import base64
from PIL import Image
import io

def get_forecast(eqp_ids, forecast_type, forecast_period):
    url = 'http://127.0.0.1:8000/forecast'
    payload = {
        "eqp_ids": eqp_ids,
        "forecast_type": forecast_type,
        "forecast_period": forecast_period
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        response_json = response.json()
        image_base64 = response_json['forecast_image']
        image_data = base64.b64decode(image_base64)
        
        # Save image
        with open('forecast_graph.png', 'wb') as f:
            f.write(image_data)
        
        # Display image
        image = Image.open(io.BytesIO(image_data))
        image.show()
        
        print("Forecast graph saved as 'forecast_graph.png' and displayed.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Example usage
get_forecast(["CR1"], "weeks", 12)