from django.shortcuts import HttpResponse,render



def home(request):
    return render(request,"home.html")

def user_registration(request):
    return render(request,"user_regist.html")
    
def officail_registration(request):
    return render(request,"official_reg.html")
    
def main(request):
    return render(request,'main.html')
   
    
def tab(request):
    return render(request,'tab.html')