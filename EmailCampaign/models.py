from django.db import models


# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email}-{self.first_name}"


class Campaign(models.Model):
    subject = models.CharField(max_length=255)
    preview_text = models.TextField()
    article_url = models.URLField()
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateTimeField()

    def __str__(self):
        return f"{self.subject}-{self.published_date}"
