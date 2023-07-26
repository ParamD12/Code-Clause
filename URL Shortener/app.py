from flask import Flask, render_template, request, redirect
import pyshorteners
import random

app = Flask(__name__)
url_mapping = {}


def generate_short_url():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


def is_valid_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return True
    return False


@app.route('/')
def home():
    return render_template('index.html', error=False)


@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']

    if not is_valid_url(original_url):
        return render_template('index.html', error=True)

    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(original_url)
    url_mapping[short_url] = original_url

    return render_template('index.html', error=False, short_url=short_url)


@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    if short_url in url_mapping:
        return redirect(url_mapping[short_url])
    else:
        return 'Invalid URL'


if __name__ == '__main__':
    app.run(debug=True)
