{{!USER_DISPLAY}}
<h2>Search for"{{KEYSTRING}}"</h2>
<table id="results">
    <tr>
        <th>Word</th>
        <th>Count</th>
    </tr>

    %for word,count in QUERY.items():
    <tr>
        <th>{{word}}</th>
        <th>{{count}}</th>
    </tr>
    %end
</table>
<p><a href='/search'>Back to Search</a></p>
