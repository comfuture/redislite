import sqlite3
from .exc import RedisliteError

def connect(dbfile=None):
    if not dbfile:
        envroot = os.path.abspath(os.path.curdir)
        dbfile = os.path.join(envroot, 'data/redislite/dump.sqlitedb')
    try:
        return sqlite3.connect(dbfile)
    except IOError:
        raise RedisliteError('failed connect sqlitedb "%s" permission denied' % dbfile)

def setup(conn):
    cur = conn.cursor()

    # table for k-v store
    cur.execute('''CREATE TABLE IF NOT EXISTS keys (
        key text,
        value text,
        timestamp text
    )''')

    # table for list store
    cur.execute('''CREATE TABLE IF NOT EXISTS lists (
        key text,
        idx integer,
        value text,
        timestamp text
    )''')

    # table for sets store
    cur.execute('''CREATE TABLE IF NOT EXISTS sets (
        key text,
        score integer,
        member text,
        timestamp text
    )''')

    # table for hash store
    cur.execute('''CREATE TABLE IF NOT EXISTS hashes (
        key text,
        prop text,
        value text,
        timestamp text
    )''')

    # table for pubsub
    cur.execute('''CREATE TABLE IF NOT EXISTS pubsub (
        channel text,
        message text
    )''')

    # function for pubsub
    def broadcast(channel, message):
        print 'published {0} from {1}'.format(
                message, channel)
    conn.create_function('broadcast', 2, broadcast)

    # trigger
    cur.execute('''CREATE TRIGGER IF NOT EXISTS pubsub_trigger
        AFTER INSERT ON pubsub FOR EACH ROW BEGIN
            SELECT broadcast(
                new.channel,
                new.message
            );
        END;
    ''')
    conn.commit()


class DAO(object):

    def __init__(self, dbfile=None):
        self.conn = connect(dbfile)

    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur

    def set(self, table, values={}):
        cur = self.conn.cursor()
        cur.execute('''INSERT OR REPLACE INTO {0}
            (?,?,?) VALUES (?,?,?)'''.format(table))

    def get(self, table, keys=[]):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM {0}'''.format(table))
        return cur.fetchone()

    def publish(self, channel, message):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO pubsub (channel, message) VALUES (?,?)''',
            channel, message)