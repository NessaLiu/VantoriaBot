# Import Discord Package
import discord
from discord import user
from discord.ext import commands
import random

# import quote functions
from quotes import *
# import database
from db_setup import *
import asyncio
# WILL COME BACK TO 
from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import GuildPermissionsData
from discord_slash.utils.manage_commands import create_choice, create_option
import os
from dotenv import load_dotenv


# Get bot token
load_dotenv()
token = os.environ.get('VantoriaBotToken')

# Create client
client = commands.Bot(command_prefix='-')

# Create slash
slash = SlashCommand(client, sync_commands=True)

# ----------------------- Guilds -----------------------

guilds_list = []

# Get the guild IDs
def get_guilds():
    return [g.id for g in client.guilds]

# Store guild IDs
@client.event
async def on_guild_join(guild):
    if guild.id not in guilds_list:
        guilds_list.append(guild.id)

# ----------------------- Database -----------------------

@slash.slash(
    name="getid",
    description = "Get a user's Discord ID",
    guild_ids= guilds_list,
    options = [
        create_option(
            name= "user",
            description = "Whose ID do you want? (provide your @)",
            option_type = 6,
            required = True
        )
    ]
)
async def _GetId(ctx: SlashContext, user: user):
    user_id = str(user.id)
    await ctx.send(f"<@{user.id}>'s ID is: {user_id}")

# Create a Profile Command
@slash.slash(
    name= "createProfile",
    description = "Add a new profile!",
    guild_ids=guilds_list,
    options = [
        create_option(
            name= "user",
            description = "Who is this profile for? (provide your @)",
            option_type = 6,
            required = True
        ),
        create_option(
            name= "name",
            description = "What is your preferred name?",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "introduction",
            description = "Share a few things about yourself!",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "favouritehobby",
            description = "What is your favourite hobby?",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "favouritecolour",
            description = "What is your favourite colour?",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "favouritefood",
            description = "What is your favourite food?",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "favouritemovie",
            description = "What is your favourite movie?",
            option_type = 3,
            required = True
        ),
        create_option(
            name= "favouritesong",
            description = "What is your favourite song?",
            option_type = 3,
            required = True
        )
    ]
)
async def _CreateProfile(ctx: SlashContext, user: user, name: str, introduction: str, favouritehobby: str, favouritecolour: str, favouritefood: str, favouritemovie: str, favouritesong: str):
     
    # Get the user's Discord ID
    user_id = str(user.id)
    
    #if not check_profile_existence(user_id):
    #    create_profile(user_id, name, introduction, favouritehobby, favouritecolour, favouritefood, favouritemovie, favouritesong)
    #    await ctx.send(f"Added a profile for <@{user.id}>!")
    #else:
    #    await ctx.send(f"<@{user.id}> already has a profile! Go check it out :)")
    try:
        create_profile(user_id, name, introduction, favouritehobby, favouritecolour, favouritefood, favouritemovie, favouritesong)
        await ctx.send(f"Added a profile for <@{user.id}>!")
    except mysql.connector.IntegrityError:
        await ctx.send(f"ERROR: <@{user.id}> already has a profile! Go check it out :)")


