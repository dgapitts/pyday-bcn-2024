\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v16 where id = :id) as dot_product from v16 order by dot_product limit 100;
