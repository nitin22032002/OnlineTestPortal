let option1=document.querySelector("#option1")
let option2=document.querySelector("#option2")
let option3=document.querySelector("#option3")
let option4=document.querySelector("#option4")
let question=document.querySelector("#question")
let timer_tag=document.querySelector("#timer")
let ans_options=document.getElementsByClassName("option")
let next_btn=document.querySelector("#next-btn")
let paperid=JSON.parse(document.querySelector('#paperid').textContent)
let questions_list;
let show_list;
let setTimer;
let ans_were={}
let question_number=1;
async function  fetchQuestions(){
    let res=await fetch(`/test/test/fetchquestion/?id=${paperid}`)
    res=await res.json()
    if(res.status){
        questions_list=res.que;
        show_list=res.quelist
        setQuestion()
    }
    else{
        alert("Server Error........")
        location.href="/"
    }
}
function setQestionTimer(timer){
    return setInterval(()=>{
        timer_tag.innerHTML=`${parseInt(timer/60)} min ${timer%60} sec`
        timer--;
        if(timer===-1){
            clearInterval(setTimer)
            next_btn.click()
        }
    },1000)
}
function setQuestion(){
    let question_obj=questions_list[question_number-1]
    if (questions_list.length === question_number) {
            next_btn.value = "Submit"
        }
    if(question_obj.questiontype===2){
        question.innerHTML=`<h2>${question_obj.question}</h2><h4>Marks : ${question_obj.marks}</h4>`
    }
    else{
        question.innerHTML=`<img src="/static/files/${question_obj.question}">`
    }
    option1.innerHTML=question_obj.optiona
    option2.innerHTML=question_obj.optionb
    option3.innerHTML=question_obj.optionc
    option4.innerHTML=question_obj.optiond
    ans_were[question_obj.questionid]
    setTimer=setQestionTimer(question_obj.time)
}
function  setAnswere(){

    for(let ans of ans_options){
        if(ans.checked){
            ans_were[questions_list[question_number-1].questionid]=ans.value
        }
        else{
            ans_were[questions_list[question_number-1].questionid]="notanswere"

        }
    }
}
async function handleClick(){
    setAnswere()
    question_number++;
    console.log(questions_list.length)
    console.log(question_number)
    console.log(questions_list.length+1===question_number)
    if(questions_list.length+1===question_number){
        clearInterval(setTimer)
      let res=await fetch("/test/submission",{
           method:"POST",
            headers:{"Accept":"application/json","X-CSRFToken":document.getElementsByName('csrfmiddlewaretoken')[0].value},
            body:JSON.stringify({"ans":ans_were})
      })
        res=await res.json()
        if(res.status){
            alert("Submitted....")
            location.href="/test/test/result/"
        }
    else{
        alert("Failed To Submit.....")
        }
    }
    else {
        setQuestion()
        clearInterval(setTimer)
    }
}


next_btn.addEventListener("click",handleClick)
fetchQuestions()