# View Profile Command
@slash.slash(
    name = "viewProfile",
    description = "Who's profile would you like to check out?",
    guild_ids=guilds_list,
    options = [
        create_option(
            name='user',
            description='The user whose profile you want to see.',
            option_type=6,
            required=True
        )
    ]
)
async def _ViewProfile(ctx: SlashContext, user: user):

    # Get the user's Discord ID
    user_id = str(user.id)
    
    # Check if the user exists and then get info
    if check_profile_existence(user_id):

        #await ctx.send("Profile Exists.")
        # info returns a tuple of length 7
        
        info = get_profile_info(user_id)

        user_name = info[1]
        user_intro = info[2]
        user_hobby = info[3]
        user_colour = info[4]
        user_food = info[5]
        user_movie = info[6]
        user_song = info[7]

        embed = discord.Embed(
            title = f"INTRODUCING...{user_name}!!!",         
            description = "Welcome! It's nice to meet you :) Let's get everyone acquainted!\n==========================================\n",
            color = 0xffffff
        )

        embed.add_field(name="Name:", value= user_name, inline=True)
        embed.add_field(name="Introduction:", value= user_intro, inline=True)
        embed.add_field(name="Hobby:", value= user_hobby, inline=True)
        embed.add_field(name="Favourite Colour:", value= user_colour, inline=True)
        embed.add_field(name="Favourite Food:", value= user_food, inline=True)
        embed.add_field(name="Favourite Movie:", value= user_movie, inline=True)
        embed.add_field(name="Favourite Song:", value= user_song, inline=True)

        await ctx.send(embeds=[embed])
    
    else:
        await ctx.send(f"<@{user.id}> has no profile, silly!")      

# Edit Profile Command
@slash.slash(
    name= "editProfile",
    description = "Edit an existing profile!",
    guild_ids=guilds_list,
    options = [
        create_option(
            name = "user",
            description = "Please enter your profile's discord ID.",
            option_type = 6,
            required = True
        ),
        create_option(
            name = "field",
            description = "How would you like to edit your profile?",
            option_type = 3,
            required = True,
            choices = [
                create_choice(
                    name= "name",
                    value = "NAME"
                ),
                create_choice(
                    name= "introduction",
                    value = "INTRODUCTION"
                ),
                create_choice(
                    name= "favouritehobby",
                    value = "FAVOURITE HOBBY"
                ),
                create_choice(
                    name= "favouritecolour",
                    value = "FAVOURITE COLOUR"
                ),
                create_choice(
                    name= "favouritefood",
                    value = "FAVOURITE FOOD"
                ),      
                create_choice(
                    name= "favouritemovie",
                    value = "FAVOURITE MOVIE"
                ),
                create_choice(
                    name= "favouritesong",
                    value = "FAVOURITE SONG"
                ) 
            ] 
        ),
        create_option(
            name = "edit",
            description = "Please enter your changes",
            option_type = 3,
            required = True
        )    
    ]
)
async def _EditProfile(ctx: SlashContext, user: user, field: str, edit: str):
    
    # Get the user ID and call function
    user_id = str(user.id)
    if check_profile_existence(user_id):
        edit_profile(user_id, field, edit)
        await ctx.send(f"Your edits have been made, <@{user.id}>!")
    else:
        await ctx.send(f"<@{user.id}> has no profile, silly!")


# Delete Profile Command
@slash.slash(
    name= "deleteProfile",
    description = "Delete a profile :/",
    guild_ids=guilds_list,
    options = [
        create_option(
            name = "user",
            description = "Please input the discord ID of the profile you'd like to delete.",
            required = True,
            option_type = 6
        )
    ]
)
async def _DeleteProfile(ctx: SlashContext, user:user):
    # get user id and call function
    user_id = str(user.id)
    if check_profile_existence(user_id):
        delete_profile(user_id)
        await ctx.send(f"Oh no! Goodbye, <@{user.id}>")
    else:
        await ctx.send(f"<@{user.id}> doesn't have a profile, silly!")

# ----------------------- Trivia files -----------------------

# Text file with all the questions 
with open('trivia_questions.txt', 'r', encoding='cp437') as File1:
    # from video in case we need later: lines = File1.readlines()
    questions = []
    for line in File1:
        questions.append(line)
File1.close()

# Text file with all answers
with open('trivia_answers.txt', 'r', encoding='cp437') as File2:
    # from video in case we need later: lines = File2.readlines()
    answers = []
    for line in File2:
        answers.append(line)
File2.close()

# Filter the question list to remove \n
filtered_questions = []
for item in questions:
    filtered_questions.append(item.strip())

