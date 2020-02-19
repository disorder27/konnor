import discord
import random
import pyowm
import datetime 
import asyncio
import requests
import pyautogui
from datetime import tzinfo, timedelta, datetime, timezone
from random import choice, randint
from discord.ext import commands


#prefix1
prefix= "!"

#prefix2
Bot = commands.Bot(command_prefix= prefix)

#Статус
@Bot.event
async def on_ready(*args):
    print("Бот настроен и готов к работе")
    type = discord.ActivityType.watching
    activity = discord.Activity(name = "за сервером", type = type)
    status = discord.Status.dnd
    await Bot.change_presence(activity = activity, status = status)

#Автороль + уведомление
@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(639573431314153492)
    channel_info = Bot.get_channel(673517407293276161)
    role = discord.utils.get(member.guild.roles, id = 668462431420547073)
    await member.add_roles(role)
    emb = discord.Embed(
        title = ':bust_in_silhouette: Уведомление о новом участнике:',
        description = f':hand_splayed: Здравствуй, {member.name}, добро пожаловать на сервер! \n :closed_book: Ознакомиться с правилами сервера и прочей информацией ты можешь в {channel_info.mention}', colour= 0x39d0d6, inline = False)
    await channel.send(embed= emb)

#Удаление стандартного help
Bot.remove_command('help')

#Удаление ошибок
@Bot.event
async def on_command_error(ctx, error):
    pass

#Несуществующие команды
@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f':exclamation: **{ctx.author.name}**, данной команды не существует.\n:page_facing_up: Для того чтобы увидеть команды сервера, пропишите **!help**', color=0xff0000)) 

#help
@Bot.command()
async def help(ctx):
    emb = discord.Embed(title= ":gear: Информация о командах:", description= f"**:information_source: Информация: **\n"
                                                                      f"!info, !messages, !time, !roleinfo, !serverinfo, !ip_info, !phone_info\n\n" 
                                                                      f"**:books: Развлечения: **\n"
                                                                      f"!coin, !random, !math, !w\n\n"
                                                                      f"**:wrench: Сервер: **\n"
                                                                      f"!report, !send\n\n"
                                                                      f"**:computer: Модерирование: **\n"
                                                                      f"!say, !clear, !add_role, !remove_role, !kick, !ban, !unban, !change_name, !channel_create, !voice_create, !move\n\n"
                                                                      ,colour= 0x39d0d6, inline = False, timestamp=ctx.message.created_at)
   
    emb.set_footer(text= "Вызвано: {}".format(ctx.message.author), icon_url= ctx.message.author.avatar_url)
    await ctx.author.send(embed= emb)
    await ctx.send(embed = discord.Embed(description = f'''**:incoming_envelope: Команды отправлены Вам в ЛС!**''', colour = 0x39d0d6))
    await ctx.message.add_reaction('✅')

#weather
@Bot.command()
async def w( ctx, *, arg ):
    owm = pyowm.OWM( 'c02012391ecdc6b36e059977c92d17eb' ) # https://openweathermap.org/api_keys
    city = arg

    observation = owm.weather_at_place( city )
    w = observation.get_weather()
    temperature = w.get_temperature( 'celsius' )[ 'temp' ]

    await ctx.send(embed = discord.Embed(description=f':thermometer: Температура в городе { city }: { temperature }', colour = 0x39d0d6 ))

#Проверка weather
@w.error 
async def w_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно введите название города!\n\n``Пример:\n!w Москва``\n\n•Название города нужно вводить на русском языке!', color=0xff0000))

