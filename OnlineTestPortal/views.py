from django.shortcuts import redirect,render
from django.http import HttpResponse
def credential(func):
    def cred(self,request):
        if(request.session.get('user',False)):
            return func(self,request)
        return redirect("/authentication/login/")
    return cred

def homePage(request):
    try:
        content={}
        return render(request,"homepage.html",content)
    except Exception as e:
        print(e)
        return HttpResponse("Server Error.......")