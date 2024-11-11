import discord
import datetime
import torch
import sklearn

from LSTM import LSTMModel
from discord.ext import commands
from sklearn.preprocessing import MinMaxScaler

TOKEN = ''

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def load_database():
    pass


@bot.event
async def on_ready():
    print(f'SHIBA_TRADER LAUNCHED\n'
          f'TIME LAUNCHED (GMT): {datetime.datetime.now()}')

@bot.event
async def on_message(message):
    pass

"""
For inputs, the user can either decide to input a current stock, which is cached
in the heap or database (still deciding). Using "!input" should be faster rather than
inputting the stock together with commands such as "!input"
"""

# cache the current stock
# !input AMZN
@bot.command
async def input(ctx):
    pass

"""
!reset

"""
@bot.command
async def reset(ctx):
    pass

# !all
# !all 40 days AMZN
@bot.command
async def all(ctx):
    pass

# !predict 10 minutes AMZN
@bot.command
async def predict(ctx):
    pass

@bot.command
async def visualize(ctx):
    pass

@bot.command
async def outlook(ctx):
    pass

if __name__ == '__main__':
    try:
        with open("database.json", "r") as f:
            database = f
    except Exception as e:
        print(str(e) + "\n### MAJOR ERROR ### FOUND EXCEPTION WHILE LOADING DATABASE; TERMINATING PROGRAM ###")

    try:
        input_size = 2
        model = LSTMModel(input_size, hidden_size=64, num_layers=1, output_size=1)
        state_dict = torch.load('lstm_model2.pth', weights_only=True)
        model.load_state_dict(state_dict)
        model.eval()
    except Exception as e:
        print(str(e) + "\n### MAJOR ERROR ### FOUND EXCEPTION WHILE LOADING LSTM WEIGHTS; TERMINATING PROGRAM ###")

    try:
        example_input = torch.randn(1, 5, input_size)
        print("Example Input:", example_input)
        with torch.no_grad():
            predictions = model(example_input)
            # Transform predictions back to original scale
            prediction = scaler_y.inverse_transform(predictions.cpu().numpy())
            print("Prediction in Original Scale:", prediction)
    except Exception as e:
        print(str(e) + "\n### MAJOR ERROR ### FOUND EXCEPTION WHILE TESTING LSTM PREDICTOR; TERMINATING PROGRAM ###")
    
    bot.run(TOKEN)
