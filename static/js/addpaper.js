let paper_question=new FormData()
let i=1;
let total_que=0;
let d_date=new Date().toISOString()
d_date=d_date.slice(0,d_date.lastIndexOf(":"))
document.querySelector("#time").setAttribute("min",d_date)
document.querySelector("#endtime").setAttribute("min",d_date)
function appendactionBtn(func) {
    let nextBtn = document.querySelector(".submit-btn")
    nextBtn.addEventListener("click", func)
}
function handlePaper(e){
    let papername=document.querySelector("#papername").value
    let number=document.querySelector("#number").value
    total_que=number
    let startdate=String(document.querySelector("#time").value)
    let enddate=String(document.querySelector("#endtime").value)
    let batch=document.querySelector("#batch").value
    paper_question.append("papername",papername)
    paper_question.append("papernumber",number)
    paper_question.append("batch",batch)
    paper_question.append("startdate",startdate)
    paper_question.append("enddate",enddate)
    uploadQuestion()
}
function uploadQuestion(){
    let main=document.querySelector(".submain")
    document.querySelector('.main').style.height="875px"
    document.body.style.height='845px'
    document.querySelector('.mycard').style.height="865px"
    document.querySelector('.mycard').style.width="40%"
    let s=`
<div class="heading">Question ${i} Upload</div>
<div class="input-heading">Question Type</div>
        <div>
        <select id="question-type" style="width: 67%" class="input-tag"  title="Question Type" >
               <option value="2">Text</option>
               <option value="1">Picture</option>
         </select>
</div>
<div style="display: flex;justify-content: space-between;align-items: center">
<div>
<div class="input-heading">
           Marks
        </div>
        <div>
            <input type="number" class="input-tag" id="marks" placeholder="Question ${i} Marks">
        </div>
        </div>
        <div>
         <div class="input-heading">
            Duration
        </div>
        <div>
            <input type="time" value="00:00" min="00:01" max="00:05" class="input-tag" id="time" placeholder="Date Start">
        </div>
        </div></div>
        <div class="input-heading">
            Question
        </div>
        <div id="que">
            <textarea cols="35" rows="2" class="input-tag" id="question"></textarea>
        </div>
        <div class="input-heading">
           Option's
        </div>
        <div style="display: flex;flex-direction: row;flex-wrap: wrap;">
        <input type="text" style="font-size: 18px;margin: 10px" id="optiona" placeholder="Option A">
        <input type="text" style="font-size: 18px;margin: 10px" id="optionb" placeholder="Option B">
        <input type="text" style="font-size: 18px;margin: 10px" id="optionc" placeholder="Option C">
        <input type="text" style="font-size: 18px;margin: 10px" id="optiond" placeholder="Option D">
</div>
<div class="input-heading">
            Answere
        </div>
        <div>
            <input type="number" class="input-tag" id="ans" placeholder="Answere">
        </div>
<center>
            <input type="button" value=${total_que===String(i)?"Upload Test":"Next"} class="btn btn-primary submit-btn">
        </center>

       
    </div>
`
    main.innerHTML=s;
    document.querySelector('#question-type').addEventListener("change",handleType)
    appendactionBtn(addQuestions)

}

function handleType(e){
    let s="<textarea cols=\"35\" rows=\"2\" class=\"input-tag\" id=\"question\"></textarea>"
    if(e.target.value==="1"){
        s="<input type='file' id='question' class='input-tag' style='width:67% '>"
    }

    document.querySelector('#que').innerHTML=s
}

async function addQuestions(){
    let type=document.querySelector('#question-type').value
        let marks=document.querySelector('#marks').value
        let time=document.querySelector('#time').value
        let question=document.querySelector('#question')
        if(type==="1"){
            question=question.files[0]
        }
    else{
        question=question.value
        }
        let optiona=document.querySelector('#optiona').value
        let optionb=document.querySelector('#optionb').value
        let optionc=document.querySelector('#optionc').value
        let optiond=document.querySelector('#optiond').value
        let ans=document.querySelector('#ans').value
        ans=[optiona,optionb,optionc,optiond][parseInt(ans)-1]
        paper_question.append(`type${i}`,type)
        paper_question.append(`marks${i}`,marks)
        paper_question.append(`time${i}`,time)
        paper_question.append(`question${i}`,question)
        paper_question.append(`optiona${i}`,optiona)
        paper_question.append(`optionb${i}`,optionb)
        paper_question.append(`optionc${i}`,optionc)
        paper_question.append(`optiond${i}`,optiond)
        paper_question.append(`answere${i}`,ans)
    if(i===parseInt(total_que)){
        let res=await fetch("/test/add/paper",{
            method:"POST",
            headers:{"Accept":"multipart/formdata","X-CSRFToken":document.getElementsByName('csrfmiddlewaretoken')[0].value},
            body:paper_question

        })
        res=await res.json()
        if(res.status){
            location.href="/test/view/papers/"
        }
    else{
        document.querySelector(".error-msg").innerHTML=`Server Error.....${res.error}`
            setTimeout(()=>{
                 location.href="/test/paper/"
            },5000)
        }
    }
    else{
         i+=1;
    uploadQuestion()
    }


}
appendactionBtn(handlePaper);