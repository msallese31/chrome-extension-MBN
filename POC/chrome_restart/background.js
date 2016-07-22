chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if(changeInfo && changeInfo.status == "complete"){
        //console.log("Tab updated: " + tab.url);

        chrome.tabs.sendMessage(tabId, {data: tab}, function(response) {
            //console.log(response);
        });

    }
});

chrome.runtime.onMessage.addListener(function(request, sender) {
    if (request.type == "notification")
      say();
});

function say() {
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
//document.body.style.backgroundColor="red";

  var URL = 'https://www.youtube.com/watch?v=K1Y6PchDYfw'
  var searchUrl = `http://127.0.0.1:8000/video_process/checkIndex?link=${URL}`;
  var x = new XMLHttpRequest();
  x.open('GET', searchUrl);
  // The Google image search API responds with JSON, so let Chrome parse it.
  x.responseType = 'text';
  x.onload = function() {
    // Parse and process the response from Google Image Search.

    var response = x.response;
/*    document.write("Processing Dictionary ");
    document.write();
    document.write("Keys: ");*/

/*    for (var keys in response) {
      document.write(keys);
    }*/

    // var length = response["test_list_of_times"].length;

    // for (var values in response["test_list_of_times"]) {
      console.log(response);
      done();
    // }
   
/*    for (var x = 0; x < length; x++) {
      document.write(response["test_list_of_times"][x]);
    }
*/
 
  };
  x.onerror = function() {
    errorCallback('Network error.');
  };
  x.send();
  });
}

function done() {
  console.log("done!!");
}