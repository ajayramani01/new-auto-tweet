from django.db import models

# Create your models here.
class tweet_history(models.Model):
    tweet=models.CharField(max_length=280)  #as allowed by twitter
    tweet_img=models.ImageField(upload_to='tweet', null=True, blank=True)

    def __str__(self):
        return self.tweet[:50]