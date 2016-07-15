import traceback
import praw
import time
import sqlite3

'''USER CONFIGURATION'''

REPLY_SUBJECT = 'Couldn\'t add flair'
REPLY_MESSAGE = 'I see you tried to flair a post, but I didn\'t understand which flair you meant. Please choose from these (not case sensitive):\n\n* !FLAIR Local News\n\n* !FLAIR Breaking\n\n* !FLAIR Housing\n\n* !FLAIR Homeless\n\n* !FLAIR Photos\n\n* !FLAIR Meetups\n\n* !FLAIR Events\n\n* !FLAIR Classifieds\n\n* !FLAIR Non-local News\n\n* !FLAIR Off Topic\n\nYour comment was removed so users don\'t get the bright idea of trying it themselves, so please post a new one.'
USERNAME  = ""
PASSWORD  = ""
USERAGENT = "/r/Portland post flair helper"
SUBREDDIT = ""
MAXPOSTS = 20
WAIT = 30
# Time between cycles
CLEANCYCLES = 20
# After this many cycles, the bot will clean its database
# Keeping only the latest (2*MAXPOSTS) items
PRAW = praw.Reddit(USERAGENT)
'''All done!'''

NUMCYCLES = 1

def init(config, cur, sql):
	USERNAME = config['reddit_username']
	PASSWORD = config['reddit_password']

	cur.execute('CREATE TABLE IF NOT EXISTS oldposts(id TEXT)')

	sql.commit()

	print('Logging in...')
	
	PRAW.login(USERNAME, PASSWORD,disable_warning=True)

def flairbot(config, cur, sql, num_cycles):
	SUBREDDIT = config['subreddit']
	r = PRAW

	print('Cycle #%i' % num_cycles)
	print('Searching %s.' % SUBREDDIT)
	subreddit = r.get_subreddit(SUBREDDIT)
	posts = list(subreddit.get_comments(limit=MAXPOSTS))
	posts.reverse()
	for post in posts:
		pid = post.id

		if post.author is None:
			continue # Author is deleted    
		
		pauthor = post.author.name
		plink = post.permalink
		
		cur.execute('SELECT * FROM oldposts WHERE ID=?', [pid])
		if cur.fetchone():
			# Already in database
			continue

		cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
		sql.commit()
		pbody = post.body.lower()
		#print( pid )
		# check for trigger phrases
		beginning = pbody[:6]
		if beginning == '!flair': 
			# check that user is allowed
			# TODO - makes mods a config option
			if pauthor == 'Osiris32' or pauthor == 'elationisfacile' or pauthor == 'ReallyHender' or pauthor == 'remotectrl' or pauthor == 'sarafist' or pauthor == 'Automoderator' or pauthor == 'Peace_Love_Happiness':
				print('\n******* Triggered by /u/' + pauthor) 
				# set which flair to use
				FLAIRNAME = 'none'
				FLAIRCSS = 'none'
				if pbody.find("flair local news") > -1:
					FLAIRNAME = 'Local news'
					FLAIRCSS = 'local-news'
				if pbody.find("flair outside news") > -1:
					FLAIRNAME = 'Outside news'
					FLAIRCSS = 'non-local-news'
				if pbody.find("flair housing") > -1:
					FLAIRNAME = 'Housing'
					FLAIRCSS = 'housing'					
				if pbody.find("flair homeless") > -1:
					FLAIRNAME = 'Homeless'
					FLAIRCSS = 'homeless'
				if pbody.find("flair classified") > -1:
					FLAIRNAME = 'Classifieds'
					FLAIRCSS = 'classifieds'
				if pbody.find("flair event") > -1:
					FLAIRNAME = 'Events'
					FLAIRCSS = 'event'
				if pbody.find("flair meetup") > -1:
					FLAIRNAME = 'Meetups'
					FLAIRCSS = 'meetup'
				if pbody.find("flair breaking") > -1:
					FLAIRNAME = 'Breaking'
					FLAIRCSS = 'breaking'
				if pbody.find("flair other") > -1:
					FLAIRNAME = 'Other'
					FLAIRCSS = 'off-topic'
				if pbody.find("flair photo") > -1:
					FLAIRNAME = 'Photo'
					FLAIRCSS = 'photo'
				if pbody.find("flair help me") > -1:
					FLAIRNAME = 'Help me'
					FLAIRCSS = 'help-me'
				if FLAIRNAME == 'none':				
					print('******* FLAIRNAME = ' + FLAIRNAME + ' and FLAIRCSS = ' + FLAIRCSS) 
					# execute
					ptop = post.submission.id
					print('******* Triggered in COMMENT ' + pid + ' on POST ' + ptop + '\n') 
					REPLY_MESSAGE = 'I see you tried to flair a post ([here](' + plink + ')), but I didn\'t understand which flair you meant. Please choose from these (not case sensitive):\n\n* !FLAIR Local News\n\n* !FLAIR Breaking\n\n* !FLAIR Housing\n\n* !FLAIR Homeless\n\n* !FLAIR Photos\n\n* !FLAIR Meetups\n\n* !FLAIR Events\n\n* !FLAIR Classifieds\n\n* !FLAIR Help me\n\n\n\n* !FLAIR Outisde News\n\n* !FLAIR Other\n\nYour comment was removed so users don\'t get the bright idea of trying it themselves, so please post a new one.'
					r.send_message(pauthor, REPLY_SUBJECT, REPLY_MESSAGE)
					# remove the flair comment
					post.remove()
				else: 
					print('******* FLAIRNAME = ' + FLAIRNAME + ' and FLAIRCSS = ' + FLAIRCSS) 
					# execute
					ptop = post.submission.id
					print('******* Triggered in COMMENT ' + pid + ' on POST ' + ptop + '\n') 
					sub = r.get_submission(submission_id=post.submission.id)
					r.set_flair(SUBREDDIT, sub, flair_text=FLAIRNAME, flair_css_class=FLAIRCSS)
					# remove the flair comment
					post.remove()
			else:
				ptop = post.submission.id
				print('******* NOT AUTHORIZED! Triggered in COMMENT ' + pid + ' on POST ' + ptop + '\n') 
				REPLY_MESSAGE = 'I removed a !FLAIR attempt by ' + pauthor + ' at ' + plink + '.'
				r.send_message('/r/Portland', 'PDXPostBot on the case', REPLY_MESSAGE)
				# remove the flair comment
				post.remove()
		else:
			print(pid + ' - no trigger')
				
def run(config):
	sql = sqlite3.connect('flair.db')
	cur = sql.cursor()
	init(config, cur, sql)
	cycles = 0
	num_cycles = 0
	while True:
		try:
			flairbot(config, cur, sql, num_cycles)
			cycles += 1
			num_cycles +=1
		except Exception as e:
			traceback.print_exc()
		if cycles >= CLEANCYCLES:
			print('Cleaning database')
			cur.execute('DELETE FROM oldposts WHERE id NOT IN (SELECT id FROM oldposts ORDER BY id DESC LIMIT ?)', [MAXPOSTS * 2])
			#cur.execute('DELETE FROM oldposts') # destroy everything, start over
			sql.commit()
			cycles = 0
		print('Running again in %d seconds \n' % WAIT)
		time.sleep(WAIT)
