from .exc import RedisliteError

class Command(object):

	def __init__(self, dao):
		self.dao = dao

	def APPEND(self, key, value):
		cur = self.dao.execute('''SELECT * FROM keys WHERE key=?''', [key])
		try:
			_key, old = cur.fetchOne()
			newstr = '{0} {1}'.format(old, value)
			cur.execute('''UPDATE keys (value) VALUES (?) WHERE key=?''',
				(newstr, _key))
			return len(newstr)
		except KeyError:
			cur.execute('''INSERT INTO keys (key, value) VALUES (?,?)''',
				(key, value,))
			return len(value)

	def AUTH(self, password):
		"""NOT IMPLEMENT"""
		return 'OK'

	def BGREWRITEAOF(self):
		"""NOT IMPLEMENT"""
		return 'OK'

	def BGSAVE(self):
		"""NOT IMPLEMENT"""
		return 'OK'

	def BITCOUNT(self, key, start=0, end=-1):
		# TODO: implement
		return 1

	def BITOP(self, op, dest, *args):
		return 'OK'

	def BLPOP(self, key, *args):
		return []

	def BRPOP(self, key, *args):
		return []

	def BRPOPLPUSH(self, source, dest, timeout):
		return 'OK'

	def CLIENT(self, cmd, *args, **kwargs):
		# KILL, LIST
		pass

	def CONFIG(self, cmd, params):
		# GET, SET, RESETSTAT
		pass

	def DBSIZE(self):
		return 0

	def DEBUG(self, cmd, key):
		# OBJECT, SEGFAULT
		return 'OK'

	def DECR(self, key):
		cur = self.dao.execute('''SELECT * FROM keys WHERE key=?''', [key])
		return 1

	def DECRBY(self, key, amount=-1):
		pass

	def DEL(self, *keys):
		return 1

	def DISCARD(self):
		pass

	def DUMP(self, key):
		pass

	def ECHO(self, message):
		return message

	def EVAL(self, script, numkeys, *args):
		pass

	def EVALSHA(sha1, numkeys, *args):
		pass

	def EXEC(self):
		'''Execute all commands issued after MULTI'''

	def EXISTS(self, key):
		pass

	# --------
	def GET(self, key):
		'''Get the value of a key'''
		return self.dao.get(key)

	def SET(self, key, value):
		self.dao.set(key, value)




