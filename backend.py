import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import discord
import json
import os
import io

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def add_helper(author, author_id, ticker):
    # Load the JSON database
    with open('database.json', 'r') as file:
        database = json.load(file)

    # Existing user logic
    for user in database['users']:
        if user['id'] == author_id:
            if ticker not in user['stocks'] and user['premium']:
                user['stocks'].append(ticker)
                result = "Stock added successfully to your list."
            else:
                user['stock'] = ticker
                result = "Stock updated successfully as your current stock."
            
            with open('database.json', 'w') as file:
                json.dump(database, file, indent=4)
            return result

    # New user creation logic
    new_user = {
        'id': author_id,
        'userid': author,
        'stock': ticker,
        'premium': 0,
        'stocks': [],
    }
    database['users'].append(new_user)

    with open('database.json', 'w') as file:
        json.dump(database, file, indent=4)
    
    return "Stock added successfully. Welcome to ShibaTrader! :)"


# more for premium users
def remove_helper(authorid, author, ticker):
    with open('database.json', 'r') as file:
        database = json.load(file)
    return


def select_helper():
    pass

def predict_helper(ticker, interval, period):
    try: 
        ticker_data = yf.download(ticker, interval=interval, period=period)
    except:
        return None, "No data downloaded for the specified parameters."
    
    try:        
        ticker_data['Close_lag1'] = ticker_data['Close'].shift(1)
        ticker_data.dropna(inplace=True)

        # Define features and target
        X = ticker_data[['Close_lag1']]
        y = ticker_data['Close']

        # Split data into training and testing sets
        split_index = int(len(X) * 0.8)
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate the model
        score = model.score(X_test, y_test)
        print(f"Model R^2 Score: {score:.2f}")

        last_feature = X_test.iloc[-1].values.reshape(1, -1)
        future_predictions = []
        for _ in range(10):
            next = model.predict(last_feature)
            future_predictions.append(next[0])
            last_feature = np.array(next).reshape(1, -1)

        # Plot predictions
        figure = plot_graph(ticker, ticker_data['Close'].values, future_predictions)

        return discord.File(fp=figure, filename='plot.png'), get_summary(ticker, future_predictions, ticker_data['Close'].values, score)

    except Exception as e:
        print(f"Error in predict_helper: {e}")
        raise  # Reraise the exception to handle it in the calling function


def get_summary(ticker, predictions, real_values, score):
    summary = (f"Predictions for {ticker}\n"
               f"Model R^2 Score: {score:.2f}\n")
    return summary

def plot_graph(ticker, original_values, predicted_values):
    plt.figure(figsize=(12, 6))
    predicted_index = np.arange(len(original_values), len(original_values) + len(predicted_values))
    plt.plot(np.arange(len(original_values)), original_values, label="Real Closing Values", color='orange')
    plt.plot(predicted_index, predicted_values, label="Predicted Closing Values", color='skyblue', linestyle='dotted')
    plt.legend()
    plt.title(f'{ticker} Actual vs Predicted Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf
