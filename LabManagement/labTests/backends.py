from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from base.models import Patient

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, model=None, **kwargs):
        if model == 'Patient':
            # Authenticate against the Patients model
            patient = Patient.objects.filter(mobile_number=username).first()
            if patient is not None and patient.password == password:
                return patient
        else:
            # Authenticate against the User model
            User = get_user_model()
            user = User.objects.filter(username=username).first()
            if user is not None and user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            patient = Patient.objects.get(pk=user_id)
            return patient
        except Patient.DoesNotExist:
            pass

        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
