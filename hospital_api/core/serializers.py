from rest_framework import serializers
from .models import User, Doctor, Patient, Assistant, Treatment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role", "DR")
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.save()
        return user

    

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Doctor
        fields = ["id", "user", "specialty"]



class PatientSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Patient
        fields = ["id", "name", "age", "doctor"]


class AssistantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_patients = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), many=True, required=False
    )

    class Meta:
        model = Assistant
        fields = ["id", "user", "assigned_patients"]


class TreatmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Treatment
        fields = ["id", "patient", "doctor", "description", "date_prescribed", "status"]
