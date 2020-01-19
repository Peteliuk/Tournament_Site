from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import session
from flask import render_template
from tournaments.db_module import DbModule

db = DbModule()

class UserModule:
	def index(self):
		user = None
		tournaments = db.select_all_tournaments_data()
		select_teams = db.select_teams
		select_matches = db.select_matches
		get_team_name = db.get_team_name

		if 'email' in session:
			user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('index.html', user = user, tournaments = tournaments, select_teams = select_teams, select_matches = select_matches, get_team_name = get_team_name)

	def registration(self):
		if 'email' in session:
			return redirect(url_for('index'))
		if request.method == 'POST':
			name = request.form['name']
			surname = request.form['surname']
			email = request.form['email']
			password = request.form['password']
			confirm_password = request.form['confirm_password']

			if name and surname and email and password and confirm_password:
				if confirm_password == password:
					if db.get_user_id(email):
						flash('Email is already exist!')
						return redirect(url_for('registration'))
					else:
						db.add_user(name, surname, email, password)
						session['email'] = email
						user = db.select_user_data(db.get_user_id(email))
						flash(f"Congratulation {user.name} {user.surname}! You're registered! Have fun!")
						return redirect(url_for('user'))
				else:
					flash('Your password is not confirmed!')
					return redirect(url_for('registration'))
			else:
				flash("All inputs are required!")
				return redirect(url_for('registration'))
		return render_template('registration.html')

	def login(self):
		if 'email' in session:
			return redirect(url_for('index'))
		if request.method == 'POST':
			email = request.form['email']
			password = request.form['password']
			if email and password:
				if db.select_user(email, password):
					session['email'] = email
					user = db.select_user_data(db.get_user_id(email))
					flash(f"Hey {user.name} {user.surname}! You're logged! Have fun!")
					return redirect(url_for('user'))
				else:
					flash("Incorrect email or password")
					return redirect(url_for('login'))
			else:
				flash("All inputs are required!")
				return redirect(url_for('login'))
		return render_template('login.html')

	def user(self):
		user = db.select_user_data(db.get_user_id(session['email']))
		tournaments = db.select_tournaments(db.get_user_id(session['email']))
		select_teams = db.select_teams
		select_matches = db.select_matches
		get_team_name = db.get_team_name
		return render_template('user.html', user = user, tournaments = tournaments, select_teams = select_teams, select_matches = select_matches, get_team_name = get_team_name)

	def update(self):
		if request.method == 'POST':
			name = request.form['name']
			surname = request.form['surname']
			email = request.form['email']
			password = request.form['password']
			confirm_password = request.form['confirm_password']

			if name and surname and email and password and confirm_password:
				if confirm_password == password:
					db.update_user(db.get_user_id(session['email']), name, surname, email, password)
					session['email'] = email
					flash("You've update your data!")
					return redirect(url_for('update'))
				else:
					flash('Your password is not confirmed!')
					return redirect(url_for('update'))
			else:
				flash("All inputs are required!")
				return redirect(url_for('update'))
		user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('update.html', user = user)

	def logout(self):
		session.pop('email', None)
		return redirect(url_for('index'))

	def delete(self):
		db.delete_user(db.get_user_id(session['email']))
		session.pop('email', None)
		flash('Your account deleted!')
		return redirect(url_for('index'))

	def create_tournament(self):
		if request.method == 'POST':
			name = request.form['name']
			description = request.form['description']

			if name and description:
				db.add_tournament(db.get_user_id(session['email']), name, description)
				flash('Tournament has been created!')
				return redirect(url_for('user'))
			else:
				flash("All inputs are required!")
				return redirect(url_for('create_tournament'))
		user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('create_tournament.html', user = user)

	def delete_tournament(self, name):
		db.delete_tournament(db.get_tournament_id(db.get_user_id(session['email']), name))
		return redirect(url_for('user'))

	def add_team(self, *args):
		if request.method == 'POST':
			name = request.form['name']
			if name:
				if not db.get_team_id(name):
					db.add_team(args[0], args[1], name)
					flash('Team has been added')
					return redirect(url_for('user'))
				else:
					flash('Team name is exist')
					return redirect(url_for('add_team'))
			else:
				flash("All inputs are required!")
				return redirect(url_for('add_team'))
		user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('add_team.html', user = user)

	def edit_tournament(self, *args):
		if request.method == 'POST':
			name = request.form['name']
			description = request.form['description']

			if name and description:
				db.update_tournament(args[1], name, description)
				flash('Tournament updated!')
				return redirect(url_for('user'))
			else:
				flash("All inputs are required!")	
				return redirect(url_for('edit_tournament'))
		tournament = db.select_tournament(args[1])
		select_teams = db.select_teams
		select_matches = db.select_matches
		get_team_name = db.get_team_name
		user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('edit_tournament.html', user = user, args = args, tournament = tournament, select_teams = select_teams, select_matches = select_matches, get_team_name = get_team_name)

	def admin(self):
		user = db.select_user_data(db.get_user_id(session['email']))
		users = db.select_all_users()
		tournaments = db.select_all_tournaments()
		return render_template('admin.html', user = user, users = users, tournaments = tournaments)

	def make_admin(self, id):
		db.make_admin(id)
		return redirect(url_for('admin'))

	def delete_user_admin(self, id):
		db.delete_user(id)
		return redirect(url_for('admin'))

	def delete_tournament_admin(self, id):
		db.delete_tournament(id)
		return redirect(url_for('admin'))

	def add_match(self, *args):
		if request.method == 'POST':
			team_home = request.form['team_home']
			team_guest = request.form['team_guest']
			tour = request.form['tour']

			if team_home and team_guest and tour:
				if team_home == team_guest:
					flash('Team can not play with themself!')
					return redirect(url_for('add_match', user_id = args[0], tournament_id = args[1]))
				else:
					db.add_match(args[1], db.get_team_id(team_home), db.get_team_id(team_guest), tour)
					flash('Match added!')
					return redirect(url_for('edit_tournament', user_id = args[0], tournament_id = args[1]))
			else:
				flash("All inputs are required!")	
				return redirect(url_for('add_match', user_id = args[0], tournament_id = args[1]))
		select_teams = db.select_teams
		user = db.select_user_data(db.get_user_id(session['email']))
		return render_template('add_match.html', user = user, args = args, select_teams = select_teams)