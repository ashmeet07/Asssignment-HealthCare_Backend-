# records/serializers.py
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping

# --- 1. Patient Serializer ---
class PatientSerializer(serializers.ModelSerializer):
    # Field to display the name of the user who created the record (Read-Only)
    created_by = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Patient
        fields = ('id', 'name', 'date_of_birth', 'address', 'phone_number', 'created_by')
        read_only_fields = ('id',) 

    # Automatically set the 'created_by' field when a patient is created
    def create(self, validated_data):
        # The authenticated user is available in the serializer's context
        validated_data['created_by'] = self.context['request'].user
        return Patient.objects.create(**validated_data)

# --- 2. Doctor Serializer ---
class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'contact_number', 'email', 'created_by')
        read_only_fields = ('id',) 

    # Automatically set the 'created_by' field when a doctor is created
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return Doctor.objects.create(**validated_data)

# --- 3. Patient-Doctor Mapping Serializer ---
# records/serializers.py (Ensure your mapping serializer matches this)

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    # These fields retrieve the names for OUTPUT (read-only)
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        # The fields the API client interacts with for POST/PUT/PATCH
        fields = ('id', 'patient', 'doctor', 'assigned_at', 'patient_name', 'doctor_name')
        read_only_fields = ('assigned_at',)
            
    def to_representation(self, instance):
        # Clean up the output to only show the names in the main response body
        representation = super().to_representation(instance)
        representation['patient'] = instance.patient.name
        representation['doctor'] = instance.doctor.name
        representation.pop('patient_name')
        representation.pop('doctor_name')
        return representation

    def validate(self, data):
        # Security check: User can only assign doctors to THEIR OWN patients
        patient = data['patient']
        user = self.context['request'].user
        if patient.created_by != user:
            raise serializers.ValidationError({"patient": "You can only assign a doctor to a patient you created."})
            
        # Check for unique assignment (prevents duplicate entries)
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=data['doctor']).exists():
            raise serializers.ValidationError({"detail": "This doctor is already assigned to this patient."})
        
        return data