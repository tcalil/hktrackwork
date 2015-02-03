# -*- coding: utf-8 -*-
__author__ = 'Vince'

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, UniqueConstraint, CheckConstraint, Time, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA, TIMESTAMP
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref
#for Oracle, Firebird
from sqlalchemy import Sequence
import settings


#for multithreading
# from twisted.web import xmlrpc, server
# from twisted.internet import reactor
from twisted.internet.defer import Deferred
from sa_decorators import DBDefer


ModelBase = declarative_base()

#create ALL models here for DB



class EventType(ModelBase):
    __tablename__ = "hk_trackwork_type"
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    Name = Column(String(100), unique=True)
    UniqueConstraint('Name', name='EventTypeName_uidx')


class Owner(ModelBase):
    __tablename__ = "owner"
    __tableargs__ = ( CheckConstraint('Homecountry in ("HKG", "SIN", "AUS", "NZL", "RSA". "ENG", "IRE", "DUB", "IRE", "SCO", "MAC")'))
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    Name = Column(String(255), unique=True)
    Homecountry = Column('Homecountry', String(3), nullable=False)
    UniqueConstraint('Name', name='OwnerName_uidx')

class Gear(ModelBase):
    __tablename__ = "hk_gear"
    id = Column(Integer, primary_key=True)
    Name = Column(String(255), unique=True)
    UniqueConstraint('Name', name='GearName_uidx')

class Going(ModelBase):
    __tablename__ = "hk_going"
    id = Column(Integer, primary_key=True)
    Name = Column(String(255), unique=True)
    UniqueConstraint('Name', name='GoingName_uidx')

class Raceclass(ModelBase):
    __tablename__ = "hk_raceclass"
    id = Column(Integer, primary_key=True)
    Name = Column(String(255), unique=True)
    UniqueConstraint('Name', name='RaceClassName_uidx')

class Distance(ModelBase):
    __tablename__= "hk_distance"
    id = Column(Integer, primary_key=True)
    MetricName = Column(Integer)
    Miles = Column(Float)
    Furlongs = Column(Integer) 
    UniqueConstraint('MetricName', name='HKDistance_MetricName_uidx')

class Railtype(ModelBase):
    __tablename__= "hk_railtype"
    id = Column(Integer, primary_key=True)
    Name = Column(String(256))
    UniqueConstraint('Name', name='HKRailType_Name_uidx')

class Horse(ModelBase):
    __tablename__ = "horse"
    __tableargs__ = ( CheckConstraint('Homecountry in ("HKG", "SIN", "AUS", "NZL", "RSA". "ENG", "IRE", "DUB", "IRE", "SCO", "MAC")'))
    id = Column(Integer, primary_key=True)
    Code = Column(String(6), nullable=False, unique=True)
    Name = Column(String(255), nullable=False)
    Sex = Column(String(2), nullable=True)
    Homecountry = Column('Homecountry', String(3), nullable=False)
    ImportType = Column(String(10), default="")
    SireName = Column(String(255), default="")
    DamName = Column(String(255), default="")
    DamSireName = Column(String(255), default="")
    UniqueConstraint('Name', 'Code', 'Homecountry', name='Horsecodehomecountry_uidx')

class HKTrackwork(ModelBase):
    __tablename__ = "hk_trackwork"
    id = Column(Integer, primary_key=True)
    EventDate = Column(Date, nullable=False)
    EventVenue = Column(String(100))
    EventDescription = Column(String(255))
    EventTypeid = Column(Integer, ForeignKey('hk_trackwork_type.id'))
    Ownerid = Column(Integer, ForeignKey("owner.id"))
    Gearid = Column(Integer, ForeignKey("hk_gear.id"))
    Horseid = Column(Integer, ForeignKey('horse.id'))
    UniqueConstraint('EventDate', 'EventDescription', 'Horseid', name='EventDateDescrHorseId_uidx')


class Jockey(ModelBase):
    __tablename__ = "jockey"
    __tableargs__ = ( CheckConstraint('Homecountry in ("HKG", "SIN", "AUS", "NZL", "RSA". "ENG", "IRE", "DUB", "IRE", "SCO", "MAC")'))
    id = Column(Integer, primary_key=True)
    Name = Column(String(100), unique=True)
    Code = Column(String(10))
    Homecountry = Column('Homecountry', String(3), nullable=False)
    UniqueConstraint('Name', name='JockeyName_uidx')

