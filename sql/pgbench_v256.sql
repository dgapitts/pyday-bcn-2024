\set id random(1, 10000)
SELECT id, name, embedding <-> (select embedding from v256 where id = :id) as dot_product from v256 order by dot_product limit 100;