#ip_info
@Bot.command()
async def ip_info( ctx, arg ):
    response = requests.get( f'http://ipinfo.io/{ arg }/json' )

    user_ip = response.json()[ 'ip' ]
    user_city = response.json()[ 'city' ]
    user_region = response.json()[ 'region' ]
    user_country = response.json()[ 'country' ]
    user_location = response.json()[ 'loc' ]
    user_org = response.json()[ 'org' ]
    user_timezone = response.json()[ 'timezone' ]

    global all_info
    emb = discord.Embed(title = f'Информация об айпи {arg}:',
    description = f':united_nations: **Страна**: { user_city }\n\n:regional_indicator_r: **Регион**: { user_region }\n\n:cityscape: **Город**: { user_country }\n\n:map: **Локация**: { user_location }\n\n:bust_in_silhouette: **Организация**: { user_org }\n\n:clock: **Временная зона**: { user_timezone }', colour= 0x39d0d6, inline = False)
    emb.set_footer(text= "Вызвано: {}".format(ctx.message.author), icon_url= ctx.message.author.avatar_url)

    await ctx.send(embed = emb)

#Проверка ip_info
@ip_info.error 
async def ip_info_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно введите айпи адрес!\n\n``Пример:\n!ip_info 74.125.77.147``\n\n•Айпи адрес нужно вводить без пробелов, только точки и цифры!', color=0xff0000))

#phone_info
@Bot.command()
async def phone_info( ctx, arg ):
    response = requests.get( f'https://htmlweb.ru/geo/api.php?json&telcod={ arg }' )

    user_country = response.json()[ 'country' ][ 'english' ]
    user_id = response.json()[ 'country' ][ 'id' ]
    user_location = response.json()[ 'country' ][ 'location' ]
    user_city = response.json()[ 'capital' ][ 'english' ]
    user_width = response.json()[ 'capital' ][ 'latitude' ]
    user_lenth = response.json()[ 'capital' ][ 'longitude' ]
    user_post = response.json()[ 'capital' ][ 'post' ]
    user_oper = response.json()[ '0' ][ 'oper' ]

    global all_info
    emb = discord.Embed(title = f'Информация о номере {arg}:',
    description = f':united_nations: **Страна**: { user_country }\n\n:id: **ID** : { user_id }\n\n:map: **Локация**: { user_location }\n\n:cityscape: **Город**: { user_city }\n\n:paperclip: **Широта**: { user_width }\n\n:paperclip: **Долгота**: { user_lenth }\n\n**:mailbox_closed: Индекс**: { user_post }\n\n:bust_in_silhouette: **Оператор**: { user_oper }', colour= 0x39d0d6, inline = False)
    emb.set_footer(text= "Вызвано: {}".format(ctx.message.author), icon_url= ctx.message.author.avatar_url)

    await ctx.send(embed = emb)

#Проверка phone_info
@phone_info.error 
async def phone_info_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно введите номер телефона!\n\n``Пример:\n!phone_info 88005553535``\n\n•Можно вводить только русские, украинские и казахстанские номера!', color=0xff0000))

#send
@Bot.command()
async def send(ctx, member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = ":grey_exclamation: Обязательно укажите: ``пользователя!``", color=0xff0000))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = ":grey_exclamation: Обязательно укажите: ``сообщение!``", color=0xff0000))

    else:

        await member.send(embed = discord.Embed(description = f':bell: Пользователь **{ctx.author.name}**, отправил Вам сообщение: **{reason}** ', colour = 0x39d0d6))
        await ctx.send(embed = discord.Embed(description = f':white_check_mark: Сообщение успешно отправлено!', colour = 0x39d0d6))

#report
@Bot.command()
async def report(ctx, *, arg):
    channel_log = Bot.get_channel(668844030787977229)
    emb_log = discord.Embed(
        title = f':rotating_light: Жалоба от пользователя {ctx.author.name}:',
        description = f':bust_in_silhouette: Жалующийся: {ctx.author.name}\n :bookmark: Причина: {arg}', colour= 0xff0000)
    emb = discord.Embed(
        description= f':alarm_clock: {ctx.author.name}, ваша жалоба принята, ждите ответа!', colour= 0x39d0d6)
    await channel_log.send(embed= emb_log)
    await ctx.send(embed=emb)

#Проверка report
@report.error 
async def report_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно упомяните @пользователя и причину!\n\n``Пример:\n!report @disorder причина\n!report 358983628073730050 причина``\n\n•Вместо @пользователь можно указать айди человека, на которого вы жалуетесь!', color=0xff0000))

