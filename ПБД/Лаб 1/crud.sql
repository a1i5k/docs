-- CREATE TYPE comb AS (
--     a       int,
--     b       int
-- );
-- ALTER TABLE public.account ADD comb_ comb;

INSERT INTO public.history_diet(id_account, id_diet) VALUES (1, 1);
UPDATE public.history_diet SET id_account=1, id_diet=1 WHERE WHERE id = 5;
DELETE FROM public.history_diet WHERE id = 5;
SELECT id, id_account, id_diet FROM public.history_diet;
