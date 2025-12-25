<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name="generator" content="Docker Image: tobi312/rpi-sensors">
		<title>Sensors</title>
		<link rel="icon" type="image/png" sizes="16x16" href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHUlEQVQ4jY3TrTOEURQG8F8QBWGDIGwUBUHYIApbRTOvJuwMhiAwGwRhwwZjNgg6YYMgCoIgCII/QBAEYYOwYYV7XvvOurs8Myecj+e555x7L9PRwvmM/C8sYq3if2AU8RIN7GE+J3AchJvwt7EfxYdBHuId9zmBVQywGwWjsBdsocA1+hHPooa3Crm0YQj08JwTaKCJgwy5tAJXle5+UETgcaL1nEC2gxq6kbz8Q+AMK7N2sI7PGQLtqMsK1GLGE2lpVXLvPwKtSNyFWAtHWJYe0+uEQHdSYAMd1MMvR6njVFreUuSa+ArOVPTj1DnpMRWVXBu3uS6qWDD+B0/SHki3cCE96XaGl0URLXewKe1pYDzuv7ATp47wIH7uN8gEZeJprBr1AAAAAElFTkSuQmCC" />
		<!--<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">-->
		<!--<link rel="stylesheet" href="style.css">-->
		<script src='https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js'></script>
		<script src='https://cdn.jsdelivr.net/npm/highcharts@12.4.0/highstock.js'></script>
		<script src='https://cdn.jsdelivr.net/npm/highcharts@12.4.0/modules/exporting.js'></script>
		<script src='https://cdn.jsdelivr.net/npm/highcharts@12.4.0/modules/offline-exporting.js'></script>
	</head>
	<body>
		<h1>Sensors:</h1>
		<p>
			<script src='js_highcharts_humidity.js'></script>
			<script src='js_highcharts_temperature.js'></script>
			<script src='js_highcharts_temperature_f.js'></script>
			<div id='containerHumidity' style='width: 95%; height: 400px; margin: 0 auto'></div><br>
			<div id='containerTemperature' style='width: 95%; height: 400px; margin: 0 auto'></div><br>
			<div id='containerTemperatureF' style='width: 95%; height: 400px; margin: 0 auto'></div><br>
			<noscript><p>Please activate Javascript!</p></noscript>
		</p>
	</body>
</html>