# Filter the answer list to remove \n
filtered_answers = []
for item in answers:
    filtered_answers.append(item.strip())

# ----------------------- Quote Data -----------------------

# store each genres' quotes as a list
love_quotes = final_quote_generator("love")
life_quotes = final_quote_generator("life")
inspirational_quotes = final_quote_generator("inspirational")
humor_quotes = final_quote_generator("humor")
wisdom_quotes = final_quote_generator("wisdom")
happiness_quotes = final_quote_generator("happiness")
motivational_quotes = final_quote_generator("motivational")
time_quotes = final_quote_generator("time")
hope_quotes = final_quote_generator("hope")

# store the number of quotes in each array for accessing purposes
num_quotes = len(love_quotes) - 1

# ----------------------- Commands -----------------------

# event for client - do actions when events occur
@client.event 
# run when code is ready (bot goes online)
# async allows it to run even if there's a delay
async def on_ready():
    
    await client.change_presence(activity=discord.Game('Listening to you :)'), status="dnd")
    # telling client to retrieve channel - access general channel

    '''
    general_channel = client.get_channel(925153227794694238)
    
    myEmbed = discord.Embed(
        title = "HELLO THERE! My name is Vantoria :D",
        description = "Thanks for inviting me. Here are some milk and cookies in return for your kindness and hospitality :)",
        color=0x95ede0)
    
    myEmbed.add_field(name='Take a look around!', value='We have games, personal care, and more! To get started, simply use the `/help` command!', inline=False)
    myEmbed.set_image(url='https://cdn.discordapp.com/attachments/846084093065953283/924129382090539038/IMG_0005.jpg')

    # wait for channel to be retrieved and then send 
    await general_channel.send(embed=myEmbed)
    '''

# runs when user sends a message
@client.event 
async def on_message(message):

    channel = message.channel
    
    if message.content.upper() == 'CAN I HAVE SOME TEA?':
        await channel.send('NO SHOTTTTT >:)))')

    elif message.content.upper() == 'PING':
        await channel.send('PONGGGGGGG')

    elif message.content.upper() == 'MOMMY?':
        await channel.send('sorry.')

    elif message.content.upper() == 'SORRY':
        await channel.send('it\'s ok')

    #await client.process_commands(message)


# test slash command
@slash.slash(
    name='test',
    description='slash command',
    guild_ids=guilds_list 
) 
async def _test(ctx:SlashContext):
    await ctx.send('success!')

#async def ping(ctx):
#    await ctx.send(f'Bot Speed = {round(client.latency)*1000}')

@client.command(name='version', aliases=['ver'])
async def version(ctx):
    await ctx.send('hi')

# Hug command
@slash.slash(
    name='hug',
    description='Give someone a hug! <3',
    guild_ids=guilds_list,
    options = [
        create_option(
            name='huggee',
            description='Who would you like to hug? Give their @!',
            option_type=6 , # user
            required=True
        )
    ]
)
async def _Hug(ctx: SlashContext, huggee: user):
    await ctx.send(f'You gave <@{huggee.id}> a nice big hug!')

# Call command
@slash.slash(
    name='Call',
    description='Let\'s call this user!',
    guild_ids=guilds_list,
    options = [
        create_option(
            name='recipient',
            description='The user whom you\'d like to call',
            option_type=6,
            required=True
        )
    ]
)
async def _Call(ctx:SlashContext, recipient: user):
    await ctx.send(f'RING RING!! Hey, <@{recipient.id}>! You\'re getting a call!!!')

