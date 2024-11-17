## Python venv setup and install `sqlalchemy psycopg2-binary pgvector pandas`

Setpu a local venv
```
~/projects/pyday-bcn-2024 main $ python3 -m venv venv
~/projects/pyday-bcn-2024 main $ source venv/bin/activate
(venv) ~/projects/pyday-bcn-2024 main $
```
install `sqlalchemy psycopg2-binary pgvector`
```
(venv) ~/projects/pyday-bcn-2024 main $  pip3 install sqlalchemy psycopg2-binary pgvector pandas
Collecting sqlalchemy
  Using cached SQLAlchemy-2.0.36-cp313-cp313-macosx_11_0_arm64.whl.metadata (9.7 kB)
Collecting psycopg2-binary
  Using cached psycopg2_binary-2.9.10-cp313-cp313-macosx_14_0_arm64.whl.metadata (4.9 kB)
...
```

Finally FYI these are versions I'm working with 
```
(venv) ~/projects/pyday-bcn-2024y main $ pip3 list installed
Package           Version
----------------- -----------
numpy             2.1.3
pandas            2.2.3
pgvector          0.3.6
pip               24.2
psycopg2-binary   2.9.10
python-dateutil   2.9.0.post0
pytz              2024.2
six               1.16.0
SQLAlchemy        2.0.36
typing_extensions 4.12.2
tzdata            2024.2
```
