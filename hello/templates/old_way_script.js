var timerStart;

function ajaxFunction(){
  var ajaxRequest
  try{
    // Opera 8.0+, Firefox, Safari
    ajaxRequest = new XMLHttpRequest();
  }catch (e){
    // Internet Explorer Browsers
    try{
      ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
    }catch (e) {
      try{
        ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
      }catch (e){
          // Something went wrong
          alert("Your browser is too old to use this service.");
          return false;
      }
    }
 }
 return ajaxRequest;
};
function submitResponse(button){
  var request = ajaxFunction();
  if (request){
    request.onreadystatechange = processResponse;

    if (!target) target = document.getElementById("userid");
    var url = "validate?id=" + escape(target.value);

    request.open("GET", url, false);
    request.setRequestHeader("X-CSRFToken",
       $('input[name="csrfmiddlewaretoken"]').val());
    request.send(button + " " + (Date.now()-timerStart));
    if (request.status === 200){
      alert(request.responseText);
      timerStart = Date.now();
    } else {
      alert("Server error: Please reload the page and attempt the trial again.\nYour previous results will not be saved.")
    }
  }
};

$(document).ready(function(){
  timerStart = Date.now()
  $("#left_option").onclick=submitResponse("left");
  $("#center_option").onclick=submitResponse("center");
  $("#right_option").onclick=submitResponse("right");
});
