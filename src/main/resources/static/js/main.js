console.log("hello fetch");
$("input").hide()
$("#loading_gif").hide()

// jQuery handler for the new movie insertion
$("form").submit(function(event) {
  event.preventDefault();
  var projectJSON = {"project" : $("textarea")[0].value}
  $("textarea")[0].value = '';
  $("#loading_gif").dimBackground();
  $("#loading_gif").show();
  $.post("/query", projectJSON, function(response) {
  	console.log(response)
  	responseJSON = JSON.parse(response);
    console.log(responseJSON);
    window.location = "/analysis?" + $.param({"idea" : responseJSON.project_idea});
  }); 
});

$("textarea").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        $("form").submit();
    }
});