from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Paper,Question,AnswereKey,Result
from OnlineTestPortal.views import credential
from django.views import View
class paper(View):
    key={"msg":""}
    @credential
    def get(self,request):
        msg=self.key.copy()
        self.key['msg']=""
        try:
            if(request.session['user']['status']):
                return render(request,"addpaper.html",msg)
            return redirect("/register/institute/")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error....{e}")

    @credential
    def post(self,request):
        try:
            data=request.POST
        except Exception as e:
            self.key['msg']="Server Error....."
            return redirect("/add/paper/")

