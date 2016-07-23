var counter = 0;

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
      sendAJAX();
      sendResponse({farewell: "bg.js - received youtube is valid"});
      
    }
  }
  counter = (counter+1)%2;
});

function sendAJAX() {
  console.log("got mesg from content");
  chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting == "hello")
      //sendResponse({farewell: "in backgorund.js"});
    chrome.tabs.executeScript(null, {file: "content.js"});
    sendResponse({farewell: "in backgorund.js"});
    console.log("whats going on");

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

    sendArray(response);

  };

  x.onerror = function() {
    errorCallback('Network error.');
  };
    x.send();
  });
}

function sendArray(response) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {greeting: "responseArray", data: response}, function(response) {
    console.log(response.farewell);
  });
});
}