DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS tests CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY, 
  username TEXT, 
  password TEXT,
  status INTEGER
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  name TEXT,
  task_info TEXT
);

CREATE TABLE tests (
  id SERIAL PRIMARY KEY,
  task_id INTEGER REFERENCES tasks,
  data TEXT,
  accept BOOLEAN
);

CREATE TABLE submissions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users,
  task_id INTEGER REFERENCES tasks,
  submission TEXT,
  result TEXT
);

INSERT INTO tasks (name, task_info) VALUES ('Tehtävä 1', 'Toteuta lauseke, joka hyväksyy kaikki merkkijonot, jotka sisältävät ainoastaan merkkiä <code>a</code>');
INSERT INTO tests (task_id, data, accept) VALUES (1, 'aaaa', TRUE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'aa', TRUE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'ab', FALSE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'b', FALSE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'c', FALSE);