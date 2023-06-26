from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.shortcuts import get_object_or_404
from .models import LabAdmin, Tests,Patient, Visit, VisitDetails
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .utils import html_to_pdf

# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'index.html')


# Lab User Signup View
class LabUserSignupView(View):
    def get(self, request):
        return render(request, 'signup.html')


    def post(self, request):
        # Get the form data
        # data = json.loads(request.body)
        # name = data.get('name')
        # email = data.get('email')
        # mobile_number = data.get('mobile_number')
        # username = data.get('username')
        # password = data.get('password')
      
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Create a new LabUser object
        error = ""
        try:
            lab_user = LabAdmin.objects.create_user(username=username, password=password)
            lab_user.name = name
            lab_user.mobile_number = mobile_number
            lab_user.email = email
            lab_user.save()
            error = "No"
        except Exception as e:
            error = "Yes"
        return render(request, 'signup.html', locals())

# Lab User Login View
class LabUserLoginView(View):
    def get(self, request):
        return render(request, 'lab_login.html')

    def post(self, request):
        # Get the form data
        # data = json.loads(request.body)
        # username = data.get('username')
        # password = data.get('password')

        username = request.POST.get('username')
        password = request.POST.get('password')
        error = ""
        # Authenticate the lab user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the lab user
            login(request, user)
            error = "No"
        else:
            error = "Yes"
        return render(request, 'lab_login.html', locals())

class TestAddView(View):
    def get(self, request):
        return render(request, 'add_tests.html')

    def post(self, request):
        error = ""
        msg = ""
        print(request.body)
        try:
            # data = json.loads(request.body)
            # name = data.get('name')
            # cost = data.get('cost')

            name = request.POST.get('name')
            cost = request.POST.get('cost')
            if Tests.objects.filter(name=name).exists():
                error = "Yes"
                msg = "Test name already exists"
                return render(request, 'add_tests.html', locals())
            test = Tests(name=name, cost=cost)
            test.save()
            error = "No"
        except Exception as e:
            error = "Yes"
            msg = "Could not add test"
        return render(request, 'add_tests.html', locals())

class TestUpdateView(View):
    def post(self, request, test_id):
        error = ""
        try:
            # data = json.loads(request.body)
            # test = Tests.objects.get(test_id=test_id)
            # test.name = data.get('name')
            # test.cost = data.get('cost')
            test = Tests.objects.get(test_id=test_id)
            # test.name = request.POST.get('name')
            test.cost = request.POST.get('cost')
            test.save()
            error = "No"
        except Exception as e:
            error = "Yes"
        return render(request, 'all_tests.html', locals())    

class TestListView(View):
    def get(self, request):
        tests = Tests.objects.all()
        response_obj = []
        for test in tests:
            test_details = {}
            test_details["test_id"] = test.test_id
            test_details["test_name"] = test.name
            test_details["test_cost"] = float(test.cost)
            response_obj.append(test_details)
        response_obj = json.dumps(response_obj)
        return render(request, 'all_tests.html', locals())


class TestDeleteView(View):
    def post(self, request, test_id):
        test = Tests.objects.get(test_id=test_id)
        test.delete()
        return HttpResponse('Test deleted successfully')


class LabRegisterPrint(View):
    def get(self, request, visit_id):
        visit = Visit.objects.get(id=visit_id)
        patient = visit.patient
        total_cost = visit.total_tests_cost
        visit_details = VisitDetails.objects.filter(visit=visit)
        pdf = html_to_pdf('pdf.html',locals())
        return HttpResponse(pdf, content_type='application/pdf')

# @method_decorator(login_required(login_url='home'), name='dispatch')
class LabUserHome(View):
    def get(self, request):
        return render(request ,'lab_home.html')

# @method_decorator(login_required(login_url='home'), name='dispatch')
class AssignTestViewTemp(View):
    def get(self, request):
        tests = Tests.objects.all()
        return render(request, 'lab_register.html', locals())

    def post(self, request):
        print(request.body)
        # data = json.loads(request.body)
        # patient_name = data.get('name')
        # patient_email = data.get('email')
        # patient_mobile = data.get('mobile_number')
        # age = data.get('age')

        patient_name = request.POST.get('name')
        patient_email = request.POST.get('email')
        patient_mobile = request.POST.get('mobile_number')
        age = request.POST.get('age')
        response_obj = {}
        # print(request.body)
        print(request.POST)
        try:
            patient, created = Patient.objects.get_or_create(email=patient_email, mobile_number=patient_mobile)
            if created:
                patient.name = patient_name
                patient.age = age
                patient.password = "admin"
                patient.save()
            # test_ids = data.get("tests", [])
            test_ids = request.POST.getlist('tests')
            print("TEST Post Data:",test_ids)
            tests = Tests.objects.filter(test_id__in=test_ids)
            total_cost = sum(test.cost for test in tests)
            visit = Visit.objects.create(patient=patient, date_time=datetime.now(), total_tests_cost=total_cost)
            test_assignments = []
            test_name = []
            for test in tests:
                test_assignment = VisitDetails.objects.create(visit=visit, test=test, test_cost=test.cost)
                test_assignments.append(test_assignment)
                test_name.append(test.name)
            response_obj["patient_name"] = patient.name
            response_obj["tests"] = test_name
            response_obj["total_cost"] = float(total_cost)       
            response_obj = json.dumps(response_obj)
            error = "No"
            print("yes")
        except Exception as e:
            print(e)
            error = "Yes"
        # return HttpResponse(response_obj)
        return render(request, 'lab_register.html', locals())
    
# @method_decorator(login_required(login_url='patientlogin'), name='dispatch')
class PatientHome(View):
    def get(self, request):
        return render(request ,'patient_home.html')


class PatientLoginView(View):
    def get(self, request):
        return render(request, 'patient_login.html')

    def post(self, request):
        # Get the form data
        # data = json.loads(request.body)
        # username = data.get('username')
        # password = data.get('password')
        print(request.body)


        username = request.POST.get('mobile_number')
        password = request.POST.get('password')
        error = ""
        # Authenticate the lab user
        print(password)
        print()
        user = authenticate(request, username=username, password=password, model="Patient")

        if user is not None:
            # Log in the lab user
            login(request, user)
            error = "No"
            print("user is auth")
        else:
            error = "Yes"
        return render(request, 'patient_login.html', locals())


class PatientTestsView(View):
    def get(self, request, id):
        patient = Patient.objects.get(id=id)
        # Generate data for displaying test history and combined bill
        visits = Visit.objects.filter(patient=patient)        
        tests_and_bills = []
        for visit in visits:
            tests = VisitDetails.objects.filter(visit=visit)
            test_data = {}

            # for test in tests:
            for i, test in enumerate(tests):
                tests = []
                tests.append(str(test.test.test_id))
                tests.append(str(test.test.name))
                tests.append(str(test.test_cost))
                test_data[i+1] = tests
                # test_data[test.test.cost] = float(test.test.cost)
                # test_data[test.test.name] = str(test.test_cost)
            # total_cost = sum(test.test.cost for test in tests)
            print(test_data)
            tests_and_bills.append({'date_time_conducted': str(visit.date_time), 'tests': test_data, 'visit_id' : visit.id, 'total_tests_cost':str(visit.total_tests_cost)})
    
        # response_obj = {"patient_name":patient.name, "tests_data" : tests_and_bills}
        response_obj = {"tests_data" : tests_and_bills}
        return render(request, 'patient_tests.html', response_obj)


class LabLogout(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
class PatientLogout(View):
    def get(self, request):
        return redirect('patientlogin')