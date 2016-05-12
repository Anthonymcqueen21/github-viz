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


    <h1>POPULARITY</h1>
    <div class="section" id="trend"></div>

    <div class="section" id="language"></div>
    <div class="section" id="star"></div>
    <div class="section" id="recommendation"></div>

    <script src="js/jquery-2.1.1.js"></script>
    <script src="//d3js.org/d3.v3.min.js"></script>
    <script src="js/analysis.js"></script>
    <script src="js/trend.js"></script>
    <script src="js/stars.js"></script>
  </body>
</html>