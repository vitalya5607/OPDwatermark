class Image:
    '''Файл для наложения водяного знака'''

    def __init__(self, filename, filename_temp):
        self.filename = filename
        self.filename_temp = filename_temp if filename_temp else 'tmp' + filename

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        from os import remove
        remove(self.filename)
        remove(self.filename_temp)


class Font:

    def __init__(self, color='gray', size=10, font_file='FiraCode-Light.ttf'):
        self.font_file = font_file
        self.size = size
        self.color = color

    def __repr__(self):
        return f'Text({self.color!r}, {self.size!r}, {self.font_file!r})'


class Watermark:
    '''Водяной знак'''

    def __init__(
        self,
        image_path,
        text='watermark',
        color_text='gray',
        start_position=(50, 50),
        # шаг смещения наложения повторения
        shift_step=(50, 50),
        # возможно лишнее, тк есть font.size
        font_ratio=1,
        fill_text=True,
        # fontfile="FiraCode-Light.ttf"
        font=Font(),
    ):

        self.image_file = image_path
        self.text = text
        self.start_position = start_position
        # возможно лишнее, тк есть font.size
        self.font_ratio = font_ratio
        self.fill_text = fill_text
        self.font = font

        color_dict = {
            'black': (0, 0, 0),
            'gray': (128, 128, 128),
            'white': (255,  255, 255),
        }
        self.color = color_dict.get(color_text, 'gray')

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
