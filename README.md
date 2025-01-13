# AGL Machine Operating Time Forecasting

An application that forecasts the operating time of port terminal machines using time series forecasting. It provides a REST API to get the predictions and it also outputs an image with the graphs. This was done using Python, FastAPI, pandas, numpy, scikit-learn, matplotlib, and seaborn.

## Project Description

This project forecasts the operating time of selected machines in AGL port terminals, helping AGL manage and optimize their port terminal operations. The application uses the SARIMAX time series forecasting model to predict future operating times by days or by weeks.

## Project Features
* **API:** A REST API developed using FastAPI.
* **Time Series Forecast:** The application uses the SARIMAX model for time series forecasting of machine operating times.
* **Visualization:**  It generates and displays a graph of the forecasting results, to help the users visualize and understand the prediction.
* **Input Flexibility:** The API takes multiple machine IDs, and accepts the forecast types of `days` or `weeks`, in order to provide a flexible interface for the end user.

## Technologies Used

*   **Python:** The primary programming language.
*   **FastAPI:**  For building the REST API.
*   **pandas:** Data analysis library.
*   **numpy:**  Numerical library for mathematical operations
*   **scikit-learn:**  For the machine learning and model training.
*   **matplotlib & seaborn:**  For creating data visualizations and graphs.
* **Joblib:** Used to save the models to a file.

## Usage

1.  **Install Dependencies:**
     Before running the code, make sure that you have installed all the required libraries using `pip install -r requirements.txt`.
2.  **Start the FastAPI server:**
    *  Run the `app.py` file by using a command such as: `python app.py`
    *   The API will run on `http://127.0.0.1:8000`.
3. **Make a request**
     * Use the `forecast_client.py` file to request data from the API, by using the following arguments:
          *  An array of machine ids such as `["CR1", "CR2"]`
          * The forecasting type, such as `days` or `weeks`
           * The period to be forecast.
         * For example: `python forecast_client.py ["CR1"] weeks 12`

## How to Contribute

If you want to collaborate and contribute to the project, you are welcome to fork this repository, make changes, and create a pull request.
