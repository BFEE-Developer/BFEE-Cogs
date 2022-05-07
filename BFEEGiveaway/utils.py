import sqlite3
from redbot.core import commands, data_manager, Config, checks, Config

PATH = 'data/bfeedb/'

__version__ = "1.0"
__author__ = "OGKaktus (OGKaktus#5299)"

class BFEEdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 3258943194, force_registration=True)
        
    def __unload(self):
        self.save()
        self.db.close()

    def save(self):
        self.db.commit()
        
    def createDatabase(self, dbname: str):
        self.db = sqlite3.connect(PATH + dbname, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row
        
    def query(self, q: str):
        if not self.db:
            pass
            
        with self.db as con:
            con.executescript(q)
    
        
    def insert(self, table: str, **kwargs):
        col =[]
        colval = []
        for key, value in kwargs.items():
            col.append(key)
            colval.append(value)
            
        sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, ', '.join(col), ', '.join('?' * len(colval)))
        
        with self.db as con:
            cur = con.execute(sql, colval)
            return true
            
    def getValue(self, table: str, col: str, **kwargs):
        wheres = []
        params = []
        for param, value in kwargs.items():
            if isinstance(value, Iterable) and not isinstance(value, str):
                if not isinstance(value, Sequence):
                    value = tuple(value)

                wheres.append(param + " IN (%s)" % ', '.join('?' * len(value)))
                params.extend(value)
            else:
                wheres.append(param + " IS ?")
                params.append(value)
        
        if wheres:
            where = " WHERE " + " AND ".join(wheres)
        else:
            where = " "
            
        sql = "SELECT * FROM %s %s " % (table, where)
        
        with self.db as con:
            cur = con.execute(sql, params)
            return cur.fetchall()