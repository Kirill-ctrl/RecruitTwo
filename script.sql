CREATE TABLE question_list(
    id SERIAL PRIMARY KEY,
    code SMALLINT UNIQUE NOT NULL
);

CREATE TABLE question(
    id SERIAL PRIMARY KEY,
    quest_text TEXT NOT NULL,
    question_list_id BIGINT REFERENCES question_list(id)
    pseudonym varchar(64) NOT NULL
);

INSERT INTO question_list(code) VALUES
	(100),
	(200),
	(300),
    (400);

INSERT INTO question(quest_text, question_list_id, pseudonym) VALUES
('Python - интерпретируемый язык?', 1, 'PythonInterpreter')
('В чем отличие Flask от Django?', 1, 'FlaskOrDjango')
('Как называются хеш-таблицы в Python?', 1, 'HashTable'),
('Как работает асинхронность в Python?', 1, 'Async'),
('Как осуществляется тестирование в Python?', 1, 'PythonTesting'),
('Как осуществляется отладка в Python?', 1, 'PythonDebugging');

INSERT INTO question(quest_text, question_list_id, pseudonym) VALUES
('Знания HTML', 2, 'HTML'),
('Знания CSS', 2, 'CSS'),
('Знания JS', 2, 'JS'),
('Фремфорки JS и для чего они нужны?', 2, 'FrameworkJS');

INSERT INTO question(quest_text, question_list_id, pseudonym) VALUES
('Основные методы HTTP', 3, 'HTTP_Protocol'),
('Протокол FTP', 3, 'FTP_Protocol'),
('Для чего нужен Postman?', 3, 'Postman'),
('Как осуществляется работа приложения через Ajax', 3, 'Ajax'),
('Что такое SPA?', 3, 'SPA');

INSERT INTO question(quest_text, question_list_id, pseudonym) VALUES
('Для чего нужен GIT?', 4, 'GIT'),
('Отслеживаемая и неотслеживаемые зоны', 4, 'Traceable_and_non_tracing'),
('Какие бывают виды конфликтов?', 4, 'Conflicts'),
('Как скопировать к себе сразу все содержимое с удаленного источника?', 4, 'CopyProject');

CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	name text NOT NULL,
	email text UNIQUE NOT NULL,
	psw text NOT NULL,
	status text NOT NULL,
);

CREATE TABLE token(
	id SERIAL PRIMARY KEY,
	token_text text NOT NULL,
	user_id BIGINT REFERENCES users(id),
	token_status boolean DEFAULT FALSE,
	token_time timestamp,
	save_temp date
)

CREATE TABLE employer(
	id SERIAL PRIMARY KEY,
	employer_name varchar(32) NOT NULL,
	city varchar(32) NOT NULL,
	users_id INTEGER REFERENCES users(id)
);


CREATE TABLE applicant(
	id SERIAL PRIMARY KEY,
	applicant_name varchar(32) NOT NULL,
	city varchar(32) NOT NULL,
	age INTEGER NOT NULL,
	email text NOT NULL,
	question_list_code SMALLINT REFERENCES question_list(code),
	employer_id BIGINT REFERENCES employer(id)
	accept BOOL NOT NULL DEFAULT FALSE,
	users_id INTEGER REFERENCES users(id)
);


CREATE TABLE answer(
    user_id INTEGER REFERENCES applicant(id),
    text_answer text,
    id_quest INTEGER REFERENCES question(id)
);
