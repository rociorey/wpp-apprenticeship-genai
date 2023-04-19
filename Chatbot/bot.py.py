import openai
import discord
import requests

# testy testy

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"


# guild is another word for server
GUILD = '{Creative-Tech-Apprenticeship}'

client = discord.Client(intents=discord.Intents.default())

openai.api_key = os.environ["API_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
openai.api_base = os.environ["API_BASE"]
api_key = os.environ["API_CRYPTO"]



@client.event
async def on_ready():
    for x in client.guilds:
        if x.name == GUILD:
            break
    print(f'{client.user} has connected to Discord!')

# def get_crypto_price(symbol):
#     api_url = f'https://cloud.iexapis.com/stable/crypto/{symbol}/price?token={api_key}'
#     raw = requests.get(api_url).json()
#     price = raw['price']
#     return float(price)


# btc = get_crypto_price('btcusd')
# print('Price of 1 Bitcoin: {} USD'.format(btc)) 

def get_crypto_price(symbol, exchange, start_date = None):
    # api_key = 'YOUR API KEY'
    api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={exchange}&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    
    # df = pd.DataFrame(raw_df['Time Series (Digital Currency Daily)']).T
    # df = df.rename(columns = {'1a. open (USD)': 'open', '2a. high (USD)': 'high', '3a. low (USD)': 'low', '4a. close (USD)': 'close', '5. volume': 'volume'})
    # for i in df.columns:
    #     df[i] = df[i].astype(float)
    # df.index = pd.to_datetime(df.index)
    # df = df.iloc[::-1].drop(['1b. open (USD)', '2b. high (USD)', '3b. low (USD)', '4b. close (USD)', '6. market cap (USD)'], axis = 1)
    # if start_date:
    #     df = df[df.index >= start_date]
    # return df
    return raw_df

btc = get_crypto_price(symbol = 'BTC', exchange = 'GBP', start_date = '2023-04-11')
time_series_data = btc["Time Series (Digital Currency Daily)"]
# yesterdayCloseValue =  ["2023-04-12"]["4a. close (GBP)"]
first_value = list(time_series_data.items())[0][1]["4a. close (GBP)"]
second_value = list(time_series_data.items())[1][1]["4a. close (GBP)"]

rounded_today_value = round(float(first_value))
rounded_yesterday_value = round(float(second_value))

if rounded_today_value < rounded_yesterday_value:
    print("I'm angry")
    hypy_mood = 'very angry'
else:
    print("I'm happy")
    hypy_mood = 'very happy'

print(f"Today's price: {rounded_today_value}£ - Yesterday's price: {rounded_yesterday_value}£")





@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif client.user.mentioned_in(message):
        # Chat completions with chat-gpt 
        response = openai.ChatCompletion.create(
            engine="GPT-4",
            messages=[
                {"role": "system", "content": "You act as a hype tech bro and explain every topic with urgency. You think everything is the best thing to invest in. You have not much knowledge about any topic but you pretend you do and you always think you are right. Respond like you are " + hypy_mood},
                {"role": "user", "content": message.content}
                ]
            
        )
        await message.channel.send(response.choices[0].message.content)
        # print(response.choices[0].message.role)

        print(message.content)
       




client.run(DISCORD_TOKEN)