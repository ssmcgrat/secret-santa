# secret santa

This is a fun little program to help orchestrate secret santa.

This reads in a list of secret santa participants and randomly assigns each person someone to buy a gift for. In the `config.yml` file, you specify who should not be matched (e.g. spouses). It then sends each participant an email telling them who they matched with. The email body is configurable from `config.yml`. It also attaches an .ics calendar file to the email, specifying date time and location. This info is also configurable.

# running the code

Rename `config-sample.yml` to `config.yml` and update as appropriate. 

Execute `secret-santa.py` to test the program. Console output will show you the would-be assignments. This does not send an email.

Once tested, to send emails to your participants, run `secret-santa.py` from the command terminal using the the `-s` parameter

	python secret-santa.py -s

# acknowledgments 

I ripped off most of the code (yml reading, recursive randomization) from this lovely repo

	https://github.com/underbluewaters/secret-santa
	
Fun way for me to learn some more stuff in python. I added the ics file code.