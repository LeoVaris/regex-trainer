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
  task_info TEXT,
  type INTEGER,
  position SERIAL
);

CREATE TABLE tests (
  id SERIAL PRIMARY KEY,
  task_id INTEGER REFERENCES tasks ON DELETE CASCADE,
  data TEXT,
  accept BOOLEAN
);

CREATE TABLE submissions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users,
  task_id INTEGER REFERENCES tasks ON DELETE CASCADE,
  submission TEXT,
  result TEXT,
  sent_at TIMESTAMP,
  status INTEGER
);