from tournaments import app
from tournaments.user_module import UserModule

um = UserModule()

@app.route('/')
def index():
	return um.index()

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
	return um.registration()

@app.route('/login', methods = ['POST', 'GET'])
def login():
	return um.login()

@app.route('/user')
def user():
	return um.user()

@app.route('/logout')
def logout():
	return um.logout()

@app.route('/update', methods = ['POST', 'GET'])
def update():
	return um.update()

@app.route('/delete')
def delete():
	return um.delete()

@app.route('/create_tournament', methods = ['POST', 'GET'])
def create_tournament():
	return um.create_tournament()

@app.route('/delete_tournament?<name>')
def delete_tournament(name):
	return um.delete_tournament(name)

@app.route('/add_team?<user_id>?<tournament_id>', methods = ['POST', 'GET'])
def add_team(user_id, tournament_id):
	return um.add_team(user_id, tournament_id)

@app.route('/edit_tournament?<user_id>?<tournament_id>', methods = ['POST', 'GET'])
def edit_tournament(user_id, tournament_id):
	return um.edit_tournament(user_id, tournament_id)

@app.route('/admin')
def admin():
	return um.admin()

@app.route('/make_admin?<user_id>')
def make_admin(user_id):
	return um.make_admin(user_id)

@app.route('/delete_user_admin?<user_id>')
def delete_user_admin(user_id):
	return um.delete_user_admin(user_id)

@app.route('/delete_tournament_admin?<tournament_id>')
def delete_tournament_admin(tournament_id):
	return um.delete_tournament_admin(tournament_id)

@app.route('/add_match?<user_id>?<tournament_id>', methods = ['POST', 'GET'])
def add_match(user_id, tournament_id):
	return um.add_match(user_id, tournament_id)