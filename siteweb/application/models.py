from django.db import models

# Create your models here.

class Server(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Person(models.Model):
    server = models.ManyToManyField(Server)
    username = models.CharField(max_length=100)
    code = models.CharField(max_length=25)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

class Message(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, blank=True, null=True)
    date_published = models.DateTimeField('date creation')
    content = models.CharField(max_length=2000)

    class Meta:
        ordering = ['date_published']

    def __str__(self):
        start = self.content[0:10]
        return self.user.username + " - " + self.server.name + " - " + start + "..."