let institute=document.querySelector('#institute')
let batch=document.querySelector('#batch')
let form=document.getElementsByTagName('form')[0]
let submitbtn=document.querySelector('#submitbtn')
let timer=parseInt(document.getElementById('timer').textContent)
if(timer!==0 && timer!==NaN){
setTimeout(()=>{
    location.href="/"
},timer)
}

console.log(timer)
async function handleLoadDom(){
    let data=await fetch('/register/fetch/allinstitute/')
    data=await data.json()
    data=data.data
    data.forEach((instituteObj)=>{
        let option=document.createElement('option')
        option.value=instituteObj.id
        option.textContent=`${instituteObj.name}(${instituteObj.code})`
        institute.appendChild(option)
    })
}
async function fillBatch(){
    let data=await fetch(`/register/fetch/allbatch/?id=${institute.value}`)
    data=await data.json()
    data=data.data
    batch.innerHTML="<option disabled selected  value='0'>--Select Batch--</option>"
    data.forEach((batchObj)=>{
        let option=document.createElement('option')
        option.value=batchObj.code
        option.textContent=`${batchObj.name}(${batchObj.code})`
        batch.appendChild(option)
    })
}
function handleSubmit(e){
    e.preventDefault()
    console.log(batch.value)
    if(institute.value!=="0" && batch.value!=="0" && document.getElementById('contact').value!==""){
        form.submit()
    }
    else{
        alert("Fill All Details First")
    }
}
handleLoadDom()
institute.addEventListener("change",fillBatch)
submitbtn.addEventListener('click',handleSubmit)
