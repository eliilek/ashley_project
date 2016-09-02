var timer_start;
var index = 0;
var trial = JSON.parse("{{ trial }}");
var responses = [];

function create_img(src){
  var elem = document.createElement("img");
  elem.setAttribute("src", "{% static 'hello/%s' %}" % src);
  return elem;
}

function post(path, parameters){
        var form = $('<form></form>');

        form.attr("method", "post");
        form.attr("action", path);

        $.each(parameters, function(key, value) {
            if ( typeof value == 'object' || typeof value == 'array' ){
                $.each(value, function(subkey, subvalue) {
                    var field = $('<input />');
                    field.attr("type", "hidden");
                    field.attr("name", key+'[]');
                    field.attr("value", subvalue);
                    form.append(field);
                });
            } else {
                var field = $('<input />');
                field.attr("type", "hidden");
                field.attr("name", key);
                field.attr("value", value);
                form.append(field);
            }
        });
        $(document.body).append(form);
        form.submit();
    }

function processResponse(response){
  timer_end = Date.now();
  responses[index] = {response_id:trial[index].response_id, given_response:response, response_time:timer_end-timer_start};
  if (trial[index].training && trial[index].correct_response == response){
    alert("That was the correct answer!\nYou answered in " + ((timer_end-timer_start)/1000.0).toFixed(2) + " seconds.");
  } else if (trial[index].training){
    alert("Sorry, that answer was incorrect.");
  }

  $("#stimulus").removeChild($("#stimulus").lastChild)
  $("#left_option").removeChild($("#left_option").lastChild)
  $("#center_option").removeChild($("#center_option").lastChild)
  $("#right_option").removeChild($("#right_option").lastChild)

  index++;
  if (index >= trial.length){
    post("{% url 'report_results' %}", responses)
  }
  refresh();
}

function refresh(){
  $("#stimulus").appendChild(create_img(trial[index].stimulus));
  $("#modifier").innerHTML=trial[index].modifier;
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
