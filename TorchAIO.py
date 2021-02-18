import math
import pygame
import webbrowser
import http.client
import httpx
import requests
import platform
import discord
import re
import colorama
from colorama import Fore
import datetime
import traceback
import json
import asyncio
from dhooks import Webhook, Embed
import os
import time
import pyfiglet
import cursor
import wikipedia
from time import sleep
from discord.ext import commands
import ctypes
from datetime import datetime
from random import randint, uniform, choice
ctypes.windll.kernel32.SetConsoleTitleW("Torch ALO | Prebeta | Version 0.0.2")
def fireworks():
    vector = pygame.math.Vector2
    gravity = vector(0, 0.3)
    DISPLAY_WIDTH = DISPLAY_HEIGHT = 800

    trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)]
    dynamic_offset = 1
    static_offset = 5

    class Firework:

        def __init__(self):
            self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.colours = (
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.firework = Particle(randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT, True,
                                     self.colour)  # Creates the firework particle
            self.exploded = False
            self.particles = []
            self.min_max_particles = vector(70, 225)

        def update(self, win):  # called every frame
            if not self.exploded:
                self.firework.apply_force(gravity)
                self.firework.move()
                for tf in self.firework.trails:
                    tf.show(win)

                self.show(win)

                if self.firework.vel.y >= 0:
                    self.exploded = True
                    self.explode()
            else:
                for particle in self.particles:
                    particle.apply_force(
                        vector(gravity.x + uniform(-1, 1) / 20, gravity.y / 2 + (randint(1, 8) / 100)))
                    particle.move()
                    for t in particle.trails:
                        t.show(win)
                    particle.show(win)

        def explode(self):
            amount = randint(self.min_max_particles.x, self.min_max_particles.y)
            for i in range(amount):
                self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, False, self.colours))

        def show(self, win):
            pygame.draw.circle(win, self.colour, (int(self.firework.pos.x), int(self.firework.pos.y)),
                               self.firework.size)

        def remove(self):
            if self.exploded:
                for p in self.particles:
                    if p.remove is True:
                        self.particles.remove(p)

                if len(self.particles) == 0:
                    return True
                else:
                    return False

    class Particle:

        def __init__(self, x, y, firework, colour):
            self.firework = firework
            self.pos = vector(x, y)
            self.origin = vector(x, y)
            self.radius = 20
            self.remove = False
            self.explosion_radius = randint(5, 18)
            self.life = 0
            self.acc = vector(0, 0)
            # trail variables
            self.trails = []  # stores the particles trail objects
            self.prev_posx = [-10] * 10  # stores the 10 last positions
            self.prev_posy = [-10] * 10  # stores the 10 last positions

            if self.firework:
                self.vel = vector(0, -randint(17, 20))
                self.size = 5
                self.colour = colour
                for i in range(5):
                    self.trails.append(Trail(i, self.size, True))
            else:
                self.vel = vector(uniform(-1, 1), uniform(-1, 1))
                self.vel.x *= randint(7, self.explosion_radius + 2)
                self.vel.y *= randint(7, self.explosion_radius + 2)
                self.size = randint(2, 4)
                self.colour = choice(colour)
                for i in range(5):
                    self.trails.append(Trail(i, self.size, False))

        def apply_force(self, force):
            self.acc += force

        def move(self):
            if not self.firework:
                self.vel.x *= 0.8
                self.vel.y *= 0.8

            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

            if self.life == 0 and not self.firework:  # check if particle is outside explosion radius
                distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
                if distance > self.explosion_radius:
                    self.remove = True

            self.decay()

            self.trail_update()

            self.life += 1

        def show(self, win):
            pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0),
                               (int(self.pos.x), int(self.pos.y)),
                               self.size)

        def decay(self):  # random decay of the particles
            if 50 > self.life > 10:  # early stage their is a small chance of decay
                ran = randint(0, 30)
                if ran == 0:
                    self.remove = True
            elif self.life > 50:
                ran = randint(0, 5)
                if ran == 0:
                    self.remove = True

        def trail_update(self):
            self.prev_posx.pop()
            self.prev_posx.insert(0, int(self.pos.x))
            self.prev_posy.pop()
            self.prev_posy.insert(0, int(self.pos.y))

            for n, t in enumerate(self.trails):
                if t.dynamic:
                    t.get_pos(self.prev_posx[n + dynamic_offset], self.prev_posy[n + dynamic_offset])
                else:
                    t.get_pos(self.prev_posx[n + static_offset], self.prev_posy[n + static_offset])

    class Trail:

        def __init__(self, n, size, dynamic):
            self.pos_in_line = n
            self.pos = vector(-10, -10)
            self.dynamic = dynamic

            if self.dynamic:
                self.colour = trail_colours[n]
                self.size = int(size - n / 2)
            else:
                self.colour = (255, 255, 200)
                self.size = size - 2
                if self.size < 0:
                    self.size = 0

        def get_pos(self, x, y):
            self.pos = vector(x, y)

        def show(self, win):
            pygame.draw.circle(win, self.colour, (int(self.pos.x), int(self.pos.y)), self.size)

    def update(win, fireworks):
        for fw in fireworks:
            fw.update(win)
            if fw.remove():
                fireworks.remove(fw)

        pygame.display.update()

    def main():
        pygame.init()
        pygame.display.set_caption("Fireworks in Pygame")
        win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        clock = pygame.time.Clock()

        fireworks = [Firework() for i in range(2)]  # create the first fireworks
        running = True

        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:  # Change game speed with number keys
                    if event.key == pygame.K_1:
                        fireworks.append(Firework())
                    if event.key == pygame.K_2:
                        for i in range(10):
                            fireworks.append(Firework())
            win.fill((20, 20, 30))  # draw background

            if randint(0, 10) == 1:  # create new firework
                fireworks.append(Firework())

            update(win, fireworks)

            # stats for fun
            # total_particles = 0
            # for f in fireworks:
            #    total_particles += len(f.particles)

            # print(f"Fireworks: {len(fireworks)}\nParticles: {total_particles}\n\n")

        pygame.quit()

    main()
def sprint(string):
    for letter in string:
        __builtins__.print(letter, end='', flush=True)
        time.sleep(0.00000001)
    __builtins__.print("")
