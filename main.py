import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    fact = get_fact().strip()
    body = requests.post('http://hidden-journey-62459.herokuapp.com/piglatinize/', data = {'input_text': fact})
    location = body.history[0].headers['Location']
    new_body = body.content.decode('utf8').replace('</body>', '\t<br/>\n\t<br/>\n\t<a href="{}" target="_blank">Original Link</a>\n\n</body>'.format(location))
    return Response(response = new_body, mimetype = 'text/html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

