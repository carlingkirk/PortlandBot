import praw
import time
import datetime
import sqlite3
from datetime import datetime, timedelta

class UpdateMenu:

	def __init__(self, config):
		#This is the bot's Username. In order to send mail, he must have some amount of Karma.
		self.username = config['reddit_username']
		#This is the bot's Password. 
		self.password = config['reddit_password']
		#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
		self.subreddit_name = config['subreddit']
		#This is a short description of what the bot does. For example "/r/pkmntcgtrades post limit bot"
		self.useragent = "/r/Portland menu updater"
		#This is how many posts you want to retreieve all at once. Max 100, but you won't need that many.
		self.max_posts = 20
		#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
		self.WAIT = 300
		self.WAITS = str(self.WAIT)
		
	def scan(self, r, cur, sql):
		print('Scanning /r/' + self.subreddit_name + '')
		subreddit = r.get_subreddit(self.subreddit_name)
		posts = subreddit.get_new(limit=self.max_posts)
		today = datetime.now().strftime("%Y-%m-%d")
		for post in posts:
			if post.author is None:
				continue # Author is deleted  
			pauthor = post.author.name
			pid = post.id
			ptext = self.subreddit_name + '/comments/' + pid
			plink = post.short_link
			ptime = post.created_utc
			ptitle = post.title 
			pbody = post.selftext 
			beginning = ptitle[:25] 
			end = ptitle[-18:] 
			print( '\nFound ' + ptext )
			cur.execute('SELECT * FROM oldposts WHERE id="%s"' % pid)
			if not cur.fetchone():
				#cur.execute('SELECT * FROM users WHERE name="%s"' % (pauthor))
				#if not cur.fetchone():
					#print('Found new user: ' + pauthor)
					#cur.execute('INSERT INTO users VALUES("%s", "%s")' % (pauthor, pid))
					#sql.commit()
					#print('***' + pauthor + ' has been added to the database.')
					#time.sleep(3)
				#else:
					#print('Post is by a known user: ' + pauthor)
				oldlink = ""
				if pauthor == 'AutoModerator':
					print('User allowed: ' + pauthor + '\nBEGINNING: "' + beginning + '"\nEND: "' + end + '"')
					if beginning == 'WEEKLY /R/PORTLAND CLASSI': 
						print('Found match: "' + beginning + '" == "WEEKLY /R/PORTLAND CLASSI"')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="classifieds"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('CLASSIFIEDS: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "classifieds"' % ( ptext ))
							sql.commit()
						else:
							cur.execute('INSERT INTO links VALUES ("classifieds", "%s")' % ( ptext ))
							sql.commit()
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					if beginning == 'WEEKLY /R/PORTLAND EVENTS': 
						print('Found match: "' + beginning + '" == "WEEKLY /R/PORTLAND EVENTS"')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="events"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('EVENTS: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "events"' % ( ptext ))
							sql.commit()
						else:
							cur.execute('INSERT INTO links VALUES ("events", "%s")' % ( ptext ))
							sql.commit()
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					if beginning == 'MONTHLY /R/PORTLAND "I\'M ': 
						print('Found match: "' + beginning + '" == "MONTHLY /R/PORTLAND "I\'M "')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="hiring"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('I\'M HIRING: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "hiring"' % ( ptext ))
							sql.commit()
						else:
							cur.execute('INSERT INTO links VALUES ("hiring", "%s")' % ( ptext ))
							sql.commit()
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					if beginning == 'MONTHLY /R/PORTLAND \"HIRE': 
						print('Found match: "' + beginning + '" == "MONTHLY /R/PORTLAND \"HIRE"')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="hireme"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('HIRE ME: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "hireme"' % ( ptext ))
							sql.commit()
						else:
							cur.execute('INSERT INTO links VALUES ("hireme", "%s")' % ( ptext ))
							sql.commit() 
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					if end == 'WEEKLY RANT THREAD': 
						print('Found match: "' + end + '" == "WEEKLY RANT THREAD"')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="rant"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('RANT: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "rant"' % ( ptext ))
							sql.commit()
							css_contents = r.get_stylesheet(self.subreddit_name)['stylesheet']
							oldid = oldlink[-6:]
							newcss = css_contents.replace( oldid, pid )
							print('CSS RANT: replacing OLDID: "' + oldid + '" with pid: "' + pid + '"')
							#print('\newcss: ' + newcss + '\n')
							r.set_stylesheet(subreddit, stylesheet=newcss)
							time.sleep(3)
						else:
							cur.execute('INSERT INTO links VALUES ("rant", "%s")' % ( ptext ))
							sql.commit()
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					if end == 'weekly rave thread': 
						print('Found match: "' + end + '" == "weekly rave thread"')
						settings = r.get_settings(self.subreddit_name)
						sidebar_contents = settings['description']
						cur.execute('SELECT url FROM links WHERE title="rave"')
						row = cur.fetchone()
						if row:
							oldlink = str(row[0])
						if oldlink != "":
							print('RAVE: replacing OLDLINK: "' + oldlink + '" with newlink: "' + ptext + '"')
							newsidebar = sidebar_contents.replace( oldlink, ptext )
							r.update_settings(subreddit, description=newsidebar)
							#print('\nSIDEBAR_CONTENTS: ' + sidebar_contents + '\n')
							#print('\nNEWSIDEBAR: ' + newsidebar + '\n')
							time.sleep(3)
							cur.execute('UPDATE links SET url = "%s" WHERE title LIKE "rave"' % ( ptext ))
							sql.commit()
							css_contents = r.get_stylesheet(self.subreddit_name)['stylesheet']
							oldid = oldlink[-6:]
							newcss = css_contents.replace( oldid, pid )
							print('CSS RANT: replacing OLDID: "' + oldid + '" with pid: "' + pid + '"')
							#print('\newcss: ' + newcss + '\n')
							r.set_stylesheet(subreddit, stylesheet=newcss)
							time.sleep(3)
						else:
							cur.execute('INSERT INTO links VALUES ("rave", "%s")' % ( ptext ))
							sql.commit()
							print('FAIL: Could not replace OLDLINK: "' + oldlink + '" ("' + row[0] if row else '' + '") with newlink: "' + ptext + '"')
					time.sleep(3)
				cur.execute('INSERT INTO oldposts VALUES("%s", "%s")' % (today, pid))
				print('Adding "%s" to database (%s)' % ( pid, today ))
			else:
				print('Already knew about %s' % ( ptext ))
			sql.commit()

	def run(self, config):
		sql = sqlite3.connect('UpdateMenusAndCSS/sql.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		print('Loaded SQL Database')
		cur = sql.cursor()

		#cur.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, lastpost TEXT)')
		#print('Loaded Users')
		cur.execute('CREATE TABLE IF NOT EXISTS oldposts(stamp TEXT, id TEXT)')
		print('Loaded Oldposts')
		cur.execute('CREATE TABLE IF NOT EXISTS links(title TEXT, url TEXT)')
		print('Loaded Links')
		sql.commit()

		# clean oldposts
		now = datetime.now()
		today = now.strftime("%Y-%m-%d")
		clean = datetime.now() - timedelta(days=32)
		too_old = clean.strftime("%Y-%m-%d")
		print('Removed post IDs from before %s' % too_old)
		cur.execute('DELETE FROM oldposts WHERE stamp < "%s"' % too_old)
		sql.commit()
		
		r = praw.Reddit(self.useragent)
		r.config.decode_html_entities = True

		Trying = True
		while Trying:
			try:
				r.login(self.username, self.password,disable_warning=True)
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
				self.scan(r, cur, sql)
			except Exception as e:
				print('An error has occured:', e)
			#cur.execute("SELECT * FROM oldposts;")
			#print('\nOLDPOSTS:')
			#print(cur.fetchall())
			print('\nRunning again in ' + self.WAITS + ' seconds.\n')
			time.sleep(self.WAIT)