# help command
@slash.slash(
    name='help',
    description='Command that provides all the bot functions.',
    guild_ids=guilds_list
)
async def _Help(ctx: SlashContext):
    await ctx.defer()
    embed = discord.Embed(
        title = 'Help is on it\'s way!',
        description=
        '''Hey there! You look a little lost.
        To help you get back on your feet, here is a list of available
        commands that you can access.\n
        ==========================================
        \n`/help` - Shows you a list of possible commands to use. \n''',
        color = 0xb8e5ff
    )
    embed.add_field(name='Profile', value=
    '''
    `/createprofile` - Let's create your personalized profile :) \n
    `/viewprofile` - Access your current profile! \n
    `/editprofile` - Want to change your profile? No problem! \n
    `/deleteprofile` - Use this command to delete an existing profile \n
    `/getid` - Retrieve a user's discord ID right here! \n
    ------------------------------------------
    ''', inline=False)
    
    embed.add_field(name='Minigames', value=
    '''
    `/8ball` - Type in any question for the Magic 8ball to give you an answer to! \n
    `/rockpaperscissors` - Input "rock", "paper" or "scissors" and try to beat us! \n
    `/trivia` - Test your knowledge with this True/False trivia game! \n
    ------------------------------------------
    ''', inline=False)
    
    embed.add_field(name='Personal Care', value=
    '''
    `/quote` - Need some inspiration? Motivation? Happiness? Don't worry - simply type in the magic spell and you'll meet Quinn, the queen of quotes! Choose your type from there ;)\n
    `/hug` - Did you know hugs are scientifically proven to be beneficial to its participants? @ someone to hug them! (or yourself)\n
    `/call` - ~ Ring Ring ~ Call your bestie with our special carrier plan :)
    ''', inline=False)

    await ctx.send(embeds=[embed])


# ----------------------- Personal Care -----------------------

@slash.slash(
    name='quotetest',
    description='quotetest',
    guild_ids=guilds_list
)
async def _quoteTest(ctx:SlashContext):
    await ctx.send(love_quotes[0])

@slash.slash(
    name='quote',
    description='We\'ve got plenty of quotes for you to indulge in!',
    guild_ids=guilds_list
)
async def _Quote(ctx:SlashContext):

    # Explain game to player -- EMBED HERE
    embed = discord.Embed(
        title = '===== QUOTES =====',
        description = '''Hey there! My name is Quinn, the queen of quotes :)
        \nWelcome to QUOTE QINGDOM!!\n
        Please use the emojis below to indicate the topic you\'d like to see!.\n
        ==========================================\n
        ''',
        color = 0xffeb8a
    )

    # Field for the different types of quotes
    embed.add_field(name='Love Quotes', value='Lookin\' for lOooOoOOve? Perhaps you\'re LOVESTRUCK? React to the ❤️!', inline=False)
    embed.add_field(name='Life Quotes', value='Let\'s find the meaning of life together :) Pick up the 🌱 and let\s go!', inline=False)
    embed.add_field(name='Inspiration Quotes', value='Need to feel ✨inspired✨? You got it - click the ✨!', inline=False)
    embed.add_field(name='Humour Quotes', value='Laughing - the best form of therapy! Let\'s hear you laugh! React to the 🤣', inline=False)
    embed.add_field(name='Wisdom Quotes', value='Where to find wisdom, you ask? Why, we have some right here! Take some 🧠 :))', inline=False)
    embed.add_field(name='Happiness Quotes', value='We can always use a bit more joy in our lives, can\'t we, traveller? Let\'s find some - react to the 😄!', inline=False)
    embed.add_field(name='Motivational Quotes', value='Lacking motivation my friend? No worries, muster up your strength and hit the 💪 emoji! ', inline=False)
    embed.add_field(name='Time Quotes', value='C\'mon, I\'ve got duties to attend to; we don\'t have all day! Click the ⏰!!', inline=False)
    embed.add_field(name='Hope Quotes', value='Feeling a bit hopeless? React to the 🙏!', inline=False)
    embed.set_footer(text='Retrieved from https://www.goodreads.com/quotes')

    quote_generator = await ctx.send(embeds=[embed])

    # If they react to the start game emoji, run the Trivia Game function
    # BOT ADDS REACTIONS
    await quote_generator.add_reaction('❤️') # love 
    await quote_generator.add_reaction('🌱') # life
    await quote_generator.add_reaction('✨') # inspiration
    await quote_generator.add_reaction('🤣') # humor
    await quote_generator.add_reaction('🧠') # wisdom
    await quote_generator.add_reaction('😄') # happiness
    await quote_generator.add_reaction('💪') # motivational
    await quote_generator.add_reaction('⏰') # time
    await quote_generator.add_reaction('🙏') # hope

    try:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, 
        user: user == ctx.author and (reaction.emoji == '❤️' or reaction.emoji == '🌱'
        or reaction.emoji == '✨' or reaction.emoji == '🤣' or reaction.emoji == '🧠'
        or reaction.emoji == '😄' or reaction.emoji == '💪' or reaction.emoji == '⏰'
        or reaction.emoji == '🙏'), timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("You took too long! QUOTE QINGDOM needs its beauty sleep! Come visit tomorrow, traveller :)")

    else:
        # Create random number to get quote
        random_quote_number = random.randint(0,num_quotes)

        if reaction.emoji == '❤️':
            await ctx.send(love_quotes[random_quote_number])
        elif reaction.emoji == '🌱':
            await ctx.send(life_quotes[random_quote_number])
        elif reaction.emoji == '✨':
            await ctx.send(inspirational_quotes[random_quote_number])
        elif reaction.emoji == '🤣':
            await ctx.send(humor_quotes[random_quote_number])
        elif reaction.emoji == '🧠':
            await ctx.send(wisdom_quotes[random_quote_number])
        elif reaction.emoji == '😄':
            await ctx.send(happiness_quotes[random_quote_number])
        elif reaction.emoji == '💪':
            await ctx.send(motivational_quotes[random_quote_number])
        elif reaction.emoji == '⏰':
            await ctx.send(time_quotes[random_quote_number])
        elif reaction.emoji == '🙏':
            await ctx.send(hope_quotes[random_quote_number])
        else:
            await ctx.send("Couldn't understand, better luck next time :)")

