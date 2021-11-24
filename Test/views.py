from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Paper,Question,AnswereKey,Result
from Institute.models import Institute,Batches
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
            paperobj.test_start=datetime.datetime.fromisoformat(data['startdate'])
            paperobj.number_question=data['papernumber']
            paperobj.institute_id=request.session['instituteid']
            paperobj.total_marks=data['papermarks']
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
                if((que.question_type)=="1"):
                    que.question=f"question{i}{paperobj.id}{paperobj.institute_id}"
                    status=uploadFile(que.question,file[f'question{i}'])
                    print(status)
                    if(not status):
                        return JsonResponse({"status":False,"error":f"Question {i} Failed To Upload"})
                else:
                    que.question=data[f"question{i}"]
                que.save()
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
            questions=Question.objects.filter(paper_id=id)
            for que in questions:
                que.delete()
        return redirect("/test/view/papers/")
    except Exception as e:
        print(e)
        return HttpResponse(f"Server Error......{e}")