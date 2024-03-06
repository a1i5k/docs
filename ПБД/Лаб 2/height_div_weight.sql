CREATE FUNCTION height_div_weight (user_id integer)
RETURNS TABLE(age integer, div real) AS $$
SELECT age, height/weight FROM account WHERE id=user_id
$$ lANGUAGE SQL