var counter = 0;
var ajaxCounter = 0;
var buttonCounter = 0;
var globalRes;
var searchTerm;
var token = false;

//alert("in bg");
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if(changeInfo && changeInfo.status == "complete"){
        //console.log("Tab updated: " + tab.url);
        
        console.log("bg.js - url changed, sending message to content.js");
        chrome.tabs.sendMessage(tabId, {data: tab, greeting: "urlChanged"}, function(response) {
            
        });

    }
});

//Listener
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (counter == 0) {
    if (request.greeting == "YouTubeValid") {
      //alert("valid youtube");
      token = true;
      sendAJAX(token);
      sendResponse({farewell: "bg.js - received youtube is valid"});
      
    } /*else if (request.greeting == "buttonPressed") {
      alert("button pressed indeed");
      var searchTerm = request.data;
      computeSearch(globalRes, searchTerm);
      sendResponse({farewell: "got term"});
    }*/
  }
  counter = (counter+1)%2;
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
if (buttonCounter == 0) {
    if (request.greeting == "buttonPressed") {
      //alert("button pressed indeed");
      var searchTerm = request.data;
      //alert(searchTerm);
      computeSearch(globalRes, searchTerm);
      //sendResponse({farewell: "got term"});
}
  }
buttonCounter = (buttonCounter+1)%2;
});
//Submit button listener
/*document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('querySubmit');
    // onClick's logic below:
    link.addEventListener('click', function() {
        //chrome.tabs.executeScript(null, {file: "content.js"});
        console.log("button clicked");
        searchTerm = document.getElementById('queryInput').value;
        computeSearch(globalRes, searchTerm);

    });
});*/

function sendAJAX(token) {
  if (ajaxCounter == 0 && token) {
    console.log("got mesg from content");

    chrome.runtime.onMessage.addListener( function(request, sender, sendResponse) {
/*      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
*/   
        //sendResponse({farewell: "in backgorund.js"});
      if (request.greeting == "YouTubeValid") {
      chrome.tabs.executeScript(null, {file: "content.js"});
      sendResponse({farewell: "in backgorund.js"});
      console.log("In sendAJAX");

    var URL = 'https://www.youtube.com/watch?v=K1Y6PchDYfw'
    
    //var URL = 'https://www.youtube.com/watch?v=lFIIMEe2Ht0'
    var searchUrl = `http://127.0.0.1:8000/video_process/checkIndex?link=${URL}`;
    var x = new XMLHttpRequest();
    x.open('GET', searchUrl);
    // The Google image search API responds with JSON, so let Chrome parse it.
    x.responseType = 'text';
    x.onload = function() {
      // Parse and process the response from Google Image Search.
      var response = x.response;
      console.log(response);

      globalRes = response;
      console.log("spacer");
      console.log(globalRes);
      sendArray(response);
      alert(response);
    };

    x.onerror = function() {
      errorCallback('Network error.');
    };
      x.send();
    }
    });
  }
  ajaxCounter = (ajaxCounter+1)%2;
}

function sendArray(response) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {greeting: "responseArray", data: response}, function(response) {
    console.log(response.farewell);

  });
});
}

function computeSearch(inputArray, inputTerm) {

  var finalSearch = [];
  var asdf = inputArray;
  var len = inputArray.length - 1;
  var a = inputArray.substring(1, len);
  var array = JSON.parse("[" + a + "]");

  for (var x = 0; x < array.length; x++) {

    if (inputTerm == array[x][0]) {
      finalSearch.push([inputTerm, array[x][1]]);
    }
  }

  console.log(finalSearch);
  var output = "Time Stamps\n\n";

  for (var x = 0; x < finalSearch.length; x++) {
    output += finalSearch[x][0] + " - " + finalSearch[x][1] + "\n\n";
  }
  alert(output);
  //document.getElementById('results').innerHTML = output;
  

}