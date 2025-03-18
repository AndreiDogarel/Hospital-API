from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# User roles
class Role(models.TextChoices):
    GENERAL_MANAGER = "GM", "General Manager"
    DOCTOR = "DR", "Doctor"
    ASSISTANT = "AS", "Assistant"


class User(AbstractUser):
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.DOCTOR
    )


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name()
    

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return self.name
    

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_patients = models.ManyToManyField(Patient, related_name="assistants")

    def __str__(self):
        return self.user.get_full_name()
    

class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField()
    date_prescribed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        default="Pending"
    )

    def __str__(self):
        return f"Treatment for {self.patient.name} by {self.doctor.user.get_full_name()}"