const USER = true;
const BOT = false;

function postMessage(){
    const chatBar = document.getElementById('userInput');
    const chatSection =document.getElementById('chatSection')
    if(chatBar.value === "")
        return;
    var message = makeMessage(chatBar.value, USER);
    chatSection.innerHTML+=message+"<br><br>";
}

function makeMessage(message, user){
    if(message === "")
        return null;
    var className;
    user ? className="user message" : className="bot message";
    var bubble = '<div class="'+className+'">'+message+'</div>';
    return bubble;
}