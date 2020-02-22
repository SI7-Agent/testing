create table copy_test 
(
    id_addon int not null primary key,
    name_addon varchar not null,
    date_addon varchar not null
);

select * from json_parse('copy_test', '/home/osboxes/Downloads/sql_5/addons.json',
    'id_addon int',
    'name_addon varchar',
    'date_addon date');

select * from copy_test;
drop table copy_test;

