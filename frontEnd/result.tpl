<!DOCTYPE html>
<html lang="en">
%import math
%import word_correction
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Search for "{{KEYSTRING}}"</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">

    <!-- Custom styles for this template -->
    <link href="/jumbotron.css" rel="stylesheet">
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
          <a class="navbar-brand" href="/search" style="font-family:Herculanum">Hit Search</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" style="font-family:Herculanum" role="form" action="/search" method="post">
            <div class="form-group">
              <input style = "width: 500px" type="text" name="keywords" placeholder="Search key word" class="form-control" spellcheck="true" autocomplete="on">
            </div>
            <button type="submit" class="btn btn-danger">Hit Please</button>
          </form>
          <ul class="nav navbar-nav navbar-right">
              <li>{{!USER_DISPLAY}}</li>
            </ul>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>

    <!-- Display result -->
    <div class="jumbotron">
      <div class="container">
        <!-- Display search suggestion -->
        %correction = word_correction.correction(KEYSTRING)
        %new_search = "%20".join(correction.split(" "))
        %if correction != KEYSTRING:
        <p style="color:orange">Did you mean: <a href="/result/{{new_search}}/1" style="color:navy">{{correction}}</a></p>
        %end
        <h2>Search for "{{KEYSTRING}}"</h2>
        <table id="results">
        %total = int(math.ceil(len(URLS)/10.0))
        %print total
        %print total
        %for n in URLS[10*PAGE_NUMBER-10:PAGE_NUMBER*10]:
            %title = n['title']
            %url = n['url']
            %description = n['description']
        <tr>
            <td><a href="{{url}}" target="_blank" style = "font-size:150%">{{title}}</td>
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
        <p style="font-size:90%">&copy; 2014 Summer&Edward</p>
      </footer>
      </div>
    </div>


    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
