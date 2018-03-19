from functools import singledispatch
from datetime import date
@singledispatch
def change(value):
    return 'null'
@change.register(None)
def _(value):
    return 'null'
@change.register(int)
def _(value):
     return str(value)
@change.register(str)
def _(value):
    return r"'"+value+r"'"
@change.register(float) 
def _(value):
    return str(value)
@change.register(date)
def _(value):
    return r"'"+'{0}'.format(value)+r"'"

def genGameID(season, game):
    return '002{0}0{1}'.format(
        '%02d'%season, '%04d'%game
    )
def genSeason(season):
    return '20{0}-{1}'.format('%02d'%season,'%02d'%(season+1))
def genDict(li):
    return {  l :i for i,l in enumerate(li)}

