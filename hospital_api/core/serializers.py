from rest_framework import serializers
from .models import User, Doctor, Patient, Assistant, Treatment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ["id", "user", "specialty"]


class PatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "name", "age", "doctor"]


class AssistantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    assigned_patients = PatientSerializer(many=True, read_only=True)

    class Meta:
        model = Assistant
        fields = ["id", "user", "assigned_patients"]


class TreatmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Treatment
        fields = ["id", "patient", "doctor", "description", "date_prescribed"]
