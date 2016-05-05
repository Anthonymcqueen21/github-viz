<html class="loading">
  <head>
    <meta charset="utf-8">
    <title>${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- In real-world webapps, css is usually minified and
         concatenated. Here, separate normalize from our code, and
         avoid minification for clarity. -->
    <link rel="stylesheet" href="css/normalize.css">
    <link rel="stylesheet" href="css/main_styling.css">
    <link href='https://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'>
  </head>
  <body> 
    <CENTER>

      <p class="headline">

        <span>F e t c h</span>

      <span class="blinking-cursor">|</span>

      </p>
      <p class="reg_text">committed to push you in the right direction</p>
      <a href="#user_input" ><img href="#user_input" class="animate-flicker" id="scroll_button" src="http://250greatminds.leeds.ac.uk/wp-content/themes/250-fellows/assets/img/down_arrow.png" style="width:50px;height:50px;">
      </a>



      <img src="http://code.jquery.com/mobile/1.3.1/images/ajax-loader.gif" id="loading_gif">
      <form>
      <p class="input_text">
       <textarea name="user_input" id="user_input" placeholder="<Enter any project idea here>"></textarea>
     </p>
     <input type="submit" value="Submit">
     </form>


    </CENTER>
    <script src="js/jquery-2.1.1.js"></script>
    <script src="js/main.js"></script>
    <script type="text/javascript" src="http://andywer.github.io/jquery-dim-background/jquery.dim-background.min.js"></script>
  </body>
  <!-- See http://html5boilerplate.com/ for a good place to start
       dealing with real world issues like old browsers.  -->
</html>