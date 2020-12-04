from flask import Flask, render_template

from .models import DB, User, Tweet

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff App!'

    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('base.html', title='Users', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Database Refreshed!', users=[])

    # @app.route('/')
    # def index():
    #     return '<b>Index page</b>'

    # @app.route('/hello/')
    # @app.route('/hello/<name>')  # if we provide a name in the URL, it will change the name in the template
    # def hello(name=None):
    #     return render_template('hello.html', name=name)

    # @app.route('/hello')
    # def hello():
    #     return '<h1>Hello, World!</h1><br>Test string'
    
    return app