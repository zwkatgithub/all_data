from Spider import Spider
import requests
from utils import genGameID, genSeason, change
from datetime import datetime
from sql import Sql
from log import Log

import argparse

class GameSpider(Spider):
    
    def __init__(self, seasons, games,
        url='https://stats.nba.com/stats/boxscoresummaryv2',
        params={'GameID':None},
        colNames=','.join(
            ['game_id','home_team_id','vistor_team_id','home_score','vistor_score','date','season']
        )):
        super(GameSpider, self).__init__()


        self.url = url
        self.params = params
        self.colNames = colNames
        self.startSeason, self.endSeason = [int(s) for s in seasons.split('-')]
        self.startGame, self.endGame = [int(g) for g in games.split('-')]
        self.data = None
        self.gameID = None
        self.season = None

    def __del__(self):
        self.conn.close()

    def getGameData(self):
        try:
            row = self.data['resultSets'][0]['rowSet'][0]
        except Exception:
            raise Exception
        date = datetime.strptime(row[0],'%Y-%m-%dT%H:%M:%S').date()
        homeTeamID = row[6]
        visitTeamID = row[7]
        row1 = self.data['resultSets'][5]['rowSet'][0]
        row2 = self.data['resultSets'][5]['rowSet'][1]
        if row1[3] == homeTeamID:
            home_score,visit_score = row1[22], row2[22]
        else:
            home_score,visit_score = row2[22], row1[22]
        return [self.gameID, homeTeamID, visitTeamID,home_score,visit_score, date, self.season]

    def run(self):
        self.conn.connect()
        for season in range(self.startSeason,self.endSeason+1):
            values = []
            for game in range(self.startGame, self.endGame+1):
                self.season = season
                self.gameID = genGameID(season,game)
                print("processing "+str(self.gameID))
                self.params['GameID'] = self.gameID
                req = requests.get(self.url, params=self.params, headers={'User-Agent':self.userAgent})
                try:
                    self.data = req.json()
                    gameData = self.getGameData()
                except Exception:
                    Log.log(__file__, 'run',self.gameID)
                    continue
                value = '('+','.join([change(d) for d in gameData])+')'
                values.append(value)
            sql = Sql.insertValues.format(table='game',colNames=self.colNames, values=','.join(values))
            try:
                #print(sql)
                self.conn.cursor.execute(sql)
            except:
                Log.log(__file__, "run")
                self.conn.rollback()
            self.conn.commit()
            
            
if __name__ == '__main__':
    #import threading

    p = argparse.ArgumentParser()
    p.add_argument('-s','--season')
    p.add_argument('-g','--game')
    args = p.parse_args()

    #ten years so 
    # game = 1230//4
    # season = 10
    # spiders = []
    # threads = []
    # for s in range(season):
    #     for i in range(1,5):
    #         start = (i-1)*game +1
    #         end = start +game
    #         spiders.append(GameSpider('%02d-%02d'%(s+7,s+8),'%04d-%04d'%(start,end)))
    #         t = threading.Thread(target=spiders[-1].run)
    #         threads.append(t)
    
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
    
    


    gameSpider = GameSpider(args.season, args.game)

    gameSpider.run()
    

        
        