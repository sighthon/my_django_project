from django.db import models

# Representation of a Person Table in Django
# create a person table with 2 columns - name and age


class Person(models.Model):
    # class variables
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.TextField(max_length=200, default='')

    def __str__(self):
        return self.name + " " + str(self.age) + " " + self.address
