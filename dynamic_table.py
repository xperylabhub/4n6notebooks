html_head="""
<!doctype html>
<html lang="fr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.10.0/bootstrap-table.min.css">
    <link rel="stylesheet" href="https://rawgit.com/vitalets/x-editable/master/dist/bootstrap3-editable/css/bootstrap-editable.css">


    <style>
    .container {
        width: 100%;
        padding: 2em;
    }
    </style>
    </head>
    <body>

        
    <h2>Messages WhatsApp</h2>

"""

table_header_part1 = """
<div id="toolbar">
    <select class="form-control">
            <option value="">Export Basique</option>
            <option value="all">Exporter Tout</option>
            <option value="selected">Exporter Selectionn&eacute;s</option>
    </select>
</div>
<div class="table-responsive">
<table class="table table-xsm table-striped table-bordered table-hover" cellspacing="0" id="table" 
         data-toggle="table"
         data-search="true"
         data-filter-control="true" 
         data-show-export="true"
         data-click-to-select="true"
         data-toolbar="#toolbar"
         data-escape="false">
<thead>
    <tr>
        <th class="th-sm" data-field="state" data-checkbox="true"></th>
"""
table_header_col = '<th class="th-sm" data-field="{}" data-filter-control="input" data-sortable="true">{}</th>'

table_header_part2 = """
    </tr>
</thead>
<tbody>
"""

table_body_row = """
    <tr>
        <td class="bs-checkbox "><input data-index="{}" name="btSelectItem" type="checkbox"></td>
"""

table_body_footer = """
</tbody>
</table>
</div>
"""

js = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.10.0/bootstrap-table.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.9.1/extensions/editable/bootstrap-table-editable.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.9.1/extensions/export/bootstrap-table-export.js"></script>
<script src="https://rawgit.com/hhurz/tableExport.jquery.plugin/master/tableExport.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.9.1/extensions/filter-control/bootstrap-table-filter-control.js"></script>

<script type="text/javascript">
$(document).ready(function () {
    var $table = $('#table');
    $('#toolbar').find('select').change(function () {
        $table.bootstrapTable('refreshOptions', {
            exportDataType: $(this).val()
        });
    });
});
</script>
"""