-- Update the city for venues using this
SELECT * FROM Venues AS v WHERE MBRContains (ST_Buffer(POINT(-15.615000,-56.093004), 0.2), v.latlon);