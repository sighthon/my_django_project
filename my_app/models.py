from django.db import models
import datetime

# Representation of a Person Table in Django
# create a person table with 2 columns - name and age

# shell commands
# from my_app.models import Person, Contact, Family, Relationship

class Person(models.Model):
    class Meta:
        db_table = "my_app_person"
        ordering = ['age']

    subject_choices = [
        ('EN', 'ENGLISH'),
        ('HN', 'HINDI'),
        ('MT', 'MATHS')
    ]

    # class variables
    name = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(null=True)
    address = models.TextField(max_length=200, default='')
    subject = models.CharField(choices=subject_choices, max_length=2, null=True)

    def __str__(self):
        return self.name + " " + str(self.age) + " " + str(self.subject)
    
    @property
    def name_age(self):
        return self.name + "_" + str(self.age)
    

class Student(Person):
    student_id = models.IntegerField(null=False)


class Contact(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True)

class Family(models.Model):
    people = models.ManyToManyField(Person, through="Relationship") # not a database field but only used for management
    name = models.CharField(max_length=20, unique=True)

class Relationship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    date_established = models.DateField(default=datetime.date.today)