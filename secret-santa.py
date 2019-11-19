import os
import yaml
import sys
import random

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

class Person:
	def __init__(self, name, invalid_matches):
		self.name = name
		#self.email = email
		self.invalid_matches = invalid_matches
		
	def __str__(self):
		return "{}, {}".format(self.name, self.invalid_matches)

class Pair:
	def __init__(self, giver, reciever):
		self.giver = giver
		self.reciever = reciever
		
	def __str__(self):
		return "{} ----> {}".format(self.giver.name, self.reciever.name)
		
def parse_yaml(yaml_path=CONFIG_PATH):
    return yaml.load(open(yaml_path))

def choose_reciever(giver, recievers):
	choice = random.choice(recievers)
	if choice.name in giver.invalid_matches or giver.name == choice.name:
		if len(recievers) is 1:
			raise Exception("Only one reciever left, try again")
		return choose_reciever(giver, recievers)
	else:
		return choice

def create_pairs(g, r):
	givers = g[:]
	recievers = r[:]
	pairs = []
	for giver in givers:
		try:
			reciever = choose_reciever(giver, recievers)
			recievers.remove(reciever)
			pairs.append(Pair(giver, reciever))
		except:
			return create_pairs(g, r)
	return pairs

	
def main():
	config = parse_yaml()
	
	participants = config["PARTICIPANTS"]
	dont_pair = config["DO-NOT-MATCH"]
	
	#print("Finding secret santa pairings for the following people:")
	#for p in participants:
	#	print(p)
		
	givers = [] # list of Person objects, each Person will be giving a gift
	for participant in participants:
		name = participant # will later parse name out from email
		name = name.strip()
		invalid_matches = []
		for pair in dont_pair:
			names = [n.strip() for n in pair.split(",")]
			if name in names:
				for n in names:
					if name != n:
						invalid_matches.append(n)
		person = Person(name, invalid_matches)
		givers.append(person)
	
	recievers = givers[:]	
	pairs = create_pairs(givers, recievers)
	
	for pair in pairs:
		print(pair)
	
	
	print("\n\ncomplete")
	
	
if __name__ == "__main__":
	sys.exit(main())