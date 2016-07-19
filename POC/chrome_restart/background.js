console.log("whats going on");
//document.body.style.backgroundColor="red";

  var URL = 'https://www.youtube.com/watch?v=K1Y6PchDYfw'
  var searchUrl = `http://127.0.0.1:8000/getspeechtotext/?link=${URL}`;
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
   		document.write(response);
   	// }
   
/*   	for (var x = 0; x < length; x++) {
   		document.write(response["test_list_of_times"][x]);
   	}
*/
 
  };
  x.onerror = function() {
    errorCallback('Network error.');
  };
  x.send();

