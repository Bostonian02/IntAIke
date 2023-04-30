function hideDiv(id){
    var elem=document.getElementById(id);
    var status = getComputedStyle(elem).display;
    // status == "none" ? elem.style.opacity=1 : elem.style.opacity=0;
    status == "none" ? elem.style.display="flex" : elem.style.display="none";
}