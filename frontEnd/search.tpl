<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <link REL="StyleSheet" TYPE="text/css" HREF="myStyle.css">
        <link href="search.css" rel="stylesheet">
    </head>

    <body>
   <div class="container">
      <div>
          <img src="./images/logo.png" width=150 height=225/>
      </div>
      <form action="/search" method="post" class="form-signin">
      <input name="keywords" placeholder="Search key word" type="text" style="font-family:Herculanum"/>
      <button class="btn btn-lg btn-warning btn-block" type="submit">Hit Please</button>
      </form>

      <div>
      %if "email" in user:
          <a href="/query">Top 20 Keywords</a> for {{user["email"]}}
              <p>
	      %for word,count in QUERY:
	          <b>{{word}}</b>: {{count}} |
	      %end
              </p>
          <a href='/logout'>logout</a>
      %else:
          Anonymous can <a href="/login">login</a><br>
      %end
      </div>

    </div> <!-- /container -->


    <div style="position: absolute; bottom: 0px;">&copy2014 Summer&Edward</div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
    </body>
</html>