def clear():
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')
def webhooker():
    print("""
     | |    | |___| |__ | |__   ___   ___ | | __   
     | | /\ | | _ \ '_ \| '_ \ / _ \ / _ \| |/ /   
      \ V  V /  __/ |_) | | | | (_) | (_) |   <    
      _\_/\_/ \___|_.__/|_| |_|\___/_\___/|_|\_\   

    """)
    url = input("Webhook URLs(ex: 1234, 1234, 1234,) ").split(", ")
    embed = {}
    embedtitle = input("Embed title: ")
    embed["title"] = embedtitle
    embeddesc = input("Embed description: ")
    embed["description"] = embeddesc
    while True:  # Thumbnail (optional)
        thumbnailornot = input("Add a thumbnail? (Yes/no): ")
        if thumbnailornot.lower() == 'yes':
            embedthumbnailurl = input("Enter a thumbnail URL: ")
            embed['thumbnail'] = {"url": embedthumbnailurl}
            break
        elif thumbnailornot.lower() == 'no':
            break
        else:
            print("Please enter either 'yes' or 'no' (without quotes).")
    embedfieldnum = input("How many fields in the embed? (Enter a number, 0 for none): ")
    try:
        embedfieldnum = int(embedfieldnum)
    except:
        print("You were supposed to enter a number xD")
    if embedfieldnum != 0:
        embed['fields'] = []
        for fieldnum in range(embedfieldnum):
            fieldtitle = input("Field {} Title: ".format(fieldnum + 1))
            fieldtext = input("Field {} Content: ".format(fieldnum + 1))
            embed['fields'].append({"name": fieldtitle, "value": fieldtext})
    embedcolor = input("Embed Hex Color (6 Digit Hex): ")
    embedcolor = int(embedcolor, 16)
    embed["color"] = embedcolor
    print(embed)
    data = {"embeds": [embed]}
    requests.post(url, json=data)
    input("Successfully sent embed! Press enter to go back to main menu!")
    mainMenu()
def spy():
    BOT_PREFIX = '.'
    client = commands.Bot(command_prefix=BOT_PREFIX)

    class TorchError(Exception):
        def __init__(self, error, reason):
            self.error = error
            self.reason = reason
            print(
                f'{Fore.LIGHTRED_EX}An error has occurred while running TorchALO. Here is some more information:{Fore.RESET}\nError: {error}\nReason: {reason}')

    clear()
    client.remove_command("help")
    with open('config.json') as f:
        config = json.load(f)
    token = config.get('token')
    time.sleep(3)

    client = discord.Client()

    sprint(f""" {Fore.RED}

  ________  _______  ___________  ____  ____    _______   
 /"       )/"     "|("     _   ")("  _||_ " |  |   __ "\  
(:   \___/(: ______) )__/  \\__/ |   (  ) : |  (. |__) :) 
 \___  \   \/    |      \\_ /    (:  |  | . )  |:  ____/  
  __/  \\  // ___)_     |.  |     \\ \__/ //   (|  /      
 /" \   :)(:      "|    \:  |     /\\ __ //\  /|__/ \     
(_______/  \_______)     \__|    (__________)(_______)    


        """)
    webhook = input(
        "What is the webhook URL you would like all messages sent to: ")
    userinput = input(
        "what are the Channel ID's of the channels you would like to monitor?[1234 1234 1234] ")
    Channels = userinput.split()
    clear()

    hook = Webhook(webhook)

    @client.event
    async def on_ready():
        sprint(f""" {Fore.RED}

  ________  _______  ___  ___  __    _____  ___    _______        __    _____  ___    __  ___________  __          __      ___        __   ________    _______  ________   
 /"       )|   __ "\|"  \/"  ||" \  (\"   \|"  \  /" _   "|      |" \  (\"   \|"  \  |" \("     _   ")|" \        /""\    |"  |      |" \ ("      "\  /"     "||"      "\  
(:   \___/ (. |__) :)\   \  / ||  | |.\\   \    |(: ( \___)      ||  | |.\\   \    | ||  |)__/  \\__/ ||  |      /    \   ||  |      ||  | \___/   :)(: ______)(.  ___  :) 
 \___  \   |:  ____/  \\  \/  |:  | |: \.   \\  | \/ \           |:  | |: \.   \\  | |:  |   \\_ /    |:  |     /' /\  \  |:  |      |:  |   /  ___/  \/    |  |: \   ) || 
  __/  \\  (|  /      /   /   |.  | |.  \    \. | //  \ ___      |.  | |.  \    \. | |.  |   |.  |    |.  |    //  __'  \  \  |___   |.  |  //  \__   // ___)_ (| (___\ || 
 /" \   :)/|__/ \    /   /    /\  |\|    \    \ |(:   _(  _|     /\  |\|    \    \ | /\  |\  \:  |    /\  |\  /   /  \\  \( \_|:  \  /\  |\(:   / "\ (:      "||:       :) 
(_______/(_______)  |___/    (__\_|_)\___|\____\) \_______)     (__\_|_)\___|\____\)(__\_|_)  \__|   (__\_|_)(___/    \___)\_______)(__\_|_)\_______) \_______)(________/  

    """)
        # print(Channels)  # this is just for debugging purposes tbh
        print('spy running as ' + client.user.name +
              "#" + client.user.discriminator)

    @client.event
    async def on_message(message):
        if str(message.channel.id) in Channels:

            # hook.send(embed=embed)
            if message.attachments:
                attachment = message.attachments[0]
                requests.post(webhook, data={'content': message.content + "\n*Attachment: " + attachment.url + "*",
                                             'username': message.author.name + ' [#' + message.channel.name + ']',
                                             'avatar_url': str(message.author.avatar_url)})
            else:
                requests.post(webhook, data={'content': message.content,
                                             'username': message.author.name + ' [#' + message.channel.name + ']',
                                             'avatar_url': str(message.author.avatar_url)})
            ok = message.embeds
            for sex in ok:
                # print(sex.description)
                author_name = sex.author.name
                author_icon = sex.author.icon
                if not author_name:
                    author_name = ''
                if not author_icon:
                    author_icon = ''
                fields = sex.fields
                description = sex.description
                timestamp = sex.timestamp
                if not description:
                    description = ''
                if not timestamp:
                    timestamp = ''
                # print(description)
                embed = Embed(
                    description=str(description),
                    # color=str(sex.color),
                    timestamp=str(timestamp)
                )
                embed.set_author(name=str(author_name),
                                 icon_url=str(author_icon))
                if sex.fields:
                    for field in fields:
                        embed.add_field(name=str(field.name),
                                        value=str(field.value))
                # print(footer.text)
                footer_text = sex.footer.text
                if not footer_text:
                    footer_text = ''
                footer_icon_url = sex.footer.icon_url
                if not footer_icon_url:
                    footer_icon_url = ''
                embed.set_footer(text=str(footer_text),
                                 icon_url=str(footer_icon_url))
                thumbnail = sex.thumbnail.url
                if not thumbnail:
                    thumbnail = ''
                embed.set_thumbnail(thumbnail)
                image = sex.image.url
                if not image:
                    image = ''
                embed.set_image(image)
                hook.send(embed=embed)

    client.run(token, bot=False)
