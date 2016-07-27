
console.log("in popup");


/*document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('querySubmit');
    // onClick's logic below:
    link.addEventListener('click', function() {
        //chrome.tabs.executeScript(null, {file: "content.js"});
        var searchTerm = document.getElementById('queryInput').value;
       chrome.runtime.sendMessage({greeting: "buttonPressed", data: searchTerm}, function(response) {
			console.log(response.farewell);
		});
       console.log(searchTerm);
    });
});*/



document.addEventListener('DOMContentLoaded', function() {
var link = document.getElementById('querySubmit');

link.addEventListener('click', function() {
	var searchTerm = document.getElementById('queryInput').value;
/*
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	chrome.tabs.sendMessage(tabs[0].id, {greeting: "buttonPressed", data: searchTerm});
	});*/

	chrome.runtime.sendMessage({greeting: "buttonPressed", data: searchTerm});
});
});