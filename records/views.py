# records/views.py (Part 1 - CRUD)
from rest_framework import viewsets, permissions, mixins, generics
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .permissions import IsCreatorOrReadOnly # Import the custom permission

# 1. Patient ViewSet: Handles POST, GET (List/Detail), PUT, DELETE for patients
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    # Requires login, and the creator permission for security
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly] 
    
    # Filters queryset to fulfill Requirement: "Retrieve all patients created by the authenticated user."
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

# 2. Doctor ViewSet: Handles POST, GET (List/Detail), PUT, DELETE for doctors
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    
    # Fulfills Requirement: "Retrieve all doctors." (No filter applied)
    def get_queryset(self):
        return Doctor.objects.all()
    

    # records/views.py (Part 2 - Mapping)

# 3. Mapping Create/Delete View: Handles POST /api/mappings/ and DELETE /api/mappings/<id>/
class PatientDoctorMappingCreateDestroy(mixins.CreateModelMixin,
                                        mixins.DestroyModelMixin,
                                        generics.GenericAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Handles assignment (POST)
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Handles removal (DELETE /api/mappings/<id>/)
        return self.destroy(request, *args, **kwargs)
    
    # Security check to ensure only the patient's creator can delete the assignment
    def perform_destroy(self, instance):
        if instance.patient.created_by != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this assignment.")
        instance.delete()

# 4. Mapping List View: Handles GET /api/mappings/list/ and GET /api/mappings/<patient_id>/doctors/
class PatientDoctorMappingList(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Start by filtering to only mappings involving the user's own patients
        queryset = PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)
        
        # Check if a patient_id is provided (for the /api/mappings/<patient_id>/doctors/ endpoint)
        patient_id = self.kwargs.get('patient_id')
        if patient_id is not None:
            # Add security check: Ensure the requested patient ID belongs to the current user
            if not Patient.objects.filter(id=patient_id, created_by=self.request.user).exists():
                raise permissions.PermissionDenied("Patient ID not found or does not belong to you.")
            
            # Filter the queryset for the specific patient
            queryset = queryset.filter(patient_id=patient_id)
            
        return queryset