from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from xhtml2pdf import pisa  
from functools import wraps
from .models import LabAdmin,Patient

def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

def lab_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request_obj = args[0]
        if not request_obj.user.is_authenticated:
            return redirect('home') 
        try:
            labuser = LabAdmin.objects.get(id=request_obj.user.id)
        except LabAdmin.DoesNotExist:
            return redirect('lablogin')  # Redirect to the login page if the authenticated user is not a labadmin
        return view_func(request, *args, **kwargs)
    return wrapper

def patient_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request_obj = args[0]
        if not request_obj.user.is_authenticated:
            return redirect('home') 
        try:
            patient = Patient.objects.get(id=request_obj.user.id)
        except Patient.DoesNotExist:
            return redirect('patientlogin')  # Redirect to the login page if the authenticated user is not a labadmin
        return view_func(request, *args, **kwargs)
    return wrapper

def generate_default_password(name):
    password = name[0:4] + "@" + "123"
    return password
