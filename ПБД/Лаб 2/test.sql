CREATE OR REPLACE FUNCTION public.multi_acc_diets()
RETURNS TABLE (name_special varchar, avr real) AS $$
DECLARE cursor_enum CURSOR FOR SELECT age, special FROM account;
DECLARE cursor_enum_special CURSOR FOR SELECT DISTINCT special FROM account;
DECLARE count_value int;
DECLARE sum_value int;
BEGIN
count_value = 0;
sum_value = 0;
	FOR enum_values_special IN cursor_enum_special LOOP
		FOR enum_values IN cursor_enum LOOP
			IF enum_values.special = enum_values_special.special THEN
				sum_value := sum_value + enum_values.age;
				count_value := count_value + 1;
			END IF;
		END LOOP;
		avr := sum_value / count_value;
		name_special := enum_values_special.special;
		count_value = 0;
		sum_value = 0;
		RETURN NEXT;
	END LOOP;
	END
$$
LANGUAGE 'plpgsql';