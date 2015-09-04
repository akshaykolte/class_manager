# Add Export As to your table
<br/>
This document assumes that the table has been given id="dataTables". The supported Export As types are pdf, excel and csv files.

### Steps:
- Add the following code to the html file (it has already been added to base_\*.html files, so there is no special need to add it to files which are derived from base_\*.html)

```
<!-- jquery export -->
<script type="text/javascript" src="/static/table_export/tableExport.js"></script>
<script type="text/javascript" src="/static/table_export/jquery.base64.js"></script>

<!-- png export -->
<script type="text/javascript" src="html2canvas.js"></script>

<!-- pdf export -->
<script type="text/javascript" src="/static/table_export/jspdf/libs/sprintf.js"></script>
<script type="text/javascript" src="/static/table_export/jspdf/jspdf.js"></script>
<script type="text/javascript" src="/static/table_export/jspdf/libs/base64.js"></script>
```

- Just after the table ends, add the following code.
```
<button onClick ="$('#dataTables').tableExport({type:'pdf',pdfFontSize:'7',escape:'false'});" class="btn btn-default">Export as PDF</button>
<button onClick ="$('#dataTables').tableExport({type:'excel',escape:'false'});" class="btn btn-default">Export as Excel</button>
<button onClick ="$('#dataTables').tableExport({type:'csv',escape:'false'});" class="btn btn-default">Export as Csv</button>
```
