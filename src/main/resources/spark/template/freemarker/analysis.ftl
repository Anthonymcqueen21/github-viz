<!DOCTYPE html>
  <head>
    <meta charset="utf-8">
    <title>${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="css/normalize.css">
    <link rel="stylesheet" href="css/analysis_styling.css?v=2">
    <link href='https://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Oswald:400,700' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="css/trend_graph.css">
    <link rel="stylesheet" href="css/stars_graph.css">
    <link rel="stylesheet" href="css/piechart_graph.css">
    <link rel="stylesheet" href="css/colorbrewer.css">
  </head>
  <body> 
    <a href="http://localhost:4567/"><img src="logo.png" id="logo" height="140" width="140"></a>
    <p class="headline">
      fetch
    </p>
    <p class="search_result">${numRepositories} projects with keyword: ${idea}</p>

    <div class="section" id="trend">
      <h1 id="section_header">POPULARITY</h1>
    </div>
    
    <div class="section" id="language">
      <h1 id="section_header">LANGUAGES</h1>
    </div>

    <div class="section" id="star">
      <h1 id="section_header">STARS</h1>
    </div>

    <h1 id="h_recommendation">FETCH<br>SAYS...</h1>
    <div id="recommendation">
    </div>

    <img src="newbutton.png" id="right" height="50" width="50">
    <img src="newbutton - right.png" id="left" height="50" width="50">
    <p id="pie_option">total</p>

  <var id="idea">${idea}</var>
  <var id="minYear">${minYear}</var>

    <script src="js/jquery-2.1.1.js"></script>
    <script src="//d3js.org/d3.v3.min.js"></script>
    <script src="js/analysis.js"></script>
    <script src="js/trend.js"></script>
    <script src="js/stars.js"></script>
    <script src="js/piechart.js"></script>
    <script src="js/recommendation.js"></script>
    <script src="js/colorbrewer.js"></script>
  </body>
</html>