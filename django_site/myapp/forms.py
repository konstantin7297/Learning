from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Product


def custom_validator(file: InMemoryUploadedFile) -> None:
    """ Пример реализации custom валидации. Проверяется, есть ли в имени файла фрагмент 'virus'. Подключается: validators=[custom_validator] """
    if file.name and 'virus' in file.name:  # Валидатор должен ничего не возвращать, но если что-то не так - вызывать исключение. # noqa
        raise ValidationError("virus in filename")


class CSVImport(forms.Form):
    """ Класс для импорта данных из файла. Детали в файле: 'admin.py'. Позволяет загрузить файл .csv для загрузки данных в БД. """
    csv_file = forms.FileField()


class LoginForm(forms.Form):
    """ Класс для входа пользователя. """
    log_in = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


class ProductForm(forms.Form):  # Форма для продуктов из 'models.py' для отображения в браузере в HTML.
    """ Так пишутся формы в коде Django для отображения их на сайте в HTML. Так же тут пишется валидация этих форм. """
    name = forms.CharField(max_length=100)
    description = forms.CharField(
        label="description",  widget=forms.Textarea(attrs={"rows": 5, "cols": 2}), validators=[  # label - имя поля. widget - размеры поля.
            validators.RegexValidator(regex=r"have", message="error"),  # regex - строка модуля 're', которая должна быть в поле.
        ])
    price = forms.DecimalField(min_value=1, max_value=100000)
    discount = forms.IntegerField(min_value=0, max_value=100)
    preview = forms.ImageField(validators=[custom_validator])  # Позволяет загрузить изображение с уникальной валидацией в данном случае.
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": False}))  # Позволяет загружать сразу несколько картинок разом, если True.


class ProductModelForm(forms.ModelForm):  # ModelForm - строит форму на основе модели таблицы из файла 'models.py'.
    class Meta:
        model = Product  # Указываем, от какой модели наследуется эта форма.
        fields = "name", "description", "price", "discount", "preview"  # Указываем нужные поля.

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": False}))  # Позволяет загружать сразу несколько картинок разом, если True.
