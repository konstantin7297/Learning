from typing import Dict

from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ Класс для сериализации данных для отправки через API на REST Framework. Он сериализует данные форматов: 'Python' <-> 'JSON' для отправок и загрузок. """  # noqa
    preview = serializers.SerializerMethodField(method_name="get_image")  # Загружает custom поле для отправки.

    class Meta:
        model = Product  # Нужная для обработки модель таблицы БД.
        fields = "pk", "name", "description", "price", "discount", "created_at", "archived", "preview", "images"  # Поля, которые будут обрабатываться для отправки.

    def get_image(self, obj: Product) -> Dict:  # Возвращает информацию о preview картинке в виде словаря. # noqa
        if obj.preview:
            return {"src": obj.preview.url, "alt": obj.preview.name}
        else:
            return {}
