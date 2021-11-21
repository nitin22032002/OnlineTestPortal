let institute=document.querySelector('#institute-join')
let batch=document.querySelector('#Batch-join')
async function handleLoadDom(){
    let data=await fetch(`/register/fetch/allinstitute/user/`)
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
    let data=await fetch(`/register/fetch/allbatch/user/?id=${institute.value}`)
    data=await data.json()
    data=data.data
    console.log(data)
    batch.innerHTML="<option disabled selected  value='0'>--Select Batch--</option>"
    data.forEach((batchObj)=>{
        let option=document.createElement('option')
        option.value=batchObj.code
        option.textContent=`${batchObj.name}(${batchObj.code})`
        batch.appendChild(option)
    })
}
handleLoadDom()
institute.addEventListener("change",fillBatch)
