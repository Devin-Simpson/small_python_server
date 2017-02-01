$(document).ready(function() {
    
    $.ajax({
      url: window.location.href + "graphdata",
      method: "GET",
      dataType: "json",
      success: buildChart
    });

});

function toggleVisibility(el) {

  var id = parseInt(el.id)

  var newVisibility = [];

  for(var i =0; i< 50; i++){

    var buttonField = $("#controlArea #"+ i);
    var button = buttonField.find("button");

    if(i != id){
      if( button.hasClass("notClicked")){
        newVisibility[i] = false;
        buttonField.css({'text-decoration':'line-through', 'color':'#888'});
      }
    }else{

      if(button.hasClass("clicked")){
        newVisibility[i] = false;
      }else{
        newVisibility[i] = true;
      }

    }
  }

  graph.setVisibility( newVisibility);

  var clickedButtonField = $("#controlArea #"+ id);
  var clickedButton = clickedButtonField.find("button");
  
  if(clickedButton.hasClass("notClicked")){
    clickedButton.removeClass("notClicked").addClass("clicked");
    clickedButtonField.css({'text-decoration':'none', 'color':'#000'});

  }else if(clickedButton.hasClass("clicked")){
    clickedButton.removeClass("clicked").addClass("notClicked");
    clickedButtonField.css({'text-decoration':'line-through', 'color':'#888'});
  }
  
}

function buildChart(chart_data){

  var line_data = [];

  for(var i  =0; i < chart_data.graphdata.length; i++){
    var current_data = chart_data.graphdata[i];
    var current_date = Date.parse(current_data[0]);
    current_data[0] = new Date(current_date);
    line_data.push(current_data);
  }

  graph = new Dygraph(document.getElementById("graphArea"),
    line_data,
    {
      title: 'TSLA',

      highlightCircleSize: 2,
      strokeWidth: 1,
      //strokeBorderWidth: isStacked ? null : 1,

      highlightSeriesOpts: {
        strokeWidth: 3,
        strokeBorderWidth: 1,
        highlightCircleSize: 5,
      },
      legend : "follow",
      labels: chart_data.labels,
      visibility: chart_data.visibility
  });

  // render controls 
  var buttonHTML = "";
  for(var i = 0; i < chart_data.buttons.length; i++){
    buttonHTML += "<div class=\"visbilityButton\" id=\""+i+"\" onClick=\"toggleVisibility(this)\"> <button class=\"notClicked\" style=\"background-color : "+ graph.colorsMap_["t"+i+":"] +"\"> </button><label for="+i+"> "+chart_data.buttons[i]+"</label><br/> </div>";
  }
  $('#controlArea').html(buttonHTML);
}