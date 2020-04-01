from flask_login import UserMixin
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(64), index=True, unique=True)
    # profile_id = db.Column(db.Integer, ForeignKey('profile.id'))
    profile = db.relationship('Profile', back_populates='user', cascade='all,delete', uselist=False)
    fantasy_team = db.relationship('FantasyTeam', back_populates='user', cascade='all,delete', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return '<Profile {}>'.format(self.user_id, self.first_name, self.last_name)


# FANTASYTEAM and PLAYER relationship Many to Many
fantasy_teams_players = db.Table('association',
                                db.Column('fantasy_team_id', db.Integer, ForeignKey('fantasy_team.id')),
                                db.Column('player_id', db.Integer, ForeignKey('player.id'))
                                )


class FantasyTeam(db.Model):
    __tablename__ = 'fantasy_team'
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship("Player",
                              secondary=fantasy_teams_players,
                              back_populates="fantasy_teams")

    name = db.Column(db.String(255))

    # USER relationship 1 to 1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='fantasy_team')

    overall_score = db.Column(db.Integer)
    # ROUNDSCORE relationship (1) to Many
    round_scores = db.relationship('RoundScore', back_populates='fantasy_team', cascade='all,delete', uselist=False)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<FantasyTeam {}>'.format(self.user_id, self.name)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fantasy_teams = db.relationship("FantasyTeam",
                                   secondary=fantasy_teams_players,
                                   back_populates="players")

    # GOAL relationship (1) to Many
    goals = db.relationship("Goal", back_populates="player")

    # TEAM relationship 1 to (Many)
    team_id = db.Column(db.Integer, ForeignKey('team.id'))
    team = db.relationship("Team", back_populates="players")

    number = db.Column(db.Integer)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    nickname = db.Column(db.String(255))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Player {}>'.format(self.fantasy_team_id)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # PLAYER relationship 1 to (Many)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player = db.relationship("Player", back_populates="goals")

    # MATCH relationship 1 to (Many)
    match_id = db.Column(db.Integer, ForeignKey('match.id'))
    match = db.relationship("Match", back_populates="goals")

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Goal {}>'.format(self.fantasy_team_id)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)

    # GOAL relationship (1) to Many
    goals = db.relationship("Goal", back_populates="match")

    # TEAM relationship (1) to Many
    # TEAM relationship (1) to Many
    team1_id = db.Column(db.Integer, ForeignKey("team.id"))
    team2_id = db.Column(db.Integer, ForeignKey("team.id"))

    team1 = db.relationship("Team", foreign_keys=[team1_id])
    team2 = db.relationship("Team", foreign_keys=[team2_id], back_populates="matches")

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Match {}>'.format(self.id)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # PLAYER relationship (1) to Many
    players = db.relationship("Player", back_populates="team")

    # MATCH relationship 1 to (Many)
    matches1 = db.relationship("Match", back_populates="team1")
    matches2 = db.relationship("Match", back_populates="team2")

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Team {}>'.format(self.user_id, self.name)


class RoundScore(db.Model):
    __tablename__ = 'round_score'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(255))
    round_score = db.Column(db.Integer)

    # FANTASYTEAM relationship 1 to (Many)
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fantasy_team = db.relationship('FantasyTeam', back_populates='round_scores')

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<RoundScore {}>'.format(self.fantasy_team_id)