#roleinfo
@Bot.command()
async def roleinfo(ctx, Role: discord.Role):
    guild = ctx.guild
    emb = discord.Embed(title='Информация о роли:', description= f":page_facing_up: **Название роли: ** {Role.name} \n\n"
                                                                 f":watch: **Создание роли: ** {Role.created_at.strftime('%b %#d, %Y')} \n\n"
                                                                 f":1234: **Позиция роли: **  {Role.position} \n\n"
                                                                 f":paintbrush: **Цвет роли: ** {Role.colour} \n\n"
                                                                 , colour= Role.colour, inline = False, timestamp=ctx.message.created_at)

    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

#Проверка roleinfo
@roleinfo.error 
async def roleinfo_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно упомяните **@роль**!\n\n``Пример:\n!roleinfo @Admins\n!roleinfo 639568498246418434``\n\n•Вместо **@роль** можно указать айди роли, информацию о которой Вы хотите узнать!', color=0xff0000))

#serverinfo
@Bot.command()
async def serverinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    emb = discord.Embed(title="Информация о сервере:", description= f":page_facing_up: **Название сервера: ** {guild.name} \n\n"
                                                                    f":watch: **Создание сервера: ** {guild.created_at.strftime('%b %#d, %Y')} \n\n"
                                                                    f":speaking_head: **Глава сервера: **  {guild.owner} \n\n"
                                                                    f":postbox: **Регион сервера: ** {guild.region} \n\n"
                                                                    f":busts_in_silhouette: **Людей на сервере: ** {guild.member_count} \n\n"
                                                                    f":military_medal: **Уровень сервера: ** {guild.premium_tier} \n\n"
                                                                    , color=0xff0000, inline = False, timestamp=ctx.message.created_at)


    emb.set_thumbnail(url=ctx.guild.icon_url)
    emb.set_footer(text=f"ID: {guild.id}")

    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


#math
@Bot.command()
async def math( ctx, a : int, arg, b : int ):

    try:

        if arg == '+':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a + b }', color=0xff0000))  

        elif arg == '-':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a - b }', color=0xff0000))  

        elif arg == '/':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a / b }', color=0xff0000))

        elif arg == '*':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a * b }', color=0xff0000))      

    except:
        
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Произошла ошибка.**', color=0xff0000)) 

#Проверка math
@math.error 
async def math_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}**, для выполнения данной команды обязательно введите выражение!\n\n``Пример:\n!math 2 - 2\n!math 2 + 2\n!math 2 / 2\n!math 2 * 2``\n\n•Между всеми знаками должны быть пробелы, выражение 2+2 не сработает!\n•Можно произвести вычисление только с двумя цифрами, выражение 2 + 2 + 2 не сработает!', color=0xff0000))

#mute
@Bot.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 
    mute_role = discord.utils.get(member.guild.roles, id = 668503719758921746) #Айди роли
    channel_log = bot.get_channel(668844030787977229) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xff0000)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xff0000))  

#Проверка mute
@mute.error 
async def mute_error(ctx, error):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, у вас нет прав для использования данной команды.**', color=0xff0000))
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))

#unmute
@Bot.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 668503719758921746) #Айди роли
        channel_log = bot.get_channel(668844030787977229) #Айди канала логов

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0xff0000)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0xff0000))    

# Работа с ошибками размута

@unmute.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0xff0000))

#tempmute
@Bot.command()
@commands.has_permissions( administrator = True )
async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 668503719758921746) #Айди роли
    channel_log = bot.get_channel(668844030787977229) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( mute_role )   

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

#avatar
@Bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f':bust_in_silhouette: Аватар пользователя {user}', color= 0x39d0d6)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)

#time
@Bot.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= Bot.user.name, icon_url=Bot.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb )  

#messages
class Messages:

    def __init__(self, Bot):
        self.Bot = Bot

    async def number_messages(self, member):
        n_messages = 0
        for guild in self.Bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit = None):
                        if message.author == member:
                            n_messages += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue
        return n_messages

