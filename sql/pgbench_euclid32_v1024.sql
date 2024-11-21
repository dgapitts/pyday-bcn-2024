\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v1024 where id = :id) as euclidean_product from v1024 order by euclidean_product limit 100;
