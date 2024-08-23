import json
from flask import Flask, render_template, session, redirect, url_for
from auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from blueprint_basket.route import blueprint_basket

app = Flask(__name__)
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_basket, url_prefix='/basket')

app.config['db_config'] = json.load(open('data_files/db_config.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['report_url'] = json.load(open('data_files/report_url.json'))
app.config['report_list'] = json.load(open('data_files/report_list.json', encoding='UTF-8'))

app.secret_key = "Secret access"

@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group') is None:
            return render_template('external_user_menu.html')
        else:
            return render_template('internal_user_menu.html')
    else:
       return render_template('index.html')

@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.pop('user_id')
    if 'user_group' in session:
        session.pop('user_group')
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5030, debug=True)

