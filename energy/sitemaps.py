from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from myapp.models import BlogPost  # Replace with your model


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

# class BlogSitemap(Sitemap):
#     priority = 0.8
#     changefreq = "daily"
#
#     def items(self):
#         return BlogPost.objects.all()
#
#     def lastmod(self, obj):
#         return obj.updated_at  # Ensure your model has an `updated_at` field