def nitrosniper():
    # if os == "Windows":
    clear()
    # else:
    #     system("clear")
    #     print(chr(27) + "[2J")
    BOT_PREFIX = '.'

    client = commands.Bot(command_prefix=BOT_PREFIX)

    codeRegex = re.compile(
        "(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
    sprint(f''' {Fore.RED}

 _____  ___    __  ___________  _______     ______         ________  _____  ___    __       _______    _______   _______   
(\"   \|"  \  |" \("     _   ")/"      \   /    " \       /"       )(\"   \|"  \  |" \     |   __ "\  /"     "| /"      \  
|.\\   \    | ||  |)__/  \\__/|:        | // ____  \     (:   \___/ |.\\   \    | ||  |    (. |__) :)(: ______)|:        | 
|: \.   \\  | |:  |   \\_ /   |_____/   )/  /    ) :)     \___  \   |: \.   \\  | |:  |    |:  ____/  \/    |  |_____/   ) 
|.  \    \. | |.  |   |.  |    //      /(: (____/ //       __/  \\  |.  \    \. | |.  |    (|  /      // ___)_  //      /  
|    \    \ | /\  |\  \:  |   |:  __   \ \        /       /" \   :) |    \    \ | /\  |\  /|__/ \    (:      "||:  __   \  
 \___|\____\)(__\_|_)  \__|   |__|  \___) \"_____/       (_______/   \___|\____\)(__\_|_)(_______)    \_______)|__|  \___) 

Caution: USE THIS AT YOUR OWN RISK. SNIPERS ARE AGAINST DISCORD TOS''')

    class TorchError(Exception):
        def __init__(self, error, reason):
            self.error = error
            self.reason = reason
            print(
                f'{Fore.LIGHTRED_EX}An error has occurred while running TorchALO. Here is some more information:{Fore.RESET}\nError: {error}\nReason: {reason}')

    client.remove_command("help")
    with open('config.json') as f:
        config = json.load(f)
    token = config.get('token')

    bot = commands.Bot(command_prefix=".", self_bot=True)
    codeRegex = re.compile(
        "(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
    a = 2
    while a == 2:

        try:
            @bot.event
            async def on_message(ctx):
                bruh = 1
                if bruh == 1:
                    print(Fore.LIGHTCYAN_EX + 'Sniping Discord Nitro and Giveaway on ' + str(
                        len(bot.guilds)) + ' Servers \n' + Fore.RESET)
                    print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ",
                                                            time.localtime()) + Fore.RESET, end='')
                    print("[+] Bot is ready")
                    ready = True
                bruh = bruh + 1

                if codeRegex.search(ctx.content):
                    print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ",
                                                            time.localtime()) + Fore.RESET, end='')
                    code = codeRegex.search(ctx.content).group(2)

                    start_time = time.time()
                    if len(code) < 16:
                        try:
                            print(
                                Fore.LIGHTRED_EX + "[=] Auto-detected a fake code: " + code + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.LIGHTMAGENTA_EX + " [" + ctx.guild.name + " > " + ctx.channel.name + "]" + Fore.RESET)
                        except:
                            print(
                                Fore.LIGHTRED_EX + "[=] Auto-detected a fake code: " + code + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.RESET)

                    else:
                        async with httpx.AsyncClient() as client:
                            result = await client.post(
                                'https://discordapp.com/api/v6/entitlements/gift-codes/' + code + '/redeem',
                                json={'channel_id': str(ctx.channel.id)},
                                headers={'authorization': token, 'user-agent': 'Mozilla/5.0'})
                            delay = (time.time() - start_time)
                            try:
                                print(
                                    Fore.LIGHTGREEN_EX + "[-] Sniped code: " + Fore.LIGHTRED_EX + code + Fore.RESET + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.LIGHTMAGENTA_EX + " [" + ctx.guild.name + " > " + ctx.channel.name + "]" + Fore.RESET)
                            except:
                                print(
                                    Fore.LIGHTGREEN_EX + "[-] Sniped code: " + Fore.LIGHTRED_EX + code + Fore.RESET + " From " + ctx.author.name + "#" + ctx.author.discriminator + Fore.RESET)

                        if 'This gift has been redeemed already' in str(result.content):
                            print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ",
                                                                    time.localtime()) + Fore.RESET, end='')
                            print(Fore.LIGHTYELLOW_EX + "[-] Code has been already redeemed" + Fore.RESET,
                                  end='')
                        elif 'nitro' in str(result.content):
                            print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ",
                                                                    time.localtime()) + Fore.RESET, end='')
                            print(Fore.GREEN +
                                  "[+] Code applied" + Fore.RESET, end='')
                        elif 'Unknown Gift Code' in str(result.content):
                            print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ",
                                                                    time.localtime()) + Fore.RESET, end='')
                            print(Fore.LIGHTRED_EX +
                                  "[-] Invalid Code" + Fore.RESET, end=' ')
                        print(" Delay:" + Fore.GREEN + " %.3fs" %
                              delay + Fore.RESET)

            bot.run(token, bot=False)
        except:
            file = open("traceback.txt", "w")
            file.write(traceback.format_exc())
            file.close()
            exit(0)
