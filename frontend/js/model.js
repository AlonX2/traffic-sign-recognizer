currentTab = undefined;
switchTab(0);

console.log(sessionStorage.getItem("testMode"));


function switchTab(index){  //tab system manager - switching to correct tab and hiding the rest.
    let tabs = document.getElementsByClassName("tab");

    if(!(typeof currentTab == 'undefined')){
        tabs[currentTab].style.display = "none";
    }

    currentTab = index;
    tabs[index].style.display = "block";
}

function submitForm(){ //submiting the data paths and checking for warnings
    const dataInput = document.getElementById('data-input');
    const modelInput = document.getElementById('model-input');
    if(!dataInput.checkValidity() || !modelInput.checkValidity() ){ //if the data is not in a valid format, returning
        return;
    }

    //if there are already warnings (not the first time in warnings tab), delete them.
    const warningDivs = document.querySelectorAll('.warning');
    if(warningDivs.length != 0){
        warningDivs.forEach((div) => div.remove());
    }
    
    eel.check_paths(modelInput.value, dataInput.value)((warnings)=>{ //checking for warnings in the paths
        if(warnings.length == 0){ //if there are none, starting training
            handleTrainTest(dataInput.value, modelInput.value, document.querySelector('#pickle-checkbox').checked);
            return;
        }
        //if there are, displaying them in a warning screen
        switchTab(1); 

        //creating warnings
        warnings.forEach((warning)=>{ 
            //duplicating warning tamplate
            const temp = document.getElementsByTagName("template")[0];
            const clone = temp.content.cloneNode(true);
            const header = document.getElementsByClassName('inner-container')[1].getElementsByTagName('h1')[0];
            header.parentNode.insertBefore(clone, header.nextSibling);

            //changing warning text to correct one
            const clones = document.querySelectorAll('.warning');
            clones[0].querySelector('.txt').innerHTML = warning;
        })

    });

}

function loadAbstractUI(){ //loading the abstract loading icon insted of the bar
    document.querySelector('.upper-container').style.display = 'none';
    document.querySelector('.abs-loader').style.display = 'block';
    document.querySelector('.stats').style.display = 'none';
}

eel.expose(updateAction);
function updateAction(txt, abstract = false){ //restarting the bar (or switching to the abstract loading icon) and changing the action text.
    if(abstract){
        loadAbstractUI();
    }
    
    else{
        document.querySelector('.upper-container').style.display = 'flex';
        document.querySelector('.abs-loader').style.display = 'none';
        document.querySelector(".progress-bar").style.width = "0%";

    }
    const actionText = document.querySelector(".progress-text");
    actionText.innerHTML = txt;
}

eel.expose(updateProgress);
const bar = document.querySelector(".progress-bar");
function updateProgress(count, total){ //progressing the progress bar
    bar.style.width = ((count*100)/total).toString() + "%";
}

eel.expose(updateStats);
function updateStats(acc, loss){ //changing the validation and loss stats.
    document.querySelector('.stats').style.display = "block";
    document.querySelector('.acc-data').innerHTML = (acc*100).toString().substring(0, 4) + "%";
    document.querySelector('.loss-data').innerHTML = loss.toString().substring(0, 5);
}


eel.expose(nextStep);
function nextStep(){ //progressing the steps that display the learning/testing progress.
    elems = document.querySelectorAll('li');
    for (let i = 0; i < elems.length; i++) {
        if(!elems[i].classList.contains("active")){
            elems[i].classList.add("active");
            return;
        }
        
    }
}

function handleTrainTest(){ //changing the tab to be a testing loading tab if needed (changing title, steps bar, etc). else just goes straight to training.
    res = sessionStorage.getItem("testMode")
    if(sessionStorage.getItem("testMode") === "true"){
        document.querySelector('.trainOnly')?.remove();
        document.querySelector('.steps').style.left= '8%';
        document.querySelector('#title').innerHTML = "Testing model";
        startTesting(...arguments);
    }
    else{
        startTraining(...arguments);
    }
}

function startTraining(dataPath, modelPath, pickle){ //switches tabs and calls the backend model creation method
    switchTab(2);
    eel.create_model(dataPath, modelPath, pickle); 
}

function startTesting(dataPath, modelPath, pickle){ //switches tabs and calls the backend model testing method
    switchTab(2);
    eel.test_model(dataPath, modelPath, pickle); 
}    


eel.expose(showResults)
function showResults(acc, loss){ //switches to results tab and displays the train\test results
    switchTab(3);
    document.querySelector('.res-acc-data').innerHTML = (acc*100).toString().substring(0, 4) + "%";
    document.querySelector('.res-loss-data').innerHTML = loss.toString().substring(0, 5);

}

eel.expose(handleError);
function handleError(text){ //switches to error screen and displays the error.
    switchTab(1);
    const temp = document.getElementsByTagName("template")[0];
    const clone = temp.content.cloneNode(true);
    const header = document.getElementsByClassName('inner-container')[1].getElementsByTagName('h1')[0];
    header.parentNode.insertBefore(clone, header.nextSibling);

    const clones = document.querySelectorAll('.warning');
    clones[0].querySelector('.txt').innerHTML = text;
}

