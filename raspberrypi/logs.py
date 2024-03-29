from time import localtime, strftime
import os
import json


def generate_log(user):
    time = strftime("%d/%m/%Y %H:%M:%S", localtime())
    log = json.dumps({'data': time, 'usuario': user})
    return(log)


def save_log(log):
    with open("logs.txt", "a") as f:
        f.write(log+'\n')
