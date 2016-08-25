var timer_start;
var index = 0;
var trial = JSON.parse("{{ trial }}");
var responses = [];

function create_img(src){
  var elem = document.createElement("img");
  elem.setAttribute("src", "static/" + src);
  return elem;
}

function processResponse(response){
  timer_end = Date.now();
  var to_return = {response_id:trial[index].response_id, given_response:response, response_time:timer_end-timer_start};
  if (trial[index].training && trial[index].correct_response == response){
    alert("That was the correct answer!");
  } else if (trial[index].training){
    alert("Sorry, that answer was incorrect.");
  }

  index++;
  refresh();
}

function refresh(){
  $("#left_option").appendChild(create_img(trial[index].left_option));
  $("#center_option").appendChild(create_img(trial[index].center_option));
  $("#right_option").appendChild(create_img(trial[index].right_option));
  $("#left_option").onclick=processResponse(trial[index].options.split(",")[0]);
  $("#center_option").onclick=processResponse(trial[index].options.split(",")[1]);
  $("#right_option").onclick=processResponse(trial[index].options.split(",")[2]);

  timer_start = Date.now();
}

$(document).ready(function(){
  refresh();
});
