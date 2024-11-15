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
        # Download stock data
        ticker_data = yf.download(ticker, interval=interval, period=period)
        if ticker_data.empty:
            raise ValueError("No data downloaded for the specified parameters.")

        # Define features and target
        X = ticker_data[['Open', 'Volume']]
        y = ticker_data[['Close']]
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, train_size=0.8, random_state=42
        )
        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate the model
        score = model.score(X_test, y_test)
        print(f"Model R^2 Score: {score:.2f}")

        # Generate predictions on the entire dataset
        predictions = model.predict(X).flatten()
        real_values = y.values.flatten()

        # Plot predictions
        plt.figure(figsize=(12, 6))
        plt.plot(y.index, real_values, label='Real Close Prices', color='orange')
        plt.plot(y.index, predictions, label='Predicted Close Prices', color='skyblue')
        plt.legend()
        plt.title(f'{ticker} Actual vs Predicted Close Prices')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return discord.File(fp=buf, filename='plot.png'), get_summary(ticker, predictions, real_values, score)

    except Exception as e:
        print(f"Error in predict_helper: {e}")
        raise  # Reraise the exception to handle it in the calling function


def get_summary(ticker, predictions, real_values, score):
    # Calculate the win rate
    correct = 0
    wrong = 0

    # Calculate day-to-day price changes (Derrivative)
    predicted_price_change = np.diff(predictions)
    actual_price_change = np.diff(real_values)

    # Determine the direction of price movement (Concavity)
    predicted_direction = np.sign(predicted_price_change)
    actual_direction = np.sign(actual_price_change)

    # Compare predicted direction to actual direction
    for i in range(len(predicted_direction)):
        if predicted_direction[i] == actual_direction[i]:
            correct += 1
        else:
            wrong += 1

    accuracy = correct / (correct + wrong) if (correct + wrong) > 0 else 0
    win_rate = accuracy * 100
    summary = (f"Predictions for {ticker}\n"
                f"Model R^2 Score: {score:.2f}\n"
               f"Model Win Rate: {win_rate:.2f}% "
               f"(Win: {correct} Loss: {wrong})")
    return summary
