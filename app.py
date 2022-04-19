#!/usr/bin/python3

# TODO
# Аргументы из локальной строки
# Поднять веб-сервер и обрабатывать загрузку файлов и выдачу файла в ответ
# Сделать RESTapi для внешних приложений на сайте


import io
import os

from flask import Flask, flash, g, render_template, request, redirect, url_for, send_file
# from werkzeug.utils import secure_filename
from utils import secure_filename


import watermark


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
FONT_FILE = "FiraCode-Light.ttf"
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024    # Ограничение на загрузку 4Mb
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # TODO
            # Почему подготовка имени файла идёт после проверки на допустимые файлы?
            # Не может ли быть такого случая, когда имя файла после подготовки станет недопустимым?
            filename = secure_filename(file.filename)
            print('file', file, 'filename', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            start_x = int(request.form['start_x']
                          ) if request.form['start_x'] else 50
            start_y = int(request.form['start_y']
                          ) if request.form['start_y'] else 50
            start_position = (start_x, start_y)
            shift_step_x = int(request.form['shift_step_x']
                          ) if request.form['shift_step_x'] else 500
            shift_step_y = int(request.form['shift_step_y']
                          ) if request.form['shift_step_y'] else 300
            shift_step = (shift_step_x, shift_step_y)
            fill_text = (request.form['fill'] == 'optionAll')
            font_ratio = int(request.form['font_ratio'])
            watermark_text = request.form['watermark'] if request.form['watermark'] else 'Водяной знак'
            watermark_file = watermark.watermark_text(
                filename,
                watermark_text,
                startpos=start_position,
                shift_step=shift_step,
                font_ratio=font_ratio,
                fill_text=fill_text,
            )
            return redirect(url_for('get_image', filename=watermark_file))
            # return redirect(url_for('upload_file'))
    return render_template('index.html')


@app.route('/get_image/<filename>')
def get_image(filename):
    if filename:
        # загружаем файл в оперативную память, чтобы не хранить его на диске
        # возможно стоит целиком работать в оперативной памяти
        return_data = io.BytesIO()
        with open(filename, 'rb') as fo:
            return_data.write(fo.read())
        # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)
        # удаляем файл с диска
        os.remove(filename)

        return send_file(return_data, as_attachment=True, attachment_filename=filename)
    return redirect(url_for('upload_file'))


if __name__ == '__main__':

    if not os.path.exists(FONT_FILE):
        print(FONT_FILE, 'not found')

    app.run()
