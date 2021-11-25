from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Paper,Question,Result
from Institute.models import Institute,Batches,User
from OnlineTestPortal.views import credential,credential_func
from OnlineTestPortal.settings import BASE_DIR
from django.views import View
import datetime
class paper(View):
    key={"msg":""}
    @credential
    def get(self,request):
        msg=self.key.copy()
        self.key['msg']=""
        try:
            if(request.session['user']['status']):
                institute=Institute.objects.get(admin_id=request.session['user']['id'])
                batches=Batches.objects.filter(institute_id=institute.id).all()
                msg['batches']=batches
                request.session['instituteid']=institute.id
                return render(request,"addpaper.html",msg)
            return redirect("/register/institute/")
        except Exception as e:
            print(e)
            return HttpResponse(f"Server Error....{e}")

    @credential
    def post(self,request):
        try:
            data=request.POST
            file=request.FILES
            paperobj=Paper()
            paperobj.name=data['papername']
            paperobj.batch_code=data['batch']
            paperobj.test_start=data['startdate']
            paperobj.test_end=data['enddate']
            paperobj.number_question=data['papernumber']
            paperobj.institute_id=request.session['instituteid']
            total=0
            paperobj.total_marks=0
            paperobj.save()
            for i in range(1,int(paperobj.number_question)+1):
                que=Question()
                que.paper_id=paperobj.id
                que.time=datetime.time.fromisoformat(data[f"time{i}"])
                que.question_type=data[f"type{i}"]
                que.option_a=data[f"optiona{i}"]
                que.option_b=data[f"optionb{i}"]
                que.option_c=data[f"optionc{i}"]
                que.option_d=data[f"optiond{i}"]
                que.answere=data[f'answere{i}']
                que.marks=data[f'marks{i}']

                total+=int(que.marks)
                if((que.question_type)=="1"):
                    que.question=f"question{i}{paperobj.id}{paperobj.institute_id}"
                    status=uploadFile(que.question,file[f'question{i}'])
                    print(status)
                    if(not status):
                        return JsonResponse({"status":False,"error":f"Question {i} Failed To Upload"})
                else:
                    que.question=data[f"question{i}"]

                que.save()
            paperobj.total_marks=total
            paperobj.save()
            return JsonResponse({"status": True})
        except Exception as e:
            print(e)
            return JsonResponse({"status":False,"error":str(e)})

def uploadFile(filename,fileobject):
    try:
        f=open(f"{BASE_DIR}/static/files/{filename}.jpg","wb")
        for chunk in fileobject.chunks():
            f.write(chunk)
        f.close()
        return True
    except Exception as e:
        print(e)
        return False
@credential_func
def viewPapers(request):
    try:
        institute = Institute.objects.filter(admin_id=request.session['user']['id'])
        if(institute):
            institute=institute[0]
            request.session['instituteid']=institute.id
            papers=Paper.objects.filter(institute_id=institute.id)
            return render(request,"viewpapers.html",{"papers":papers})
        raise Exception("Invalid User")
    except Exception as e:
        print(e)
        return HttpResponse(f"Server Error......{e}")
@credential_func
def deletePapers(request):
    try:
        if(request.session.get('instituteid',False) and request.session['user']['status']):
            id=request.GET['id']
            Paper.objects.get(id=id).delete()
        return redirect("/test/view/papers/")
    except Exception as e:
        print(e)
        return HttpResponse(f"Server Error......{e}")

@credential_func
def userPaper(request):
    try:
        i_id=request.GET['i_id']
        b_id=request.GET['b_id']
        user=User.objects.filter(institute_id=i_id,batch_code=b_id)
        if(len(user)==0):
            raise Exception("Invalid User")
        elif(not user[0].status):
            return JsonResponse({"status":True,"user_status":False})
        else:
            papers=Paper.objects.filter(institute_id=i_id,batch_code=b_id).all()
            content=[]
            for paper in papers:
                content.append({"id":paper.id,"end":paper.test_end,"name":paper.name,"marks":paper.total_marks,"number":paper.number_question,"start":paper.test_start})
            return JsonResponse({"status":True,"user_status":True,"paper":content})
    except Exception as e:
        print(e)
        return JsonResponse({"status":False})