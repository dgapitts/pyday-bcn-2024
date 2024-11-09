## Mysql pk versus secondary index efficiency

### Generating randomo datasets the mysql way

Apparently this isn't easy i.e. based on this [how-to-generate-1000000-rows-with-random-data stackoverflow post](https://stackoverflow.com/questions/25098747/how-to-generate-1000000-rows-with-random-data):

```
create database test;
use test;

CREATE TABLE `data` 
(
  `id`         bigint(20) NOT NULL      AUTO_INCREMENT,
  `id2`        bigint(20)               DEFAULT NULL,
  `datetime`   timestamp  NULL          DEFAULT CURRENT_TIMESTAMP,
  `channel`    int(11)                  DEFAULT NULL,
  `value`      float                    DEFAULT NULL,

  PRIMARY KEY (`id`)
);


DELIMITER $$
CREATE PROCEDURE generate_data()
BEGIN
  DECLARE i INT DEFAULT 0;
  WHILE i < 1000 DO
    INSERT INTO `data` (`datetime`,`value`,`channel`) VALUES (
      FROM_UNIXTIME(UNIX_TIMESTAMP('2014-01-01 01:00:00')+FLOOR(RAND()*31536000)),
      ROUND(RAND()*100,2),
      1
    );
    SET i = i + 1;
  END WHILE;
END$$
DELIMITER ;

CALL generate_data();
```

NB Script here : [sql/demo01-mysql-simple-1000-data-table.sql](../sql/demo01-mysql-simple-1000-data-table.sql)

next to demo the secondary index affect add a secondary index on column id2 


```
update data set id2 = id where 1=1;
create index data_idx on data(id2);
create unique index data_idx_uniq on data(id2);
```

and then run `show index data;`

```
mysql> show index from data;
+-------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name      | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| data  |          0 | PRIMARY       |            1 | id          | A         |        1000 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
| data  |          0 | data_idx_uniq |            1 | id2         | A         |        1000 |     NULL |   NULL | YES  | BTREE      |         |               | YES     | NULL       |
| data  |          1 | data_idx      |            1 | id2         | A         |        1000 |     NULL |   NULL | YES  | BTREE      |         |               | YES     | NULL       |
+-------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
3 rows in set (0.01 sec)
```


now for individual short operations (single value lookups) it is hard to see the diference - at least at 1/100 second level


```
mysql> explain analyze select * from data where id2 = 345;
+-------------------------------------------------------------------------------------------------------+
| EXPLAIN                                                                                               |
+-------------------------------------------------------------------------------------------------------+
| -> Rows fetched before execution  (cost=0.00..0.00 rows=1) (actual time=0.000..0.001 rows=1 loops=1)
 |
+-------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> explain analyze select * from data where id = 345;
+-------------------------------------------------------------------------------------------------------+
| EXPLAIN                                                                                               |
+-------------------------------------------------------------------------------------------------------+
| -> Rows fetched before execution  (cost=0.00..0.00 rows=1) (actual time=0.000..0.000 rows=1 loops=1)
 |
+-------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```


but this is more telling

```
mysql> explain analyze select * from data where id2 > 800;
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| EXPLAIN                                                                                                                                                                        |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| -> Index range scan on data using data_idx_uniq over (800 < id2), with index condition: (`data`.id2 > 800)  (cost=90.26 rows=200) (actual time=0.065..0.645 rows=200 loops=1)
 |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)

mysql> explain analyze select * from data where id > 800;
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| EXPLAIN                                                                                                                                                                                                                           |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| -> Filter: (`data`.id > 800)  (cost=40.35 rows=200) (actual time=0.081..0.358 rows=200 loops=1)
    -> Index range scan on data using PRIMARY over (800 < id)  (cost=40.35 rows=200) (actual time=0.077..0.315 rows=200 loops=1)
 |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### Retesting with 'explain FORMAT=JSON' - can see that secondary index is 3.5 times more expensive

Next I tested using 

```
explain FORMAT=JSON select * from data where id > 800;
explain FORMAT=JSON select * from data where id2 > 800;
```

Noew wsing the id (i.e. the PK)

> Primary Key Index (Clustered Index): In InnoDB, the table data is stored in a B-tree structure that is organized based on the primary key. This is called the clustered index. Every row in the table is physically stored according to the order of the primary key.

so we have direct access to the "index orientated table" and lower "read_cost": "20.35"

```
        "read_cost": "20.35",
        "eval_cost": "20.00",
        "prefix_cost": "40.35",
        "data_read_per_join": "6K"
      },
```


vs the almost identical unique index `id2`  we see x3.5 times higher read cost
```
      "cost_info": {
        "read_cost": "70.26",
        "eval_cost": "20.00",
        "prefix_cost": "90.26",
        "data_read_per_join": "6K"
      },
```

> Secondary indexes in InnoDB are also B-trees, but they do not store the actual row data. Instead, they store the indexed column(s) and a reference to the corresponding primary key value.

Note for completeness: Here is the full output
```
mysql> explain FORMAT=JSON select * from data where id2 > 800;

 {
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "90.26"
    },
    "table": {
      "table_name": "data",
      "access_type": "range",
      "possible_keys": [
        "data_idx_uniq",
        "data_idx"
      ],
      "key": "data_idx_uniq",
      "used_key_parts": [
        "id2"
      ],
      "key_length": "9",
      "rows_examined_per_scan": 200,
      "rows_produced_per_join": 200,
      "filtered": "100.00",
      "index_condition": "(`test`.`data`.`id2` > 800)",
      "cost_info": {
        "read_cost": "70.26",
        "eval_cost": "20.00",
        "prefix_cost": "90.26",
        "data_read_per_join": "6K"
      },
      "used_columns": [
        "id",
        "id2",
        "datetime",
        "channel",
        "value"
      ]
    }
  }
}
```

and
```
mysql> explain FORMAT=JSON select * from data where id > 800;

 {
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "40.35"
    },
    "table": {
      "table_name": "data",
      "access_type": "range",
      "possible_keys": [
        "PRIMARY"
      ],
      "key": "PRIMARY",
      "used_key_parts": [
        "id"
      ],
      "key_length": "8",
      "rows_examined_per_scan": 200,
      "rows_produced_per_join": 200,
      "filtered": "100.00",
      "cost_info": {
        "read_cost": "20.35",
        "eval_cost": "20.00",
        "prefix_cost": "40.35",
        "data_read_per_join": "6K"
      },
      "used_columns": [
        "id",
        "id2",
        "datetime",
        "channel",
        "value"
      ],
      "attached_condition": "(`test`.`data`.`id` > 800)"
    }
  }
}
```

