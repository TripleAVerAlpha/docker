import hashlib
import os
from pathlib import Path
import pandas as pd
from loguru import logger
from flask import Flask, render_template, request, redirect, url_for
from .config import *

logger.add(LOG_FOLDER + "log.log")
logger.info("Наш запуск")

ANSWER = {
    "Успех": False,
    "Задача": "",
    "Сообщение": ""
}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/<task>")
def main(task: str):
    return render_template('index.html', task=task)

@app.route("/add_data", methods=['POST'])
def upload_file():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    answer = ANSWER.copy()
    answer['Задача'] = 'add_data'

    if 'file' not in request.files:
        answer['Сообщение'] = 'Нет файла'
        return answer
    file = request.files['file']

    if file.filename == '':
        answer['Сообщение'] = 'Файл не выбран'
        return answer
    
    if file and allowed_file(file.filename):
        filename = hashlib.md5(file.filename.encode()).hexdigest() 
        file.save(os.path.join(UPLOAD_FOLDER, filename + file.filename[file.filename.find('.'):]))
        answer['Сообщение'] = 'Файл успешно загружен!'
        answer['Успех'] = True
        answer['Путь'] = filename
        return answer
    else:
        answer['Сообщение'] = 'Файл не загружен'
        return answer
        
@app.route("/show_data", methods=['GET'])
def show_file():
    answer = ANSWER.copy()
    answer['Задача'] = 'show_file'

    if 'path' not in request.args:
        answer['Сообщение'] = 'Не указан путь файла'
        return answer
    
    file = request.args.get('path') 
    
    if 'type' not in request.args:
        answer['Сообщение'] = 'Не указан тип файла'
        return answer
    
    type = request.args.get('type')

    file_path = os.path.join(UPLOAD_FOLDER, file + '.' + type)

    if not os.path.exists(file_path):
        answer['Сообщение'] = 'Файл не существует'
        return answer

    answer['Сообщение'] = 'Файл успешно загружен!'
    answer['Успех'] = True
    
    if type == 'csv':
        answer['Данные'] = pd.read_csv(file_path).to_dict()
        return answer
    else:
        answer['Данные'] = 'Не поддерживаемы тип'
        return answer
    