# --------------------------- Games -----------------------------

# 8BALL GAME
@slash.slash(
    name='8ball',
    description='Let the magic 8ball answer all of your questions!',
    guild_ids=guilds_list,
    options = [
        create_option(
            name='question',
            description='What question do you have for the 8ball?',
            option_type=3,
            required=True
        )
    ]
)
#async def _8ball(ctx, *, question):
async def _8ball(ctx: SlashContext, question: str):
    # Create and store responses
    responses =[
        'For sure, bro.',
        '*cricket cricket*',
        'UHHH UNLIKELY',
        'Not looking too good :/',
        'Questionable O.O',
        'Good question!',
        'Interesting...',
        'Good luck man!',
        'Reply hazy, please try again later.',
        'Without a doubt!',
        'HEAD EMPTY NO THOUGHTS',
        'OF COURSE!!!',
        'The chances are low.',
        'So true bestie!',
        'Yeeeeee',
        'I would not bet on it if I were you...',
        'Nah.',
        'YUH - FO SHO',
        'yes yes yes',
        'yeah nO.',
        'Terrible.'
    ]
    
    embed = discord.Embed(
        title='--------------------------------\nThe Magic 8Ball Speaks...\n--------------------------------',
        description='You asked and we provided! Let\'s see the results.',
        color=0xd2b7ed
    )

    embed.add_field(name='**Your question**:', value=f'{question}', inline=False)
    embed.add_field(name='**The Magical :8ball: Answer**:', value=f'{random.choice(responses)}', inline=False)
    
    await ctx.send(embeds=[embed])

