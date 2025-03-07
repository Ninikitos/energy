# from django.db import models
#
#
# class Comment(models.Model):
#     name = models.CharField(max_length=18, blank=True, null=True)
#     comment = models.TextField(max_length=256, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.comment[:50]} {self.created_at}"
