<html>
    <head>
        <link REL="StyleSheet" TYPE="text/css" HREF="myStyle.css">
    </head>

    <body>
    <div>
        <img src="./images/logo.png" width=150 height=225/>
    </div>

    <form action="/search" method="post">
    Hit Please: <input name="keywords" type="text"/>
    <input value="GO!" type="submit"/>
    </form>

    <div>
    %if "email" in user:
        <a href="/query">Top 20 Keywords</a><br>
        Welcome: {{user["email"]}}
        <a href='/logout'>logout</a>
    %else:
        Anonymous can <a href="/login">login</a><br>
    %end
    </div>

    <div style="position: absolute; bottom: 0px;">&copy2014 Summer&Edward</div>

    </body>
</html>
