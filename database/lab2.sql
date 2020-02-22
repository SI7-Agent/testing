select distinct*
from cards
where (cards.attack > cards.manacost) and (cards.manacost < 3)
---
select distinct*
from addons
where ((select extract (year from addons.date_addon)) between '2015' and '2017')
order by addons.date_addon
---
with tmp as 
(
	select distinct gameplays.gameplay_name
	from gameplays
	where (gameplays.gameplay_name like '%deck on the go%')
)

select row_number()over() as id_gameplays, gameplay_name
from tmp
---
select distinct *
from players
where players.id_player in
(
	select games.id_player_1
	from games
	where games.winner = 1
)
order by players.id_player
---
select distinct cards.name_card
from cards
where exists
(
	select distinct histories.last_card_id
	from histories
	where (histories.last_card_id = cards.id_card) and (cards.id_add = 10)
)
---
select cards.id_add, cards.name_card, cards.races, cards.rarity, cards.attack, cards.manacost
from cards
where cards.manacost > ALL
(
	select cards.attack
	from cards
	where cards.id_add = 6
)
order by cards.id_add
---
select avg(cast (cards.attack as float)) as Average_Attack_per_addon, 
	avg(cast (cards.health as float)) as Average_Health_per_addon, 
	avg(cast (cards.manacost as float)) as Average_Manacost_per_addon
from cards
group by cards.id_add
---
select players.player_nickname,
	(
		select min (histories.turns_num)
		from histories
		where (games.id_game = histories.game_id) and (games.winner = 2)
	) as Min_turns_for_sec_guy,
	(
		select max (histories.turns_num)
		from histories
		where (games.id_game = histories.game_id) and (games.winner = 2)
	) as Max_turns_for_sec_guy
from games join histories on games.id_game = histories.game_id join players on games.id_player_2 = players.id_player
where winner = 2
---
select addons.name_addon,
	case 
		when extract(year from addons.date_addon) = 2019 then 'New addon'
		when extract(year from addons.date_addon) = 2018 then 'Actual addon'
		else 'Wild addon'
	end as class_addon
from addons
---
select cards.name_card, cards.rarity, cards.attack, cards.health, cards.manacost, 
	case
		when cards.attack + cards.attack < cards.manacost 
			or ((cards.attack + cards.attack < 3) and cards.manacost = 0) then 'Too weak card'
		when cards.attack + cards.attack < 2*cards.manacost 
			or ((cards.attack + cards.attack < 5) and cards.manacost = 0) then 'Playable card'
		when (cards.attack + cards.attack > 3*cards.manacost) 
			or ((cards.attack + cards.attack > 5) and cards.manacost = 0) then 'Overpowered card'
		else 'Balanced card'
	end as balance_of_card
from cards
---
select distinct players.id_player, players.player_nickname
into temp winners
from players join games on players.id_player = (case when games.winner = 1 then games.id_player_1
	else games.id_player_2 end)
where games.id_mode = 4 or games.id_mode = 5
order by players.id_player
---
select *
from cards join
(
	select distinct last_card_id as id_card
	from histories
	where 500 < histories.last_card_id 
	order by histories.last_card_id
) as ll_req on ll_req.id_card = cards.id_card
---
select *
from players
where players.id_player in
	(
		select case when games.winner = 1 then games.id_player_1
			else games.id_player_2 end as id_player
		from games, histories

		where id_game = game_id and histories.last_card_id in (
				select (id_card)
				from (
						select id_add, id_card, manacost
						from cards 
						where (cards.attack between 15 and 25) and (cards.id_add = 3)
				) as name1
				where manacost < (select avg(manacost)
								  from cards)
		) 
	)
---
with tmp as(
select distinct id_history, id_mode, 
	cast(avg(histories.turns_num)over(partition by games.id_mode) as float) as avg_per_mode_turns,
	cast(avg(histories.turns_num)over() as float) as avg_turns,
	max(histories.turns_num)over(partition by games.id_mode) as max_turns, 
	min(histories.turns_num)over(partition by games.id_mode) as min_turns,
	(sum(histories.turns_num)/count(*)) as name2
from histories join games on games.id_game = histories.game_id
	group by histories.id_history, games.id_mode
)
select distinct id_history, id_mode, avg_per_mode_turns, avg_turns, max_turns, min_turns
from tmp
where tmp.avg_turns > tmp.name2

order by tmp.id_history

---
select id_history, id_mode, 
	cast(avg(histories.turns_num)over(partition by games.id_mode) as float) as avg_per_mode_turns,
	cast(avg(histories.turns_num)over() as float) as avg_turns,
	max(histories.turns_num)over(partition by games.id_mode) as max_turns, 
	min(histories.turns_num)over(partition by games.id_mode) as min_turns
from histories join games on games.id_game = histories.game_id
group by histories.id_history, games.id_game
having cast(avg(histories.turns_num) as int) >
(
	select (sum(histories.turns_num)/count(*))
	from histories
)
order by id_history
---
insert into games values((select count(*) from games)+1, 295, 376, 1, 4);
---
insert into winners(id_player, player_nickname)
	(select 
		(select max(id_player)
		from winners
	 	where player_nickname like '%sho%a%')
	, (select player_nickname
		from winners
		where id_player = (select (select max(id_player)
				from winners
	 			where player_nickname like '%sho%a%'))
		))
---
update winners
set id_player = winners.id_player * 1000
where winners.id_player = 5
---
update winners
set id_player = 
(
	select (min(winners.id_player) - 1)
	from winners
)
where winners.id_player = 5000
---
delete from winners
where winners.id_player > 999
---
delete from winners
where id_player in
(
	select id_player
	from winners join games on
		(case when games.winner = 1 then games.id_player_2 = winners.id_player
	else games.id_player_1 = winners.id_player end)
)
---
with table_virazhenie(add_name, card_name, ability, rarity) as
(
	select addons.name_addon, cards.name_card, cards.ability, cards.rarity
	from cards join addons on addons.id_addon = cards.id_add
	where ((cards.ability like '%steal%' or cards.ability like '%fury%') 
		and cards.rarity like '%gendary%') or 
		(cards.ability like '%shield%' 
			and (cards.rarity like '%are%' or cards.rarity like '%pic%'))
)
	
select * 
from table_virazhenie
---
select row_number()over() as rn, manacost
into temp test_rec
from cards join histories on id_card = last_card_id;

with recursive recurs (rn, m_cost, res) as
 (
 	select rn, test_rec.manacost, test_rec.manacost
	from test_rec
	where rn = 1
	  
	union all
	 
	select test_rec.rn, test_rec.manacost, test_rec.manacost+recurs.res
	from recurs join test_rec on recurs.rn+1 = test_rec.rn
 )
 
 select res from recurs
 where recurs.rn = (select max(recurs.rn) from recurs)
---
select distinct addons.name_addon, 
	cast(avg(cards.attack)over(partition by cards.id_add) as int) as avg_attack,
	cast(avg(cards.health)over(partition by cards.id_add) as int) as avg_health,
	cast(avg(cards.manacost)over(partition by cards.id_add) as int) as avg_mana,
	count(*)over(partition by cards.id_add)
from addons join cards on addons.id_addon = cards.id_add
order by addons.name_addon
---
with tmp as
(
 	select *, 
		row_number()over(partition by id_gameplay) as mark
  	from test_dubles
)

select *
into no_dubles
from tmp
where mark = 1;

//OR

with tmp as
(
	select id_gameplay,
    		row_number()over(order_by id_gameplay) as row_num,
    		rank()over(order_by id_gameplay) as rank
  	from test_dubles
)
select *
into no_dubles
from tmp
where row_num = rank;
---