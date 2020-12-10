# Package Imports
from os import getenv
# from decouple import config
from flask import Flask, render_template, request

# Local Imports
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users


# Add config vars on command line with `heroku config:set KEY='VALUE'`


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
	DB.init_app(app)

	@app.route('/')
	def root():
		users = User.query.all()
		return render_template('base.html', title='Home', users=users)

	@app.route('/user', methods=['POST'])
	@app.route('/user/<name>', methods=['GET'])
	def user(name=None, message=''):
		name = name or request.values['user_name']
		try:
			if request.method == "POST":
				add_or_update_user(name)
				message = f'User {name} successfully added/updated!'
			tweets = User.query.filter(User.name == name).one().tweets
		except Exception as e:
			message = f'Error adding user {name}: {str(e)}'
			tweets = []
		return render_template('user.html', title=name, tweets=tweets, message=message)

	@app.route('/predict', methods=['POST'])
	def predict(message=''):
		user1, user2 = sorted([request.values['user1'],
							   request.values['user2']])
		if user1 == user2:
			message = 'Cannot compare a user to themself!'
		else:
			tweet_text = request.values['tweet_text']
			prediction = predict_user(user1, user2, tweet_text)
			message = '"{}" is more likely to be said by {} than {}'.format(
				tweet_text,
				user1 if prediction else user2,
				user2 if prediction else user1
			)
		return render_template('prediction.html', title='Prediction',
							    message=message)

	@app.route('/reset')
	def reset():
		DB.drop_all()
		DB.create_all()
		return render_template('base.html', title='Reset database!')

	@app.route('/update')
	def update():
		update_all_users()
		return render_template('base.html',
							   title='All Tweets Updated!',
							   users=User.query.all())


	return app