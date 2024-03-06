CREATE OR REPLACE FUNCTION public.multi_acc_diets(user_id integer)
RETURNS TABLE (diet_id integer, name_diet varchar) AS $$
	BEGIN
	IF user_id = 1 THEN
	UPDATE account SET comb_.a = 1 WHERE id = user_id;
	END IF;
	
	RETURN QUERY
	SELECT d.id, d.name
	FROM history_diet AS h
		JOIN diet AS d ON h.id_diet = d.id
	WHERE h.id_account = user_id;
	END
$$
LANGUAGE 'plpgsql';