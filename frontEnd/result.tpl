<!DOCTYPE html>
<html lang="en">
%import math
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Jumbotron Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">

    <!-- Custom styles for this template -->
    <link href="jumbotron.css" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#" style="font-family:Herculanum">Hit Search</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" style="font-family:Herculanum" role="form" action="/search" method="post">
            <div class="form-group">
              <input style = "width: 500px" type="text" name="keywords" placeholder="Search key word" class="form-control">
            </div>
            <button type="submit" class="btn btn-danger">Hit Please</button>
          </form>
          <ul class="nav navbar-nav navbar-right">
              <li>{{!USER_DISPLAY}}</li>
            </ul>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <h2>Search for "{{KEYSTRING}}"</h2>
        <table id="results">
    
        %import math
        %total = int(math.ceil(len(URLS)/10.0))
        %print total
        %print total
        %for n in URLS[10*PAGE_NUMBER-10:PAGE_NUMBER*10]:
            %title = n['title']
            %url = n['url']
            %description = n['description']
        <tr>
            <td><a href='{{title}}' target="_blank" style = "font-size:150%">{{title}}</td>
        </tr>
        <tr>
            <td><p style="color:green;font-size:100%">{{url}}</p></td>
        </tr>
        <tr>
            <td><p style = "font-size:120%">{{description}}</p></td>
        </tr>
        %end
    </table>
      <hr>

      <ul class="pagination">
            %if PAGE_NUMBER != 1:
            <li><a href="/result/{{QUERY}}/{{PREVIOUS}}">«</a></li>
            %end
            %for i in range(total):
            %j=i+1
            %if j==PAGE_NUMBER:
            <li class="disabled"><a href="/result/{{QUERY}}/{{j}}">{{j}}</a></li>
            %else:
            <li><a href="/result/{{QUERY}}/{{j}}">{{j}}</a></li>
            %end
            %end
            %if PAGE_NUMBER != total:
            <li><a href="/result/{{QUERY}}/{{NEXT}}">»</a></li>
            %end
            %end
        </ul>

      <footer>
        <p>&copy; Summer & Edward 2014</p>
      </footer>
      </div>
    </div>


    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
