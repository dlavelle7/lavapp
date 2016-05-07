// TODO: Different types of graphs
// TODO: Improve graph layout

function capitalize(string_value) {
    return string_value.charAt(0).toUpperCase() + string_value.slice(1);
}

function drawPieChart(data, div_id) {
    var title = capitalize(div_id.split("-")[1])
    $(div_id).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: title
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: title,
            colorByPoint: true,
            data: data
        }]
    });
}

$( document ).ready(function() {
    $.ajax({
        url: '/user/balance',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-summary')
        }
    });

    $.ajax({
        url: '/user/expenses',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-expense')
        }
    });

    $.ajax({
        url: '/user/incomes',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-income')
        }
    });
});


