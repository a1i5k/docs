CREATE TYPE special AS ENUM ('Болезнь', 'Здоровый');
ALTER TABLE account ADD COLUMN special special;