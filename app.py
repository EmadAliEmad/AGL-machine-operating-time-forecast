# FastAPI application code for forecasting machine operating time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List, Literal
import io
import base64
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

app = FastAPI()

# Load your model and scaler here
model = joblib.load("model.pkl")  # Load using joblib
scaler = joblib.load("scaler.pkl")
data = pd.read_csv("Machine_Data.csv")
data['Last_Move_Eqp_Dt_YearMonthDay'] = pd.to_datetime(data['Last_Move_Eqp_Dt_YearMonthDay'])

class ForecastRequest(BaseModel):
    eqp_ids: List[str]   # Limit to 1-5 equipment IDs
    forecast_type: Literal['days', 'weeks']
    forecast_period: int

@app.post("/forecast")
async def forecast(request: ForecastRequest):
    try:
        # Input validation
        if request.forecast_period <= 0 or request.forecast_period > 52:
            raise HTTPException(status_code=400, detail="Forecast period must be between 1 and 52")
        
        # Filter data for requested equipment IDs
        filtered_data = data[data['Eqp_ID'].isin(request.eqp_ids)]
        
        if filtered_data.empty:
            raise HTTPException(status_code=404, detail="No data found for the specified equipment IDs")
        
        # Generate forecast data
        forecast_data = generate_forecast_data(filtered_data, request.forecast_type, request.forecast_period)
        
        # Generate the plot
        plt.figure(figsize=(15, 8))
        sns.set_style("whitegrid")
        sns.set_palette("colorblind")
        
        for eqp_id in request.eqp_ids:
            eqp_historical_data = filtered_data[filtered_data['Eqp_ID'] == eqp_id]
            eqp_forecast_data = forecast_data[forecast_data['Eqp_ID'] == eqp_id]
            
            # Plot actual historical data
            sns.lineplot(x='Last_Move_Eqp_Dt_YearMonthDay', y='Operating_Time', data=eqp_historical_data, 
                         label=f'Actual {eqp_id}', alpha=0.7)
            
            # Generate and plot historical predictions
            historical_dates = eqp_historical_data['Last_Move_Eqp_Dt_YearMonthDay']
            historical_scaled = scaler.transform(eqp_historical_data[['Networking_Time', 'First_Move_Eqp_Dt_Year', 'Last_Move_Eqp_Dt_Year']])
            historical_predictions = np.expm1(model.predict(historical_scaled).flatten())  # Flatten for 1D array
            sns.lineplot(x=historical_dates, y=historical_predictions, label=f'Predicted {eqp_id} (Historical)', linestyle=':', alpha=0.7)
            
            # Plot future predictions
            future_scaled = scaler.transform(eqp_forecast_data[['Networking_Time', 'First_Move_Eqp_Dt_Year', 'Last_Move_Eqp_Dt_Year']])
            future_predictions = np.expm1(model.predict(future_scaled).flatten())  # Flatten for 1D array
            sns.lineplot(x=eqp_forecast_data['Forecast_Date'], y=future_predictions, label=f'Forecast {eqp_id}', linestyle='--')
        
        plt.title(f'Operating Time Forecast by {request.forecast_type.capitalize()}', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Operating Time', fontsize=12)
        plt.legend(fontsize=10)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        
        # Encode the image to base64
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        
        return {"forecast_image": img_base64}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_forecast_data(filtered_data, forecast_type, forecast_period):
    forecast_data = []
    
    for _, equipment in filtered_data.groupby('Eqp_ID'):
        last_date = equipment['Last_Move_Eqp_Dt_YearMonthDay'].max()
        
        for i in range(1, forecast_period + 1):
            if forecast_type == 'days':
                forecast_date = last_date + timedelta(days=i)
            else:  # weeks
                forecast_date = last_date + timedelta(weeks=i)
            
            forecast_data.append({
                'Eqp_ID': equipment['Eqp_ID'].iloc[0],
                'Forecast_Date': forecast_date,
                'Networking_Time': equipment['Networking_Time'].mean(),
                'First_Move_Eqp_Dt_Year': equipment['First_Move_Eqp_Dt_Year'].iloc[0],
                'Last_Move_Eqp_Dt_Year': forecast_date.year
            })
    
    return pd.DataFrame(forecast_data)


