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
  </head>
  <body> 
    <p class="headline">
      fetch
    </p>
    <p class="search_result">1,000 projects with keyword: ${idea}</p>

    <div class="section" id="trend">
      <h1 id="section_header">POPULARITY</h1>
    </div>
    
    <div class="section" id="language">
      <h1 id="section_header">LANGUAGES</h1>
    </div>

    <div class="section" id="star">
      <h1 id="section_header">STARS</h1>
    </div>

    <div class="section" id="recommendation">
      <h1 id="h_recommendation">FETCH<br>SAYS...</h1>
    </div>

    <script src="js/jquery-2.1.1.js"></script>
    <script src="//d3js.org/d3.v3.min.js"></script>
    <script src="js/analysis.js"></script>
    <script src="js/trend.js"></script>
    <script src="js/stars.js"></script>
  </body>
</html>