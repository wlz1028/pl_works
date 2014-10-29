{{!USER_DISPLAY}}
<h2>Top 20 key words</h2>
<table id="history">
    <tr>
        <th>Word</th>
        <th>Count</th>
    </tr>

    %for word,count in QUERY:
    <tr>
        <th>{{word}}</th>
        <th>{{count}}</th>
    </tr>
    %end
</table>
<p><a href='/search'>Back to Index</a></p>
