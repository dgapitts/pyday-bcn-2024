\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v32 where id = :id) as dot_product from v32 order by dot_product limit 100;
