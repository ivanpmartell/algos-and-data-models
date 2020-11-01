-- Update the city for venues using this
SELECT * FROM Venues AS v WHERE MBRContains (ST_Buffer(POINT(-15.615000,-56.093004), 0.2), v.latlon);

DROP PROCEDURE IF EXISTS AssignCities;
DELIMITER ;;
USE assignment1;;
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

SELECT Count(id) FROM Venues WHERE assignedCity IS NOT NULL;
select routine_name from information_schema.routines where routine_type = 'PROCEDURE';

-- POWER BI JOIN ALL TABLES QUERY TODO: Change SELECT * to make the columns have readable names
SELECT * FROM Checkins LEFT JOIN Venues ON Checkins.venueId = Venues.id LEFT JOIN Cities ON Cities.id = Venues.assignedCity LEFT JOIN Countries ON Countries.code = Cities.countryCode WHERE Venues.assignedCity IS NOT NULL;

SELECT Checkins.userId as CheckinUser,
       Checkins.utcTime as CheckinUTCTime,
       Checkins.utcOffset as CheckinUTCOffset,
       Checkins.localDatetime as CheckinTime,
       Venues.category as VenueCategory,
       X(Venues.latlon) as VenueLatitude,
       Y(Venues.latlon) as VenueLongitude,
       Cities.name as City,
       X(Cities.latlon) as CityLatitude,
       Y(Cities.latlon) as CityLongitude,
       Cities.isNationalCapital as isNationalCapital,
       Cities.isProvincialCapital as isProvincialCapital,
       Cities.isEnclave as isEnclave,
       Countries.code as CountryCode,
       Countries.name as Country
FROM Checkins
LEFT JOIN Venues
ON Checkins.venueId = Venues.id
LEFT JOIN Cities
ON Cities.id = Venues.assignedCity
LEFT JOIN Countries
ON Countries.code = Cities.countryCode
WHERE Venues.assignedCity IS NOT NULL;