from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import markovify as mark
import random as rngesus
import string
from os import getcwd
from os.path import isfile, join
from time import sleep
import sqlite3
from home.models import CachedPage

SENTENCES_PER_BLURB = 16

ID_LENGTH = 20

MIN_WAIT_TIME = 1.0
MAX_WAIT_TIME = 3.0

NEW_PAGE_LINKS = 4

TAR_PIT_ENTERANCE = "more_information/HdtMq3cW6jCxZsuWEz8C"

corpus_path = "corpus.txt"
generated_corpus = False

# Generates a markov chain model from a given corpus text
def generate_model(file_name: str) -> None:
        with open(corpus_path, "r")as t_file:
            corpus_text = t_file.read()
        return mark.Text(corpus_text)

# Randomly generates a paragraph of sentances with the markov model
def generate_blurb(t_model) -> str:
    text = "\t"
    for i in range(SENTENCES_PER_BLURB):
        t_text = t_model.make_sentence()
        while not t_text:
            t_text = t_model.make_sentence()
        text += (" " + t_text)
    return text

# Generates a random string of 20 characters to use as the page id
def generate_id() -> str:
    chars = string.ascii_letters + string.digits
    return "".join(rngesus.choice(chars) for i in range(ID_LENGTH))


### VIEWS ###

def home(request):
    template = loader.get_template('home.html')
    t_url = request.get_full_path()
    return HttpResponse(template.render({"more_info_url": t_url + TAR_PIT_ENTERANCE}))

def more_information(request, id):
    template = loader.get_template('more_information.html')
    # wait for a few seconds to keep traffic managable
    sleep(rngesus.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME))
    # check if the page was already cached, and if so load it
    if CachedPage.objects.filter(id=id):
        t_page = CachedPage.objects.get(id=id)
        context = {"text": t_page.text, "link1": t_page.link1, "link2": t_page.link2, "link3": t_page.link3, "link4": t_page.link4, "image": t_page.image}
        return HttpResponse(template.render(context, request))
    # otherwise, generate the markov text, choose an image, and make 4 new links
    text_model = generate_model(corpus_path)
    t_text = generate_blurb(text_model)
    context = {"text": t_text}
    t_url = request.get_full_path()[:-ID_LENGTH]
    for i in range(1, NEW_PAGE_LINKS + 1):
        context["link" + str(i)] = t_url + generate_id()
        print(context["link" + str(i)])
    context["image"] = str(rngesus.choice(list(range(7)))) + ".png"
    # now save the new page
    t_page = CachedPage.objects.create(id = id, text = t_text, time = timezone.now(), link1 = context["link1"], link2 = context["link2"], link3 = context["link3"], link4 = context["link4"], image = context["image"])
    t_page.save()
    # return the page
    return HttpResponse(template.render(context, request))

