import asyncio

import random

import discord
from discord import Member, Guild

clienet = discord.Client()


antworten = ['Ja', 'Nein', 'Villeicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']


@clienet.event
async def on_ready():
    print("Wir sind eingeloggt als user {}".format(clienet.user.name))
    clienet.loop.create_task(status())


async def status():
    colors= [discord.Color.red(), discord.Color.orange(), discord.Color.gold(), discord.Color.green(), discord.Color.blue(),
             discord.Color.purple()]
    while True:
        await clienet.change_presence(activity=discord.Game('https://discord.gg/ZRAVnrh'), status=discord.Status.online)
        await asyncio.sleep(10)
        await clienet.change_presence(activity=discord.Game('auf 1 Server'), status=discord.Status.online)
        await asyncio.sleep(10)
        guild: Guild = clienet.get_guild(687670997880406061)
        if guild:
            role = guild.get_role(693968945933451335)
            if role:
                if role.position < guild.get_member(clienet.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))


def is_not_pinned(mess):
    return not mess.pinned


@clienet.event
async def on_member_join(member):
    if not member.bot:
        member(member).add_role(role_id=693106772860207184)
        embed = discord.Embed(title='Wilkommen {} auf dem HazeCloud Discord Server :blue_heart:'.format(member.name),
                              description='Wir heißen dich herzlich Wilkommen auf unserem Server!', color=0x22a7f0)
        try:
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print('Es konnte keine Wilkommensnachricht an {} gesendet werden'.format(Member.name))



@clienet.event
async def on_message(message):
    if message.author.bot:
        return
    if '!help' in message.content:
        await message.channel.send('**Hilfe zu HazeCloud-Discord**\r\n'
                                   '!help - Zeigt diese Hilfe an\r\n'
                                   '!clear <Zahl> - Cliert eine bestimmte Nachrichtenanzahl\r\n'
                                   '!userinfo <Name> - Gibt dir informationen über den angegebenen User\r\n'
                                   '!8ball <Nachricht> - Sieht die Zukunft vorraus')

    if message.content.startswith('!userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für: {}'.format(member.name),
                                      description='Dies ist eine Userinfo für {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ' '
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Bot programmiert von Cancelcloud#6069')
                mess = await message.channel.send(embed=embed)
                await mess.add_reaction('💯')

    if message.content.startswith('!clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted)-1))
                    await asyncio.sleep(0.5)
                    await message.channel.send('Diese Nachricht wird automatisch gelöscht!')
                    await asyncio.sleep(3)
                    await message.channel.purge(limit=2, check=is_not_pinned)

    if message.content.startswith('!8ball'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:])
            mess = await message.channel.send('Ich versuche deine Frage `{0}` zu beantworten'.format(frage))
            await asyncio.sleep(2)
            await mess.edit(content='Ich kontaktiere das Orakel...')
            await asyncio.sleep(2)
            await mess.edit(content='Deine Antwort zur Frage `{0}` lautet `{1}`'.format(frage, random.choice(antworten)))


clienet.run("NjkyNzYyNjI4OTY3MzY2Njc2.XoCpIg.Un8yZf8a_rD80BVOGcGatRRUbQo")
