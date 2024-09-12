from myapp.sitemap import ProductSitemap  # noqa


sitemaps = {  # Нужно для хорошего индексирования страниц приложения в поисковиках.
    "myapp": ProductSitemap,
}
