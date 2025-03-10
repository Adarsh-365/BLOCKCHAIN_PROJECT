from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os
import json
from loguru import logger
from datetime import date
from .dabase_user import create_safe_table_name, create_user, add_record,read_data

user1_data = {
        'full_name': 'Jane Smith',
        'aadhaar_number': '9876-5432-1098',
        'email': 'jane.smith@email.com',
        'phone_number': '098-765-4321',
        'date_of_birth': '1985-08-20',
        'owner_name': 'John Doe',
        'survey_no': 2,
        'area_sqft': 850.0,
        'city_district': 'Los Angeles',
        'pin_code': '90001',
        'state': 'California',
        'registration_date': '2025-02-10',
        'status': 'In Progress',
        'address': '456 Oak Ave',
        'last_updated': '2025-02-10'
    }


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os



def clerkdashboard(request):
    return render(request,"clerkdashboard.html")

# @csrf_exempt
# def submit_land_request(request):
#     print("call")
#     if request.method == 'POST':
#         # Handling PDF file upload
#         document = request.FILES.get('land-request-pdf-upload')
#         file_path = None
        
#         if document:
#             if not document.name.endswith('.pdf'):
#                 return JsonResponse({'message': 'Only PDF files are allowed.'}, status=400)
            
#             file_path = os.path.join('uploads', document.name)
#             default_storage.save(file_path, ContentFile(document.read()))

#         # Extracting form data
#         form_data = {key: request.POST.get(key, '') for key in [
#             'land-request-fullName',
#             'land-request-email',
#             'land-request-phoneNumber',
#             'land-request-aadharNumber',
#             'land-request-dob',
#             'land-request-ownerName',
#             'land-request-surveyNumber',
#             'land-request-area',
#             'land-request-address',
#             'land-request-state',
#             'land-request-cityDistrict',
#             'land-request-pinCode'
#         ]}

#         # Printing for debugging (remove in production)
#         print("Received Form Data:", form_data)
#         print("Uploaded File Path:", file_path if file_path else "No file uploaded")

#         return JsonResponse({'message': 'Form submitted successfully!', 'data': form_data, 'file_path': file_path}, status=200)

#     return JsonResponse({'message': 'Invalid request method.'}, status=405)




