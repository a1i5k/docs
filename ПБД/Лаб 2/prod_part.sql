-- UPDATE account SET age = 1 WHERE id = 100 RETURNING age;

-- SELECT age, special, rank() OVER (order by age), row_number() OVER (order by age), dense_rank() OVER (order by age), ntile(4) OVER (order by age) FROM account;

-- CREATE OR REPLACE FUNCTION public.system_fun()
-- RETURNS text AS
-- 'SELECT * FROM current_query()'
-- LANGUAGE SQL volatile;

WITH RECURSIVE p(last_arrival, destination, point_arrival, found) AS (
  SELECT a_from.name,
         a_to.name,
         ARRAY[a_from.name],
         a_from.name = a_to.name
  FROM   point a_from, point a_to
  WHERE  a_from.name = 'A'
  AND    a_to.name = 'D'
  UNION ALL
  SELECT r.out,
         p.destination,
         (p.point_arrival || r.out),
         bool_or(r.out = p.destination) OVER ()
  FROM   way r, p
  WHERE  r.in = p.last_arrival
  AND    NOT r.out = ANY(p.point_arrival)
  AND    NOT p.found
)
SELECT point_arrival
FROM   p
WHERE  p.last_arrival = p.destination;


WITH RECURSIVE p(last_arrival, destination, point_arrival) AS (
  SELECT a_from.name,
         a_to.name,
         ARRAY[a_from.name]
--          a_from.name = a_to.name
  FROM   point a_from, point a_to
  WHERE  a_from.name = 'A'
  AND    a_to.name = 'D'
  UNION ALL
  SELECT r.out,
         p.destination,
         (p.point_arrival || r.out)
--          bool_or(r.out = p.destination) OVER ()
  FROM   way r, p
  WHERE  r.in = p.last_arrival
  AND    NOT r.out = ANY(p.point_arrival)
--   AND    NOT p.found
)
SELECT point_arrival
FROM   p
WHERE  p.last_arrival = p.destination;