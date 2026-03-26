
async function addStudent(){
let name=document.getElementById('name').value;
let course=document.getElementById('course').value;

await fetch('/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,course})});
load();
}

async function load(){
let res=await fetch('/get');
let data=await res.json();
let list=document.getElementById('list');
list.innerHTML="";
data.forEach(s=>{
list.innerHTML+=`<li class="list-group-item d-flex justify-content-between">
${s.name} - ${s.course}
<button onclick="del(${s.id})" class="btn btn-sm btn-danger">X</button>
</li>`;
});
}

async function del(id){
await fetch('/delete/'+id,{method:'DELETE'});
load();
}

load();
