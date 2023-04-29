// function postMessage(){
//     const chatBar = document.getElementById('userInput');
//     var message = chatBar.value;
//     alert(message);
// }
const postMessage = async () => {
    const chatBar = document.getElementById('userInput');
    var message = chatBar.value;

    var obj = { message: message }
    var js = JSON.stringify(obj)

    try
    {
        var response = await fetch('http://127.0.0.1:5000/api/sendMessage',
        { method: 'POST', body: js, headers: { 'Content-Type': 'application/json' } });

        var res = await response.text();

        console.log(res);

    }
    catch(e)
    {
        console.log(e);
    }
}