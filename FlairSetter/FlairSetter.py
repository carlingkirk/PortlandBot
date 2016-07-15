import praw
import time
import datetime
import sqlite3
from datetime import datetime, timedelta

USERNAME = ""
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD = ""
#This is the bot's Password. 
USERAGENT = "/r/Portland menu updater"
#This is a short description of what the bot does. For example "/r/pkmntcgtrades post limit bot"
SUBREDDIT = "Portland"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 15
#This is how many posts you want to retreieve all at once. Max 100, but you won't need that many.
WAIT = 300
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
WAITS = str(WAIT)
# Which post should the test comments go to
MSGPOSTID = "4dhpyb"

sql = sqlite3.connect('sql.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
print('Loaded SQL Database')
cur = sql.cursor()

#cur.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, lastpost TEXT)')
#print('Loaded Users')
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(stamp TEXT, id TEXT)')
print('Loaded Oldposts')
#cur.execute('CREATE TABLE IF NOT EXISTS links(title TEXT, url TEXT)')
#print('Loaded Links')
sql.commit()

# clean oldposts
now = datetime.now()
today = now.strftime("%Y-%m-%d")
clean = datetime.now() - timedelta(days=32)
too_old = clean.strftime("%Y-%m-%d")
print('Removed post IDs from before %s' % too_old)
cur.execute('DELETE FROM oldposts WHERE stamp < "%s"' % too_old)
sql.commit()

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
		time.sleep(5)
		
def scan():
	newflairtext = 'No Matches'
	newflaircss = 'no matches'
	print('Scanning /r/' + SUBREDDIT + '')
	subreddit = r.get_subreddit(SUBREDDIT)
	posts = subreddit.get_new(limit=MAXPOSTS)
	for post in posts:
		pauthor = post.author.name
		pid = post.id
		plink = post.short_link
		ptime = post.created_utc
		ptitle = post.title
		pbody = post.selftext
		pflair = post.link_flair_css_class
		print( '\nFound ' + plink )
		# does it have flair?
		flair = str(pflair)
		if flair != "None":
			print( 'Already has ' + flair + ' flair' )
		else: 
			cur.execute('SELECT * FROM oldposts WHERE id="%s"' % pid)
			if not cur.fetchone():
				# make strings
				stitle = str(ptitle)
				sbody = str(pbody)
				title = stitle.lower()
				body = sbody.lower()
				# figure out what flair to use
				print('No flair. Running title and body through phrase-matcher.')
				msg = '%s\n\n%s\n\n%s' % ( plink, title, newflairtext )
				
				# PASTE TITLE FLAIR PHRASE OUTPUT BELOW ######################################################################################################
				
				phrases = None
				helpmePhrases = ('anybody', 'anyone know', 'anyone tried ', 'are there', 'best sushi', 'does anyone', 'has anyone', 'help me', 'how safe', 'how should', 'how to', 'how was', 'need idea', 'question', 'question', 'recommendation', 'request', 'what are', 'what are your', 'what is', 'what\'s your', 'where can', 'where is the', 'where is the', 'who to', 'who\'s your', 'why does')
				for phrases in helpmePhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Help Me'
						newflaircss = 'help-me'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				classifiedsPhrases = ('anyone want to', 'bike stolen', 'bike was stolen', 'car stolen', 'car was stolen', 'found a bike', 'found a cat', 'found a dog', 'found a purse', 'found a wallet', 'found bike', 'found cat', 'found dog', 'found id', 'found purse', 'found wallet', 'found your bike', 'found your cat', 'found your dog', 'found your id', 'found your purse', 'found your wallet', 'free box', 'free clothes', 'free for', 'free pass', 'free ticket', 'interested in', 'looking for a', 'lost bike', 'lost cat', 'lost dog', 'lost id', 'lost my bike', 'lost my cat', 'lost my dog', 'lost my id', 'lost my purse', 'lost my wallet', 'lost purse', 'lost wallet', 'stolen bike', 'stolen car', 'to donate', 'wanted')
				for phrases in classifiedsPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Classifieds'
						newflaircss = 'classifieds'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				eventPhrases = ('being held at', 'come support', 'fair is coming', 'mfnw', 'monthly', 'proceeds benefit', 'rose festival', 'tour adds dates', 'trivia')
				for phrases in eventPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Events'
						newflaircss = 'event'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				housingPhrases = ('00 per month', 'apartment', 'condo', 'home prices', 'house hunting', 'house share', 'housing', 'price increase', 'rent', 'roommate')
				for phrases in housingPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Housing'
						newflaircss = 'housing'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				homelessPhrases = ('camper', 'halesville', 'homeless', 'springwater', 'tent city', 'panhandl')
				for phrases in homelessPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Homeless'
						newflaircss = 'homeless'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				meetupPhrases = ('banana', 'board games', 'fantasy book club', 'meetup', 'mfp', 'official party')
				for phrases in meetupPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Meetups'
						newflaircss = 'meetup'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				breakingPhrases = ('accident at', 'mass shooting', 'traffic alert')
				for phrases in breakingPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Breaking'
						newflaircss = 'breaking'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				localnewsPhrases = ('')
				for phrases in localnewsPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Local News'
						newflaircss = 'local-news'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				nonlocalnewsPhrases = ('')
				for phrases in nonlocalnewsPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Outside News'
						newflaircss = 'non-local-news'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				photoPhrases = ('')
				for phrases in photoPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Photos'
						newflaircss = 'photo'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				phrases = None
				offtopicPhrases = ('')
				for phrases in offtopicPhrases:
					if title.find(phrases) != -1:
						newflairtext = 'Other'
						newflaircss = 'off-topic'
						msg = '%s\n\n%s\n\n%s\n\n%s' % ( plink, title, newflairtext, phrases )

				# PASTE TITLE FLAIR PHRASE OUTPUT ABOVE ######################################################################################################
				
				print( 'Triggered ' + newflairtext )				
				# flair chosen, set it and record id in oldposts
				#set_flair(SUBREDDIT, post, newflairtext, newflaircss)
				time.sleep(3)
				cur.execute('INSERT INTO oldposts VALUES("%s", "%s")' % (today, pid))
				print( 'Adding "%s" to database (%s)' % ( pid, today ) )
				# notify			
				msgpost = r.get_submission(submission_id=MSGPOSTID)			
				msgpost.add_comment(msg)
				
			else:
				print('Already knew about %s' % ( plink ))
			sql.commit()

while True:
	try:
		scan()
	except Exception as e:
		print('An error has occured:', e)
	#cur.execute("SELECT * FROM oldposts;")
	#print('\nOLDPOSTS:')
	#print(cur.fetchall())
	print('\nRunning again in ' + WAITS + ' seconds.\n')
	time.sleep(WAIT)