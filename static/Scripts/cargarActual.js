$(document).ready(function () {
    CargarTemperatura();
    var response = new Object();
    response.temperatura = "40";
    response.humedad = "30";
    var data = [response]
    CargarTablaTemperaturas("dtTemperaturas",data);

});

function CargarTemperatura() {
    
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "",
        "method": "GET"
        // "data": json,
        // "headers": {
        //     "Content-Type": "application/json; charset=utf-8",
        //     "cache-control": "no-cache"
        // }
    };

    $.ajax(settings).done(function (response) {
        if (response !== "" && response !== null) {
            CargarTablaTemperaturas("dtTemperaturas",response);
        }
    }).fail(function (response) {
        console.log(response);
    });
}

function CargarTablaTemperaturas(nombreTabla, temperaturas) {
 
    if ($.fn.DataTable.isDataTable('#' + nombreTabla + '')) {
        $('#' + nombreTabla + '').dataTable().fnDestroy();
    }
    tableP = $('#' + nombreTabla + '').DataTable({
        responsive: true,
        select: true,
        language: {
            url: "../Scripts/DataTable/Spanish.json"
        },
        //scrollY: 400,
        data: temperaturas,
        columns: [
            { 'data': 'temperatura' },
            { 'data': 'humedad' } 
        ]
    });
 
    //var dt = $('#' + nombreTabla + '').DataTable();
    //dt.column(1).visible(false);
}
