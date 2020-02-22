create or replace function test_func() --table func
	returns table(t1 varchar) as
	$$
		select cards.races as f
		from cards
	$$
	immutable
	language sql
	
select distinct test_func()	

--------------------------------------
create or replace function is_debuff_needed(cards) --scalar func
	returns boolean as
	$$
		with o1 as 
		(
			select distinct count(*) as overall
			from cards
		), 
		o2 as
		(
			select distinct count(*) as normal
			from cards
			where cards.attack + cards.health <= cards.manacost + 2
		)
		
		select 
			case when cast (max(o2.normal) as float) / cast (max(o1.overall) as float) * 100 > 85.0 then false
			else true
			end
		from o1, o2
	$$
	immutable
	language sql

select distinct is_debuff_needed(cards.*)
from cards

---------------------------------------
create or replace function what_can_i_do(m_value int)-- multi operator function
	returns table (id_card int, name_card varchar, id_add int, races varchar, ability varchar, rarity varchar, health int, attack int, manacost int)
	as
	$$
    begin
    	return query(select * from cards 
		where cards.manacost < m_value);
	end
	$$

	language plpgsql;
	
select what_can_i_do(15)

---------------------------------------
create or replace function recursia1(res int) -- recursive function
returns int 
as
$$
	begin
	if res < 3
	then 
		return 1;
	else 
		return recursia1(res-1)+recursia1(res-2);
	end if;
	end;
$$
language plpgsql;
	
select * from recursia1(6);

---------------------------------------

CREATE OR REPLACE PROCEDURE del_with_substr(substr varchar) -- keep procedure
LANGUAGE SQL
AS 
$$
	DELETE FROM winners
	WHERE winners.player_nickname like substr;
$$;

---------------------------------------

create or replace procedure recursia(res int) -- recursive procedure
	as
	$$
	declare
	var int;
	
	begin
	
	var = var + 1;
	
	if var < 10
	then 
		call recursia(var);
	else
		raise notice 'end';
	end if;
	
	end;
$$
language plpgsql
	
call recursia(0);

-----------------------------------------

CREATE OR REPLACE PROCEDURE find_constraints(tabling varchar) --cursor + meta
LANGUAGE plpgsql
AS 
$$
	declare 
	get_result float;
	tipo_table cursor (naming varchar) for
	select count(*)
       FROM pg_catalog.pg_constraint con
            INNER JOIN pg_catalog.pg_class rel
                       ON rel.oid = con.conrelid
            INNER JOIN pg_catalog.pg_namespace nsp
                       ON nsp.oid = connamespace
       WHERE rel.relname = naming;

	begin
	open tipo_table(tabling);
	fetch tipo_table into get_result;

	raise notice 'constraints num = %', get_result;
	end;
$$;

---------------------------------------
create or replace function c_i() --after trigger
returns trigger AS 
$emp_stamp$
    begin
        if new.id_player is null then
            raise exception 'id cannot be null';
        end if;
		
        if new.player_nickname is null then
            raise exception 'player cannot have null nickname';
        end if;

        new.last_date := current_timestamp;
        new.last_user := current_user;
        return new;
    end;
$emp_stamp$
language plpgsql;

create trigger check_insert after insert
on winners
for each row execute procedure c_i()

------------------------------------------
create or replace function m_i_d() --try of instead of trigger
returns trigger AS 
$$
    begin
        if new.id_player is null then
            raise exception 'id cannot be null';
        end if;
		
        if new.player_nickname is null then
            raise exception 'player cannot have null nickname';
        end if;
		
		--insert into test_trigger values (new.id_player, new.player_nickname);
		--select new.id_player, new.player_nickname;

        return new;
    end;
$$
language plpgsql;

create trigger make_insert instead of delete
on test_trigger
for each row execute procedure m_i_d()

