\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v4 where id = :id) as dot_product from v4 order by dot_product limit 100;
