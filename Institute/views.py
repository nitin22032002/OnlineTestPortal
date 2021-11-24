from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from Authentication.models import User_website
from .models import Institute,User,Batches
from OnlineTestPortal.views import credential
class Register_Institute(View):
    key={"msg":""}
    @credential
    def get(self,request):
        try:
            msg=self.key.copy()
            self.key['msg']=""
            status=request.session['user']['status']
            if(not status):
                return render(request,"register/instituteRegistration.html",msg)
            return redirect('/')
        except Exception as e:
            return HttpResponse(f"Server Error......{e}")
    @credential
    def post(self,request):
        try:
            data=request.POST
            name,address,contact_number,institute_code=data['name'],data['address'],data['contact_number'],data['institute_code']
            print(name)
            user_id=request.session['user']['id']
            institute=Institute.objects.filter(name=name,institute_code=institute_code)
            if(len(institute)==0):
                Institute(name=name,address=address,contact_number=contact_number,institute_code=institute_code,admin_id=user_id).save()
                user=User_website.objects.get(id=user_id)
                user.institute_status=True
                user.save()
                request.session['user']['status']=True
                return redirect("/")
            self.key['msg']="This Institute Already Register"
            return redirect("/register/institute/")
        except Exception as e:
            print(e)
            self.key['msg']="Server Error......"
            return redirect("/register/institute/")
class Register_User(View):
    key={"msg":"","timer":0}
    @credential
    def RequestUser(self,request):
        try:
            if(request.session['user']['status']):
                users=User.objects.filter(institute_id=Institute.objects.get(admin_id=request.session['user']['id']).id)
                for user in users:

                    user.admin_id=User_website.objects.get(id=user.admin_id).user_name
                return render(request,"register/requests.html",{"requests":users})
            raise Exception("Invalid User")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error......{e}")
    @credential
    def DeleteUser(self,request):
        try:
            if (request.session['user']['status']):
                user=User.objects.get(id=request.GET['id'])
                user.delete()
                return redirect("/register/requests/")
            raise Exception("Invalid User")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error......{e}")
    @credential
    def verifyUser(self,request):
        try:
            if (request.session['user']['status']):
                user=User.objects.get(id=request.GET['id'])
                user.status=not user.status
                user.save()
                return redirect("/register/requests/")
            raise Exception("Invalid User")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error......{e}")
    @credential
    def get(self,request):
        msg=self.key.copy()
        self.key['msg']=""
        self.key['timer']=0
        try:
            return render(request,"register/user.html",msg)
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error...... {e}")

    @credential
    def post(self,request):
        try:
            userid=request.session['user']['id']
            institute=request.POST['instituteid']
            batch=request.POST['batch']
            user=User.objects.filter(admin_id=userid,institute_id=institute,batch_code=batch)
            if(len(user)==0):
                User(admin_id=userid,institute_id=institute,batch_code=batch,contact_number=request.POST['contact_number']).save()
                self.key['msg'] = "You Registration is Pending at institution level if accept show in homepage"
                self.key['timer']=5000
                return redirect("/register/user/")
            self.key['msg']="You Already Register In This Batch"
            return redirect("/register/user/")
        except Exception as e:
            print(e)
            self.key['msg']="Server Error....."
            return redirect("/register/user/")
    @credential
    def getAllInstitute(self,request):
        try:
            institutes=Institute.objects.all()
            res=[]
            for item in institutes:
                res.append({"id":item.id,"name":item.name,"code":item.institute_code})
            return JsonResponse({"data":res})
        except Exception as e:
            print(e)
            return JsonResponse({"data":[]})

    @credential
    def getAllBatch(self, request):
        try:
            id=request.GET['id']
            batches = Batches.objects.filter(institute_id=int(id)).all()
            res = []
            for item in batches:
                res.append({"code": item.batch_code, "name": item.batch_name})
            return JsonResponse({"data": res})
        except Exception as e:
            print(e)
            return JsonResponse({"data": []})

    @credential
    def getInstituteUser(self,request):
        try:
            userid= request.session['user']['id']
            users=User.objects.filter(admin_id=userid)
            d=set()
            for item in users:
                d.add(item.institute_id)
            res = []
            for item in d:
                item=Institute.objects.get(id=item)
                res.append({"id": item.id, "name": item.name, "code": item.institute_code})
            return JsonResponse({"data": res})
        except Exception as e:
            print(e)
            return JsonResponse({"data":[]})

    @credential
    def getBatchUser(self, request):
        try:
            userid = request.session['user']['id']
            id=request.GET['id']
            users = User.objects.filter(admin_id=userid,institute_id=id)
            d = set()
            for item in users:
                d.add(item.batch_code)
            res = []
            for item in d:
                item = Batches.objects.get(batch_code=item)
                res.append({"name": item.batch_name, "code": item.batch_code})
            return JsonResponse({"data": res})
        except Exception as e:
            print(e)
            return JsonResponse({"data": []})
class Batch(View):
    key={"msg":""}
    @credential
    def get(self,request):
        msg=self.key.copy()
        self.key['msg']=""
        try:
            if(request.session['user']['status']):
                return render(request,"register/batch.html",msg)
            else:
                return redirect("/register/institute/")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error...{e}")
    @credential
    def post(self,request):
        try:
            userid=request.session['user']['id']
            institute=Institute.objects.get(admin_id=userid)
            batch=Batches.objects.filter(institute_id=institute.id,batch_code=request.POST['batchcode'])
            if(len(batch)==0):
                Batches(institute_id=institute.id,batch_code=request.POST['batchcode'],batch_name=request.POST['batchname']).save()
                return redirect("/")
            self.key['msg']="This Batch Already Register"
            return redirect("/register/batch/")
        except Exception as e:
            print(e)
            self.key['msg']="Server Error...."
            return redirect("/register/batch/")