from django.db import models
from django.contrib.auth import get_user_model

# Get the built-in Django User model
User = get_user_model()

# --- 1. Doctor Model ---
class Doctor(models.Model):
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='doctors',
    )
    
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

# --- 2. Patient Model ---
class Patient(models.Model):
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='patients',
    )

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"Patient: {self.name}"

# --- 3. Patient-Doctor Mapping Model (COMPLETED) ---
class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='assignments'
    )
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='assigned_patients'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents a patient from being assigned to the same doctor more than once
        unique_together = ('patient', 'doctor') 
    
    def __str__(self):
        return f"{self.patient.name} assigned to {self.doctor.name}"