def tokenfinder():
    clear()

    def clear():
        if platform.system() == 'Linux':
            os.system('clear')
        elif platform.system() == 'Windows':
            os.system('cls')

    clear()

    print(f"""{colorama.Fore.LIGHTCYAN_EX}
          /$$$$$$$$        /$$                                 /$$$$$$$$ /$$                 /$$                    
         |__  $$__/       | $$                                | $$_____/|__/                | $$                    
            | $$  /$$$$$$ | $$   /$$  /$$$$$$  /$$$$$$$       | $$       /$$ /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$ 
            | $$ /$$__  $$| $$  /$$/ /$$__  $$| $$__  $$      | $$$$$   | $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
            | $$| $$  \ $$| $$$$$$/ | $$$$$$$$| $$  \ $$      | $$__/   | $$| $$  \ $$| $$  | $$| $$$$$$$$| $$  \__/
            | $$| $$  | $$| $$_  $$ | $$_____/| $$  | $$      | $$      | $$| $$  | $$| $$  | $$| $$_____/| $$      
            | $$|  $$$$$$/| $$ \  $$|  $$$$$$$| $$  | $$      | $$      | $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$      
            |__/ \______/ |__/  \__/ \_______/|__/  |__/      |__/      |__/|__/  |__/ \_______/ \_______/|__/{colorama.Fore.RESET}
    {colorama.Style.DIM}
    {colorama.Fore.LIGHTMAGENTA_EX}
    by SeedOfArson#4954                                               
    {colorama.Fore.RESET}
    """)

    def find_tokens(path):
        path += '\\Local Storage\\leveldb'

        tokens = []

        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        return tokens

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    tokenz = []
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        tokens = find_tokens(path)
        for token in tokens:
            tokenz.append(token)

    for token in tokenz:
        req = requests.get("https://canary.discordapp.com/api/v6/users/@me", headers={'authorization': token})
        if req.status_code == 401:
            print(
                f"{colorama.Fore.RED}Invalid Token{colorama.Fore.LIGHTWHITE_EX}{colorama.Style.BRIGHT}:{colorama.Style.NORMAL}{colorama.Fore.LIGHTRED_EX} {token}")
        elif req.status_code == 200:
            req_json = req.json()
            user_name = f'{req_json["username"]}#{req_json["discriminator"]}'
            print(
                f"{colorama.Fore.GREEN}{user_name}{colorama.Fore.LIGHTWHITE_EX}{colorama.Style.BRIGHT}:{colorama.Style.NORMAL}{colorama.Fore.LIGHTGREEN_EX} {token}")
    input(
        f"\n\n{colorama.Fore.WHITE}Press {colorama.Style.BRIGHT}enter{colorama.Style.NORMAL} to exit!{colorama.Fore.RESET}")

    mainMenu()
