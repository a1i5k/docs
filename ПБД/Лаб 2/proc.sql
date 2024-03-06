CREATE OR REPLACE PROCEDURE public.create_table(tablename varchar(100))
AS $$
BEGIN
IF length(tablename) > 3 THEN
EXECUTE format('CREATE TABLE %I (id integer PRIMARY KEY, title varchar(100))', tablename);
ELSE RAISE EXCEPTION USING errcode='E0001',
message='Длина меньше 3';
END IF;

EXCEPTION WHEN SQLSTATE '42P07' THEN
RAISE EXCEPTION USING errcode='E0002',
message='Таблица уже существует';
END
$$
LANGUAGE 'plpgsql';