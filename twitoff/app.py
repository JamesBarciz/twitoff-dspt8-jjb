from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return '<b>Index page</b>'

    @app.route('/hello/')
    @app.route('/hello/<name>')  # if we provide a name in the URL, it will change the name in the template
    def hello(name=None):
        return render_template('hello.html', name=name)

    # @app.route('/hello')
    # def hello():
    #     return '<h1>Hello, World!</h1><br>Test string'
    
    return app