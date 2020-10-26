from django.db import models

# Create your models here.


class Employee(models.Model):
    firstName = models.CharField(max_length=40, blank=False, null=False)
    lastName = models.CharField(max_length=40, blank=False, null=False)
    employeeId = models.CharField(
        blank=False, unique=True, null=False, max_length=20
    )
    city = models.CharField(max_length=25, blank=False, null=False)


@property
def __str__(self):
    return self.employeeId