@Bot.command(name = "messages")
async def num_msg(ctx, member: discord.Member = None):
    user = ctx.message.author if (member == None) else member
    number = await Messages(Bot).number_messages(user)
    embed = discord.Embed(description = f":envelope: Количество сообщений на сервере от **{user.name}** — **{number}**!", color= 0x39d0d6)
    await ctx.send(embed = embed)

#ban
@Bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.ban(reason = reason)
    await ctx.send(f':octagonal_sign: Пользователь {member.mention} был забанен', color= 0xff0000)
    print(f'[INFO] Пользователь {member.name} был заблокирован')

#Проверка ban
@ban.error 
async def ban_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#unban
@Bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member: discord.Member):
    await ctx.channel.purge(limit = 1)
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f':octagonal_sign: Пользователь {user.mention} был разблокирован', color= 0xff0000)
        return
    print(f'[INFO] Пользователь {member.name} был разблокирован')

#Проверка unban
@unban.error 
async def unban_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#kick
@Bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.kick(reason = reason)
    await ctx.send(f':octagonal_sign: Пользователь {member.mention} был кикнут', color= 0xff0000)
    print(f'[INFO] Пользователь {member.name} был кикнут')

#Проверка kick
@kick.error 
async def kick_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))


#voice_create
@Bot.command()
@commands.has_permissions(administrator = True)
async def voice_create(ctx, *, arg): 
    guild = ctx.guild
    channel = await guild.create_voice_channel(f'{arg}')
    await ctx.send(embed = discord.Embed(description = f'**:microphone2: Голосовой канал "{arg}" успешно создан!**', color=0xff0000))

#Проверка voice_create
@voice_create.error 
async def voice_create_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#channel_create
@Bot.command()
@commands.has_permissions(administrator = True)
async def channel_create(ctx, *, arg): 
    guild = ctx.guild
    channel = await guild.create_text_channel(f'{arg}')
    await ctx.send(embed = discord.Embed(description = f'**:keyboard: Текстовый канал "{arg}" успешно создан!**', color=0xff0000))

#Проверка channel_create
@channel_create.error 
async def voice_create_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#remove_role
@Bot.command()
@commands.has_permissions(administrator= True)
async def remove_role(ctx, user: discord.Member, role: discord.Role):

    await discord.Member.remove_roles(user, role)
    await ctx.send(embed = discord.Embed(description = f':white_check_mark: Роль успешна была забрана!', color=0xff0000))

#Проверка remove_role
@remove_role.error 
async def remove_role_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#change_name
@Bot.command(name = "change_name", aliases = ["rename", "change"])
@commands.has_permissions(kick_members = True)
async def name(ctx, member: discord.Member = None, nickname: str = None):
    try:
        if member is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите **пользователя**!"))
        elif nickname is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите ник!"))
        else:
            await member.edit(nick = nickname)
            await ctx.send(embed = discord.Embed(description = f"У пользователя **{member.name}** был изменен ник на **{nickname}**"))
    except:
        await ctx.send(embed = discord.Embed(description = f"Я не могу изменить ник пользователя **{member.name}**!"))
    print(f'[INFO] Пользователь {ctx.author.name} сменил никнейм {member.name} на {nickname}')

#move
@Bot.command()
@commands.has_permissions(administrator = True)

async def move(ctx, channel: discord.VoiceChannel = None, channel2: discord.VoiceChannel = None, member: discord.Member = None):
    await ctx.message.delete()
    if channel == None:
        pass

    elif channel2 == None:
        pass

    elif member == None:
        x = channel.members

    for member in x:
        await member.edit(voice_channel=channel2)
    else: 
        await member.edit(voice_channel=channel2)

#Проверка move
@move.error 
async def move_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#Логи удаленных сообщений
@Bot.event
async def on_message_delete(message):
    channel = Bot.get_channel(668844030787977229)
    if message.content is None:
        return
    embed = discord.Embed(colour=0xff0000, description=f"**{message.author} Удалил сообщение в канале {message.channel}** \n{message.content}",timestamp=message.created_at)

    embed.set_author(name=f"{message.author}", icon_url=f'{message.author.avatar_url}')
    embed.set_footer(text=f'ID Пользователя: {message.author.id} | ID Сообщения: {message.id}')
    await channel.send(embed=embed)
    return

