import discord
import datetime
import torch
import sklearn

from LSTM import LSTMModel
from discord.ext import commands
from sklearn.preprocessing import MinMaxScaler
from backend import *

TOKEN = ''

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


"""
Current database is locally run, but this will be updated
to a MongoDB database.
"""
def load_database():
    pass


@bot.event
async def on_ready():
    print(f'SHIBA_TRADER LAUNCHED\n'
          f'TIME LAUNCHED (GMT): {datetime.datetime.now()}')

@bot.event
async def on_message(message):
    if message.user == bot:
        pass


"""
This command would remove a certain stock from a user's cached
list of downloaded stock, and can be called as "!remove AMZN"
"""
# cache the current stock
# !input AMZN
@bot.command
async def add(ctx):
    try:
        add_helper(ctx[0], ctx[1], ctx[2])
    except Exception as e:
        print(e)

"""
This command would remove a certain stock from a user's cached
list of downloaded stock, and can be called as "!remove AMZN"
"""
@bot.command
async def remove(ctx):
    try:
        remove_helper(ctx[0])
    pass


"""
This selects the stock from the list of stocks that are
currently cached for the user.
"""
@bot.command
async def select(ctx):
    pass

"""
This command would reset the user's current stocks 
"""
@bot.command
async def reset(ctx):
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
    pass

"""
This command will simply only predict the stock for the user.
The user can input their stock here as "!predict 10 minutes in 5 days AMZN"
(10 minutes will be the interval, and days will be what is shown of the non-predicted stock)
"""
# !predict 10 minutes AMZN
@bot.command
async def predict(ctx):
    predict

"""
This command visualizes the stock data; the user can input
their stock as "!visualize AMZN" and the command will automatically
visualize the stock for them.
"""
@bot.command
async def visualize(ctx):
    pass

@bot.command
async def outlook(ctx):
    pass

@bot.command
async def summary(ctx):
    pass

if __name__ == '__main__':
    try:
        with open("database.json", "r") as f:
            database = f
    except Exception as e:
        exit(str(e) + "\n### FATAL ERROR ### FOUND EXCEPTION WHILE LOADING DATABASE; TERMINATING PROGRAM ###")

    try:
        input_size = 2
        model = LSTMModel(input_size, hidden_size=64, num_layers=1, output_size=1)
        state_dict = torch.load('lstm_model2.pth', weights_only=True)
        model.load_state_dict(state_dict)
        model.eval()
    except Exception as e:
        exit(str(e) + "\n### FATAL ERROR ### FOUND EXCEPTION WHILE LOADING LSTM WEIGHTS; TERMINATING PROGRAM ###")

    try:
        example_input = torch.randn(1, 5, input_size)
        print("Example Input:", example_input)
        with torch.no_grad():
            predictions = model(example_input)
            # Transform predictions back to original scale
            prediction = scaler_y.inverse_transform(predictions.cpu().numpy())
            print("Prediction in Original Scale:", prediction)
    except Exception as e:
        exit(str(e) + "\n### FATAL ### FOUND EXCEPTION WHILE TESTING LSTM PREDICTOR; TERMINATING PROGRAM ###")
    
    bot.run(TOKEN)
