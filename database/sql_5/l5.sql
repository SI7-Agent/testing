copy (select to_jsonb(cards.*) from cards)
to '/home/osboxes/Downloads/sql_5/cards.json';

copy (select to_jsonb(addons.*) from addons)
to '/home/osboxes/Downloads/sql_5/addons.json';

copy (select to_jsonb(gameplays.*) from gameplays)
to '/home/osboxes/Downloads/sql_5/gameplays.json';

copy (select to_jsonb(games.*) from games)
to '/home/osboxes/Downloads/sql_5/games.json';

copy (select to_jsonb(histories.*) from histories)
to '/home/osboxes/Downloads/sql_5/historis.json';

copy (select to_jsonb(modes.*) from modes)
to '/home/osboxes/Downloads/sql_5/modes.json';

copy (select to_jsonb(players.*) from players)
to '/home/osboxes/Downloads/sql_5/players.json';

create or replace function json_parse(tablename text, path text, variadic arr text[])
returns int
as $$
    p = ""
    for i in range(len(arr)):
        p+= arr[i]
        if i != len(arr)-1:
            p += ", "
    file = open(path, "r")
    for s in file:
        plpy.execute("INSERT INTO " + tablename + " SELECT * from jsonb_to_record('" + s + "') as x ( " + p + " );")
    return 0
$$ language plpython3u;

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
