import discord
import csv

token = open('token.txt', 'r').read()
client = discord.Client()
weapon_list = []


class Weapon:
    def __init__(self, name, stat, full_reload, tact_reload, rof, ads):
        self.name = name
        self.stat = stat
        self.full_reload = full_reload
        self.tact_reload = tact_reload
        self.rof = rof
        self.ads = ads

    def get_name(self):
        return self.name

    def get_stat(self):
        return self.stat

    def get_full_reload(self):
        return self.full_reload

    def get_tact_reload(self):
        return self.tact_reload

    def get_rof(self):
        return self.rof

    def get_ads(self):
        return self.ads


def binary_search(low, high, value):
    file = open('weapon_aliases.csv')
    proper_name_csv = csv.reader(file, delimiter=',')
    proper_name_list = list(proper_name_csv)
    proper_name = [[element.upper() for element in sublist] for sublist in proper_name_list]

    if high >= low:
        mid = (high + low)//2

        if proper_name[mid][0] == value.upper():
            return mid

        elif proper_name[mid][0] > value.upper():
            return binary_search(low, mid - 1, value)

        else:
            return binary_search(mid + 1, high, value)

    else:
        return -1


def linear_search(alias, mode):
    file = open('weapon_aliases.csv')
    aliases_csv = csv.reader(file, delimiter=',')
    aliases_list = list(aliases_csv)
    aliases = [[element.upper() for element in sublist] for sublist in aliases_list]

    # for row in aliases:
    #    for column in row:
    #        if aliases[row][column] == alias.upper():
    #            return 0

    if mode == 'search':
        if any(alias.upper() in rows for rows in aliases):
            return 0

    if mode == 'check':
        row_lst = [[i for i, lst in enumerate(aliases) if alias.upper() in lst][0]]
        row = row_lst.__getitem__(0)
        return aliases[row][0]

    return -1


def add_alias(name, alias):
    file = open('weapon_aliases.csv')
    weapon_aliases = csv.reader(file, delimiter=',')
    weapon_aliases = list(weapon_aliases)
    added = False

    # do stuff
    search_result = binary_search(0, 86, name)

    if search_result == -1:
        return -1  # name was not found

    alias_search = linear_search(alias, 'search')

    if alias_search == 0:
        return 0  # name was found but alias already exists

    for i in range(len(weapon_aliases[search_result])):
        if weapon_aliases[search_result][i] == '':
            weapon_aliases[search_result][i] = alias
            added = True
            break

    if not added:
        weapon_aliases[search_result].append(alias)
        added = True

    write_to_file = open('weapon_aliases.csv', 'w+', newline='')
    with write_to_file:
        write = csv.writer(write_to_file)
        write.writerows(weapon_aliases)

    if added:
        return 1  # alias was added
    else:
        return -2


def read_file(weapon_name):
    file = open('R6S Weapon Stats.csv')
    weapon_data = csv.reader(file, delimiter=',')
    weapon_to_find = weapon_name
    weapon_to_find = weapon_to_find.upper()
    found = False
    found_by_alias = False

    for row in weapon_data:
        if weapon_to_find == row[0].upper():
            weapon_list.append(Weapon(row[0], row[1], row[44], row[45], row[47], row[49]))
            found = True

    file.seek(0)

    if not found:
        weapon_to_find = linear_search(weapon_name, 'check')
        for row in weapon_data:
            if weapon_to_find.upper() == row[0].upper():
                weapon_list.append(Weapon(row[0], row[1], row[44], row[45], row[47], row[49]))
                found = True

    file.seek(0)

    pulled_weapon_name = weapon_list[0].get_name()
    weapon_dmg = weapon_list[0].get_stat()
    weapon_rof = weapon_list[0].get_rof()
    weapon_dps = weapon_list[1].get_stat()
    stk1arm = weapon_list[2].get_stat()
    ttk1arm = weapon_list[3].get_stat()
    stk2arm = weapon_list[4].get_stat()
    ttk2arm = weapon_list[5].get_stat()
    stk3arm_1r = weapon_list[6].get_stat()
    ttk3arm_1r = weapon_list[7].get_stat()

    weapon_list.clear()
    found = False
    embed = discord.Embed(title="Weapon", description=pulled_weapon_name)
    embed.add_field(name="Damage", value=weapon_dmg, inline=True)
    embed.add_field(name="DPS", value=weapon_dps, inline=True)
    embed.add_field(name="Rate Of Fire", value=weapon_rof, inline=True)
    embed.add_field(name="STK vs 1 Armors", value=stk1arm, inline=False)
    embed.add_field(name="TTK vs 1 Armors", value=ttk1arm, inline=True)
    embed.add_field(name="STK vs 2 Armors", value=stk2arm, inline=True)
    embed.add_field(name="TTK vs 2 Armors", value=ttk2arm, inline=True)
    embed.add_field(name="STK vs 3 Armors/1 Armors + Rook", value=stk3arm_1r, inline=False)
    embed.add_field(name="TTK vs 3 Armors/1 Armors + Rook", value=ttk3arm_1r, inline=True)

    return embed


# For debugging
# def main():
#    read_file('CSRX 300')


# if __name__ == '__main__':
#    main()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!weaponstat'):
        string_array = message.content.split()
        if len(string_array) == 1:
            await message.channel.send('Please give a weapon name for the command to work!\n'
                                       'Type !help to see more.')
            return

        if len(string_array) == 3:
            string_array[1] = string_array[1] + ' ' + string_array[2]

        weapon_name = string_array[1]
        embed = read_file(weapon_name)
        await message.channel.send(embed=embed)
        return

    if message.content == '!help':
        await message.channel.send('To use this bot type "!weaponstat gun_name" without the " " (double quotes).\n '
                                   'E.g. !weaponstat F2 to get the stats for the F2.\n'
                                   'Don\'t forget to type the actual name of the gun, smg-11 and not smg11.\n \n'
                                   'Stats are taken from Rogue-9\'s spreadsheet. https://docs.google.com/spreadsheets/d/1QF72f4Bm7PfbWeSWbl8R8uL0mOzXpG_1vOjqEjXcFGk/edit')

    if message.content.startswith('!alias'):
        string_array = message.content.split()
        if len(string_array) < 3:
            await message.channel.send('Please provide the weapon\'s actual name first and its alias second.')

        if len(string_array) == 4:
            name = string_array[1] + ' ' + string_array[2]
            alias = string_array[3]
        else:
            name = string_array[1]
            alias = string_array[2]

        alias_no = add_alias(name, alias)

        if alias_no == -1:
            await message.channel.send('Weapon name was not found.\n'
                                       'Make sure you are writing the proper name first and correctly.')

        if alias_no == 0:
            await message.channel.send('Weapon alias already exists.')

        if alias_no == 1:
            await message.channel.send('Weapon alias has been added.\n'
                                       'Thank you for your contribution')


client.run(token)
