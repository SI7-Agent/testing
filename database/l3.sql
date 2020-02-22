--create scalar python func

create or replace function py_skal(arg addons)
returns varchar(300)
as $$
        s1 = s2 = ""
        s1 = arg["name_addon"]
        s2 = arg["date_addon"]
        return s1 + " " + s2
$$ language plpython3u;

-----------------------------------------------------------------------
--create agregative func
create or replace function mul(state int, arg int)
returns int
as $$
	return state * arg
$$ language plpython3u;

create aggregate my_agr(int)
(
	sfunc = mul,
	stype = int,
	initcond = 1
);
-----------------------------------------------------------------------
--create table func
create or replace function my_table_func(from_l int, to_l int)
returns table(Addon text, Year int)
as $$
p = plpy.execute("select * from public.addons")
result = []
for i in range (len(p)):
	yy = int(p[i]["date_addon"][:4])
	nn = str(p[i]["name_addon"])
	if (len(str(yy)) + len(str(nn)) > from_l and len(str(yy)) + len(str(nn)) < to_l):
		result.append({"addon": str(nn).strip(), "year": str(yy).rstrip()})
return result
$$ language plpython3u;
-----------------------------------------------------------------------
--create procedure
create or replace procedure my_proc(name1 text, name2 text) 
as $$
r = plpy.execute("select * from " + name1) 
res = []
count = []
for i in range (len(r)):
	if (r[i]["attack"] not in res):
		res.append(r[i]["attack"])
		count.append[1] 
	else:
		count[res.index(r[i]["attack"])] += 1
for i in range (len(res)):
	plpy.execute("insert into " + str(name2) + " values (" + str(res[i]) + "," + str(count[i]) + ")")
$$ language plpython3u;

--create public.counts(attack int, count int);
--call my_proc1('public.cards', 'public.counts');
--select * from public.counts order by attack;
----------------------------------------------------------------------
--create trigger
create or replace function tr_before()
returns trigger
as $$
if TD["event"] == "DELETE":
	a = str(TD["old"]["id_history"]) 
	b = str(TD["old"]["game_id"]) 
	c = str(TD["old"]["turns_num"]) 
	d = str(TD["old"]["last_card_id"]) 
	plpy.execute("insert into public.deleted_history values (" + a + ", " + b + ", " + c + ", " + d + ")")
return "OK"
$$ language plpython3u;

create trigger trig before delete on public.histories
for each row execute procedure tr_before(); 
-----------------------------------------------------------------------
--create user type
create type game_cut as
(
	winner varchar,
	loser varchar,
	name_mode varchar
);

create or replace function get_cut_info (id_ integer)
returns game_cut
as $$
plan = plpy.prepare("select winner, id_player_1, id_player_2, id_mode from games where id_game = $1", ["int"])
cr = plpy.execute(plan, [id_])
res = [] 
if (cr[0]["winner"]) == 1:
	res.append(cr[0]["id_player_1"])
	res.append(cr[0]["id_player_2"])
else:
	res.append(cr[0]["id_player_2"])
	res.append(cr[0]["id_player_1"])
res.append(cr[0]["id_mode"])

plan_get_name = plpy.prepare("select player_nickname from players where id_player = $1", ["int"])
plan_get_mode = plpy.prepare("select name_mode from modes where id_mode = $1", ["int"])

c1 = plpy.execute(plan_get_name, [res[0]])
c2 = plpy.execute(plan_get_name, [res[1]])
c3 = plpy.execute(plan_get_mode, [res[2]])

return (c1[0]["player_nickname"], c2[0]["player_nickname"], c3[0]["name_mode"])
$$ language plpython3u; 
-----------------------------------------------------------------------