#Логи редактированных сообщений
@Bot.event
async def on_message_edit(before, after):
    channel = Bot.get_channel(668844030787977229)
    if before.author == Bot.user:
        return
    if before.content is None:
        return
    elif after.content is None:
        return
    message_edit = discord.Embed(colour=0xff0000,
                                 description=f"**{before.author} Изменил сообщение в канале {before.channel}** "
                                             f"\nСтарое сообщение:{before.content}"
                                             f"\n\nНовое сообщение: {after.content}",timestamp=before.created_at)

    message_edit.set_author(name=f"{before.author}",icon_url=f"{before.author.avatar_url}")
    message_edit.set_footer(text=f"ID Пользователя: {before.author.id} | ID Сообщения: {before.id}")
    await channel.send(embed=message_edit)
    return

#add_role
@Bot.command()
@commands.has_permissions(administrator= True)
async def add_role(ctx, user: discord.Member, role: discord.Role):
    await discord.Member.add_roles(user, role)
    await ctx.send(embed= discord.Embed(description= f":white_check_mark: Роль успешно выдана!", color=0xff0000))
    print(f'[INFO] Пользователь {member.name} выдал роль {role} участнику {ctx.author.name}')

#Проверка add_role
@add_role.error 
async def add_role_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#clear
@Bot.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed= discord.Embed(description= f":white_check_mark: Сообщения успешно удалены!", color=0xff0000))
    print(f'[INFO] Пользователь {member.name} удалил {amount} сообщений')

#Проверка clear
@clear.error 
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#Удаление сообщений
@Bot.event
async def  on_message(msg):
    await Bot.process_commands(msg)
    ban_msg = ["Артем"]
    if msg.content in ban_msg:
        await msg.delete()

#say
@Bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *args):
    await ctx.message.delete()
    args = ''.join(args).split('/', maxsplit = 1)
    try:
        user = Bot.get_user(int(args[0][args[0].find("!") + 1 : -1]))
        await user.send(args[1])
    except:
        await ctx.send(args[0])
    print(f'[INFO] Пользователь {member.name} написал через бота')

#Проверка say
@say.error 
async def say_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f':no_entry: {ctx.author.name}, для выполнения данной команды обязательно введите аргумент!', color=0xff0000))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed= discord.Embed(description= f':no_entry: {ctx.author.name}, для выполнения данной команды у Вас недостаточно прав!.', color=0xff0000))

#coin
@Bot.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0xff0000))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0xff0000)) 


#hello
@Bot.command()
async def hello(ctx):
    await ctx.send(embed= discord.Embed(description= f":hand_splayed: Приветствую, {ctx.author.name}, я Коннор из компании Oriflame. Для того чтобы увидеть список команд, введите **!help**. В случае нахождения багов, писать главному разработчику в личные сообщения ВК: **/disorder27**", color= 0x39d0d6))

#info
@Bot.command()
async def info(ctx, Member: discord.Member):
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация об игроке.'.format(Member.name), description=f"**Участник зашёл на сервер**: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"**Имя**: {Member.name}\n\n"
                                                                                      f"**Никнейм**: {Member.nick}\n\n"
                                                                                      f"**Статус**: {Member.status}\n\n"
                                                                                      f"**ID**: {Member.id}\n\n"
                                                                                      f"**Высшая роль**: {Member.top_role}\n\n",color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

#random
@Bot.command()
async def random(ctx, number: int = None, number2: int = None):
    await ctx.message.delete() # Удаляет написанное вами сообщение
    if number == None:
        await ctx.send(int(randint(1, 100))) # Генерация числа
    else:
        await ctx.send(randint(number, number2)) # Генерация числа


#Token
Bot.run('NjY3NDIxMzIxMzMxNzM2NTc5.XiCe8Q.6uLAjbjzDR-bag30luAGSDV5tQs')