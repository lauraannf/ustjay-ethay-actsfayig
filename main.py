""" mashup gets fact and pig latinizes it"""
import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """gets the random fact"""

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def pig_fact(fact):
    """turns the fact into pig latin"""
    data = {'input_text': fact}
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                             data=data, allow_redirects=False)  # it's a 302, post, redirect
    return response.headers['location']  # url we want is in header

@app.route('/')
def home():
    fact = get_fact().strip()
    body = '<a href="{}">{}</a>'.format(pig_fact(fact), pig_fact(fact)) # link
    return Response(response=body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
