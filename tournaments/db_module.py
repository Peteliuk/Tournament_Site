from tournaments import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(40), nullable = False)
	surname = db.Column(db.String(50), nullable = False)
	email = db.Column(db.String(100), unique = True, nullable = False)
	password = db.Column(db.String(30), nullable = False)
	admin = db.Column(db.Boolean, nullable = False, default = False)

class Tournaments(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, nullable = False)
	name = db.Column(db.String(100), nullable = False)
	description = db.Column(db.String(500), nullable = False)

class Teams(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, nullable = False)
	tournament_id = db.Column(db.Integer, nullable = False)
	name = db.Column(db.String(40), nullable = False)

class Matches(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	tournament_id = db.Column(db.Integer, nullable = False)
	team_home_id = db.Column(db.Integer, nullable = False)
	team_guest_id = db.Column(db.Integer, nullable = False)
	tour = db.Column(db.Integer, nullable = False)

class DbModule:
	def get_user_id(self, email):
		user = Users.query.filter_by(email = email).first()
		return user.id if user else None

	def add_user(self, *args):
		query = Users(name = args[0], surname = args[1], email = args[2], password = args[3])
		db.session.add(query)
		db.session.commit()

	def select_user_data(self, id):
		user_data = Users.query.filter_by(id = id).first()
		return user_data

	def select_user(self, *args):
		user = Users.query.filter_by(email = args[0], password = args[1]).first()
		return user

	def update_user(self, *args):
		user = Users.query.filter_by(id = args[0]).first()
		user.name = args[1]
		user.surname = args[2]
		user.email = args[3]
		user.password = args[4]
		db.session.commit()

	def delete_user(self, id):
		user = Users.query.filter_by(id = id).first()
		db.session.delete(user)
		db.session.commit()

	def get_tournament_id(self, *args):
		tournament = Tournaments.query.filter_by(user_id = args[0], name = args[1]).first()
		return tournament.id

	def add_tournament(self, *args):
		tournament = Tournaments(user_id = args[0], name = args[1], description = args[2])
		db.session.add(tournament)
		db.session.commit()

	def select_tournaments(self, id):
		tournaments = Tournaments.query.filter_by(user_id = id).all()
		return tournaments

	def select_tournament(self, id):
		tournament = Tournaments.query.filter_by(id = id).first()
		return tournament

	def select_all_tournaments_data(self):
		tournaments = db.session.query(Users, Tournaments).outerjoin(Tournaments, Users.id == Tournaments.user_id).all()
		return tournaments

	def update_tournament(self, *args):
		tournament = Tournaments.query.filter_by(id = args[0]).first()
		tournament.name = args[1]
		tournament.description = args[2]
		db.session.commit()

	def delete_tournament(self, id):
		tournament = Tournaments.query.filter_by(id = id).first()
		db.session.delete(tournament)
		db.session.commit()

	def add_team(self, *args):
		team = Teams(user_id = args[0], tournament_id = args[1], name = args[2])
		db.session.add(team)
		db.session.commit()

	def select_teams(self, *args):
		teams = Teams.query.filter_by(user_id = args[0], tournament_id = args[1]).all()
		return teams

	def select_all_users(self):
		users = Users.query.all()
		return users

	def select_all_tournaments(self):
		tournaments = Tournaments.query.all()
		return tournaments

	def make_admin(self, id):
		user = Users.query.filter_by(id = id).first()
		user.admin = True
		db.session.commit()

	def get_team_id(self, name):
		team = Teams.query.filter_by(name = name).first()
		return team.id if team else None

	def get_team_name(self, id):
		team = Teams.query.filter_by(id = id).first()
		return team.name
		
	def add_match(self, *args):
		match = Matches(tournament_id = args[0], team_home_id = args[1], team_guest_id = args[2], tour = args[3])
		db.session.add(match)
		db.session.commit()

	def select_matches(self, id):
		matches = Matches.query.filter_by(tournament_id = id).all()
		return matches