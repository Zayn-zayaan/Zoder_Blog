from django.db import models

# Create your models here.
class Contact(models.Model):
    Sno      = models.AutoField(primary_key=True)
    name     = models.CharField(max_length=60)
    phone    = models.CharField(max_length=13)
    email    = models.EmailField(max_length=100)
    date     = models.DateTimeField(auto_now_add=True, blank=False)
    content  = models.TextField(max_length=1000)

    def __str__(self):
        return "Msg from-" + self.name + "-" + self.email
