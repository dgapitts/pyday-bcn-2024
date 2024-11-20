\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v8 where id = :id) as dot_product from v8 order by dot_product limit 100;
