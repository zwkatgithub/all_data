from sql import Sql

class GameTable:
    game_id = None
    home_team_id = None
    vistor_team_id = None
    home_score = None
    vistor_score = None
    date = None
    season = None
    colNames = [
        'game_id','home_team_id',
        'vistor_team_id','home_score',
        'vistor_score','date','season'
    ]

    def __init__(self,game_id,home_team_id, 
        vistor_team_id, home_score, 
        vistor_score,date,season):
        self.game_id, self.home_team_id, self.vistor_team_id, \
        self.home_score, self.vistor_score, self.date, self.season = \
        game_id, home_team_id, vistor_team_id, home_score, vistor_score, \
        date, season

    def toSql(self):
        pass#Sql.insertValue()
        

    