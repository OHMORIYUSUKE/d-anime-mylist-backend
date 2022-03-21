CREATE TABLE d_anime.mylists (
  id varchar not null primary key, 
  name varchar
);

CREATE TABLE d_anime.mylistContents (
  id varchar, 
  title varchar,
  image varchar,
  url varchar,
  primary key(id, title)
);