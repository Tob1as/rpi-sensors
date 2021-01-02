/*
 *	Highstock Demos › Compare multiple series
 *	http://www.highcharts.com/stock/demo/compare
 *	http://www.highcharts.com/docs
 */
 
$(function () {
    var seriesOptions = [],
        seriesCounter = 0,
        names = ['Humidity'];

    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart() {

        $('#containerHumidity').highcharts('StockChart', {

            rangeSelector: {
                selected: 4
            },

            yAxis: {
				/*
				title: {
					text: 'Humidity (%)'
				},
				*/
                labels: {
                    formatter: function () {
                        return (this.value > 0 ? ' + ' : '') + this.value + '%';
                    }
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }]
            },
			
			xAxis: {
				type: 'datetime'
			},
			
			title: {
				text: 'Humidity (%)'
			},

            plotOptions: {
                series: {
                    //compare: 'value',
					turboThreshold:5000
                }
            },

            tooltip: {
                //pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
				pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
				changeDecimals: 2,
                valueDecimals: 2
            },

            series: seriesOptions
        });
    }

        $.getJSON('sensors_api.php?type=highcharts',    function (data) {
		
		$.each( data, function( i, item ) {
			if($.inArray(item.name, names) >=0){
				seriesOptions[seriesCounter] = {
					name: item.name,
					data: item.data
				};
				seriesCounter+=1;
			}
			});
		createChart();
		});
});