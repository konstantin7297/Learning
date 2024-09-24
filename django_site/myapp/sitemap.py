from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ProductSitemap(Sitemap):
    """ Sitemap помогает поисковикам понимать структуру и содержимое сайта. """
    changefreq = "never"  # Как часто меняется информация о продуктах. Варианты: always | hourly | daily | weekly | monthly | yearly | never # noqa
    priority = 0.5  # Возвращает приоритет для каждого объекта в sitemap. 1 - Самый важный объект. 0 - Самый неважный объект.

    def items(self):  # Возвращает queryset объектов, которые должны быть включены в sitemap. В данном случае последние 5 продуктов. # noqa
        return Product.objects.prefetch_related("orders", "images").filter(archived=False).order_by("-pk")[:5]  # noqa

    def lastmod(self, obj: Product):  # Возвращает дату последнего обновления для каждого объекта в sitemap. # noqa
        return obj.created_at  # Можно и другие поля выводить, например: 'obj.pk'.

    def item_link(self, obj: Product):  # Добавляет ссылку для деталей объектов. get_absolute_url прямо в модели таблицы заменит этот метод. # noqa
        return reverse("myapp:ProductDetailView", kwargs={"pk": obj.pk})