class Trainer(ModelBase):
    __tablename__ = "trainer"
    __tableargs__ = ( CheckConstraint('Homecountry in ("HKG", "SIN", "AUS", "NZL", "RSA". "ENG", "IRE", "DUB", "IRE", "SCO", "MAC")'))
    id = Column(Integer, primary_key=True)
    Name = Column(String(255), unique=True)
    Code = Column(String(10))
    Homecountry = Column('Homecountry', String(3), nullable=False)
    UniqueConstraint('Name', name='Trainername_uidx')

class HKRace(ModelBase):
    __tablename__ = "hk_race"
    __tableargs__ = ( 
        CheckConstraint('RacecourseCode in ("HV", "ST")'), UniqueConstraint('PublicRaceIndex'), {'autoload': True})
    id = Column(Integer, primary_key=True)
    Url = Column('Url', String)
    RacecourseCode = Column('RacecourseCode', String, nullable=False)
    Name = Column('Name', String(255), nullable=True)
    RaceDate = Column('RaceDate', Date, nullable=True)
    RaceDateTime = Column('RaceDateTime', String, nullable=True)
    RaceNumber = Column('RaceNumber', Integer, nullable=False)
    PublicRaceIndex = Column('PublicRaceIndex', String, nullable=False)
    RaceIndex = Column('RaceIndex', String, nullable=True)
    IncidentReport = Column('IncidentReport', String, nullable=True)
    Goingid = Column(Integer, ForeignKey("hk_going.id"))
    Raceclassid = Column(Integer, ForeignKey("hk_raceclass.id"))
    Distanceid = Column(Integer, ForeignKey("hk_distance.id"))
    Railtypeid = Column(Integer, ForeignKey("hk_railtype.id"))
    HKDividendid = Column(Integer, ForeignKey("hk_dividend.id"))
    Raceratingspan = Column(String)
    Prizemoney = Column(Integer)
    Surface = Column('Surface', String)
    Inraceimage = Column('Inraceimage', BYTEA, nullable=True)
    UniqueConstraint('PublicRaceIndex', name='HKRace_PublicRaceIndex_uidx')



    def __repr__(self):
        return "HKRace(RacecourseCode='%s', Name= '%s', RaceDate='%s', RaceNumber='%d', RaceIndex='%s',Prizemoney='%s')" % \
        (self.RacecourseCode, self.Name, self.RaceDate, self.RaceNumber, self.RaceIndex, self.RaceIndex, self.Prizemoney)  

class HKDividend(ModelBase):
    __tablename__ = "hk_dividend"
    id = Column(Integer, primary_key=True)
    RacecourseCode = Column('RacecourseCode', String, nullable=False)
    RaceDate = Column('RaceDate', String, nullable=False)
    RaceNumber = Column('RaceNumber', String, nullable=False)
    PublicRaceIndex = Column('PublicRaceIndex', String, nullable=False)
    WinDiv= Column(Float, nullable=False)
    Place1Div = Column(Float, nullable=True)
    Place2Div = Column(Float, nullable=True)
    Place3Div = Column(Float, nullable=True)
    QNDiv = Column(Float, nullable=True)
    QP12Div = Column(Float, nullable=True)
    QP13Div = Column(Float, nullable=True)
    QP23Div = Column(Float, nullable=True)
    TierceDiv = Column(Float, nullable=True)
    TrioDiv = Column(Float, nullable=True)
    FirstfourDiv = Column(Float, nullable=True)
    #optionals
    QuartetDiv = Column(Float)
    ThisDouble11Div = Column(Float)
    ThisDouble12Div = Column(Float)
    Treble111Div = Column(Float)
    Treble112Div = Column(Float)
    ThisDoubleTrioDiv = Column(Float)
    TripleTrio111Div = Column(Float)
    TripleTrio112Div = Column(Float)
    SixUpDiv = Column(Float)
    SixUpBonusDiv = Column(Float)
    UniqueConstraint('RacecourseCode', 'RaceDate','RaceNumber', name='HKDividendRCCodeDateRaceNumber_uidx') 

