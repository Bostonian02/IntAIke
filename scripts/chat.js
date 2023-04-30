const USER = true;
const BOT = false;
// var globalMod = 1

// user parameter is meant to be a boolean. USER is true and BOT is false
const postMessage = async (user) => {
    const chatBar = document.getElementById('userInput');
    const chatSection =document.getElementById('chatSection')
    if(chatBar.value === "")
        return;
    var message = makeMessage(chatBar.value, user);
    chatSection.innerHTML+='<div class="messageRow">'+message+'</div>';
    
    chatSection.scroll({
        top: 10000000000,
        behavior: "smooth",
      }); 

    var obj = { message: chatBar.value };
    var js = JSON.stringify(obj);

    try
    {
        var response = await fetch('http://127.0.0.1:5000/api/sendMessage',
        { method: 'POST', body: js, headers: { 'Content-Type': 'application/json' } });

        var res = await response.text()

        console.log(res);
    }
    catch (e)
    {
        console.log(e)
    }
}

function makeMessage(message, user){
    if(message === "")
        return null;
    var className;
    user ? className="user message" : className="bot message";
    var bubble = '<div class="'+className+'">'+message+'</div>';
    return bubble;
}