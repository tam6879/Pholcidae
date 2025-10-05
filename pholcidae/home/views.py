from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import markovify as mark
import random as rngesus
import string
from os import listdir, getcwd
from os.path import isfile, join
from time import sleep
import sqlite3
import pickle
from home.models import CachedPage
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch

SENTENCES_PER_BLURB = 16

ID_LENGTH = 20

MIN_WAIT_TIME = 1.0
MAX_WAIT_TIME = 3.0

NEW_PAGE_LINKS = 4

corpus_path = "corpus.txt"
generated_corpus = False

def generate_model(file_name: str) -> None:
        with open(corpus_path, "r")as t_file:
            corpus_text = t_file.read()
        return mark.Text(corpus_text)

def generate_image(prompt: str, id: str) -> str:
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.to("cuda").manual_seed(0) 
    t_scheduler = EulerDiscreteScheduler(beta_start=0.00085, beta_end=0.012,beta_schedule="scaled_linear")
    t_image = pipe("Create an image illustrating this exerpt of text: " + prompt, scheduler = t_scheduler, num_inference_steps=10, guidance_scale =3.0,).images[0]
    image.save("test.png")

def generate_blurb(t_model) -> str:
    text = "\t"
    for i in range(SENTENCES_PER_BLURB):
        t_text = t_model.make_sentence()
        while not t_text:
            t_text = t_model.make_sentence()
        text += (" " + t_text)
    return text

def generate_id() -> str:
    chars = string.ascii_letters + string.digits
    return "".join(rngesus.choice(chars) for i in range(ID_LENGTH))


### VIEWS ###

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def more_information(request, id):
    
    template = loader.get_template('more_information.html')
    sleep(rngesus.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME))
    if CachedPage.objects.filter(id=id):
        print("SEEN THIS ID")
        t_page = CachedPage.objects.get(id=id)
        context = {"text": t_page.text, 
        "link1": t_page.link1,
        "link2": t_page.link2,
        "link3": t_page.link3,
        "link4": t_page.link4,
        "image": t_page.image}
        return HttpResponse(template.render(context, request))
        
    else:
        print("UNIQUE ID")

    text_model = generate_model(corpus_path)
    t_text = generate_blurb(text_model)
    # generate_image(t_text, id)
    context = {"text": t_text}

    t_url = request.get_full_path()[:-20]

    for i in range(1, NEW_PAGE_LINKS + 1):
        context["link" + str(i)] = t_url + generate_id()
        print(context["link" + str(i)])
    context["image"] = str(rngesus.choice(list(range(7)))) + ".png"
    print("image url: ", context["image"])

    t_page = CachedPage.objects.create(id = id, text = t_text, time = timezone.now(), link1 = context["link1"], link2 = context["link2"], link3 = context["link3"], link4 = context["link4"], image = context["image"])
    t_page.save()

    return HttpResponse(template.render(context, request))

