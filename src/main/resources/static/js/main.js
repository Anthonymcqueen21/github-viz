console.log("hello fetch");

// jQuery handler for the new movie insertion
$("#user_input").submit(function(event) {
  event.preventDefault();
  var projectJSON = {"project" : $("input")[0].value}
  $("input")[0].value = '';
  $.post("/query", projectJSON, function(response) {
    console.log(response);
  }); 
});