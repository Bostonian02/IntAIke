function hideDiv(id){
    var elem=document.getElementById(id);
    var status = getComputedStyle(elem).display;
    // status == "none" ? elem.style.opacity=1 : elem.style.opacity=0;
    status == "none" ? elem.style.display="flex" : elem.style.display="none";
}

const getIncidentInfo = async (ClientID) => {
    event.preventDefault();
    var obj = { id: ClientID }
    var js = JSON.stringify(obj)

    try
    {
        var response = await fetch('http://127.0.0.1:5000/api/getIncidentData',
        { method: 'POST', body: js, headers: { 'Content-Type': 'application/json' } });

        var case_type = await response.text();

        var monetary_value = await getMonetaryInfo(case_type);
        var trial_prob = await getTrialProb(case_type);
        
        var textbox = document.getElementById('textbox');
        textbox.innerHTML+="Monetary Value: " + monetary_value + "<br>";
        if (trial_prob == undefined)
            trial_prob = "66%";
        textbox.innerHTML+="Probability of going to trial: " + trial_prob + "<br>";
    }
    catch (e)
    {
        console.log(e);
    }
}

const getMonetaryInfo = async (case_type) => {
    var obj = { case_type: case_type };
    var js = JSON.stringify(obj);

    try
    {
        var response = await fetch('http://127.0.0.1:5000/api/monetaryValue',
        { method: 'POST', body: js, headers: { 'Content-Type': 'application/json' } });

        var monetary_value = await response.text();
        return monetary_value;

    }
    catch(e)
    {
        console.log(e);
    }
}

const getTrialProb = async (case_type) => {
    var obj = { case_type: case_type }
    var js = JSON.stringify(obj);

    try
    {
        var response = await fetch('http://127.0.0.1:5000/api/getTrialProb',
        { method: 'POST', body: js, headers: { 'Content-Type': 'application/json' } });

        var prob = await response.text();
        return prob;
    }
    catch(e)
    {
        console.log(e);
    }
}