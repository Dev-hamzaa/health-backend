import django_filters
from .models import Doctor, Patient, Appointment, Treatment

class TreatmentFilter(django_filters.FilterSet):
    doctor_name = django_filters.CharFilter(method='filter_doctor_name')
    treatment_type = django_filters.CharFilter(field_name='treatmentType', lookup_expr='icontains')

    class Meta:
        model = Treatment
        fields = ['doctor_name', 'treatment_type']

    def filter_doctor_name(self, queryset, name, value):
        return queryset.filter(doctors__name__icontains=value)


class AppointmentFilter(django_filters.FilterSet):
    doctor_name = django_filters.CharFilter(field_name='doctor__name', lookup_expr='icontains')
    patient_name = django_filters.CharFilter(field_name='patient__name', lookup_expr='icontains')
    treatment_name = django_filters.CharFilter(method='filter_treatment')
    date = django_filters.DateFilter(field_name='scheduledAt__date')

    class Meta:
        model = Appointment
        fields = ['doctor_name', 'patient_name', 'treatment_name', 'date']

    def filter_treatment(self, queryset, name, value):
        from .models import Treatment
        appointment_ids = Treatment.objects.filter(treatmentType__icontains=value).values_list('appointment_id', flat=True)
        return queryset.filter(id__in=appointment_ids)



class DoctorFilter(django_filters.FilterSet):
    specialty = django_filters.CharFilter(lookup_expr='iexact')
    available = django_filters.BooleanFilter()

    class Meta:
        model = Doctor
        fields = ['specialty', 'available']


class PatientFilter(django_filters.FilterSet):
    doctor_name = django_filters.CharFilter(field_name='doctor__name', lookup_expr='icontains')
    treatment_name = django_filters.CharFilter(method='filter_treatment')
    appointment_date = django_filters.DateFilter(method='filter_appointment_date')

    class Meta:
        model = Patient
        fields = ['doctor_name', 'treatment_name', 'appointment_date']

    def filter_treatment(self, queryset, name, value):
        patient_ids = Treatment.objects.filter(treatmentType__icontains=value).values_list('patient_id', flat=True)
        return queryset.filter(id__in=patient_ids)

    def filter_appointment_date(self, queryset, name, value):
        patient_ids = Appointment.objects.filter(scheduledAt__date=value).values_list('patient_id', flat=True)
        return queryset.filter(id__in=patient_ids)
