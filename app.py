from flask import Flask, url_for, g, session, Blueprint, request, redirect, render_template, flash
import requests
import os
import functools
import json
import rps

'''
App factory
Exception handling
Module off WSClient
Module off game
'''

app = Flask(__name__, instance_relative_config=True, template_folder='web/templates', static_folder='web/static')
app.config.from_mapping(
    SECRET_KEY='dev',
    SERVICE='service1',
    SERVICE_HOST='34.42.125.145:8080'
)
bp = Blueprint('/', __name__, url_prefix='/')

with app.app_context():
    
    '''
    WSC client
    '''

    @bp.before_app_request
    def load_logged_in_user():
        '''Takes none. Gives none.'''
        token = session.get('session')
        if token is None:
            g.token = None
        else:
            g.token = session

    app.register_blueprint(bp)

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            '''Takes view. Returns view or res dict.'''
            if g.token is None:
                error = "Login is required"
                res = {
                    "code": -1,
                    "body" : error
                }
                return redirect(f"http://{app.config['SERVICE_HOST']}", code=302)
            
            return view(**kwargs)
        
        return wrapped_view

    @app.route('/login', methods=['POST'])
    def login():
        # logout()
        username = request.form['username']
        password = request.form['password']
        if request.form['login'] == 'login':

            response = requests.post(f'http://{app.config["SERVICE_HOST"]}/api/login', json={
                "service": app.config['SERVICE'],
                "username": username,
                "password": password
            })
            
            if response.json()['code'] == 0:
                session.update(response.cookies)
                session['username'] = response.json()['body']['username']
            elif response.json()['code'] == -1:
                flash(f"Failed: {response.json()['body']}")
                print(response.json)

        elif request.form['login'] == 'reg':
            response = requests.post(f'http://{app.config["SERVICE_HOST"]}/api/register', json={
                "service": app.config['SERVICE'],
                "username": username,
                "password": password
            })
            data = response.json()
            if data['code'] == 0:
                flash('Registered')
            elif data['code'] == -1:
                flash(f'Failed {data["body"]}')

        elif request.form['login'] == 'logout':
            return redirect(url_for('logout'))

        return redirect(url_for('index'))
    
    @app.route('/update', methods=['POST'])
    def update():
        input1 = request.form['input1']
        input2 = request.form['input2']
        if request.form['update'] == 'name':
            response = requests.post(f'http://{app.config["SERVICE_HOST"]}/api/update/username', json={
                
            })
    
    @app.route('/logout')
    @login_required
    def logout():
        # response = requests.get(f"http://{app.config['SERVICE_HOST']}/api/logout", cookies=g.token)
        session.clear()
        return redirect(url_for('index'))
    
    
    '''
    App routes
    '''

    @app.route('/')
    def index():
        game = session.get('game')
        if session.get('username') and game is None:
            session['game'] = {
                "character": None,
                "hp": None,
                "dmg": None,
                "dragon_hp": rps.dragon_hp,
                "dragon_dmg": rps.dragon_dmg,
                "turn": "dragon"
            }
        else:
            session['game'] = game
        print(g.token)
        print(type(g.token))
        # response = requests.get(f"http://{app.config['SERVICE_HOST']}/api/home", cookies=g.token)
        data = session
        game = session['game']
        return render_template('base.html', data=data)
    
    @app.route('/char_select', methods=['POST'])
    @login_required
    def char_select():
        char = request.form['char']
        print(char)
        if char == "wizard":
            session['game']['character'] = rps.wizard
            session['game']['hp'] = rps.wizard_hp
            session['game']['dmg'] = rps.wizard_dmg
        elif char == "human":
            session['game']['character'] = rps.human
            session['game']['hp'] = rps.human_hp
            session['game']['dmg'] = rps.human_dmg
        elif char == "elf":
            session['game']['character'] = rps.elf
            session['game']['hp'] = rps.elf_hp
            session['game']['dmg'] = rps.elf_dmg
        elif char == "orc":
            session['game']['character'] = rps.orc
            session['game']['hp'] = rps.orc_hp
            session['game']['dmg'] = rps.orc_dmg
        session.modified = True

        return redirect(url_for('index'))
    
    @app.route('/play', methods=['POST'])
    @login_required
    def play():
        turn = session['game']['turn']
        
        result = rps.play(request.form['hand'])
        if turn == 'dragon' and result == 'win':
            flash("You remain unscathed!")
            session['game']['turn'] = "player"
        elif turn == 'dragon' and result == 'lose':
            session['game']['hp'] = session['game']['hp'] - session['game']['dragon_dmg']
            flash("The dragon damaged you!")
            session['game']['turn'] = "player"
        elif turn == 'dragon' and result == 'draw':
            flash(f"You are unscathed, but the {turn} attacks again")

        if turn == 'player' and result == 'win':
            session['game']['dragon_hp'] = session['game']['dragon_hp'] - session['game']['dmg']
            flash("You have damaged the dragon!")
            session['game']['turn'] = "dragon"
        if turn == 'player' and result == 'lose':
            flash("The dragon evaded your attack")
            session['game']['turn'] = "dragon"
        if turn == 'player' and result == 'draw':
            flash("You missed, but attack again!")

        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)