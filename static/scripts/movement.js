const el= document;
el.addEventListener("mousemove",(e) =>{
    document.body.style.setProperty('--x', -e.clientX/10 + "px");
    document.body.style.setProperty('--y', -e.clientY/20 + "px");
}, true);

function switchIn(){
    document.getElementById('caseSelector').className='slider';
    document.getElementById('caseTypeForm').className='closer';
    document.getElementById('intakeMethods').className='moveup';
    document.getElementById('intakeMethods').style.display='inline-block';
}