from django.shortcuts import render
from rest_framework import viewsets, permissions
from core.models import User, Doctor, Patient, Assistant, Treatment
from core.serializers import DoctorSerializer, PatientSerializer, AssistantSerializer, TreatmentSerializer, UserSerializer
from django.http import JsonResponse
from core.permissions import IsGeneralManager, IsDoctor, IsAssistant
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
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
    
    def get_permissions(self):
        if self.action == "assign_patient":
            if IsGeneralManager().has_permission(self.request, self):
                return [IsGeneralManager()]
            elif IsDoctor().has_permission(self.request, self):
                return [IsDoctor()]

        return [IsGeneralManager()]


    @action(detail=True, methods=["post"])
    def assign_patient(self, request, pk=None):
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
        if self.action == "apply_treatment":
            return [IsAssistant()]
        if self.action == "create":
            return [IsDoctor()]
        
        if self.request.user.is_authenticated:
            if IsGeneralManager().has_permission(self.request, self):
                return [IsGeneralManager()]
            elif IsDoctor().has_permission(self.request, self):
                return [IsDoctor()]

        return [IsGeneralManager()]
    
    @action(detail=True, methods=["patch"], url_path="apply-treatment")
    def apply_treatment(self, request, pk=None):
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


@api_view(["GET"])
@permission_classes([IsGeneralManager | IsDoctor])
def patient_treatments_report(request, patient_id):
    treatments = Treatment.objects.filter(patient_id=patient_id).values(
        "id", "description", "doctor", "status", "date_prescribed"
    )

    if not treatments.exists():
        return Response({"error": "No treatments found for this patient"}, status=404)

    return Response({"patient_id": patient_id, "treatments": list(treatments)})


@api_view(["GET"])
@permission_classes([IsGeneralManager])
def doctors_report(request):
    doctors = Doctor.objects.prefetch_related("patients").all()
    total_doctors = doctors.count()
    total_patients = Patient.objects.count()
    
    data = []
    for doctor in doctors:
        patients = doctor.patients.values("id", "name", "age")
        data.append({
            "doctor": doctor.user.get_full_name() or doctor.user.username,
            "specialty": doctor.specialty,
            "patients": list(patients),
            "total_patients": len(patients)
        })

    return Response({
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "doctors": data
    })