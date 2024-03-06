CREATE OR REPLACE FUNCTION public.multi_acc_diets()
RETURNS TABLE (name_special varchar, avr real) AS $$
DECLARE cursor_enum CURSOR FOR SELECT age, special FROM account;
DECLARE count_value_health int;
DECLARE sum_value_health int;
DECLARE count_value_pain int;
DECLARE sum_value_pain int;
BEGIN
count_value_pain = 0;
sum_value_pain = 0;
count_value_health = 0;
sum_value_health = 0;
	FOR enum_values IN cursor_enum LOOP
	IF enum_values.special = 'Здоровый' THEN
		sum_value_health := sum_value_health + enum_values.age;
		count_value_health := count_value_health + 1;
	ELSE
		sum_value_pain := sum_value_pain + enum_values.age;
		count_value_pain := count_value_pain + 1;
	END IF;
	END LOOP;
	name_special := 'Здоровый';
	avr := sum_value_health / count_value_health;
	RETURN NEXT;
	name_special := 'Болезнь';
	avr := sum_value_pain / count_value_pain;
	RETURN NEXT;
	END
$$
LANGUAGE 'plpgsql';