#This bot was adapted from /u/GoldenSights by /r/FatZombieMama for /r/Portland

import praw
import time
import datetime
import sqlite3

def run(config):
	USERNAME = config['reddit_username']
	#This is the bot's Username. In order to send mail, he must have some amount of Karma.
	PASSWORD = config['reddit_password']
	#This is the bot's Password. 
	USERAGENT = "/r/Portland report monitor"
	#This is a short description of what the bot does. For example "/r/pkmntcgtrades post limit bot"
	SUBREDDIT = "PortlandTesting"
	#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
	MAXPOSTS = 20
	#This is how many posts you want to retrieve all at once. Max 100, but you won't need that many.
	WAIT = 30
	#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
	DELAY = 86400
	#This is the time limit between a user's posts, IN SECONDS. 1h = 3600 || 8h = 28800 || 12h = 43200 || 24h = 86400 || 144h = 518400
	WAITS = str(WAIT)

	sql = sqlite3.connect('LimitDomains/sql.db')
	print('Loaded SQL Database')
	cur = sql.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, lastpost TEXT, domain TEXT)')
	print('Loaded Users')
	cur.execute('CREATE TABLE IF NOT EXISTS oldposts(id TEXT)')
	print('Loaded Oldposts')
	sql.commit()

	r = praw.Reddit(USERAGENT)

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

	while True:
		try:
			scan(r, cur, sql, SUBREDDIT, MAXPOSTS, DELAY)
		except Exception as e:
			print('An error has occured:', e)
		print('Running again in ' + WAITS + ' seconds.\n')
		time.sleep(WAIT)

def getTime(bool):
	timeNow = datetime.datetime.now(datetime.timezone.utc)
	timeUnix = timeNow.timestamp()
	if bool == False:
		return timeNow
	else:
		return timeUnix

def scan(r, cur, sql, SUBREDDIT, MAXPOSTS, DELAY):
	print('Scanning ' + SUBREDDIT)
	subreddit = r.get_subreddit(SUBREDDIT)
	posts = subreddit.get_new(limit=MAXPOSTS)
	for post in posts:
		pauthor = post.author.name
		pid = post.id
		plink = post.short_link
		ptime = post.created_utc
		pdomain = post.domain
		cur.execute('SELECT * FROM oldposts WHERE id="%s"' % pid)
		if not cur.fetchone():
			cur.execute('SELECT * FROM users WHERE name="%s" AND domain="%s"' % (pauthor, pdomain))
			if not cur.fetchone():
				print('Found new user: ' + pauthor)
				print('Domain was: ' + pdomain)
				cur.execute('INSERT INTO users VALUES("%s", "%s", "%s")' % (pauthor, pid, pdomain))
				#r.send_message(pauthor, 'Welcome to /r/PortlandTesting!','Dear ' + pauthor + ',\n\n Our bot has determined that this is your first time posting in /r/PortlandTesting. Please take the time to read [the guidelines](http://www.reddit.com/r/Portland/wiki/index) to understand how the subreddit works.\n\nIf you have any questions, feel free to [message the moderators.](http://www.reddit.com/message/compose?to=%2Fr%2FPortland) Thanks, and stay dry!', captcha=None)
				sql.commit()
				print('\t' + pauthor + ' (' + pdomain + ') has been added to the database.')
				time.sleep(5)
			else:
				cur.execute('SELECT * FROM users WHERE name="%s" AND domain="%s"' % (pauthor, pdomain))
				fetch = cur.fetchone()
				print('Found post by known user: ' + pauthor + ' (' + pdomain + ')')
				#if user is one of these
				if pauthor == 'VoodooAndPowells' or pauthor == 'jr98664' or pauthor == 'imyxle' or pauthor == 'BikeTheftVictim' or pauthor == 'Imnaha2':
					#if domain is one of these
					if pdomain == 'oregonlive.com' or pdomain == 'katu.com' or pdomain == 'kgw.com' or pdomain == 'kptv.com' or pdomain == 'koin.com' or pdomain == 'golocalpdx.com' or pdomain == 'm.portlandmercury.com' or pdomain == 'portlandmercury.com' or pdomain == 'wweek.com' or pdomain == 'projects.oregonlive.com' or pdomain == 'bikeportland.org':
						previousid = fetch[1]
						previous = r.get_info(thing_id='t3_'+previousid)
						previoustime = previous.created_utc
						if ptime > previoustime:
							curtime = getTime(True)
							difference = curtime - previoustime
							if difference >= DELAY:
								print('\tPost complies with timelimit guidelines. Permitting')
								cur.execute('DELETE FROM users WHERE name="%s" AND domain="%s"' % (pauthor, pdomain))
								cur.execute('INSERT INTO users VALUES("%s", "%s", "%s")' % (pauthor, pid, pdomain))
								sql.commit()
								print('\t' + pauthor + "'s database info has been reset.")
							else:
								differences = str(DELAY - difference)
								print('*******************************************************************************Post does not comply with timelimit guidelines. Author must wait ' + differences)
								print('*******************************************************************************' + pauthor + "'s database info remains unchanged")
								post.add_comment('You are posting from ' + pdomain + ' too frequently, so your post has been removed. Please do not submit more than one post per 24 hours from that domain, to comply with existing rules/reddiquette [^1](https://www.reddit.com/wiki/reddiquette#wiki_in_regard_to_new_submissions) [^2](https://www.reddit.com/wiki/selfpromotion#wiki_here_are_some_guidelines_for_best_practices.3A) [^3](https://www.reddit.com/r/Portland/wiki/index#wiki_what_are_the_rules_for_posting_in_.2Fr.2Fportland.3F).\n\nIf you have any questions, feel free to [message the moderators](http://www.reddit.com/message/compose?to=%2Fr%2FPortland).')
								post.remove(spam=False)
								r.send_message('/r/Portland', 'Removed a post: '+ pauthor +', '+ pdomain, 'Removed: ' + plink + '\n\n'+ pauthor +', '+ pdomain)
								time.sleep(5)
			#end else
			cur.execute('INSERT INTO oldposts VALUES("%s")' % pid)
		sql.commit()
