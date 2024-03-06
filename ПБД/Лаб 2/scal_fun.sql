CREATE OR REPLACE FUNCTION public.scal_fun(min_weight integer)
RETURNS integer AS
'SELECT max(age) FROM public."account" WHERE weight > min_weight LIMIT 3'
LANGUAGE SQL volatile