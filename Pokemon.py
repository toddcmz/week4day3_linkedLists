import requests
from Node import Node
from LinkedList import LinkedList
#from IPython.display import Image

# this is a copy paste of my final code in the original poke api hw,
# leaving my original evolution implementation alone, which allows for
# level-by-level evolution. I'll write a separate method for getting the
# complete evolution chain. 

# week 4 hw starts around line 140 

class Move_Tutor:
    
    def __init__(self, move_list = []):
        self.move_list = move_list
        
    def learn_new_move(self):
        print(f'Moves that {self.name} knows:')
        print(self.move_list)
        new_move = input("Enter a move to learn: ")
        if new_move in self.move_list:
            self.already_knows_move(new_move)
        elif len(self.move_list) == 4:
            self.make_room_move(new_move)
        else:
            self.move_list.append(new_move)
    
    def already_knows_move(self, new_move):
        print(f'The move {new_move} is already known.')
        user_choice = input("Would you like to try to learn a different move? y/n: ").lower()
        if user_choice == "y":
            self.learn_new_move()
        else:
            print("Done learning moves.")
    
    def make_room_move(self, new_move):
        print(f"There are already 4 moves in {self.name}'s move list:'")
        print(self.move_list)
        user_choice = input(f"Would you like to forget a move to learn {new_move}? y/n").lower()
        if user_choice == "n":
            print("Done learning moves")
        else:
            user_choice = input(f"Which move would you like to forget?")
            if user_choice in self.move_list:
                self.move_list.remove(user_choice)
                self.move_list.append(new_move)
                print(f"Your pokemon {self.name} forgot {user_choice} and learned {new_move}!")
            else:
                print("That move isn't in the known list, did you type it correctly?")
                self.make_room_move(new_move)
        
