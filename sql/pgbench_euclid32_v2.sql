\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v2 where id = :id) as euclidean_product from v2 order by euclidean_product limit 100;
