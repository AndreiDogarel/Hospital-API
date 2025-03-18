from django.shortcuts import render
from rest_framework import viewsets, permissions
from core.models import User, Doctor, Patient, Assistant, Treatment
from core.serializers import DoctorSerializer, PatientSerializer, AssistantSerializer, TreatmentSerializer, UserSerializer
from django.http import JsonResponse
from core.permissions import IsGeneralManager, IsDoctor, IsAssistant
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsGeneralManager]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsDoctor | IsGeneralManager]

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]

    @action(detail=True, methods=["post"])
    def assign_patient(self, request, pk=None):
        """ Assigns a Pacient to an Assistant """
        assistant = self.get_object()
        patient_id = request.data.get("patient_id")

        if not patient_id:
            return Response({"error": "patient_id is required"}, status=400)

        patient = get_object_or_404(Patient, id=patient_id)
        assistant.assigned_patients.add(patient)
        return Response({"message": f"Patient {patient.name} assigned to Assistant {assistant.user.username}"})

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    def get_permissions(self):
        if self.action == "create":  
            return [IsDoctor()] if isinstance(IsDoctor, type) else [IsDoctor(), IsGeneralManager()]
        
        if self.action == "apply_treatment":
            return [IsAssistant()] if isinstance(IsAssistant, type) else [IsAssistant()]
        
        return [permissions.IsAuthenticated()]

    
    @action(detail=True, methods=["patch"], url_path="apply-treatment")
    def apply_treatment(self, request, pk=None):
        treatment = self.get_object()
        if not IsAssistant().has_permission(request, self):  
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        treatment = self.get_object()
        treatment.status = "Completed"
        treatment.save()
        return Response({"message": "Treatment applied successfully!"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


def home(request):
    return JsonResponse({"message": "Hospital API is running!"})