def selfbot():
    class TorchError(Exception):
        def __init__(self, error, reason):
            self.error = error
            self.reason = reason
            print(
                f'{Fore.LIGHTRED_EX}An error has occurred while running TorchALO. Here is some more information:{Fore.RESET}\nError: {error}\nReason: {reason}')

    clear()
    colorama.init()
    with open('config.json') as f:
        config = json.load(f)

    def Init():
        if config.get('token') == "token here":
            clear()
            raise TorchError(
                error='Login Error',
                reason='Can\'t log into Discord without a token. (Did you enter a token in config.json?)')
        else:
            try:
                client.run(token, bot=False, reconnect=True)
            except Exception as error:
                print(f"Error logging into token: {error}")
                input()

    token = config.get('token')
    prefix = "."
    val = "60"

    client = commands.Bot(description="Torch stuff",
                          command_prefix=prefix, self_bot=True)

    client.remove_command('help')
    clear()
    try:
        ctypes.windll.kernel32.SetConsoleTitleW('Login Success')
    except:
        pass
    print(
        f"                   {Fore.LIGHTCYAN_EX}Made by the TorchFNF team{Fore.RESET}")

    @client.event
    async def on_connect():
        clear()
        print(
            f'{Fore.RESET}{Fore.RED}SELFBOTS ARE AGAINST DISCORD TOS! BY CONTINUING YOU ACKNOWLEDGE THIS AND RECOGNIZE THAT THE CREATORS OF THIS TOOL ARE NOT RESPONSIBLE FOR ANY DAMAGES CAUSED!{Fore.RESET}')
        time.sleep(5)
        clear()
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'Welcome to TorchALO, {client.user.name}#{client.user.discriminator}.')
        except:
            pass
        splash()

    def splash():
        sprint(f'''{Fore.RED}

 ___________  ______     _______    ______    __    __        ________  _______  ___       _______  _______     ______  ___________  
("     _   ")/    " \   /"      \  /" _  "\  /" |  | "\      /"       )/"     "||"  |     /"     "||   _  "\   /    " \("     _   ") 
 )__/  \\__/// ____  \ |:        |(: ( \___)(:  (__)  :)    (:   \___/(: ______)||  |    (: ______)(. |_)  :) // ____  \)__/  \\__/  
    \\_ /  /  /    ) :)|_____/   ) \/ \      \/      \/      \___  \   \/    |  |:  |     \/    |  |:     \/ /  /    ) :)  \\_ /     
    |.  | (: (____/ //  //      /  //  \ _   //  __  \\       __/  \\  // ___)_  \  |___  // ___)  (|  _  \\(: (____/ //   |.  |     
    \:  |  \        /  |:  __   \ (:   _) \ (:  (  )  :)     /" \   :)(:      "|( \_|:  \(:  (     |: |_)  :)\        /    \:  |     
     \__|   \"_____/   |__|  \___) \_______) \__|  |__/     (_______/  \_______) \_______)\__/     (_______/  \"_____/      \__|     





    {Fore.RESET}{Fore.LIGHTYELLOW_EX}Welcome to {Fore.RED}TorchALO Selfbot{Fore.RESET}
    {Fore.CYAN}Info{Fore.RESET}

    {Fore.LIGHTGREEN_EX}Prefix: {Fore.WHITE}{prefix}{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}Help Command: {Fore.LIGHTRED_EX}{prefix}help{Fore.RESET}
    {Fore.LIGHTRED_EX}Number of commands: {len(client.commands)} {Fore.RESET}
    {Fore.LIGHTGREEN_EX}Number of server's you are in: {len(client.guilds)}{Fore.RESET}
    {client.user.name}#{client.user.discriminator}{Fore.RESET}
    {Fore.LIGHTBLUE_EX}Display Name: {client.user.name}
    {Fore.LIGHTMAGENTA_EX}Delete after: {val} seconds
            ''' + Fore.RESET)

    @client.command()
    async def bump(ctx):
        await ctx.message.delete()
        await ctx.send("Starting..", delete_after=int(val))
        while True:
            try:
                await ctx.send('!d bump')
                await asyncio.sleep(7200)
            except Exception as e:
                print(
                    f"Couldn't bump. Did the channel get deleted? Error: {e}")

    @client.command(aliases=['whois'])
    async def userinfo(ctx, member: discord.Member = None):
        await ctx.message.delete()
        if not member:
            member = ctx.message.author
        roles = [role for role in member.roles]
        embed = discord.Embed(color=0xFFFAFA, timestamp=ctx.message.created_at,
                              title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Display Name", value=member.display_name)
        try:
            embed.add_field(name="Mutual Friends", value=str(len(await member.mutual_friends())))
        except:
            pass

        embed.add_field(name="Created Account On", value=member.created_at.strftime(
            "%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On", value=member.joined_at.strftime(
            "%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles", value="".join(
            [role.mention for role in roles]))
        embed.add_field(name="Highest Role", value=member.top_role.mention)
        await ctx.send(embed=embed, delete_after=20)

    @client.command()
    async def help(ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='**__All Commands__**', color=0xff0000)
        embed.add_field(name="**setprefix**",
                        value="[prefix] lets you change the prefix from discord", inline=False)
        embed.add_field(
            name="**whois**", value="Get info about other users")
        embed.add_field(
            name="**bump**", value="bumps server that it is ran in automatically every 7200 seconds.", inline=False)
        embed.add_field(
            name="**purge**", value="Purges all of your messages in whatever channel/dm it is sent in", inline=False)
        embed.add_field(name="**downchecker**",
                        value="[website url] pings a **website.**", inline=False)
        embed.add_field(
            name="**stop**", value='Closes the selfbot.', inline=False)
        embed.add_field(name="**copy**",
                        value="copies the server that it is ran in.", inline=False)
        embed.add_field(name="**allcommands**",
                        value="sends every command in the selfbot as a list.", inline=False)
        embed.add_field(name="**hypesquad**",
                        value="Automatically changes your hypesquad badge to either [balance | brilliance | bravery | leave]",
                        inline=False)
        embed.add_field(name='**serverinfo**',
                        value='sends server info.', inline=False)
        embed.add_field(name='**listservers**',
                        value='lists all the servers you are in inside the console', inline=False)
        embed.add_field(name='**reset**',
                        value='clears the CLI of the selfbot.', inline=False)
        embed.add_field(
            name="**wiki**", value="Returns a summary of any wikipedia page", inline=False)
        embed.add_field(name="**listening**",
                        value="changes your discord status.", inline=False)
        embed.add_field(name="**playing**",
                        value="changes your discord status.", inline=False)
        embed.add_field(
            name='**embed**', value='Imbeds whatever text you want', inline=False)
        embed.add_field(name="**ascii**",
                        value="text to ascii art.", inline=False)
        embed.add_field(
            name="**tweet**", value="Sends a fake tweet image.", inline=False)
        embed.set_footer(text=f"Command prefix is \"{client.command_prefix}\"")
        await ctx.send(embed=embed, delete_after=int(val))

    @client.command()
    async def purge(ctx, amount: int):
        await ctx.message.delete()
        async for message in ctx.channel.history(limit=amount):
            if message.author == client.user:
                await message.delete()
            else:
                pass

    @client.command(aliases=['downchecker'])
    async def downtester(ctx, *, website):
        global r
        await ctx.message.delete()
        if website is None:
            pass
        else:
            try:
                r = requests.get(website).status_code
            except Exception as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)
            if r == 404:
                embed = discord.Embed(title=website + "** is down.**",
                                      description=f"responded with a status code of {r}",
                                      color=0xFFFAFA)
                await ctx.send(embed=embed, delete_after=int(val))
            else:
                embed = discord.Embed(title=website + " ** is online.**",
                                      description=f"sent status code of {r}",
                                      color=0xFFFAFA)
                await ctx.send(embed=embed, delete_after=int(val))

    @client.command(aliases=['stop'])
    async def logout(ctx):
        await ctx.message.delete()
        await ctx.send("Shutting down..", delete_after=0.2)
        await asyncio.sleep(2)
        exit(0)

    @client.event
    async def on_message_edit(before, after):
        await client.process_commands(after)

    @client.event
    async def on_command_error(ctx, error):
        error_str = str(error)
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            print(
                f"{Fore.RED}[ERROR]: {Fore.LIGHTCYAN_EX}YOU DONT HAVE THE PERMS TO DO THAT." + Fore.RESET)
        elif isinstance(error, commands.MissingRequiredArgument):
            print(
                f"{Fore.RED}[ERROR]: {Fore.LIGHTGREEN_EX}Missing arguments: {error}" + Fore.RESET)
        elif isinstance(error, discord.errors.Forbidden):
            print(
                f"{Fore.RED}[ERROR]: {Fore.CYAN}Not Allowed: {error}" + Fore.RESET)
        elif "Cannot send an empty message" in error_str:
            print(
                f"{Fore.RED}[ERROR]: {Fore.LIGHTYELLOW_EX}Cannot send an empty message" + Fore.RESET)
        else:
            print(
                f"{Fore.RED}[ERROR]: {Fore.LIGHTRED_EX}{error_str}" + Fore.RESET)

    @client.command()
    async def info(ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="**Selfbot Information**", color=0xFFFAFA)
        embed.add_field(name="**MADE BY**", value="TORCHFNF TEAM")
        embed.add_field(name="**running on**",
                        value=f"{client.user.name}#{client.user.discriminator}")
        embed.set_footer(text="Thank you for being a member!")
        await ctx.send(embed=embed, delete_after=int(val))

    @client.command(aliases=['reset'])
    async def cls(ctx):
        await ctx.message.delete()
        await ctx.send("Clearing Console..", delete_after=0.1)
        clear()
        splash()

    @client.command()
    async def playing(ctx, *, message):
        await ctx.message.delete()
        game = discord.Game(
            name=message
        )
        await client.change_presence(activity=game)

    @client.command()
    async def listening(ctx, *, message):
        await ctx.message.delete()
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=message,
            ))

    @client.command(aliases=['moreinfo'])
    async def clientinfo(ctx):
        await ctx.message.delete()
        await ctx.send("Moreinfo", delete_after=5)
        splash()
        print("\n")
        print(Fore.LIGHTCYAN_EX + 'More Info \n')
        print("Token: " + token)
        print(f"Email: {client.user.email}")
        print(f"Nitro: {format(client.user.premium)}")
        print(f"Verified: {format(client.user.verified)}")
        print("Name: " + client.user.name + "\n\n")

    @client.command(aliases=['bit'])
    async def btc(ctx):
        await ctx.message.delete()
        r = requests.get(
            'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,GBP')
        r = r.json()
        usd = r['USD']
        eur = r['EUR']
        gbp = r['GBP']
        embed = discord.Embed(title='**PRICE OF BTC**', color=0xFFFAFA)
        embed.add_field(name="**USD**", value=usd)
        embed.add_field(name="**EUR**", value=eur)
        embed.add_field(name="**GBP**", value=gbp)
        await ctx.send(embed=embed, delete_after=int(val))

    @client.command(aliases=['listservers'])
    async def allservers(ctx):
        await ctx.message.delete()
        async for guild in client.fetch_guilds():
            print(guild)
        await asyncio.sleep(25)
        splash()

    @client.command()
    async def embed(ctx, *, message):
        await ctx.message.delete()
        embed = discord.Embed(color=0xFFFAFA, description=message)
        embed.set_author(name=str(client.user.display_name + "#" +
                                  client.user.discriminator), icon_url=client.user.avatar_url)
        await ctx.send(embed=embed, delete_after=int(val))

    @client.command()
    async def getpfp(ctx, member: discord.Member = None):
        await ctx.message.delete()
        print(Fore.LIGHTBLUE_EX + f'{member.display_name}#{member.discriminator}\'s profile picture link: ' +
              Fore.LIGHTGREEN_EX + str(member.avatar_url))
        await asyncio.sleep(20)
        splash()

    @client.command()
    async def channels(ctx):
        await ctx.message.delete()
        await ctx.send('\n'.join([channel.mention for channel in ctx.guild.channels]))

    @client.command()
    async def ascii(ctx, *, message):
        await ctx.message.delete()
        result = pyfiglet.figlet_format(message)
        if len(result) > 1992:
            return
        else:
            await ctx.send('```' + result + '```')

    @client.command()
    async def tweet(ctx, username, *, message):
        await ctx.message.delete()
        r = requests.get(f'https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}').json()
        rstring = str(r)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', rstring)
        urlstring = str(urls)
        slicedurl = urlstring[2:]
        superslicedurl = slicedurl[:-4]
        await ctx.send(superslicedurl)

    @client.command()
    async def changemymind(ctx, texttest):  # formating or something
        await ctx.message.delete()  # deletes the command that you type in (.changemymind test should return https://nekobot.xyz/imagegen/a/f/c/d6882e1d521365634d52825dc2583.png)
        r = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=changemymind&text={texttest}').json()  # grabs the contents of the site
        rstring = str(r)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', rstring)
        urlstring = str(urls)
        slicedurl = urlstring[2:]
        superslicedurl = slicedurl[:-4]
        print(superslicedurl)
        await ctx.send(superslicedurl)

    @client.command()
    async def notaneasteregg(ctx):
        await ctx.message.delete()
        await ctx.send(
            "**I just wanted to say that the team here is super grateful that you even use our programs, thank you from the bottom of our hearts** \n -The Team")

    @client.command()
    async def setprefix(ctx, arg):
        await ctx.message.delete()
        client.command_prefix = arg
        clear()
        splash()

    @client.command(aliases=['serverinfo'])
    async def guildinfo(ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='**Guild Info**', color=0xFFFAFA)
        guild = ctx.message.guild
        roles = [role.mention for role in reversed(guild.roles)]
        embed.add_field(name='**Owner**',
                        value=f'<@{ctx.message.guild.owner_id}>', inline=False)
        embed.add_field(name='**Created **',
                        value=guild.created_at, inline=False)
        embed.add_field(name='**Rolecount**',
                        value=len(guild.roles), inline=False)
        embed.add_field(name='**Membercount**',
                        value=len(guild.members), inline=False)
        await ctx.send(embed=embed, delete_after=5)

    @client.command()
    async def allcommands(ctx):
        await ctx.message.delete()
        await ctx.send('```' + '\n'.join([str for str in client.all_commands]) + '```', delete_after=int(val))

    @client.command()
    async def wiki(ctx, *message):
        await ctx.message.delete()
        try:
            try:
                await ctx.send(wikipedia.summary(message, sentences=2))
            except UserWarning:
                pass
        except Exception as e:
            await ctx.send(e)

    @client.command()
    async def latency(ctx):
        await ctx.message.delete()
        await ctx.send(f'{int(round(client.latency * 1000))} ms')

    @client.command()
    async def nemesisspammer(ctx, message):
        await ctx.message.delete()
        for n in range(0, 10000):
            sleep(0.5)
            await ctx.send(message)



    @client.command()
    async def copy(ctx):
        await ctx.message.delete()
        xd = await client.create_guild(f'{ctx.guild.name}')
        g = await client.fetch_guild(xd.id)
        for cate in ctx.guild.categories:
            x = await g.create_category(f"{cate.name}")
            for chann in cate.channels:
                if isinstance(chann, discord.VoiceChannel):
                    await x.create_voice_channel(f"{chann}")
                if isinstance(chann, discord.TextChannel):
                    await x.create_text_channel(f"{chann}")
        try:
            await g.edit(icon=ctx.guild.icon_url)
        except:
            pass

    if __name__ == '__main__':
        try:
            cursor.hide()
        except:
            pass
        Init()
    else:
        mainMenu()
