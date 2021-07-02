import requests
import random
import smtplib

pokemon_id = random.randint(0, 800)

# ------------- USING POKEMON API -------------------

response = requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
response.raise_for_status()

pokemon_data = response.json()
pokemon_name = pokemon_data['name']

all_types = pokemon_data['types']
pokemon_types_list = [_type['type']['name'] for _type in all_types]

pokemon_types = ' '.join([str(elem) for elem in pokemon_types_list])

pokemon_height = pokemon_data['height']
pokemon_weight = pokemon_data['weight']
pokemon_sprite_front = pokemon_data['sprites']['front_default']
# pokemon_stats = pokemon_data['stats']

pokemon_moves_list = []
new_list = pokemon_data['moves']
all_moves = [move['move']['name'] for move in new_list]
if len(all_moves) == 4:
    pokemon_moves_list = all_moves
else:
    pokemon_moves_list = random.sample(all_moves, 4)

pokemon_moves = ' '.join([str(elem).capitalize() for elem in pokemon_moves_list])

# print(f"{pokemon_name}: {pokemon_weight}: {pokemon_height}\n"
#       f"{pokemon_sprite_front}: {pokemon_types}\n"
#       f"{pokemon_moves}")

# --------------------------EMAIL---------------------
# enter your own emails and password
my_email = ""
password = ""
current_recipient = ""

email_template = open("./email_template.txt").read()
current_template = email_template

email_template = current_template\
    .replace("[POKEMON_NAME]", pokemon_name.capitalize())\
    .replace("[POKEMON_SPRITE]", pokemon_sprite_front)\
    .replace("[POKEMON_TYPE]", pokemon_types.capitalize())\
    .replace("[POKEMON_HEIGHT]", str(pokemon_height))\
    .replace("[POKEMON_WEIGHT]", str(pokemon_weight))\
    .replace("[POKEMON_MOVES]",  pokemon_moves)

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(my_email, password)

    connection.sendmail(to_addrs=current_recipient,
                        from_addr=my_email,
                        msg=f"Subject:You encountered a new Pokemon!\n\n"
                            f"{email_template}")
