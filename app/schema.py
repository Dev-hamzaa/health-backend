from rest_framework import serializers
from .models import Patient, Doctor, Appointment, Treatment, Review , Medication, HealthReport , VitalStat
from datetime import date
from django.utils.timezone import now

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class HealthReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReport
        fields = '__all__'
# ===== Shared Utility =====
def extract_doctor_names(treatment):
    if treatment:
        return [doctor.name for doctor in treatment.doctors.all()]
    return []


# ===================== Appointment Serializers =====================

class OngoingAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    treatment_name = serializers.SerializerMethodField()
    gender = serializers.CharField(source='patient.gender')
    age = serializers.SerializerMethodField()
    address = serializers.CharField(source='patient.address')
    notes = serializers.CharField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'scheduledAt', 'patient_name', 'doctor_name', 'treatment_name',
            'gender', 'age', 'address', 'notes'
        ]

    def get_treatment_name(self, obj):
        treatment = Treatment.objects.filter(appointment=obj).first()
        return treatment.treatmentType if treatment else None

    def get_age(self, obj):
        today = date.today()
        dob = obj.patient.dob
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class UpcomingAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    treatment_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'scheduledAt', 'patient_name', 'doctor_name', 'treatment_name']

    def get_treatment_name(self, obj):
        treatment = Treatment.objects.filter(appointment=obj).first()
        return treatment.treatmentType if treatment else None

# ===================== Review Serializer =====================

class ReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_names = serializers.SerializerMethodField()
    treatment_type = serializers.CharField(source='treatment.treatmentType', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'comment', 'treatment', 'treatment_type', 'patient',
            'patient_name', 'doctor_names', 'createdAt'
        ]

    def get_doctor_names(self, obj):
        return extract_doctor_names(obj.treatment)

# ===================== Doctor Serializers =====================

class DoctorListSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'profilePhoto', 'specialty', 'contact', 'reviews_count', 'average_rating']

    def get_reviews_count(self, obj):
        return obj.review_set.count()

    def get_average_rating(self, obj):
        reviews = obj.review_set.all()
        if not reviews.exists():
            return None
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(), 2)


class AppointmentSummarySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'scheduledAt', 'status', 'patient_name']


class DoctorDetailSerializer(serializers.ModelSerializer):
    patients_count = serializers.SerializerMethodField()
    appointments = AppointmentSummarySerializer(many=True, source='appointment_set', read_only=True)
    reviews = ReviewSerializer(many=True, source='review_set', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialty', 'contact', 'profilePhoto', 'about', 'experience',
            'email', 'address', 'available', 'patients_count', 'appointments', 'reviews'
        ]

    def get_patients_count(self, obj):
        return obj.patients.count()

# ===================== Patient Serializers =====================

class PatientListSerializer(serializers.ModelSerializer):
    appointment_date = serializers.SerializerMethodField()
    appointment_time = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    treatment_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'appointment_date', 'appointment_time',
            'doctor_name', 'treatment_name', 'status'
        ]

    def get_appointment_date(self, obj):
        appointment = Appointment.objects.filter(patient=obj).order_by('-scheduledAt').first()
        return appointment.scheduledAt.date() if appointment else None

    def get_appointment_time(self, obj):
        appointment = Appointment.objects.filter(patient=obj).order_by('-scheduledAt').first()
        return appointment.scheduledAt.time() if appointment else None

    def get_doctor_name(self, obj):
        return obj.doctor.name if obj.doctor else None

    def get_treatment_name(self, obj):
        treatment = Treatment.objects.filter(patient=obj).order_by('-date').first()
        return treatment.treatmentType if treatment else None

    def get_status(self, obj):
        appointment = Appointment.objects.filter(patient=obj).order_by('-scheduledAt').first()
        return appointment.status if appointment else None


class VitalStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalStat
        fields = [
            'temperature', 'heart_rate', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'respiratory_rate', 'recorded_at'
        ]

class HealthReportSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReport
        fields = ['reportType', 'filePath', 'uploadedAt']

class PatientDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    vital_stats = serializers.SerializerMethodField()
    upcoming_appointments = serializers.SerializerMethodField()
    past_appointments = serializers.SerializerMethodField()
    other_notes = serializers.SerializerMethodField()
    health_reports = HealthReportSummarySerializer(many=True, source='healthreport_set', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'about', 'gender', 'dob', 'age', 'phone',
            'email', 'emergency_contact', 'address',
            'status', 'vital_stats', 'upcoming_appointments',
            'past_appointments', 'other_notes', 'health_reports'
        ]

    def get_age(self, obj):
        today = date.today()
        dob = obj.dob
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def get_status(self, obj):
        latest_appointment = Appointment.objects.filter(patient=obj).order_by('-scheduledAt').first()
        return latest_appointment.status if latest_appointment else None

    def get_vital_stats(self, obj):
        vitals = VitalStat.objects.filter(patient=obj).order_by('-recorded_at')[:3]
        return VitalStatSerializer(vitals, many=True).data

    def get_upcoming_appointments(self, obj):
        upcoming = Appointment.objects.filter(patient=obj, scheduledAt__gt=now()).order_by('scheduledAt')
        data = []
        for appt in upcoming:
            treatment = Treatment.objects.filter(appointment=appt).first()
            doctor = appt.doctor
            data.append({
                "doctor_name": doctor.name if doctor else None,
                "doctor_photo": doctor.profilePhoto.url if doctor and doctor.profilePhoto else None,
                "treatment_type": treatment.treatmentType if treatment else None,
                "date": appt.scheduledAt.date(),
                "time": appt.scheduledAt.time()
            })
        return data

    def get_past_appointments(self, obj):
        past = Appointment.objects.filter(patient=obj, scheduledAt__lt=now()).order_by('-scheduledAt')
        data = []
        for appt in past:
            treatment = Treatment.objects.filter(appointment=appt).first()
            data.append({
                "treatment_type": treatment.treatmentType if treatment else None,
                "date": appt.scheduledAt.date(),
                "time": appt.scheduledAt.time()
            })
        return data

    def get_other_notes(self, obj):
        notes = Appointment.objects.filter(patient=obj).exclude(status__in=['scheduled', 'ongoing']).exclude(notes='').order_by('-scheduledAt')
        return [{"note": appt.notes, "date": appt.scheduledAt.date(), "time": appt.scheduledAt.time()} for appt in notes]

# ===================== General Serializers =====================

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    treatment_type = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'scheduledAt', 'status', 'notes',
            'patient', 'patient_name',
            'doctor', 'doctor_name',
            'treatment_type'
        ]

    def get_treatment_type(self, obj):
        treatment = Treatment.objects.filter(appointment=obj).first()
        return treatment.treatmentType if treatment else None

class TreatmentSerializer(serializers.ModelSerializer):
    doctor_names = serializers.SerializerMethodField()
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    appointment_id = serializers.IntegerField(source='appointment.id', read_only=True)

    class Meta:
        model = Treatment
        fields = [
            'id',
            'treatmentType',
            'about',
            'category',          # ✅ Added
            'date',
            'appointment_id',
            'patient',
            'patient_name',
            'doctor_names'
        ]

    def get_doctor_names(self, obj):
        return extract_doctor_names(obj)  # You must define this function somewhere