@csrf_exempt
def user_login(request):
    """Handles normal user login"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # user_dashboard(data={"username":username})
                
                request.session["username"] = user.username
                print("Stored username in session:", request.session["username"])  # Debugging line

                # return redirect("user_dashboard") 
                request.session["success_message"] = "Login Succesfully"
                return JsonResponse({"status": "success", "redirect_url": "user_dashboard"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Invalid username or password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid request format"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def official_login(request):
    """Handles official user login with group verification"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            designation = data.get("designation")  # Group name
            print(username,password)
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if user belongs to the correct group (designation)
                if user.groups.filter(name=designation).exists():
                    login(request, user)
                    return JsonResponse({"status": "success", "redirect_url": "clerkdashboard"}, status=200)
                else:
                    return JsonResponse({"status": "error", "message": "User does not have the correct role"}, status=403)
            else:
                return JsonResponse({"status": "error", "message": "Invalid official ID or password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid request format"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")
        first_name = request.POST.get("firstName")
        middle_name = request.POST.get("middleName", "")
        last_name = request.POST.get("lastName")
        designation = request.POST.get("designation")
        dob = request.POST.get("dob")
        gov_id = request.POST.get("govId")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            print("Passwords do not match")
            return redirect("home")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            print("Username already taken.")
            return redirect("home")

        # Create the user
        user = User.objects.create(
            username=username,
            password=make_password(password),  # Hash the password
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Create or get the "Official Store" group
        group, created = Group.objects.get_or_create(name=designation)
        user.groups.add(group)  # Add user to the group

        # Success message
        print("Registration successful. You are now part of the Official Store group.")
        messages.success(request, "Registration successful. You are now part of the Official Store group.")
        return redirect("home")

    return render(request, "register.html")



@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract data from the request
            username = data.get("username")
            password = data.get("password")
            confirm_password = data.get("confirmPassword")
            first_name = data.get("firstName")
            middle_name = data.get("middleName", "")  # Optional
            last_name = data.get("lastName")
            gender = data.get("gender")
            dob = data.get("dob")
            email = data.get("email", "")  # Optional
            phone_number = data.get("phoneNumber")
            aadhar_number = data.get("aadharNumber")
            street = data.get("street")
            city = data.get("city")
            state = data.get("state")
            zip_code = data.get("zipCode")

            # Validate required fields
            if not all([username, password, confirm_password, first_name, last_name, gender, dob, phone_number, aadhar_number, street, city, state, zip_code]):
                return JsonResponse({"status": "error", "message": "All required fields must be filled."}, status=400)

            # Validate password match
            if password != confirm_password:
                return JsonResponse({"status": "error", "message": "Passwords do not match."}, status=400)

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username already exists."}, status=400)

            # Create user
            user = User.objects.create(
                username=username,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Optionally, you can store additional user details in another model if needed
            try:
              
                create_user(full_name=username,aadhaar_number=aadhar_number)
                
                logger.success("user added and database Created")
            except:
                 logger.success("Database not Created")

                

            return JsonResponse({"status": "success", "message": "User registered successfully!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


def home(request):
    return render(request,"index.html")

def user_registration(request):
    return render(request,"user_regist.html")
   
def forget_pass(request):
     return render(request,"forget_pass.html")
    
     
def officail_registration(request):
    return render(request,"official_reg.html")
    
def main(request):
    return render(request,'main.html')
   
@csrf_exempt   
def tab(request):
    print("does it clalling1")
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Extract form data
        form_data = {
            "request_type": request.POST.get("land-request-requestType"),
            "full_name": request.POST.get("land-request-fullName"),
            "email": request.POST.get("land-request-email"),
            "phone_number": request.POST.get("land-request-phoneNumber"),
            "aadhar_number": request.POST.get("land-request-aadharNumber"),
            "date_of_birth": request.POST.get("land-request-dob"),
            "owner_name": request.POST.get("land-request-ownerName"),
            "survey_number": request.POST.get("land-request-surveyNumber"),
            "area": request.POST.get("land-request-area"),
            "address": request.POST.get("land-request-address"),
            "state": request.POST.get("land-request-state"),
            "city_district": request.POST.get("land-request-cityDistrict"),
            "pin_code": request.POST.get("land-request-pinCode"),
            "main_category": request.POST.get("land-request-mainCategory"),
            "sub_category": request.POST.get("land-request-subCategory"),
            "acknowledgement": request.POST.get("land-request-acknowledgement") == "on"  # Checkbox returns "on" if checked
        }

        # Handle file upload (PDF)
        print(form_data)
        # pdf_file = request.FILES.get("land-request-pdf-upload")
        # if pdf_file:
        #     # Validate file type and size
        #     if pdf_file.content_type != "application/pdf":
        #         return JsonResponse({"error": "Please upload a PDF file only."}, status=400)
        #     if pdf_file.size > 20 * 1024 * 1024:  # 20 MB in bytes
        #         return JsonResponse({"error": "File size must be less than or equal to 20 MB."}, status=400)

        #     # Save the file to a designated directory (e.g., media/uploads)
        #     upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        #     os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist
        #     file_path = os.path.join(upload_dir, pdf_file.name)
        #     with open(file_path, "wb+") as destination:
        #         for chunk in pdf_file.chunks():
        #             destination.write(chunk)

        # Process the data (e.g., save to database, generate response, etc.)
        # For now, just return the data as a JSON response
        # return JsonResponse({
        #     "status": "success",
        #     "data": form_data,
        #     "pdf_uploaded": pdf_file.name if pdf_file else None
        # })
    # else:
        # return JsonResponse({"error": "Invalid request"}, status=400)
    return render(request,'tab.html')

def dashboard(request):
    return render(request,'dashboard.html')



def user_dashboard(request):
    username = request.session.get("username")  # Retrieve username from session
    print("Username retrieved from session:", username)  # Debugging line
    # success_message = request.session.pop("success_message", None)
    data = {
        "username": username if username else "Guest",  # Default to "Guest" if session is empty
    }
    
    return render(request, "user_dashboard.html", data)



def load_tab(request, tab):
    # print("does it clalling")
    print(tab,type(tab))
    if tab==10 or tab==16:
        username = request.session.get("username")
        data132 = read_data(full_name=username,aadhaar_number='123456789')
        
        # [(1, 123, 'Rahul', '123456789123', 'adarshtayde9011@gmail.com', '1231231231',
        # '2005-05-05', 'bk', 4554.0, 'adsad', '23654', '121321',
        # '2025-03-10', 'Pending', 'adasd',
        # '2025-03-10'), (2, 420, 'Rahul', '8525852258852', 'tushar@hotmail.com',
        # '7878787878787', '2000-08-05', 'Aambani', 515.0, 'Mumbai', '
        # 84578', 'maharashtra', '2025-03-10', 'Pending', '68 mumbia', '2025-03-10')]
        data = {}
        data["record"] = []
        for record in data132:
                dictsol = {}
                dictsol["full_name"] = record[2]
                dictsol["aadhaar_number"]= record[3]
                dictsol["email"]= record[4]
                dictsol["phone_number"]= record[5]
                dictsol["date_of_birth"]= record[6]
                dictsol["owner_name"]= record[7]
                dictsol["survey_no"]= record[8]
                dictsol["area_sqft"]= record[1]
                dictsol["city_district"]= record[9]
                dictsol["pin_code"]= record[10]
                dictsol["state"]= record[11]
                dictsol["registration_date"]= record[12]
                dictsol["status"]= record[13]
                dictsol["address"]= record[14]
                dictsol["last_updated"]= record[15]
               
                data["record"].append( dictsol)
            
        print(data)
        # data = {"username":"adarsh",}
        return render(request, f'tabs/tab{tab}.html',{'data': data})
        
    return render(request, f'tabs/tab{tab}.html')



@csrf_exempt  # Use this if not handling CSRF tokens in AJAX; otherwise, configure CSRF properly
def submit_land_request(request):
    if request.method == "POST":
        # Extract form data
        form_data = {
            "full_name": request.POST.get("fullName"),
            "email": request.POST.get("email"),
            "phone_number": request.POST.get("phoneNumber"),
            "aadhar_number": request.POST.get("aadharNumber"),
            "date_of_birth": request.POST.get("dob"),
            "owner_name": request.POST.get("ownerName"),
            "survey_number": request.POST.get("surveyNumber"),
            "area": request.POST.get("area"),
            "address": request.POST.get("address"),
            "state": request.POST.get("state"),
            "city_district": request.POST.get("cityDistrict"),
            "pin_code": request.POST.get("pinCode"),
        }

        # Check if all required fields are present and non-empty
        required_fields = [
            "full_name", "email", "phone_number", "aadhar_number", "date_of_birth",
            "owner_name", "survey_number", "area", "address", "state", "city_district", "pin_code"
        ]
        missing_fields = [field for field in required_fields if not form_data.get(field)]

        if missing_fields:
            return JsonResponse({
                "error": "All fields are required.",
                "missing_fields": missing_fields
            }, status=400)

        # Handle file upload (PDF) - optional in this case
        pdf_file = request.FILES.get("land-request-pdf-upload")
        if pdf_file:
            # Validate file type and size
            if pdf_file.content_type != "application/pdf":
                return JsonResponse({"error": "Please upload a PDF file only."}, status=400)
            if pdf_file.size > 20 * 1024 * 1024:  # 20 MB in bytes
                return JsonResponse({"error": "File size must be less than or equal to 20 MB."}, status=400)

            # Save the file to a designated directory (e.g., media/uploads)
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist
            file_path = os.path.join(upload_dir, pdf_file.name)
            with open(file_path, "wb+") as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
            form_data["pdf_path"] = file_path  # Optionally store the file path
            newdata = user1_data.copy()
        username = request.session.get("username")
        newdata = {
                'full_name': username,
            'aadhaar_number': form_data["aadhar_number"],
            'email': form_data['email'],
            'phone_number': form_data['phone_number'],
            'date_of_birth': form_data['date_of_birth'],
            'owner_name': form_data['owner_name'],
            'survey_no':form_data['survey_number'],
            'area_sqft':form_data['area'],
            'city_district': form_data['city_district'],
            'pin_code': form_data['pin_code'],
            'state':form_data['state'],
            'registration_date':str(date.today()),
            'status': "Pending",
            'address':form_data['address'],
            'last_updated':str(date.today()),
            
            }
        try:
                add_record(newdata)
                logger.success("kya bolati public")
        except:
            logger.critical("loda bc")
            

        # Log the form data for debugging
        print("Form Data:", form_data)

        # Set success message in session
        request.session["success_message"] = "Your land registration was successful!"
        
        # Redirect to user dashboard
        return redirect("user_dashboard")
     
    else:
        return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)