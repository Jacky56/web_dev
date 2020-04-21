from django.db import models

# model map to database table

# Create your models here.

# creates a table in database with these fields
class new_table(models.Model):
    # column named title
    title = models.CharField(max_length=200)
    # column named content
    content = models.TextField(default="you can set default value")
    # columned named published
    published = models.DateTimeField("date name ?")

    #? replace return type with a readable string
    def __str__(self):
        return self.title
