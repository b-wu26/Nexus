from flask import Flask, request

app = Flask(__name__)

@api.route('/feed/<user_id>')
def feed(user_id):
    pass

@api.route('/post/<post_id>')
def show_post(post_id):
    pass

@api.route('/upload')
def upload():
    pass

@api.route('/settings/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def settings(user_id):
    if request.method == 'GET':

    if request.method == 'POST':

    if request.method == 'DELETE':