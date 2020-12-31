INSERT INTO tasks (name, task_info, type) VALUES ('Tehtävä 1', 'Toteuta lauseke, joka hyväksyy kaikki merkkijonot, jotka sisältävät ainoastaan merkkiä <code>a</code>', 1);
INSERT INTO tasks (name, task_info, type) VALUES ('Ohje 1', 'Komento <code>+</code> matchaa kaikki merkit', 2);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'aaaa', TRUE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'aa', TRUE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'ab', FALSE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'b', FALSE);
INSERT INTO tests (task_id, data, accept) VALUES (1, 'c', FALSE);