import openai
import discord

# guild is another word for server
GUILD = 'RocioLilServer'

client = discord.Client(intents=discord.Intents.default())

with open('myToken.txt') as f:
    lines = f.read().split('\n')
    openai.api_key = lines[0]

    DISCORD_TOKEN = lines[1]
f.close()


@client.event
async def on_ready():
    for x in client.guilds:
        if x.name == GUILD:
            break
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif client.user.mentioned_in(message):
        # Chat completions with chat-gpt 
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You act as a hype tech bro and explain every topic with the same excitement and urgency. You think everything is the best thing to invest in. You have not much knowledge about any topic but you pretend you do and you always think you are right."},
                {"role": "user", "content": message.content}
                ]
        )
        await message.channel.send(response.choices[0].message.content)
        print(message.content)
print(response)

client.run(DISCORD_TOKEN)