--
-- Table `measurements` for dht22 sensors
--

CREATE TABLE IF NOT EXISTS measurements (
    id int auto_increment,
    sensor_id int DEFAULT NULL,
    temperature_f double DEFAULT NULL,
    temperature double DEFAULT NULL,
    humidity double DEFAULT NULL,
    date_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
