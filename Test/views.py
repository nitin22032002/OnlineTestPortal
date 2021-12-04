from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Paper,Question,Result
from Institute.models import Institute,Batches,User
from OnlineTestPortal.views import credential,credential_func
from OnlineTestPortal.settings import BASE_DIR
from django.views import View
import datetime
import json
import random
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
        user=User.objects.filter(institute_id=i_id,batch_code=b_id,admin_id=request.session['user']['id'])
        if(len(user)==0):
            raise Exception("Invalid User")
        elif(not user[0].status):
            return JsonResponse({"status":True,"user_status":False})
        else:
            papers=Paper.objects.filter(institute_id=i_id,batch_code=b_id).all()
            content=[]
            for paper in papers:
                status=Result.objects.filter(paper_id=paper.id,user_id=user[0].id)

                if(len(status)>0):
                    status=True
                else:
                    status=False
                content.append({"status":status,"id":paper.id,"end":paper.test_end,"name":paper.name,"marks":paper.total_marks,"number":paper.number_question,"start":paper.test_start})
            return JsonResponse({"status":True,"user_status":True,"paper":content})
    except Exception as e:
        print(e)
        return JsonResponse({"status":False})
@credential_func
def TestPaper(request):
    try:
        paper=Paper.objects.get(id=request.GET['id'])
        user_id = User.objects.get(admin_id=request.session['user']['id'], institute_id=paper.institute_id,batch_code=paper.batch_code).id
        print(user_id)
        result=Result.objects.filter(paper_id=request.GET['id'],user_id=user_id)
        if(len(result)==0):
            return render(request,"testplace.html",{"id":request.GET['id'],"enddate":paper.test_end,"start":paper.test_start})
        return HttpResponse("You Already Given The Test.....")
    except Exception as e:
        print(e)
        return HttpResponse("Server Error......")
@credential_func
def fetchQuestion(request):
    try:
        que=Question.objects.filter(paper_id=request.GET['id'])
        content=[]
        n=len(que)
        total=0
        for question in que:
            question.time=int(question.time.minute)*60
            total+=question.time
            content.append({"questionid":question.id,"questiontype":question.question_type,"marks":question.marks,"time":question.time,"question":question.question,"optiona":question.option_a,"optionb":question.option_b,"optionc":question.option_c,"optiond":question.option_d})
        que_list=list(range(0,n))
        random.shuffle(que_list)
        return JsonResponse({"status":True,"que":content,"quelist":que_list,"total":total})
    except Exception as e:
        print(e)
        return JsonResponse({"status":False})

@credential_func
def submission(request):
    try:
        data=json.load(request)
        ans=data['ans']
        questions=Question.objects.filter(paper_id=ans['paperid']).all()
        content=[]
        score=0
        wr=0
        cr=0
        for que in questions:
            if(str(que.id) in ans):
                s = ans[str(que.id)]
                if(que.answere==s):
                    cr+=1
                    score+=que.marks
                else:
                    wr+=1
                    score-=1
            else:
                s="notanswere"
            l = {"question": que.question, "type": que.question_type, "ans": que.answere, "mark": s}
            content.append(l)
        result=Result()
        result.paper_id=que.paper_id
        result.marks_obtain=score
        result.question_attempt=cr+wr
        result.question_left=len(questions)-cr-wr
        result.question_wrong=wr
        paper=Paper.objects.get(id=result.paper_id)
        result.user_id=User.objects.get(admin_id=request.session['user']['id'],institute_id=paper.institute_id,batch_code=paper.batch_code).id
        result.save()
        request.session['result']={"que":content,"score":score,"wr":wr,"cr":cr,"left":len(questions)-cr-wr}
        return JsonResponse({"status": True})
    except Exception as e:
        print(e)
        return JsonResponse({"status":False})
@credential_func
def testResultDiscription(request):
    try:
        content=request.session['result']
        del request.session['result']
        return render(request,"testResultDiscription.html",content)
    except Exception as e:
        print(e)
        return HttpResponse("Server Error.........")

@credential_func
def userResult(request):
    try:
        paper=Paper.objects.get(id=request.GET['id'])
        user_id=User.objects.get(admin_id=request.session['user']['id'],institute_id=paper.institute_id,batch_code=paper.batch_code).id
        result=Result.objects.get(user_id=user_id,paper_id=paper.id)
        d={"paperid":result.paper_id,"name":paper.name,"questionleft":result.question_left,"questionwrong":result.question_wrong,"questionattempt":result.question_attempt,"questioncorrect":result.question_attempt-result.question_wrong,"marksobtain":result.marks_obtain,"total":paper.total_marks}
        return render(request,"result.html",d)
    except Exception as e:
        print(e)
        return HttpResponse("Server Error......")