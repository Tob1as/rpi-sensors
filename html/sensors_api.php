<?php
	######################################  CONFIG  ######################################
	
	#$protocol = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';
	
	#$sqlDatabaseType = getenv('DB_HOST');		// mysql/mariadb or postgresql
	$sqlDatabaseType = "mariadb";				// Default: mariadb
	$sqlHost = getenv('DB_HOST');				// Default: localhost
	$sqlPort = getenv('DB_PORT');				// Default: mysql->3306, postgresql->5432
	$sqlUser = getenv('DB_USER');				// Important: DO NOT USE root OR OTHER admin USER!
	$sqlPassword = getenv('DB_PASSWORD');		// Use the Password from SQL User
	$sqlDatabaseName = getenv('DB_DATABASE');	// Default: sensors | if sqlite then sqlite-filepath
	$sqlTable = "measurements";					// Default: measurements
	
	######################################################################################
	
	// SQL Query function
	$db_connection_array = array($sqlDatabaseType, $sqlHost, $sqlPort, $sqlUser, $sqlPassword, $sqlDatabaseName);
	function sql($sqlquerystring, $resulttype, $db_connection_array){
		// PDO: http://php.net/manual/de/book.pdo.php
		
		$sqlDatabaseType = $db_connection_array[0];
		$sqlHost = $db_connection_array[1];
		$sqlPort = $db_connection_array[2];
		$sqlUser = $db_connection_array[3];
		$sqlPassword = $db_connection_array[4];
		$sqlDatabaseName = $db_connection_array[5];
		
		if (strcasecmp($sqlDatabaseType, 'pgsql') == 0 || strcasecmp($sqlDatabaseType, 'postgresql') == 0 || strcasecmp($sqlDatabaseType, 'postgres') == 0 || strcasecmp($sqlDatabaseType, 'postgis') == 0){
			$sqlDatabaseType='pgsql';
			if ($sqlPort==null || $sqlPort==0){
				$sqlPort = 5432;
			}
		}
		if (strcasecmp($sqlDatabaseType, 'mysql') == 0 || strcasecmp($sqlDatabaseType, 'mariadb') == 0){
			$sqlDatabaseType='mysql';
			if ($sqlPort==null || $sqlPort==0){
				$sqlPort = 3306;
			}
		}
		
		try {
			if (strcasecmp($sqlDatabaseType, 'sqlite') == 0){
				$pdo = new PDO($sqlDatabaseType.':'.$sqlDatabaseName);
			} else {
				#$sqlServer = $sqlDatabaseType.':dbname='.$sqlDatabaseName.'; host='.$sqlHost.'; port='.$sqlPort.'; charset=utf8';
				$sqlServer = $sqlDatabaseType.':dbname='.$sqlDatabaseName.'; host='.$sqlHost.'; port='.$sqlPort;
				$pdo = new PDO($sqlServer, $sqlUser, $sqlPassword);
			}

			#if (version_compare(PHP_VERSION, '5.3.6', '<')) {
				$pdo->exec("set names utf8");
			#}
			#$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			$stmt = $pdo->prepare($sqlquerystring);
			$stmt->execute();
			if (strcasecmp($resulttype, 'INSERTINTO') == 0 || strcasecmp($resulttype, 'DELETE') == 0 || strcasecmp($resulttype, 'UPDATE') == 0) {
				// NO RETURN!
			} else {
				// RETURN (if $resulttype == 'SELECT')
				$result = $stmt->fetchAll(PDO::FETCH_ASSOC); // PDO::FETCH_ASSOC is optional
				return $result;
			}
			#print_r($result);
			$pdo = null;
		} catch (PDOException $e) {
			return 'Database Connection failed: ' . $e->getMessage();
			#die();
		}
	}
	
	// EXAMPLE:
	#$sqlquery = sql("SELECT * FROM $sqlTable",'SELECT',$db_connection_array);
	#print_r($sqlquery);
	
	######################################################################################
	
	if(isset($_GET['count']) && !empty($_GET['count']) && is_numeric($_GET['count'])){
		$count = htmlspecialchars($_GET['count']);
		if ($count>=1){
			$selectDataLimit = $count;
			$limit = "LIMIT $selectDataLimit";
		}
	} else {
		$limit = '';
		#$limit = "LIMIT 100";
	}
	
	if(isset($_GET['values']) && !empty($_GET['values']) && preg_match("/^[a-zA-Z0-9\,\_\-]+$/s",$_GET['values'])){
		$selectValues = htmlspecialchars($_GET['values']);
	} else {
		$selectValues = "*";
	}
	
	if(isset($_GET['orderby']) && !empty($_GET['orderby']) && preg_match("/^[a-zA-Z0-9\,\_\-]+$/s",$_GET['orderby']) && strcasecmp($_GET['orderby'], 'ASC') == 0){
		$sqlOrderByType = htmlspecialchars($_GET['orderby']); // ASC
	} else {
		$sqlOrderByType = "DESC"; // DESC -> new first, ASC -> old first
	}
	
	if(isset($_GET['sensorid']) && !empty($_GET['sensorid']) && is_numeric($_GET['sensorid'])){
		$sensorid = htmlspecialchars($_GET['sensorid']);
		$where = "WHERE sensor_id=$sensorid";
	} else {
		$where = '';
	}
	
	$sqlquery = sql("SELECT $selectValues FROM $sqlTable $where ORDER BY id $sqlOrderByType $limit;",'SELECT',$db_connection_array);
	
	header('Content-Type: application/json');
	
	if(!isset($_GET['values']) && !isset($_GET['orderby']) && isset($_GET['type']) && !empty($_GET['type']) && strcasecmp($_GET['type'], 'highcharts') == 0){
		// http://theonlytutorials.com/highcharts-load-json-data-via-ajax-php/
		$arrayID = array();
		$arrayDateTime = array();
		$arrayHumidity = array();
		$arrayTemperature = array();
		$arrayTemperatureF = array();
		$result = array();
		$j = 0;
		foreach ($sqlquery as $row => $measure){
			//highcharts needs name, but only once, so give a IF condition
			if($j == 0){
				$arrayHumidity['name'] = 'Humidity';
				$arrayTemperature['name'] = 'Temperature';
				$arrayTemperatureF['name'] = 'TemperatureF';
				$j++;
			}
			
			$timestamp = strtotime($measure['date_time']." UTC")*1000;  // Timestamp for JS
			$arrayHumidity['data'][] = array($timestamp,$measure['humidity']);
			$arrayTemperature['data'][] = array($timestamp,$measure['temperature']);
			$arrayTemperatureF['data'][] = array($timestamp,$measure['temperature_f']);
			
		}

		$arrayHumidity['data'] = (array_reverse($arrayHumidity['data']));
		$arrayTemperature['data'] = (array_reverse($arrayTemperature['data']));
		$arrayTemperatureF['data'] = (array_reverse($arrayTemperatureF['data']));
		
		array_push($result,$arrayHumidity);
		array_push($result,$arrayTemperature);
		array_push($result,$arrayTemperatureF);

		$json=json_encode($result,JSON_NUMERIC_CHECK);
	} else {
		$json=json_encode($sqlquery,JSON_NUMERIC_CHECK);
	}
	echo $json;
?>