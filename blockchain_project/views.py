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
    # print("does it clalling1")
    return render(request,'tab.html')

def dashboard(request):
    return render(request,'dashboard.html')

def load_tab(request, tab):
    # print("does it clalling")
    return render(request, f'tabs/tab{tab}.html')