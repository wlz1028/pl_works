<html>
%import math
<head>
<link rel="stylesheet" type="text/css" href="/mystyle.css">
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
</head>

    <body>
    {{!USER_DISPLAY}}
    <div>
    <form action="/search" method="post" style="text-align:left">
    Hit Please: <input name="keywords" type="text"/>
    <input value="GO!" type="submit"/>
    </form>
    </div>

    <h1>Search for"{{KEYSTRING}}"</h1>
    <table id="results">
    
        %import math
        %total = int(math.ceil(len(URLS)/10.0))
        %print total
        %print total
        %for n in URLS[10*PAGE_NUMBER-10:PAGE_NUMBER*10]:
        <tr>
            <td><a href='{{n}}' target="_blank" style="margin-left: 1cm">{{n}}</a></td>
        </tr>
        %end
    </table>
        <ul class="pagination">
            %if PAGE_NUMBER != 1:
            <li><a href="/result/{{QUERY}}/{{PREVIOUS}}">«</a></li>
            %end
            %for i in range(total):
            %j=i+1
            <li><a href="/result/{{QUERY}}/{{j}}">{{j}}</a></li>
            %end
            %if PAGE_NUMBER != total:
            <li><a href="/result/{{QUERY}}/{{NEXT}}">»</a></li>
            %end
        </ul>
    <p><a href='/search'>Back to Search</a></p>
    </body>
</html>


