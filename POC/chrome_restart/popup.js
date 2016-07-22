console.log("in popup");

document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('querySubmit');
    // onClick's logic below:
    link.addEventListener('click', function() {
        chrome.tabs.executeScript(null, {file: "content.js"});
        console.log("button clicked");
    });
});
