from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from .models import *
import pprint
import gspread
import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import PermissionDenied
from django.views import View
from .forms import *
from django.core.exceptions import *
from django.contrib import messages

# initialize pprint
pp = pprint.PrettyPrinter()


# Create your views here.

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request, template_name="registration/registration.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("base")
                # return render(request=request, template_name="employee/employee.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("base")


def base(request):
    return render(request=request, template_name='base.html')


def create_employee(request):
    if request.method == "POST":
        form = NameEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Created.")
            return redirect("employee")
        else:
            messages.error(request, "employee Creation Failed. Invalid information.")
            return redirect("employee")
    else:
        form = NameEmployeeForm
    return render(request=request, template_name="employee/employee.html", context={"form": form})


def upload_sheet_link(request, id=None):
    if request.user.is_authenticated:
        # ori_url='https://docs.google.com/spreadsheets/d/13yyd8s008LlRn0tn6LC5moH1fcBELBkYw2THX6gjdHU/edit?usp=sharing'
        # df = pd.read_csv(ori_url)
        # id='13yyd8s008LlRn0tn6LC5moH1fcBELBkYw2THX6gjdHU'
        id = id
        try:
            df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{id}/export?format=csv")
            records = df.to_dict(orient='records')
            pp.pprint(records)
        except Exception:
            messages.error(request, "Not able to fetch please check id")
            return redirect("employee")
            for record in records:
                emp = Employee(firstName=record["First Name"], lastName=record["Last Name"],
                               employeeId=record["Employee ID"], city=record["City"])
                emp.save()
                messages.success(request, f"Data fetched sucessfully for{emp.employeeId} from Google Sheet")
        except Exception:
            messages.error(request,"Exception data not valid or data already present")
            return redirect("employee")
        else:
            messages.success(request, "Data fetched sucessfully from Google Sheet")
            return redirect("employee")
    else:
        messages.error(request, "Please login")
        return redirect("login")


def upload_sheet_api(request, id=None):
    if request.user.is_authenticated:
        id = id
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'credentials.json')

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        # SAMPLE_SPREADSHEET_ID = '13yyd8s008LlRn0tn6LC5moH1fcBELBkYw2THX6gjdHU'
        SAMPLE_SPREADSHEET_ID = id
        SAMPLE_RANGE_NAME = 'Sheet1'

        # Shows basic usage of the Sheets API.Prints values from a sample spreadsheet
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    file_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        try:
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
            pp.pprint(result)
            values = result["values"]
        except Exception:
            messages.error(message='Not able to fetch check id', request=request)
            return redirect("employee")
        if not values:
            print('No data found.')
            messages.error(request,"No data found")
        else:
            df = pd.DataFrame(result["values"], columns=result["values"][0]).to_dict(orient='records')
            print("res", df)
            try:
                for record in df:
                    emp = Employee(firstName=record["First Name"], lastName=record["Last Name"],
                                   employeeId=record["Employee ID"], city=record["City"])
                    emp.save()
            except Exception:
                messages.error(request,"Data already present or data not valid")
            messages.success(request,"Data fetched")
            return redirect("employee")
    else:
        messages.error(request,"User Not authenticated")
        return  redirect("login")
