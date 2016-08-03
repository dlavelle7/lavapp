// TODO: Different types of graphs
// TODO: Improve graph layout

$( document ).ready(function() {
    drawBudget();
});

function drawBudget() {
    var select = document.getElementById("selectBudget");
    var budgetId = select.options[select.selectedIndex].value;
    getDataAndDraw(budgetId);
}

function getDataAndDraw(budgetId) {
    $.ajax({
        url: '/budget/' + budgetId + '/summary',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-summary')
        }
    });

    $.ajax({
        url: '/budget/' + budgetId + '/expenses',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-expense')
        }
    });

    $.ajax({
        url: '/budget/' + budgetId + '/incomes',
        dataType: 'json',
        success: function(data) {
            drawPieChart(data, '#container-income')
        }
    });
}

function drawPieChart(data, div_id) {
    $(div_id).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: data["title"]
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                size: "100%",
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
            name: data["title"],
            colorByPoint: true,
            data: data["data"]
        }]
    });
}
