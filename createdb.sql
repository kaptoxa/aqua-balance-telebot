create table drunk(
    id integer primary key,
    mdate datetime,
    drink text,
    volume integer,
    user_id integer,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

create table users(
    id integer primary key,
    name varchar(255),
    norm integer,
    glass integer,
    bottle integer
);


