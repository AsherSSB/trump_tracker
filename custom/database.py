import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("trump.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS channel (
                serverid INTEGER PRIMARY KEY,
                channelid INTEGER)""")
        
    def enter_server(self, server_id, channel_id):
        self.cur.execute("""
            INSERT OR IGNORE INTO channel VALUES (?, ?)""", (server_id, channel_id))
        self.con.commit()

    def fetch_channel(self, server_id):
        res = self.cur.execute("""
            SELECT channelid FROM channel WHERE
            serverid = ?""", (server_id,))
        
        return res.fetchone()[0] if res is not None else -1 

    def set_channel(self, server_id, channel_id):
        res = self.cur.execute("""
            UPDATE channel SET
            channelid = ?
            WHERE serverid = ?""", (channel_id, server_id))
        self.con.commit()
