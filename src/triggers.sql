--- country validation check

CREATE OR REPLACE FUNCTION check_country() 
RETURNS trigger AS $check_country$
DECLARE
  curr_population int;
  curr_area float;
  max_population int;
  max_area float;
BEGIN

	SELECT INTO curr_population, curr_area
				SUM(c.population), SUM(c.area)
        FROM app_country as c
        WHERE c.continent_id = NEW.continent_id AND c.id != NEW.id;
				
	SELECT INTO max_population, max_area
				c.population, c.area
				FROM app_continent as c
				WHERE c.id = NEW.continent_id;
				
	IF curr_population is NULL then
		curr_population := 0;
	end if;
	
	if curr_area is NULL then
		curr_area := 0;
	end if;	
    
  IF curr_population + NEW.population > max_population THEN
    RAISE EXCEPTION 'Country populations cannot be more than continent population';
  END IF;

  IF curr_area + NEW.area > max_area THEN
    RAISE EXCEPTION 'Country areas cannot be more than continent area';
  END IF;

  RETURN NEW;
END;
$check_country$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS country_insert_or_update ON app_country;

CREATE TRIGGER country_insert_or_update
  BEFORE INSERT OR UPDATE
  ON app_country
  FOR EACH ROW
  EXECUTE PROCEDURE check_country();

--- city validation check

CREATE OR REPLACE FUNCTION check_city() 
RETURNS trigger AS $check_city$
DECLARE
  curr_population int;
  curr_area float;
  max_population int;
  max_area float;
BEGIN

	SELECT INTO curr_population, curr_area
				SUM(c.population), SUM(c.area)
        FROM app_city as c
        WHERE c.country_id = NEW.country_id AND c.id != NEW.id;
				
	SELECT INTO max_population, max_area
				c.population, c.area
				FROM app_country as c
				WHERE c.id = NEW.country_id;

  IF curr_population is NULL then
		curr_population := 0;
	end if;
	
	if curr_area is NULL then
		curr_area := 0;
	end if;	
    
  IF curr_population + NEW.population > max_population THEN
    RAISE EXCEPTION 'City populations cannot be more than country population';
  END IF;

  IF curr_area + NEW.area > max_area THEN
    RAISE EXCEPTION 'City areas cannot be more than country area';
  END IF;

  RETURN NEW;
END;
$check_city$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS city_insert_or_update ON app_city;

CREATE TRIGGER city_insert_or_update
  BEFORE INSERT OR UPDATE
  ON app_city
  FOR EACH ROW
  EXECUTE PROCEDURE check_city();