-- Update the city for venues using this
SELECT * FROM Venues AS v WHERE MBRContains (ST_Buffer(POINT(-15.615000,-56.093004), 0.2), v.latlon);

DROP PROCEDURE IF EXISTS AssignCities;
DELIMITER ;;
USE Electronics;;
CREATE PROCEDURE AssignCities()
BEGIN
DECLARE citiesAmount INT;
DECLARE i INT;
DECLARE totalSum INT;
DECLARE currentSum INT;
DECLARE currentCityId INT;
DECLARE currentCityLatlon POINT;
SELECT COUNT(id) FROM Cities INTO citiesAmount;
SET i = 0;
SET totalSum = 0;
WHILE i < citiesAmount DO
    SELECT id, latlon INTO currentCityId, currentCityLatlon FROM Cities LIMIT i,1;
    SELECT COUNT(*) INTO currentSum FROM Venues WHERE (assignedCity IS NULL AND MBRContains (ST_Buffer(currentCityLatlon, 0.13), latlon));
    SET totalSum = totalSum + currentSum;
    SET i = i + 1;
END WHILE;
SELECT totalSum;
END;
;;
DELIMITER ;
CALL AssignCities();