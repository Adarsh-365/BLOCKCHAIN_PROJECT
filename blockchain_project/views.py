from django.shortcuts import HttpResponse,render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings



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
    return render(request,"user_dashboard.html")
def load_tab(request, tab):
    # print("does it clalling")
    return render(request, f'tabs/tab{tab}.html')




@csrf_exempt  # Use this if you're not handling CSRF tokens in your AJAX request; otherwise, configure CSRF properly
def submit_land_request(request):
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

        # Process the data (e.g., save to database, generate response, etc.)
        # For now, just return the data as a JSON response
        return JsonResponse({
            "status": "success",
            "data": form_data,
            "pdf_uploaded": pdf_file.name if pdf_file else None
        })
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)