<!DOCTYPE html>
  <head>
    <meta charset="utf-8">
    <title>${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- In real-world webapps, css is usually minified and
         concatenated. Here, separate normalize from our code, and
         avoid minification for clarity. -->
    <link rel="stylesheet" href="css/normalize.css">
    <link rel="stylesheet" href="css/analysis_styling.css">
    <link href='https://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="css/trend_graph.css">
  </head>
  <body> 
    <CENTER>
      <p class="headline_analysis">
        <span>Analytics for:<br>${idea}</span>
      </p>



    </CENTER>
    <script src="js/jquery-2.1.1.js"></script>
    <script src="//d3js.org/d3.v3.min.js"></script>
    <script src="js/analysis.js"></script>
    <script src="js/trend.js"></script>
  </body>
  <!-- See http://html5boilerplate.com/ for a good place to start
       dealing with real world issues like old browsers.  -->
</html>