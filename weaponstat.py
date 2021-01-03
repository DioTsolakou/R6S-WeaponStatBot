#import discord
import csv

#client = discord.Client()
weapon_data = csv.reader(open("R6S Weapon Stats.csv", "r"), delimiter=',')


def main():
    found = False
    weapon_to_find = "SMG11"
    weapon_to_find = weapon_to_find.upper()

    for row in weapon_data:
        if weapon_to_find == row[0]:
            print(row)
            found = True
    if not found:
        print("Please provide proper weapon name. Including hyphens")


if __name__ == "__main__":
    main()


#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

#    if message.content.startsWith('!weaponstat'):
#        string_array = message.split()
#        weapon_name = string_array[1]
#        weapon_name.lower()


#client.run('Nzk1MzA3NTM2OTk0NjY0NTI4.X_Hd3A.oxNy37f0tVuOZpLxV1WD6nhefDM')