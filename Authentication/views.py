from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import User_website
class Login(View):
    key={"msg":""}
    def get(self,request):
        msg=self.key.copy()
        self.key['msg'] = ""
        try:
            if(request.session.get('user',False)):
                return redirect("/")
            return render(request,"auth/login.html",msg)
        except Exception as e:
            return HttpResponse(f"Error 500 {e}")
    def post(self,request):
        try:
            emailid=request.POST['emailid']
            password=request.POST['password']
            user=User_website.objects.filter(emailid=emailid,password=password)
            if(len(user)>0):
                user=user[0]
                user={'username':user.user_name,"emailid":user.emailid,"id":user.id,"status":user.institute_status}
                request.session['user']=user
                return redirect("/")
            self.key['msg']="Invalid Authetication....."
            return redirect("/authentication/login/")
        except Exception as e:
            self.key['msg']="Server Error......"
            return redirect("/authentication/login/")
class SignUp(View):
    key = {"msg": ""}
    def get(self,request):
        msg=self.key.copy()
        self.key['msg']=""
        try:
            if (request.session.get('user', False)):
                return redirect("/")
            return render(request,"auth/signup.html",msg)
        except Exception as e:
            return HttpResponse(f"Error 500 {e}")
    def post(self,request):
        try:
            if(len(User_website.objects.filter(emailid=request.POST['emailid']))==0):
                user=User_website(user_name=request.POST['username'],emailid=request.POST['emailid'],password=request.POST['password'])
                user.save()
                user = {'username': user.user_name, "emailid": user.emailid,"id":user.id,"status":user.institute_status}
                request.session['user']=user
                return redirect("/")
            else:
                self.key['msg'] = "EmailI Already Exist..."
                return redirect("/authentication/signup/")
        except Exception as e:
            print(e)
            self.key['msg']="Server Error...."
            return redirect("/authentication/signup/")
class Logout(View):
    def get(self,request):
        try:
            del request.session['user']
            return redirect("/")
        except Exception as e:
            return HttpResponse(f"Error 500 {e}")