from django.db import models
from accounts.models import CustomUser

class BlogManager(models.Manager):
    def by_user(self, user):
        return self.get_queryset().filter(user=user)

    def search(self, keyword):
        return self.get_queryset().filter(title__icontains=keyword)


class Blog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on {self.blog.title}"
