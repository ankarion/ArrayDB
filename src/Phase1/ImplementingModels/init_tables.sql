drop table AuthorLists;
drop table Contain;
drop table Bibligrophies;
drop table Repositories;
drop table Articles;
drop table Authors;

create table Repositories(
	id serial primary key,
	url varchar,
	name varchar
);
create Table Articles(
	id serial,
	venue varchar,
	year integer not null default 1900,
	title varchar,
	primary key(id)
);
create table Contain(
	repository_id integer not null,
	article_id integer,
       	foreign key(repository_id) references Repositories(id),
	foreign key(article_id) references Articles(id)
);
create table Bibligrophies(
	article_id integer,
	reference_id integer,
	foreign key (article_id) references Articles(id),
	foreign key (reference_id) references Articles(id)
);
create table Authors(
	id serial,
	name varchar not null default '',
	primary key(id)
);
create table AuthorLists(
	author_id integer,
	article_id integer,
	foreign key(author_id) references Authors(id),
	foreign key(article_id) references Articles(id)
);
