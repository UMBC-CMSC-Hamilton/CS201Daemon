from django.db import models


class Assignment(models.Model):
    pass


class Problem(models.Model):
    pass


class GradeBook(models.Model):
    pass


class Ticket(models.Model):
    id = models.CharField(max_length=31, primary_key=True)
    user = models.CharField(max_length=255)
    status = models.IntegerField()
    description = models.TextField()
    creation_date = models.DateTimeField()
    response = models.TextField()
    type = models.CharField(max_length=127)

    def __str__(self):
        return self.id
