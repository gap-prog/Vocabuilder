import requests
import textblob
from flask import Flask, render_template, request

app = Flask(__name__)
words = {}


def get_word(word):
    res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()
    data = {}
    if 'title' not in res:
        res = res[0]
        meanings = {}
        for i in res['meanings']:
            meanings[i['partOfSpeech']] = {
                'definition': i['definitions'][0]['definition'] if 'definition' in i['definitions'][0] else None,
                'example': i['definitions'][0]['example'] if 'example' in i['definitions'][0] else None,
            }
        audio = None
        if len(res['phonetics']) > 0:
            if 'audio' in res['phonetics'][0]:
                audio = res['phonetics'][0]['audio']
        data = {
            'word': res['word'],
            'phonetic': res['phonetic'] if 'phonetic' in res else None,
            'audio': audio,
            'meanings': meanings,
            'sentiment': round(textblob.TextBlob(res['word']).sentiment.polarity, 1),
            'error': None,
        }
    else:
        data['error'] = f'No word {word} found.'
    return data


@app.route('/', methods=['GET', 'POST'])
def home():
    data = None
    if request.method == 'POST':
        word = request.form['word']
        if len(word) > 1:
            data = get_word(word)
        else:
            random_word = requests.get('https://random-word-api.herokuapp.com/word').json()[0]
            data = get_word(random_word)
            while data['error']:
                random_word = requests.get('https://random-word-api.herokuapp.com/word').json()[0]
                data = get_word(random_word)
        words[data['word']] = data['meanings']
    return render_template('index.html', data=data, words=words)


if __name__ == '__main__':
    app.run()
