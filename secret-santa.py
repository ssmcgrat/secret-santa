import getopt
import os
import yaml
import sys
import random
import smtplib
from os.path import basename
import email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

class Person:
	def __init__(self, name, email, invalid_matches):
		self.name = name
		self.email = email
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

	
def send_emails_old(pairs):
	config = parse_yaml()
	
	server.starttls()
	server.login(config['USERNAME'], config['PASSWORD'])
	frm = config["FROM"]
	for pair in pairs:
		to = pair.giver.email
		body = config['BODY']
		body = body.replace("{santa}", pair.giver.name)
		body = body.replace("{santee}", pair.reciever.name)
		subject=config["SUBJECT"]
		message = 'Subject: {}\n\n{}'.format(subject, body)
		server.sendmail(frm, [to], message)
	server.quit()
	
def send_emails(pairs):
	config = parse_yaml()
	server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
	server.starttls()
	server.login(config['USERNAME'], config['PASSWORD'])
	f = r"C:\Users\Sean\Documents\python\secret-santa\secretsanta.ics"
	#server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
	for pair in pairs:
		msg = MIMEMultipart()
		msg['From'] = config["FROM"]
		msg['To'] = pair.giver.email
		msg['Subject'] = config["SUBJECT"]
		body = config['BODY']
		body = body.replace("{santa}", pair.giver.name)
		body = body.replace("{santee}", pair.reciever.name)
		msg.attach(MIMEText(body))
		with open(f, "rb") as fil:
			part = MIMEApplication(
			fil.read(),
			Name=basename(f)
		)
		# After the file is closed
		part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
		msg.attach(part)
		server.sendmail(config["FROM"], pair.giver.email, msg.as_string())
	server.close()
		
	
def main():
	opts, args = getopt.getopt(sys.argv[1:], "shc", ["send", "help"])
	send = False
	for option, value in opts:
		print(option)
		if option in ("-s", "--send"):
			send = True
	
	config = parse_yaml()
	
	participants = config["PARTICIPANTS"]
	dont_pair = config["DO-NOT-MATCH"]
	
	#print("Finding secret santa pairings for the following people:")
	#for p in participants:
	#	print(p)
		
	givers = [] # list of Person objects, each Person will be giving a gift
	for participant in participants:
		name = participant.split(",")[0] # will later parse name out from email
		name = name.strip()
		email = participant.split(",")[1].strip()
		invalid_matches = []
		for pair in dont_pair:
			names = [n.strip() for n in pair.split(",")]
			if name in names:
				for n in names:
					if name != n:
						invalid_matches.append(n)
		person = Person(name, email, invalid_matches)
		givers.append(person)
	
	recievers = givers[:]	
	pairs = create_pairs(givers, recievers)
	
	for pair in pairs:
		print(pair)
	
	if send:
		send_emails(pairs)
	
	print("\n\ncomplete")
	
	
if __name__ == "__main__":
	sys.exit(main())