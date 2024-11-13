import discord
import datetime
import torch
import sklearn
import json

from backend import *
from LSTM import LSTMModel
from discord.ext import commands
from sklearn.preprocessing import MinMaxScaler

TOKEN = ''

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'SHIBA_TRADER LAUNCHED\n'
          f'TIME LAUNCHED (GMT): {datetime.datetime.now()}')

"""
This command would remove a certain stock from a user's cached
list of downloaded stock, and can be called as "!remove AMZN"
"""
# cache the current stock
# !add AMZN
@bot.command(name='add')
async def add(ctx, ticker: str):
    try:
        # Pass only the author's name and ID to add_helper
        msg = add_helper(ctx.author.name, ctx.author.id, ticker)
    except json.JSONDecodeError:
        msg = "An error occurred with the database file. It may be corrupt."
    except TypeError as e:
        msg = f"An unexpected error occurred: {str(e)}"
    except Exception as e:
        msg = f"An unexpected error occurred: {str(e)}"
    await ctx.send(msg)

"""
This command would remove a certain stock from a user's cached
list of downloaded stock, and can be called as "!remove AMZN"
"""
# !remove AMZN
@bot.command
async def remove_stock(ctx, ticker):
    try:
        remove_stock_helper(ctx[0])
    except:
        pass

"""
### May be a premium feature if database space limitations occur ###
This selects the stock from the list of stocks that are
currently cached for the user.
"""
# !select AMZN
@bot.command
async def select(ctx, ticker):
    try:
        select_helper(ticker)
    except:
        await ctx.send("Error Selecting Stock")

"""
This command would reset the user's current stocks 
"""
# !reset
@bot.command
async def reset(ctx):
    try:
        reset_helper()
    except:
        await ctx.send("Error Resetting")
    pass

"""
This command will print all statements possible.
THe user inputs their stock such as:
"!all AMZN" and the bot will give a detailed breakdown
of whether the stock is a good purchase or not based on
how it is doing. It will also give a 10-day, 10-minute, and 10-hour
in-advance prediction of the stock
"""
# !all
# !all 40 days AMZN
@bot.command
async def all(ctx):
    try:
        all_helper(ctx)
    except:
        await ctx.send("Error Generating Breakdown")

"""
This command will simply only predict the stock for the user.
The user can input their stock here as "!predict 10 minutes in 5 days AMZN"
(10 minutes will be the interval, and days will be what is shown of the non-predicted stock)
"""
# !predict 1m 5d AMZN
@bot.command(name='predict')
async def predict(ctx, interval, period, stock):
    try:
        # Attempt to generate the prediction image
        file, summary = predict_helper(stock, interval, period)
        await ctx.send(summary, file=file)
    except Exception as e:
        await ctx.send("Error Generating Prediction")
        print(f"Error: {e}")

"""
This command visualizes the stock data; the user can input
their stock as "!visualize AMZN" and the command will automatically
visualize the stock for them.
"""
@bot.command
async def visualize(ctx):
    try:
        visualize_helper(ctx)
    except:
        await ctx.send("Error Generating Visualization")

@bot.command
async def outlook(ctx):
    try:
        outlook_helper(ctx)
    except:
        await ctx.send("Error Generating Outlook")

@bot.command
async def summary(ctx):
    try:
        summary_helper(ctx)
    except:
        await ctx.send("Error Generting Summary")

if __name__ == '__main__':
    global database
    try:
        with open("database.json", "r") as f:
            database = f
    except Exception as e:
        exit(f"{str(e)}\n### FATAL ERROR ### FOUND EXCEPTION WHILE LOADING DATABASE; TERMINATING PROGRAM ###", 1)

    try:
        input_size = 2
        model = LSTMModel(input_size, hidden_size=64, num_layers=1, output_size=1)
        state_dict = torch.load('lstm_model2.pth', weights_only=True)
        model.load_state_dict(state_dict)
        model.eval()
    except Exception as e:
        exit(f"{str(e)}\n### FATAL ERROR ### FOUND EXCEPTION WHILE LOADING LSTM WEIGHTS; TERMINATING PROGRAM ###", 1)

    try:
        example_input = torch.randn(1, 5, input_size)
        print("Example Input:", example_input)
        with torch.no_grad():
            predictions = model(example_input)
            # Transform predictions back to original scale
            print("Prediction in Original Scale:", predictions)
    except Exception as e:
        exit(f"{str(e)}\n### FATAL ### FOUND EXCEPTION WHILE TESTING LSTM PREDICTOR; TERMINATING PROGRAM ###", 1)
    
    try:
        with open('database.json', 'r') as f:
            database = json.load(f)
        total_user_count = database['users']
        print(f"{total_user_count} unique users have used shiba-trader!")
    except Exception as e:
        exit(f"{str(e)}\n### FATAL ### FOUND EXCEPTION LOADING DATABASE; TERMINATING PROGRAM ###")
    
    print("\n\n\n### ALL TESTS PASSED; LAUNCHING SHIBA TRADER ###\n\n\n")

    bot.run(TOKEN)
