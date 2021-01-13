DROP TABLE IF EXISTS people_id;
CREATE TABLE people_id
                     (id_people INT PRIMARY KEY NOT NULL,
                      name TEXT NOT NULL,
                      face BYTEA NOT NULL);

DROP TABLE IF EXISTS events;
CREATE TABLE events
                     (id_event INT PRIMARY KEY NOT NULL,
                      name TEXT NOT NULL,
                      first_detection TIMESTAMP NOT NULL,
                      current_detection TIMESTAMP NOT NULL,
                      location TEXT NOT NULL);

DROP TABLE IF EXISTS recognitions;
CREATE TABLE recognitions
                     (id_recognition INT PRIMARY KEY NOT NULL,
                      name TEXT NOT NULL,
                      transaction_time TIMESTAMP NOT NULL);

DROP TABLE IF EXISTS logs;
CREATE TABLE logs
                     (name TEXT NOT NULL,
                      description TEXT NOT NULL,
                      transaction_time TIMESTAMP NOT NULL);

DROP TABLE IF EXISTS user;
CREATE TABLE users
                     (firstName TEXT NOT NULL,
                      lastName TEXT NOT NULL,
                      username TEXT NOT NULL,
                      gender TEXT NOT NULL,
                      password TEXT NOT NULL);

DROP TABLE IF EXISTS pics;
CREATE TABLE pics
                     (id_pic INT PRIMARY KEY NOT NULL,
                      orig_picture TEXT NOT NULL,
                      mime TEXT NOT NULL);

DROP TABLE IF EXISTS pics_data;
CREATE TABLE pics_data
                     (id_data INT PRIMARY KEY NOT NULL,
                      id_dependent INT NOT NULL,
                      label TEXT NOT NULL,
                      gender TEXT NOT NULL,
                      emote TEXT NOT NULL,
                      location TEXT NOT NULL);

INSERT INTO pics VALUES(1, '1111', '2222');
INSERT INTO pics VALUES(2, '1111', '2222');
INSERT INTO pics VALUES(3, 'unical_picture', 'unical_mime');

INSERT INTO pics_data VALUES(1, 3, 'some_label', 'None', 'None', 'None');
INSERT INTO pics_data VALUES(2, 3, 'some_label2', 'None', 'None', 'None');