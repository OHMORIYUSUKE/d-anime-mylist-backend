SET client_encoding = 'UTF8';
SET TIME ZONE 'Asia/Tokyo';

CREATE TABLE mylists (
  id varchar primary key, 
  name varchar,
  createdAt timestamp with time zone
);

CREATE TABLE mylistContents (
  id varchar, 
  title varchar,
  image varchar,
  url varchar,
  primary key(id, title)
);