from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Doctor, Patient, Assistant, Treatment
from .serializers import DoctorSerializer, PatientSerializer, AssistantSerializer, TreatmentSerializer
from django.http import JsonResponse
from .permissions import IsGeneralManager, IsDoctor, IsAssistant

# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [permissions.IsAuthenticated]

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]


def home(request):
    return JsonResponse({"message": "Hospital API is running!"})