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


def tuple_to_string(tuple_to_change):
    string = ''.join(tuple_to_change)
    return string


def read_file(weapon_name):
    file = open('R6S Weapon Stats.csv')
    weapon_data = csv.reader(file, delimiter=',')
    weapon_to_find = weapon_name
    weapon_to_find = weapon_to_find.upper()
    found = False

    for row in weapon_data:
        if weapon_to_find == row[0]:
            weapon_list.append(Weapon(row[0], row[1], row[44], row[45], row[47], row[49]))
            found = True

    if not found:
        return 'Please provide proper weapon name. Including hyphens.'

    file.seek(0)

    #For debugging
#    print('Weapon\t Damage\t DPS\t STK vs 1 armor\t TTK vs 1 armor\t STK vs 2 armor\t TTK vs 2 armor\t '
#          'STK vs 3 armor/1+rook\t TTK vs 3 armor/1+rook\t Rate of Fire\n')
    #For debugging
#    print('{:>3}  {:>6}  {:>5} {:>12}  {:>14}  {:>14} {:>14}  {:>18}  {:>22} {:>20} '.format(
#        weapon_list[0].get_name(), weapon_list[0].get_stat(), weapon_list[1].get_stat(),
#        weapon_list[2].get_stat(), weapon_list[3].get_stat(), weapon_list[4].get_stat(),
#        weapon_list[5].get_stat(), weapon_list[6].get_stat(), weapon_list[7].get_stat(), weapon_list[0].get_rof()))


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

    #tuple view
    #message_tuple = ('Weapon\t', weapon_list[0].get_name(), '\t\t\tDamage\t',
    #                 weapon_list[0].get_stat(), '\t\tDPS\t', weapon_list[1].get_stat(),
    #                 '\t\tRate of Fire\t', weapon_list[0].get_rof(), '\n',
    #                 'STK vs 1 armor\t', weapon_list[2].get_stat(), '\t\tTTK vs 1 armor\t',
    #                 weapon_list[3].get_stat(), '\t\tSTK vs 2 armor\t', weapon_list[4].get_stat(), '\n',
    #                 'TTK vs 2 armor\t', weapon_list[5].get_stat(), '\tSTK vs 3 armor/1+rook\t',
    #                 weapon_list[6].get_stat(), '\tTTK vs 3 armor/1+rook\t', weapon_list[7].get_stat())

    #message = tuple_to_string(message_tuple)

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

#For debugging
#def main():
#    read_file('CSRX 300')


#if __name__ == '__main__':
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
              'Stats are taken from Rogue-9\'s spreadsheet.')


client.run(token)
