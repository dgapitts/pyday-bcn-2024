\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v16 where id = :id) as euclidean_product from v16 order by euclidean_product limit 100;
