from flask import Flask, request, flash, url_for, render_template, redirect
from wtforms import Form, StringField, validators
from pymongo import MongoClient

from necrobot import app


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/add_subreddit', methods=['GET', 'POST'])
def add_subreddit():
    form = AddSubredditForm(request.form)
    if request.method == 'POST' and form.validate():
        email_address= form.email_address.data
        subreddit = 'https://reddit.com/r/{}/'.format(form.subreddit.data)
        key_word = form.key_word.data
        mongo_client = MongoClient()
        mongo_db = mongo_client.test
        mongo_collection = mongo_db.test_collection

        entry_count = mongo_collection.find({"email": email_address}).count()
        if entry_count == 0:
            mongo_collection.insert_one(
                {
                    "email": email_address,
                    "subreddits": [
                        subreddit
                    ],
                    "key_words": [
                        key_word
                    ]
                }
            )
            flash('Thanks for the submission!')
        elif entry_count < 5:
            mongo_collection.update_one(
                { "email": email_address },
                { "$push": { "subreddits":subreddit, "key_words":keyword } }
            )
            flash('Thanks for the submission!')
        else:
            flash('Only 5 submissions per email please.')

        mongo_client.close()

        return redirect(url_for('index'))

    return render_template('add_subreddit.html', form=form)


class AddSubredditForm(Form):
    email_address = StringField('Email Address', [
        validators.Email(message="Please enter a valid email address."),
        validators.DataRequired()
    ])
    subreddit = StringField('Subreddit', [
        validators.Length(max=20, message="Subreddits only have a max length of 20."),
        validators.DataRequired()
    ])
    key_word = StringField('Key Word', [
        validators.Length(max=120, message="Key words cannot be longer than a tweet."),
        validators.DataRequired()
    ])

