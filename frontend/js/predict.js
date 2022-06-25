currentTab = undefined;
switchTab(0);
const dropArea = document.getElementById('drop-area');
const images = [];
const containers = [];
let predicted = false;

function switchTab(index){  //tab system manager - switching to correct tab and hiding the rest.
    let tabs = document.getElementsByClassName("tab");

    if(!(typeof currentTab == 'undefined')){
        tabs[currentTab].style.display = "none";
    }

    currentTab = index;
    tabs[index].style.display = "block";
}


function submitForm(){ //submiting the model path and checking for warnings
  const modelInput = document.querySelector('#model-input');

  if(!modelInput.checkValidity()){
    return;
  }

  const warningDivs = document.querySelectorAll('.warning');
  if(warningDivs.length != 0){
      warningDivs.forEach((div) => div.remove());
  }

  eel.check_paths(modelInput.value)((warnings)=>{ //checking for warnings in the path
    if(warnings.length == 0){ //if there are none, starting training
        eel.set_network(modelInput.value)
        switchTab(2);
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

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
  })
  
  function preventDefaults (e) { //preventing default behvior.
    e.preventDefault()
    e.stopPropagation();
  }
  
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, ()=>{dropArea.classList.add('highlight')} , false)
  });
  
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, ()=>{dropArea.classList.remove('highlight')} , false)
  })
  




  dropArea.addEventListener('drop', (e)=>{handleFiles(e.dataTransfer.files)}, false)


function handleFiles(files) { //displaying the files in the gallery and adding them to the image array. in addition, hiding any remaining files that were already predicted on.
  if(predicted){
    document.getElementById('gallery').textContent = '';
    predicted = false;
  }

  files = [...files]
  files.forEach(displayFile)
  files.forEach(indexFile);
}


function displayFile(file) { //displaying the file in the gallery.
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onloadend = () => {
    const fig = document.createElement('figure');
    containers.push(fig);

    const img = document.createElement('img');
    img.src = reader.result;
    fig.appendChild(img);

    const figcap = document.createElement('figcaption'); //this will later hold the prediction string.
    fig.appendChild(figcap);

    document.getElementById('gallery').appendChild(fig);
  }
}


function indexFile(file){ //adding the file to the images array.
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onloadend = function() {
    const img = new Image();
    img.src = reader.result;
    images.push(img);
  }
}

function showPredictions(arr){ //display all the prediction strings, by changing the values of the figcaptions that all the images have (created in "displayFile").
  let counter = 0;
  arr.forEach(str => {

    const figcap = containers[counter].getElementsByTagName('figcaption')[0];
    figcap.innerHTML = str;
    counter++;
  });

  predicted = true;
}



function requestPredictions(){ //requesting predictions on all the images from the backend.
  const res = [];
  images.forEach(img => {
    eel.handle_and_predict(img.src)(out =>{
      //checking for errors with the image
      if(out.split(';;')[0] === 'Error'){
        console.log(out.split(';;')[1])
        out = 'Failed.'
      }
      //adding value to result array.
      res.push(out);

      //if this was the last image, shows the results.
      if(res.length === images.length){
        showPredictions(res);
      }
      
    });
  });

}

eel.expose(handleError);
function handleError(text){//switches to error screen and displays the error. used only for fatal errors, not problems with a specific prediction image.
    switchTab(1);
    const temp = document.getElementsByTagName("template")[0];
    const clone = temp.content.cloneNode(true);
    const header = document.getElementsByClassName('inner-container')[1].getElementsByTagName('h1')[0];
    header.parentNode.insertBefore(clone, header.nextSibling);

    const clones = document.querySelectorAll('.warning');
    clones[0].querySelector('.txt').innerHTML = text;
}