def setup():
    with open('./config.json', 'w') as fp:
        setup_token = input('Enter your Discord token here: ')
        setup_ClaimerTokens = list(map(str, input('Enter Claimer Tokens(12n41jr, nfajdnk): ').split(', ')))
        setup_data = {
            "token": setup_token,
            "ClaimerTokens": setup_ClaimerTokens
        }
        print('Settings can be changed at any time in "Configuration Editor"')
        time.sleep(3)
        json.dump(setup_data, fp, indent=4)
def initialSetup():
    if not os.path.exists('./config.json'):
        clear()
        print(Fore.LIGHTCYAN_EX +
              'Welcome to the initial setup process for the TorchALO.')
        setup()
    try:
        config = json.load(open('config.json'))
        config['token']
        config['ClaimerTokens']
    except json.decoder.JSONDecodeError:
        clear()
        print('\033[1;31mBroken configuration, repeating setup process...\n\033[1;00m')
        setup()
    clear()
def confedit():
    clear()
    print('''\033[1;33m
               __ _                    _   _                   _ _ _           
  __ ___ _ _  / _(_)__ _ _  _ _ _ __ _| |_(_)___ _ _    ___ __| (_) |_ ___ _ _ 
 / _/ _ \ ' \|  _| / _` | || | '_/ _` |  _| / _ \ ' \  / -_) _` | |  _/ _ \ '_|
 \__\___/_||_|_| |_\__, |\_,_|_| \__,_|\__|_\___/_||_| \___\__,_|_|\__\___/_|  
                   |___/                                                       
                   ''')
    config = json.load(open('config.json'))
    print('\033[1;33m    	Token: \033[1;m' + config['token'] +'\n\033[1;33m    	Delete After: \033[1;m' + '\n\033[1;33m    	Claimer Tokens: \033[1;m' + str(config['ClaimerTokens']))
    confopt = input("Edit configuration? (yes/no):").lower()
    if confopt == 'yes':
        with open('./config.json', 'w') as fp:
            setup()
    clear()