# ROCK PAPER SCISSORS
#@client.command(aliases=['rpc', 'rock paper scissors', 'RPC'])
@slash.slash(
    name='rockPaperScissors',
    description='Play rock paper scissors with me!',
    guild_ids=guilds_list,
    options = [
        create_option(
            name='move',
            description='What will you play?',
            option_type=3,
            required=True
        )
    ]
)
#async def _rockpaperscissors(ctx, *, player_move):
async def _rockPaperScissors(ctx: SlashContext, move: str):
    
    # bot move
    bot_move = ['ROCK', 'PAPER', 'SCISSORS']
    bot_response = random.choice(bot_move)

    embed = discord.Embed(
        title = '--------------------------\n**Game Results**\n--------------------------',
        description = 'Here\'s how our game went:',
        color = 0xfab9a5
    )

    if move.upper() == 'ROCK':
        
        if bot_move == 'PAPER':
            embed.add_field(name='***YOU LOST!***',
            value='**Your move**: :rock:\n**My Move:** :newspaper:')
        elif bot_move == 'SCISSORS':
            embed.add_field(name='***YOU WON!***',
            value='**Your move**: :rock:\n**My Move:** :scissors:')
        else:
            embed.add_field(name='***WE TIED! UNTIL NEXT TIME!***',
            value ='**Your move**: :rock:\n**My Move:** :rock:')

    elif move.upper() == 'PAPER':
        
        if bot_move == 'SCISSORS':
            embed.add_field(name='***YOU LOST!***', 
            value='**Your move:** :newspaper:\n**My move:** :scissors:')
        elif bot_move == 'ROCK':
            embed.add_field(name='***YOU WON!***',
            value='**Your move:** :newspaper:\n**My move:** :rock:')
        else:
            embed.add_field(name='***WE TIED! UNTIL NEXT TIME!***',
            value='**Your move:** :newspaper:\n**My move:** :newspaper:')
            
    elif move.upper() == 'SCISSORS':
        
        if bot_move == 'SCISSORS':
            embed.add_field(name='***WE TIED! UNTIL NEXT TIME!***',
            value='**Your move:** :scissors:\n**My move:** :scissors:')
        elif bot_move == 'ROCK':
            embed.add_field(name='***YOU LOST!***',
            value='**Your move:** :scissors:\n**My move:** :rock:')
        else:
            embed.add_field(name='***YOU WON!***',
            value='**Your move:** :scissors:\n**My move:** :newspaper:')
    else:
        embed.add_field(name='**Stop trolling!!!**', value= 'Gimme a real challenge >:)')

    await ctx.send(embeds=[embed])


# TRIVIA GAME
@slash.slash(
    name='trivia',
    description='Play a True or False Trivia Game!',
    guild_ids=guilds_list
)
async def _Trivia(ctx: SlashContext): 
    
    # Explain game to player -- EMBED HERE
    embed = discord.Embed(
        title = 'Welcome to trivia! Please read the instructions below.',
        description = 'Please use the emojis below to indicate whether you are ready. ' +
                      'When the game starts, simply use the T and F emojis as True and False, respectively.'
    )
    # add more embeds ...
    # ...
    # ...

    trivia_game = await ctx.send(embeds=[embed])

    # If they react to the start game emoji, run the Trivia Game function
    # BOT ADDS REACTIONS
    await trivia_game.add_reaction('👍')

    try:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji == '👍', timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("It's okay if you aren't! We all get the jitters sometimes :)")

    else:
        if reaction.emoji == '👍':
           
            # Make a random number generator to get random questions
            num_questions = len(filtered_questions) - 1
            random_question_number = random.randint(0,num_questions)
            random_question = filtered_questions[random_question_number]
            correct_response = filtered_answers[random_question_number]

            await ctx.send("Your question is: " + random_question)

            try:
                message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send("Oops! Looks like you ran out of time.")
                
            else:
                if correct_response.lower() == message.content.lower():
                    await ctx.send("We have a winner! Congratulations!! :D")
                else:
                    await ctx.send("Oh norrrhh - that's wrong! :') Better luck next time!")


# Run client
def start_client():
    client.run(token) # Bot ID
