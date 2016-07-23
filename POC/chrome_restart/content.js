console.log("Begin - In Content.js");
//var res = [[u'right', 0.42, 0.67], [u'after', 0.67, 0.92], [u'the', 0.92, 1.02], [u'break', 1.02, 1.25], [u"we're", 1.25, 1.34], [u'going', 1.34, 1.46], [u'to', 1.46, 1.56], [u'interview', 1.56, 2.14], [u'Eric', 2.17, 2.61], [u'why', 2.61, 3.03], [u'him', 3.03, 3.21], [u'mayor', 3.21, 3.67], [u'who', 3.67, 3.97], [u'climb', 3.97, 4.39], [u'the', 4.39, 4.49], [u'highest', 4.49, 4.99], [u'mountain', 4.99, 5.27], [u'in', 5.27, 5.34], [u'the', 5.34, 5.43], [u'world', 5.43, 5.74], [u'Mount', 5.74, 6.01], [u'Everest', 6.01, 6.52], [u'but', 6.88, 7.31], [u"he's", 7.65, 8.01], [u'gay', 8.01, 8.5], [u'I', 8.53, 8.6], [u'mean', 8.6, 8.78], [u"he's", 8.78, 8.99], [u'gay', 8.99, 9.31], [u'excuse', 9.31, 9.81], [u'me', 9.81, 9.92], [u'he', 9.92, 10.05], [u'is', 10.05, 10.16], [u'blind', 10.16, 10.84], [u'so', 11.14, 11.29], [u"we're", 11.29, 11.42], [u'here', 11.42, 11.61], [u'about', 11.61, 11.82], [u'that', 11.82, 12.02], [u'coming', 12.02, 12.25], [u'okay', 12.25, 12.59], [u'as', 12.63, 12.81], [u'we', 12.81, 12.89], [u'had', 12.89, 13.01], [u'the', 13.01, 13.11], [u'break', 13.11, 13.44], [u'a', 13.44, 13.51], [u'look', 13.51, 13.69], [u'at', 13.69, 13.76], [u'the', 13.76, 13.84], [u'six', 13.84, 14.05], [u"o'clock", 14.05, 14.3]];
var counter = 0;

//Listener
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.greeting == "urlChanged") {
	    console.log("URL CHANGED: " + request.data.url);
	    
	    if (counter == 0) {
	    	checkURL();
	    }
	    	counter = (counter+1)%2;
	    /*sendResponse({farewell: "goodbye"});*/
	} else if (request.greeting == "responseArray") {
		console.log(request.data);
		sendResponse({farewell: "response array obtained"});
	} else {
		console.log("no valid matches");
	}
});

function sendAJAX(url) {
	console.log("Sending ajax");

	//Sender
	chrome.runtime.sendMessage({greeting: "YouTubeValid"}, function(response) {
  		console.log(response.farewell);
	});
}

function checkURL() {
	var url = window.location.href;
	var isYoutube = false;

	if (url.includes("youtube") && url.substring(0,23) == "https://www.youtube.com") {
		isYoutube = true;
	}

	if (isYoutube && url.includes("watch")) {
	    console.log("YouTube detected");
	    var length = url.length;
	    var ampersand = 0;

	    if (url.includes("list")) {
	    	//Can use .indexOf here...
	    	console.log("Album Detected");

	    	for (var x = length; x > 0; x--) {
	    		if (url.charAt(x) == "&") {
	    			ampersand = x;
	    		}
	    	}
	    	url = url.substr(0, ampersand);
	    } else {
	    	console.log("Video Detected");
	    }
	    console.log(url);
	    sendAJAX(url);
	} else {
	    console.log("This ain't YouTube/Isn't valid YouTube");
	}
}