class HKRunner(ModelBase):
    __tablename__ = "hk_runner"
    id = Column(Integer, primary_key=True)
    Raceid = Column(Integer, ForeignKey("hk_race.id"))
    Horseid = Column(Integer, ForeignKey("horse.id"))
    Place = Column(Integer, ForeignKey("horse.id"))
    isVetScratched = Column('isVetScratched', Boolean)
    Gearid = Column(Integer, ForeignKey("hk_gear.id"))
    Ownerid = Column(Integer, ForeignKey("owner.id"))
    HorseNumber= Column('HorseNumber', String, nullable=True)
    Jockeyid =Column(Integer, ForeignKey("jockey.id"))
    Trainerid =Column(Integer, ForeignKey("trainer.id"))
    Jockey= Column('Jockey', String, nullable=True)
    JockeyWtOver = Column('JockeyWtOver', Integer, nullable=True)
    Trainer= Column('Trainer', String, nullable=True)
    ActualWt= Column('ActualWt', Integer, nullable=True)
    DeclarHorseWt= Column('DeclarHorseWt', Integer, nullable=True)
    HorseWtDeclarChange = Column('HorseWtDeclarChange', Integer, nullable=True)
    HorseWtpc = Column('HorseWtpc', Float, nullable=True)
    Draw= Column('Draw', Integer, nullable=True)
    LBW= Column('LBW', Float, nullable=True)
    Last6runs = Column('Last6runs', String(30), nullable=True)
    Priority = Column('Priority', String(10), nullable=True)
    RunningPosition= Column('RunningPosition', String, nullable=True)
    Rating =Column('Rating', Integer, nullable=True)
    RatingChangeL1 = Column('RatingChangeL1', Integer, nullable=True)
    SeasonStakes = Column('SeasonStakes', Integer, nullable=True)
    WFA = Column('WFA', Integer, nullable=True)
    isRanOn = Column('isRanOn', Boolean, nullable=True)
    Sec1DBL = Column('Sec1DBL', Float, nullable=True)
    Sec2DBL = Column('Sec2DBL', Float, nullable=True)
    Sec3DBL = Column('Sec3DBL', Float, nullable=True)
    Sec4DBL = Column('Sec4DBL', Float, nullable=True)
    Sec5DBL = Column('Sec5DBL', Float, nullable=True)
    Sec6DBL = Column('Sec6DBL', Float, nullable=True)
    FinishTime= Column('FinishTime', Time, nullable=True)  #e.g. 1.49.08 --> '00:01:49.08' hhmmss.nn always < 5mins
    Sec1Time = Column('Sec1Time', Time, nullable=True)
    Sec2Time = Column('Sec2Time', Time, nullable=True)
    Sec3Time = Column('Sec3Time', Time, nullable=True)
    Sec4Time = Column('Sec4Time', Time, nullable=True)
    Sec5Time = Column('Sec5Time', Time, nullable=True)
    Sec6Time = Column('Sec6Time', Time, nullable=True)
    WinOdds= Column('WinOdds', Float, nullable=True)
    HorseReport = Column('HorseReport', String, nullable=True)
    HorseColors = Column('HorseColors', BYTEA, nullable=True)
    UniqueConstraint('Raceid', 'Horseno', 'Horseid', name='HKRunner_raceidhorsenohorseid_uidx')

#OTHER TABLES

class HKOdds(ModelBase):
    __tablename__ = "hk_odds"
    id = Column(Integer, primary_key=True)
    Horsenumber = Column(Integer, nullable=False)
    Updatedate = Column(Date, nullable=False)
    Updatetime = Column(Time, nullable=False)
    Winodds = Column(Float)
    Placeodds = Column(Float)
    Raceid = Column(Integer, ForeignKey("hk_race.id"))
    # Horseid = Column(Integer, ForeignKey("horse.id"))
    UniqueConstraint('Raceid', 'HorseNumber', 'UpdateDate', 'UpdateTime', name='HKOdds_RaceidHorseNoUpdateDateTime_uidx')

    # 1:M race:HKodds
    race = relationship("HKRace", backref=backref("odds", order_by=(Updatedate, Updatetime)))


def get_engine():
    return create_engine(URL(**settings.DATABASE))
    # return DBDefer(URL(**settings.DATABASE))

def create_schema(engine):
    ModelBase.metadata.create_all(engine)

