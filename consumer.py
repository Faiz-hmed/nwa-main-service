from asyncore import read
from datetime import datetime
from venv import create
import pika
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nwa_api.settings')
import django
django.setup()
from app import models

connection = pika.BlockingConnection(pika.ConnectionParameters('mq'))
channel = connection.channel()

def query_db(kwargs):
    ath_obs = []
    c_obs = []
    article = None 
    created = None
    
    time_written = kwargs.get("TimeWritten", None)

    if type (kwargs["Author"])== str:
        kwargs["Author"] = list(kwargs["Author"])
    print("kwargs...",kwargs)
    return
    for a in kwargs["Author"]:
        ath_obs.append( models.Author.objects.get_or_create(name=a, publication=kwargs["Publication"])[0] )

    if "Category" in kwargs:
        for c in kwargs["Category"]:
            c_obs.append( models.Category.objects.get_or_create(cat_name=c)[0] )
    
    if time_written is not None:
        time_written = datetime.fromtimestamp(time_written/1000.0)
        article,created = models.Article.objects.get_or_create(title = kwargs["Title"], time_written = time_written, 
                                            article_file = kwargs["ContentFileName"], article_link = kwargs["Link"], reading_time=kwargs["Reading_time"])    #THREAT: Empty foreign key values
    else:
        article,created = models.Article.objects.get_or_create(title = kwargs["Title"], article_file = kwargs["ContentFileName"], 
                                            article_link = kwargs["Link"], reading_time=kwargs["Reading_time"])
    if created: print("Article created!")

    article.category.add(*c_obs)
    article.author.add(*ath_obs)

    if "Images" in kwargs:
        if isinstance(kwargs["Images"], str):
            kwargs["Images"] = list(kwargs["Images"])

        for i in kwargs["Images"]:
            if i is not None:
                article.images.create(image = i)



def callback(ch, methods, properties, body):
    data = json.loads(body)
    
    d_k = list(data.keys())
    for k in d_k:
        if(d_k.index(k) == 0):
            print("Messages being recieved & queried to database,\n {}: \t{}".format(k, data[k]))
        else:
            print("{}\t: {}".format(k,data[k]))
    
    query_db(data)

channel.basic_consume(queue='Articles', on_message_callback = callback, auto_ack=True)

try:
    channel.start_consuming()
except Exception as e:
    print(e)
    channel.stop_consuming()
    connection.close()