def BASICS():
    clear()

    with open('config.json') as f:
        config = json.load(f)
    token = config.get('token')
    claimertokens = config.get('ClaimerTokens')

    client = discord.Client()
    mode = input("""   What mode would you like to monitor with?
    
        By Server [1]  
    
        By channel [2]
        
        enter your choice """)

    if mode == '1':
        MonitoredIDs = list(map(int, input('Enter Server IDs (1234, 1234): ').split(', ')))
        clear()
        kws = list(map(str, input('Enter Keywords (bot, aio): ').split(', ')))
        clear()
        print(f'    Monitoring Servers {MonitoredIDs}\n')
        print(f'    With The Keywords {kws}\n')
    elif mode == '2':
        MonitoredIDs = list(map(int, input('Enter Channels IDs (1234, 1234): ').split(', ')))
        clear()
        kws = list(map(str, input('Enter Keywords (bot, aio): ').split(', ')))
        clear()
        print(f'    Monitoring Servers {MonitoredIDs}\n')
        print(f'    With The Keywords {kws}\n')
    else:
        print("thats not a valid option bro")
        BASICS()
    print(f"Claiming Invites on the accounts: ", end='')
    for x in claimertokens:
        claimtoken = x.replace(' ', '')
        req = requests.get("https://canary.discordapp.com/api/v6/users/@me", headers={'authorization': claimtoken})
        if req.status_code == 401:
            print("one of your tokens is invalid... that's kinda a you problem but idk")
        elif req.status_code == 200:
            req_json = req.json()
            user_name = f'{req_json["username"]}#{req_json["discriminator"]}'
            print(f"{user_name} ", end='')

    async def inviteclaim(invite):
        print(f"Found Invite: {invite}")
        code = invite.replace('https://discord.com/invite/', '').replace('@here', '').replace('restock', '').replace(
            '@everyone', '').replace('discord.gg/', '').replace('discordapp.com', '').replace(' ', '')
        print(f"Found Invite Code: {code}")
        for x in claimertokens:
            claimertoken = x.replace(' ', '')
            start = datetime.now()
            dhttp = http.client.HTTPSConnection('discord.com')
            headers = {
                'authority': 'discord.com',
                'accept-language': 'en-US',
                'path': f'/api/v8/invites/{code}',
                'method': 'POST',
                'authorization': claimertoken,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://discord.com/channels/@me',
            }
            dhttp.request('POST', f'/api/v8/invites/{code}', headers=headers)
            stop = datetime.now()
            res = dhttp.getresponse()
            status = res.status
            time = stop - start
            totaltime = int(time.total_seconds() * 1000)
            if status == 200:
                req = requests.get("https://canary.discordapp.com/api/v6/users/@me",
                                   headers={'authorization': claimertoken})
                if req.status_code == 200:
                    req_json = req.json()
                    user_name = f'{req_json["username"]}#{req_json["discriminator"]}'
                    print(
                        f'{Fore.GREEN}We copped the discord invite in {totaltime} ms on {user_name} ms under the monitoring account {client.user.name}#{client.user.discriminator}')
            else:
                print(f'{Fore.RED}We failed in {totaltime} ms')
            print(f'\n\n\n{Fore.RESET}')

    @client.event
    async def on_message(message):
        if mode == '1':
            if message.guild == None:
                pass
            elif message.guild.id in MonitoredIDs:
                urls = re.findall("""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+""",
                                  message.content)
                invites = re.findall("""discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})""",
                                     message.content)

                if invites:
                    print("we found a discord invite")
                    for x in range(len(invites)):
                        await inviteclaim(invites[x])

                for keyword in kws:
                    if keyword in message.content:
                        if urls:
                            print('we found  a URL with your keywords')
                            for x in range(len(urls)):
                                webbrowser.open(urls[x])
        elif mode == '2' and message.channel.id in MonitoredIDs:
            urls = re.findall("""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+""",
                              message.content)
            invites = re.findall("^(https)://(([a-zA-Z0-9\-]{2,52}))(\.metalabs\.)(group|gg|xyz|wtf|dashboard|sucks|dash)/([a-zA-Z0-9\-]{2,90})", message.content)
            if invites:
                print("we found a discord invite")
                for x in range(len(invites)):
                    await inviteclaim(invites[x])
            for keyword in kws:
                if keyword in message.content:
                    if urls:
                        print('we found a URL with your keywords')
                        for x in range(len(urls)):
                            webbrowser.open(urls[x])
        if "discord.gift/" in message.content:
            headers = {"authorization": token, "content-type": "application/json"}
            code = message.content.split('discord.gift/')[1].split(' ')[0]
            if len(code) < 16:
                print(f"{Fore.RED}{code} IS A FAKE CODE{Fore.RESET}")
            else:
                start = datetime.now()
                r = requests.post(f"https://discord.com/api/v8/entitlements/gift-codes/{code}/redeem", headers=headers)
                end = datetime.now()
                time1 = end - start
                time = int(time1.total_seconds() * 1000)
                if r.status_code == 200:
                    print(f"We claimed DA Nitro in {time} ms !, {code}")
                elif r.status_code == 400:
                    print(f"We failed in {time} ms OOPS, sadge {code}")
                else:
                    print(f"we failed in {time} ms, oops, sadge {code}")

    @client.event
    async def on_ready():
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Welcome to TorchScripts 0.0.1 {client.user.name}#{client.user.discriminator}.')
        print(f"\n\nMonitoring On the account: {client.user.name}#{client.user.discriminator}")
        print('\n\n\nBot Successfully Started')

    client.run(token, bot=False)
