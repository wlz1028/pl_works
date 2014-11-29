<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Hit Search">
    <meta name="author" content="Edwrad & Summer">

    <title>Hit Search by Edward & Summer</title>

    <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">


    <!-- Custom styles for this template -->
    <link href="search.css" rel="stylesheet">

  </head>

  <body>

    <div class="container">

      <form action="/search" method="post" class="form-signin">
      <div style="text-align: center">
          <img src="./images/logo.png" width=150 height=225/>
      </div>

      <input name="keywords" placeholder="Search key word" type="text" style="font-family:Herculanum" class="form-control"/>
      <button class="btn btn-lg btn-warning btn-block" type="submit">Hit Please</button>
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
  </body>
</html>
