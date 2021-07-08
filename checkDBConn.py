"""
Created on Sun Oct  31 15:01:50 2020
@author: Viswanathan A
@Descirpion : Database Manager Class with Class Methods. This Code lets you connect to the Game Database.

"""

import sqlite3

class DatabaseManager:
    ''' This is the Database Manager class'''

    def __init__(self, db_name):
        self.db_name = db_name  # database name
        #self.tbl_name = tbl_name # Table Name 
        self.conn = None        # connection

    def create_connection(self):
        """ create a database connection to a SQLite database """
    
        try:
            self.conn = sqlite3.connect(self.db_name)
            return True
            #print(sqlite3.version)
        except :
            #print(e)
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def create_PlayerTable(self):
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        curr.execute("""CREATE TABLE IF NOT EXISTS PlayersData (
	                First_Name Text NOT NULL,
	                Last_Name Text NOT NULL,
                    High_Score INTEGER DEFAULT 0,
                    PRIMARY KEY (First_Name,Last_Name)
	                )""")

    def insert_PlayerData(self, player):
        '''This function Inserts the player data into the PlayersData Table'''
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        with self.conn:
            curr.execute("INSERT INTO PlayersData (First_Name,Last_Name,High_Score) VALUES (:First_Name, :Last_Name, :High_Score)", {'First_Name': player.first, 'Last_Name': player.last, 'High_Score': player.HighScore})    

    def check_PlayerExists(self, player):
        '''This function Checks if the Player Exists in the PlayersData Table. If Exists Return 1 Else Return 0'''
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        with self.conn:
            curr.execute("SELECT COUNT(1) FROM PlayersData WHERE First_Name = :First_Name AND Last_Name = :Last_Name", 
                    {'First_Name': player.first, 'Last_Name': player.last})   
        n =  curr.fetchone()
        return n[0]

    def update_PlayerData(self, player,High):
        '''This Function is called to update the Players  HighScore to the PlayersData Table'''
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        curr.execute("""UPDATE PlayersData SET High_Score = :High_Score
                    WHERE First_Name = :First_Name AND Last_Name = :Last_Name""",
                    {'First_Name': player.first, 'Last_Name': player.last, 'High_Score': High})
        self.conn.commit()

    def get_HighScoreByPlayer(self,player):
        ''' This function returns the Highest Score of the Player from the Table PlayersData'''
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        curr.execute("SELECT HIGH_SCORE FROM PlayersData WHERE First_Name = :First_Name AND Last_Name = :Last_Name", 
                    {'First_Name': player.first, 'Last_Name': player.last})
        x =  curr.fetchone()
        return x[0]
    
    def get_HighScore(self):
        ''' This function returns the Highest Score of the Player from the Table PlayersData'''
        self.conn = sqlite3.connect(self.db_name)
        curr = self.conn.cursor()
        curr.execute("SELECT MAX(HIGH_SCORE) FROM PlayersData")
        x =  curr.fetchone()
        return x[0]