def credits():
    print(f"{Fore.RED}SeedOfArson       -------          owner, coded a majority of the toolbox :)\n\n")
    print(f"{Fore.RED}Paper Mario       ------- co-owner, helped with organization and fixing up the code\n\n")
    print(f"{Fore.RED}https://github.com/LytixDev/pygame_fireworks/blob/master/fireworks.py  -------  Fireworks\n\n")
    print(f"{Fore.RED}Saa from Nemesis  -------  Helped with Torch Scripts and all around nice guy\n\n")
    OPT33 = input("Press 1 to go back to main menu and 2 to go to fireworks: ")
    if OPT33 == "1":
        mainMenu()
    else:
        fireworks()
        mainMenu()
def mainMenu():
    clear()
    initialSetup()
    sprint(f'''{Fore.RED}
                               (       )   
  *   )              )   (     )\ ) ( /(   
` )  /(   (       ( /(   )\   (()/( )\())  
 ( )(_)|  )(   (  )\()|(((_)(  /(_)|(_)\   
(_(_()))\(()\  )\((_)\ )\ _ )\(_))   ((_)  
|_   _((_)((_)((_) |(_)(_)_\(_)_ _| / _ \  
  | |/ _ \ '_/ _|| ' \  / _ \  | | | (_) | 
  |_|\___/_| \__||_||_|/_/ \_\|___| \___/  
                                           


          ''' + Fore.RESET)
    print(f"""
\033[1;31m---------\033[1;m Main Menu\033[1;31m---------
\033[1;33m    	1.\033[1;m TorchScripts
\033[1;33m    	2.\033[1;m Torch Profile Converter(*NOT ACTUALLY REAL)
\033[1;33m    	3.\033[1;m TorchPorch(place holder)
\033[1;33m    	4.\033[1;m Torch Oneclick Generator(*NOT ACTUALLY REAL)
\033[1;33m    	5.\033[1;m Secondary Modules
\033[1;33m    	6.\033[1;m {colorama.Fore.LIGHTYELLOW_EX}Configuration Editor{colorama.Fore.RESET}
\033[1;33m    	7.\033[1;m CREDITS
            """)

    OPT = input("\033[1;35m  Select:\033[1;m ")
    if OPT == "1":
        clear()
        print(f"{colorama.Fore.LIGHTCYAN_EX}Scripts, Choosen{colorama.Fore.RESET}")
        sleep(2)
        BASICS()
    elif OPT == "2":
        clear()
        print("NOT ACTUALLY REAL")
        sleep(5)
        mainMenu()
    elif OPT == "3":
        clear()
        print("NOT ACTUALLY REAL")
        sleep(5)
        mainMenu()
    elif OPT == "4":
        clear()
        print("NOT  REAL")
        sleep(5)
        mainMenu()
    elif OPT == "5":
        clear()
        print(f"{colorama.Fore.LIGHTCYAN_EX}Secondary Menu, Choosen")
        sleep(5)
        SecondMenu()
    elif OPT == "6":
        clear()
        confedit()
        mainMenu()
    elif OPT == "7":
        clear()
        credits()
        mainMenu()
    else:
        clear()
        print(f"{colorama.Fore.RED}Invalid Option, Sending you back to the menu.{colorama.Fore.RESET}")
        sleep(1)
        mainMenu()
def SecondMenu():
    clear()
    initialSetup()
    sprint(f'''{Fore.RED}
                                         (        )   
      *   )                  )    (      )\ )  ( /(   
    ` )  /(     (         ( /(    )\    (()/(  )\())  
     ( )(_))(   )(    (   )\())((((_)(   /(_))((_)\   
    (_(_()) )\ (()\   )\ ((_)\  )\ _ )\ (_))    ((_)  
    |_   _|((_) ((_) ((_)| |(_) (_)_\(_)| |    / _ \  
      | | / _ \| '_|/ _| | ' \   / _ \  | |__ | (_) | 
      |_| \___/|_|  \__| |_||_| /_/ \_\ |____| \___/ 

              ''' + Fore.RESET)
    print("""
    \033[1;31m---------\033[1;m Main Menu\033[1;31m---------
    \033[1;33m    	1.\033[1;m Spycord / Forwarder(Forwards from channels of your choice to webhook of your choice) 
    \033[1;33m    	2.\033[1;m webhooker(shitty UI, mass webhook sender)
    \033[1;33m    	3.\033[1;m FAST Nitro Sniper(But only the nitro sniper)
    \033[1;33m    	4.\033[1;m TorchSelfbot
    \033[1;33m    	5.\033[1;m NOTHING
    \033[1;33m    	6.\033[1;m Back To Main Menu
                """)
    OPT2 = input("\033[1;35m  Select:\033[1;m ")
    if OPT2 == "1":
        clear()
        print(f"{colorama.Fore.LIGHTCYAN_EX}Spycord, Choosen{colorama.Fore.RESET}")
        sleep(2)
        spy()
    elif OPT2 == "2":
        clear()
        print(f"{colorama.Fore.LIGHTCYAN_EX}Mass Webhook Sender, Choosen{colorama.Fore.RESET}")
        sleep(2)
        webhooker()
    elif OPT2 == "3":
        clear()
        print(f"{colorama.Fore.LIGHTCYAN_EX}Nitro Sniper, Choosen{colorama.Fore.RESET}")
        sleep(2)
        nitrosniper()
    elif OPT2 == "4":
        clear()
        print("Torch Selfbot")
        sleep(2)
        selfbot()
    elif OPT2 == "6":
        clear()
        print("back to main menu")
        sleep(2)
        mainMenu()
    else:
        clear()
        print(f"{colorama.Fore.RED}Invalid Option, Sending you back to the menu.{colorama.Fore.RESET}")
        sleep(3)
        SecondMenu()
mainMenu()
