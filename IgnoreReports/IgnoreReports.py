import praw
import time
import datetime
from datetime import datetime, timedelta

USERNAME = ""
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD = ""
#This is the bot's Password. 
USERAGENT = "/r/Portland report monitor"
#This is a short description of what the bot does. For example "/r/pkmntcgtrades post limit bot"
SUBREDDIT = ""
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 15
#This is how many posts you want to retreieve all at once. Max 100, but you won't need that many.
WAIT = 60
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
WAITS = str(WAIT)

r = praw.Reddit(USERAGENT)
r.config.decode_html_entities = True

Trying = True
while Trying:
	try:
		r.login(USERNAME, PASSWORD,disable_warning=True)
		print('Successfully logged in')
		Trying = False
	except praw.errors.InvalidUserPass:
		print('Wrong Username or Password')
		quit()
	except Exception as e:
		print("%s" % e)
		time.sleep(2)
		
def scan():
	print('Scanning /r/' + SUBREDDIT)
	subreddit = r.get_subreddit(SUBREDDIT)
	reported = subreddit.get_reports(limit=MAXPOSTS)
	for item in reported:
		pid = item.id
		print( 'Ignored ' + pid )
		item.ignore_reports()
		time.sleep(2)
		item.approve()

while True:
	try:
		scan()
	except Exception as e:
		print('An error has occured:', e)
	print('Running again in ' + WAITS + ' seconds.\n')
	time.sleep(WAIT)