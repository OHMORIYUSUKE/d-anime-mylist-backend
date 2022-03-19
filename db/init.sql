set client_encoding = 'UTF8';

CREATE TABLE mylists (
  id varchar primary key, 
  name varchar
);

CREATE TABLE mylist_contents (
  id varchar, 
  title varchar,
  image varchar,
  url varchar,
  primary key(id, title)
);