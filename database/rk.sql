create database rk2;

create table vacine
(
	primary key (id_vacine),
	id_vacine serial not null,
	name_vacine varchar(150) not null,
	descride_vacine varchar(150) not null
);

create table clinic
(
	primary key (id_clinic),
	id_clinic serial not null,
	name_clinic varchar(150) not null,
	date_clinic date not null,
	describe_clinic varchar(150) not null
);

create table baby
(
	primary key (id_baby),
	id_baby serial not null,
	name_baby varchar(150) not null,
	date_baby date not null,
	adress_baby varchar(150) not null,
	phone_baby varchar(150) not null
);

create table baby_vacine
(
	primary key (id_baby_vacine),
	id_baby_vacine serial not null,
	id_b serial not null references baby,
	id_v serial not null references vacine
);

create table clinic_vacine
(
	primary key (id_clinic_vacine),
	id_clinic_vacine serial not null,
	id_c serial not null references clinic,
	id_v serial not null references vacine
);

insert into baby values (1, 'Vasya', '01-01-1999', 'adress1', '8-926-688-52-96');
insert into baby values (2, 'Ilya', '01-01-1998', 'adress2', '8-926-688-52-95');
insert into baby values (3, 'Kirill', '01-01-2000', 'adress3', '8-926-688-52-94');
insert into baby values (4, 'Mixa', '01-01-2001', 'adress4', '8-926-688-52-93');
insert into baby values (5, 'Max', '01-01-2003', 'adress5', '8-926-688-52-92');
insert into baby values (6, 'Fedor', '01-01-2001', 'adress6', '8-926-688-52-91');
insert into baby values (7, 'Sergey', '01-01-1998', 'adress7', '8-926-688-52-90');
insert into baby values (8, 'Kolya', '01-01-2000', 'adress8', '8-926-688-52-89');
insert into baby values (9, 'Artur', '01-01-2002', 'adress9', '8-926-688-52-88');
insert into baby values (10, 'Katya', '01-01-1999', 'adress10', '8-926-688-52-87');

insert into clinic values (1, 'Super_Clinic', '01-01-1969', 'good clinic');
insert into clinic values (2, 'Mega_Clinic', '01-01-1953', 'very good clinic');
insert into clinic values (3, 'Ultra_Clinic', '01-01-1929', 'best clinic');
insert into clinic values (4, 'Norm_Clinic', '01-01-1978', 'usual clinic');
insert into clinic values (5, 'Uzas_Clinic', '01-01-1933', 'not good clinic');
insert into clinic values (6, 'Prosto_Clinic', '01-01-1955', 'clinic');
insert into clinic values (7, 'Nazvanie_Clinic', '01-01-1989', 'eche odna clinic');
insert into clinic values (8, 'Kolya_Clinic', '01-01-1991', 'eto tozhe clinic');
insert into clinic values (9, 'Siyanie_Clinic', '01-01-1902', 'you will like it');
insert into clinic values (10, 'Nikolson_Clinic', '01-01-1801', 'clinic?');

insert into vacine values (1, 'Super_Vacine', 'good vacine');
insert into vacine values (2, 'Mega_Vacine', 'very good vacine');
insert into vacine values (3, 'Ultra_Vacine', 'best vacine');
insert into vacine values (4, 'Norm_Vacine', 'usual vacine');
insert into vacine values (5, 'Uzas_Vacine', 'not good vacine');
insert into vacine values (6, 'Prosto_Vacine', 'vacine');
insert into vacine values (7, 'Nazvanie_Vacine', 'eche odna vacine');
insert into vacine values (8, 'Kolya_Vacine', 'eto tozhe vacine');
insert into vacine values (9, 'Siyanie_Vacine', 'you will like it');
insert into vacine values (10, 'Nikolson_Vacine', 'vacine?');

insert into baby_vacine values (1, 2, 5);
insert into baby_vacine values (2, 3, 4);
insert into baby_vacine values (3, 4, 8);
insert into baby_vacine values (4, 8, 2);
insert into baby_vacine values (5, 3, 5);
insert into baby_vacine values (6, 8, 1);
insert into baby_vacine values (7, 9, 7);
insert into baby_vacine values (8, 3, 1);
insert into baby_vacine values (9, 7, 7);
insert into baby_vacine values (10, 3, 8);

insert into clinic_vacine values (1, 5, 2);
insert into clinic_vacine values (2, 4, 3);
insert into clinic_vacine values (3, 8, 4);
insert into clinic_vacine values (4, 2, 8);
insert into clinic_vacine values (5, 5, 3);
insert into clinic_vacine values (6, 1, 8);
insert into clinic_vacine values (7, 7, 9);
insert into clinic_vacine values (8, 1, 3);
insert into clinic_vacine values (9, 7, 7);
insert into clinic_vacine values (10, 8, 3);

-----------------------------------------------

select name_baby, date_baby, phone_baby
from baby join baby_vacine on baby.id_baby = baby_vacine.id_b join vacine on baby_vacine.id_v = vacine.id_vacine
where ((select extract (year from baby.date_baby)) > '2000')
--выводит информацию о вакцинированных детях с годом рождения более, чем 2000

select distinct name_baby, date_baby, phone_baby, count(*) over (partition by baby_vacine.id_b) as number_vacine
from baby join baby_vacine on baby.id_baby = baby_vacine.id_b join vacine on baby_vacine.id_v = vacine.id_vacine
--выводит информацию о вакцинированных детях и количестве их вакцинаций

select distinct name_clinic, date_clinic describe_clinic
from (select *
	 from clinic join clinic_vacine on clinic.id_clinic = clinic_vacine.id_c 
	  join vacine on clinic_vacine.id_v = vacine.id_vacine join baby_vacine
	  on baby_vacine.id_v = vacine.id_vacine join baby on baby_vacine.id_b = baby.id_baby
	 where clinic.id_clinic > 1 and vacine.id_vacine > 3) as test
--выводит информацию о поликлинниках с порядковым номером > 1, в которых проводилась вакцинация вакцинами с порядковым номером > 3

-----------------------------------------------

create or replace procedure name_of_restrict(base text)
language sql 
as
$$
	SELECT con.conname
       FROM pg_catalog.pg_constraint con
	   INNER JOIN pg_catalog.pg_class rel
                       ON rel.oid = con.conrelid
            INNER JOIN pg_catalog.pg_namespace nsp
                       ON nsp.oid = connamespace
	WHERE contype = 'c' and rel.relname = text
$$;

call name_of_restrict('rk2')
--создает и вызывает непустую процедуру

