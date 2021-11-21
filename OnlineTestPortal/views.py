from django.shortcuts import redirect,render
from django.http import HttpResponse
from Institute.models import Institute
def credential(func):
    def cred(self,request):
        if(request.session.get('user',False)):
            return func(self,request)
        return redirect("/authentication/login/")
    return cred
def credential_func(func):
    def cred(request):
        if(request.session.get('user',False)):
            return func(request)
        return redirect("/authentication/login/")
    return cred
def homePage(request):
    try:
        content={}
        if(request.session.get('user',False) and request.session['user']['status']):
            getInstituteDetails(request,content)
            print(content)
        return render(request,"homepage.html",content)
    except Exception as e:
        print(e)
        return HttpResponse("Server Error.......")

def getInstituteDetails(request,content):
    try:
        institute=Institute.objects.get(admin_id=request.session['user']['id'])
        content.update({"institute_name":institute.name,"institute_contact":institute.contact_number,"institute_address":institute.address,"institute_code":institute.institute_code})
    except Exception as e:
        print(e)

@credential_func
def profile(request):
    try:
        user=request.session['user']
        return render(request,"profile.html",user)
    except Exception as e:
        print(e)
        return redirect("/")

def about(request):
    try:
        return render(request,"about.html")
    except Exception as e:
        print(e)
        return redirect("/")