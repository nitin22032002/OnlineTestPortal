let search_status=document.querySelector("#search-status")
let  table_body=document.querySelector("#table-body")
async function handleClick(e){
    if(institute.value==="0" || batch.value==="0"){
        alert("Choose any batch or institute first")
    }
    else{
        try{
        let res=await fetch(`/test/check/user/status/paper/?i_id=${institute.value}&b_id=${batch.value}`)
        res=await res.json()
            console.log(res)
        if(res.status){
            if(res["user_status"]){
                s=`<tr>
<td>Paper Id</td>
<td>Paper Name</td>
<td>Maximum Marks</td>
<td>Number Of Question</td>
<td>Test Start</td>
<td>Test End</td>
<td>Action</td>
</tr>`
                res['paper'].forEach((data)=>{
                    console.log(new Date(data.start))
                    s+=`<tr>
<td>${data.id}</td>
<td>${data.name}</td>
<td>${data.marks}</td>
<td>${data.number}</td>
<td>${data.start}</td>
<td>${data.end}</td>
<td>
${new Date(data.start)<=new Date() && new Date()<=new Date(data.end)?`<a href="/test/start/test?id=${data.id}">Start Test</a>`:new Date(data.start)>new Date()?"Test Not Start Yet":`<a href="/test/result/user/?id=${data.id}">Result</a>`}
</td>
</tr>`
                })
                table_body.innerHTML=s;
            }
            else{
                table_body.innerHTML=`<tr>
            You Are Not Verify By Institute In This Batch Yet
            </tr>`
            }
        }
    else{
        alert("Server Error....")
        }}
        catch (e){
            alert(`Server Error....${e}`)
        }
    }
}








search_status.addEventListener("click",handleClick)
