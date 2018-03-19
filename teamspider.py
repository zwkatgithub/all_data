import requests 

from useragent import UserAgent
from log import Log
from databaseconn import DatabaseConnector
from sql import Sql
from utils import  change
#https://stats.nba.com/stats/teamdetails

class TeamSpider(UserAgent):
    url = 'https://stats.nba.com/stats/leaguedashteamstats'
    params = {
        'Conference':"",
        'DateFrom': "",
        'DateTo': "",
        'Division': "",
        'GameScope': "",
        'GameSegment': "",
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': "",
        'MeasureType': "Base",
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': "",
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience':'', 
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': '2017-18',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference':'', 
        'VsDivision':'' 
    }

    def __init__(self):
        try:
            self.data = requests.get(self.url, 
                        headers={'User-Agent':self.userAgent}, 
                        params=self.params)
        except Exception:
            Log.log(__file__,"__init__")
    def run(self):
        conn = DatabaseConnector()
        conn.connect()
        try:
            teams = self.data.json()['resultSets'][0]['rowSet']
            

            for team in teams:
                print('processing team %r' % team[0])
                value = ','.join([change(team[0]),
                        change(team[1])])
                colNames = ','.join(['team_id','name'])
                sql = Sql.insertValue.format(table = 'team',
                    colNames = colNames,
                    value = value)
                print(sql)
                conn.cursor.execute(sql)
            conn.commit()
        except Exception:
            Log.log(__file__,"run",65)
            conn.rollback()
        finally:
            conn.close()

def run(teamID,cur):
    url = 'https://stats.nba.com/stats/teamdetails'
    res = requests.get(url, params={'teamID':teamID},headers={'User-Agent':UserAgent.userAgent})
    data = res.json()
    row = data['resultSets'][0]['rowSet'][0]
    try:
        cur.execute(
            "UPDATE team SET nick_name={0},city={1} WHERE team_id={2};".format(
                change(row[1]), change(row[4]), change(teamID)
            )
        )
    except Exception:
        print('Error '+str(teamID))


if __name__ == '__main__':
    conn = DatabaseConnector()
    conn.connect()
    conn.cursor.execute('SELECT team_id FROM team;')
    res = conn.cursor.fetchall()
    for r in res:
        print('processing '+str(r[0]))
        run(r[0],conn.cursor)
    conn.commit()
    conn.close()