# recreate your pokemon class here
class Encounter_Pokemon(Move_Tutor):

    def __init__(self, name, move_list):
        super().__init__(move_list)
        self.name = name
        self.abilities = []
        self.types = []
        self.weight = None
        self.image = None
        self.pokenum = None

    def throw_pokeball(self):
        catch_attempt = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}')
        if catch_attempt.status_code == 200:
            print(f'You successfully caught {self.name}')
            data = catch_attempt.json()
            self.name = data["name"] # this will allow for passing in either a full name or an integer index during the prior API call
            self.weight = data["weight"]
            self.abilities = [this_ability["ability"]["name"] for this_ability in data["abilities"]]
            self.types = [this_type["type"]["name"] for this_type in data["types"]]
            self.image = data["sprites"]['front_default']
            self.pokenum = data["id"]
        else:
            print(f'Error, status code {catch_attempt.status_code}')
        
    def successful_evolution(self):
        evo_attempt = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}')
        if evo_attempt.status_code == 200:
            print('Bum dum bum dum bum dum baaaa')
            data = evo_attempt.json()
            self.name = data["name"] # this will allow for passing in either a full name or an integer index during the prior API call
            self.weight = data["weight"]
            self.abilities = [this_ability["ability"]["name"] for this_ability in data["abilities"]]
            self.types = [this_type["type"]["name"] for this_type in data["types"]]
            self.image = data["sprites"]['front_default']
            self.pokenum = data["id"]
        else:
            print(f'Error on retrieving evolution info, status code {evo_attempt.status_code}')
            
    # def i_choose_you(self):
    #     display(Image(self.image, width = 100))
        
    def wants_to_evolve(self):
        get_evo_data = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{self.pokenum}/')
        if get_evo_data.status_code == 200:
            print(f'{self.name} wants ...')
            tempData = get_evo_data.json()
            self.find_evo_data(tempData["evolution_chain"]["url"])
        else:
            print(f'Error on species page retrieval, status code {get_evo_data.status_code}')

    def find_evo_data(self, found_url):
        get_evo_data = requests.get(found_url)
        if get_evo_data.status_code == 200:
            print("...to evolve!")
            self.try_to_evolve(get_evo_data.json())
        else:
            print(f'Error on evo chain retrieval, status code {get_evo_data.status_code}')

    # This is my old try to evolve method from the original hw which works on a single pokemon,
    # does one evolution at a time if asked, and only goes through two evos at most. See next
    # method for week 4 hw.
    def try_to_evolve(self, evo_data):
        # pokemon is bottom level, goes to next level if next level exists
        if self.name == evo_data["chain"]["species"]["name"]:
            # if next level exists:
            if evo_data["chain"]["evolves_to"]:
                self.oldName = self.name
                self.name = evo_data["chain"]["evolves_to"][0]["species"]["name"]
                self.successful_evolution()
                print(f'Congratulations, your {self.oldName} evolved into {self.name}')
            else:
                print(f"Sorry, your {self.name} can't evolve any further.")
        # pokemon is middle level, goes to next level if next level exists
        elif self.name == evo_data["chain"]["evolves_to"][0]["species"]["name"]:
            # if next level exists:
            if evo_data["chain"]["evolves_to"][0]["evolves_to"]:
                self.oldName = self.name
                self.name = evo_data["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                self.successful_evolution()
                print(f'Congratulations, your {self.oldName} evolved into {self.name}')
            else:
                print(f"Sorry, your {self.name} can't evolve any further.")
        # we'll assume there are at most three evolutions for now, I see we could go deeper, I'm
        # sure there's way more efficient code out there for doing all this
        else:
            print(f"Sorry, your {self.name} can't evolve any further.")

    # This is the new code for the homework asking to spit out the entire evo chain as a linked list.
    def get_entire_evo_chain(self):
        # this is all just grabbing the evo chain info page
        get_evo_data = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{self.pokenum}/')
        if get_evo_data.status_code == 200:
            tempData = get_evo_data.json()
            get_evo_data = requests.get(tempData["evolution_chain"]["url"])
            if get_evo_data.status_code == 200:
                print("Found evo chain")
                evo_data = get_evo_data.json()['chain']
            else:
                print(f'Error on evo chain retrieval, status code {get_evo_data.status_code}')
        else:
            print(f'Error on species page retrieval, status code {get_evo_data.status_code}')

        # initialize blank list to hold all evolutions
        full_chain = []
        # my approach starts at the base level and appends it, then gets into
        # the evolves_to list - this method lets me handle pokemon with multiple
        # options at the same evolution stage, like eevee or ralts -> kirlia -> gardevoir or gallande (sp?)
        full_chain.append(evo_data['species']['name'])
        evo_data = evo_data['evolves_to'] 
        # now get all the stages above the base level
        while evo_data:
            # if there are multiple options, get all of them and append as a string so that the __repr__ Dylan wrote
            # still works (originally I appended as a list within a list)
            if len(evo_data) != 1:
                temp_forms = []
                for ele in evo_data:
                    temp_forms.append(ele['species']['name'])
                    string_forms = "-OR-".join(temp_forms)
                full_chain.append(string_forms)
            else:
                # otherwise we just add this one and move on
                full_chain.append(evo_data[0]['species']['name'])
            # next level of while loop gets into the first item's "evolves to". I don't
            # know if any pokemon have multiple options for a middle stage; if they do this won't grab them.
            evo_data = evo_data[0]['evolves_to']
        return(full_chain)

    # and make this a linked list:
    def evo_chain_linked_list(self):
        print("Working on the linked list:")
        evo_list = self.get_entire_evo_chain()
        self.linked_list = LinkedList()
        self.linked_list.add_list(evo_list)

# todd's test cases

my_pokemon = Encounter_Pokemon("moltres", ["lick"])
my_pokemon.throw_pokeball()
print(my_pokemon.get_entire_evo_chain())

my_pokemon.evo_chain_linked_list()
print(my_pokemon.linked_list)

my_pokemon = Encounter_Pokemon("gengar", ["lick"])
my_pokemon.throw_pokeball()
print(my_pokemon.get_entire_evo_chain())

my_pokemon.evo_chain_linked_list()
print(my_pokemon.linked_list)

my_pokemon = Encounter_Pokemon("eevee", ["lick"])
my_pokemon.throw_pokeball()
print(my_pokemon.get_entire_evo_chain())

my_pokemon.evo_chain_linked_list()
print(my_pokemon.linked_list)

my_pokemon = Encounter_Pokemon("kirlia", ["lick"])
my_pokemon.throw_pokeball()
print(my_pokemon.get_entire_evo_chain())

my_pokemon.evo_chain_linked_list()
print(my_pokemon.linked_list)