create table addons(
	primary key (id_addon),
	id_addon serial not null,
	name_addon varchar(150) not null,
	date_addon date not null
);

create table cards(
	primary key (id_card),
	id_card serial not null,
	name_card varchar(150) not null,
	id_add int not null references addons,
	races varchar(100) not null,
	ability varchar(100) not null,
	rariry varchar(50) not null,
	health int not null,
			constraint negative_health
			check (health > 0),
	attack int not null,
			constraint negative_attack
			check (attack >= 0),
	manacost int not null
			constraint negative_manacost
			check (manacost >= 0)
);

create table modes(
	primary key (id_mode),
	id_mode serial not null,
	name_mode varchar(150) not null,
	costs varchar(50) not null
);

create table players(
	primary key (id_player),
	id_player serial not null,
	player_nickname varchar(75) not null
);

create table games(
	primary key (id_game),
	id_game serial not null,
	id_player_1 int not null references players,
			constraint negative_id_1
			check (id_player_1 > 0),
	id_player_2 int not null references players,
			constraint negative_id_2
			check (id_player_2 > 0),
	winner int not null,
			constraint winner_limit
			check ((winner > 0) and (winner <= 2)),
	id_mode int not null references modes,
			constraint negative_id_mode
			check (id_mode > 0)
);

create table histories(
	primary key (id_history),
	id_history serial not null,
	game_id int not null references games,
			constraint negative_game_id
			check (game_id > 0),
	turns_num int not null,
			constraint turns_limit
			check ((turns_num > 0) and (turns_num <= 45)),
	last_card_id int not null references cards,
			constraint negative_card_id
			check (last_card_id > 0)
);

create table gameplays(
	primary key (id_gameplay),
	id_gameplay serial not null,
	id_mode int not null references modes,
	gameplay_name varchar(150) not null
);


