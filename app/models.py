from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.utils import timezone
from django.db.models import JSONField

# ========== PATIENT ==========
class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{10,15}$')])
    gender = models.CharField(max_length=10)
    about = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15)
    medicalRecordNo = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, related_name='patients')

# ========== DOCTOR ==========
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    profilePhoto = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    about = models.TextField(blank=True)
    experience = JSONField()  # e.g., {"years": 5, "fields": ["cardiology", "surgery"]}
    email = models.EmailField(unique=True)
    address = models.TextField()
    available = models.BooleanField(default=True)

# ========== APPOINTMENT ==========
class Appointment(models.Model):
    scheduledAt = models.DateTimeField()
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

# ========== SURGERY PERFORMED ==========
class SurgeryPerformed(models.Model):
    surgeryType = models.CharField(max_length=100)
    performedAt = models.DateTimeField()
    room = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

# ========== SURGERY SCHEDULE ==========
class SurgerySchedule(models.Model):
    surgeryType = models.CharField(max_length=100)
    scheduledAt = models.DateTimeField()
    room = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

# ========== TREATMENT ==========
class Treatment(models.Model):
    treatmentType = models.CharField(max_length=100)
    about = models.TextField()
    category = models.CharField(max_length=100)  # ✅ newly added
    date = models.DateTimeField(default=timezone.now)

    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.CASCADE,
        related_name="treatments"
    )

    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE
    )

    doctors = models.ManyToManyField(
        'Doctor',
        related_name="treatments"
    )

    def __str__(self):
        return f"{self.treatmentType} - {self.patient}"

# ========== REVIEW ==========
class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

# ========== PAYMENT ==========
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    paidAt = models.DateTimeField()
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)

# ========== MESSAGE ==========
class Message(models.Model):
    content = models.TextField()
    sentAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    senderType = models.CharField(max_length=20)
    senderId = models.IntegerField()
    receiverType = models.CharField(max_length=20)
    receiverId = models.IntegerField()

# ========== ADMIN USER ==========
class AdminUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    passwordHash = models.CharField(max_length=255)

# ========== MEDICATION ==========
class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    alergy = JSONField()
    frequency = models.CharField(max_length=50)
    prescribedAt = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

# ========== HEALTH REPORT ==========
class HealthReport(models.Model):
    reportType = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    filePath = models.FileField(upload_to='health_reports/')
    uploadedAt = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class VitalStat(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_stats')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)

    temperature = models.FloatField(help_text="Body temperature in Celsius")
    heart_rate = models.IntegerField(help_text="Beats per minute")
    blood_pressure_systolic = models.IntegerField(help_text="Systolic BP")
    blood_pressure_diastolic = models.IntegerField(help_text="Diastolic BP")
    respiratory_rate = models.IntegerField(help_text="Breaths per minute")

    recorded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Vitals for {self.patient.name} at {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
