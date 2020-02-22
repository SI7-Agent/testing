create table empoyees (
	id_em int,
	fio varchar(350),
	birth date,
	otdel varchar (50));
	
create table empoyees_time (
	id_t int,
	sys_date date,
	weekday varchar(50),
	time_event time,
	type_out int);
	
insert into empoyees values (1, 'rab1', '1990-09-25', 'it');
insert into empoyees values (2, 'rab2', '1987-11-12', 'buch');
insert into empoyees values (3, 'rab3', '1964-05-11', 'it');
insert into empoyees values (4, 'rab4', '1996-09-01', 'buch');

insert into empoyees_time values (1, current_date, 'saturday', '9:03', 1);
insert into empoyees_time values (1, current_date, 'saturday', '9:20', 2);
insert into empoyees_time values (1, current_date, 'saturday', '10:00', 1);
insert into empoyees_time values (2, current_date, 'saturday', '10:20', 1);
insert into empoyees_time values (2, current_date, 'saturday', '11:00', 2);
insert into empoyees_time values (3, current_date, 'saturday', '9:29', 1);
insert into empoyees_time values (4, current_date, 'saturday', '8:56', 1);
insert into empoyees_time values (4, current_date, 'saturday', '12:20', 2);

create or replace function get_late()
returns float as
$$
	with late as(
		select id_em as res
		from empoyees join empoyees_time on empoyees.id_em = empoyees_time.id_t
		where (extract (hour from time_event) > 9 or extract (hour from time_event) = 9 and extract (minute from time_event) > 0) 
			and type_out = 1 and otdel = 'it'
		group by id_em)

	select avg(extract (year from current_date) - extract (year from birth)) from empoyees join late on id_em = res 
$$
language sql;

select get_late();

