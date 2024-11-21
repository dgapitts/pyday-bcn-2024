\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v512 where id = :id) as euclidean_product from v512 order by euclidean_product limit 100;
