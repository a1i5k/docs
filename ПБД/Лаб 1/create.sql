CREATE TABLE account (
id integer AUTOINCREMENT NOT NULL,
	age integer -- more 0,
	height real,
	weight real,
	login varchar,
	password varchar
);
CREATE TABLE account (
id integer AUTOINCREMENT NOT NULL,
	name varchar,
	description varchar,
	age integer -- more 0,
	height real,
	weight real
);

CREATE TABLE history_diet (
id integer AUTOINCREMENT NOT NULL,
	id_account integer -- more 0,
	id_diet real
);