from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    upload = FileField('Выберите файл:', validators=[
                        FileRequired(),
                        FileAllowed(['jpg', 'png'], 'Только изображения!')
                        ])
    watermarString = StringField('Введите текст для водяного знака', validators=[Required()])
    submit = SubmitField('Обработать')
