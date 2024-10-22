CREATE TABLE users (
    id serial4,
    first_name varchar,
    last_name varchar,
    email varchar unique,
    password varchar,
    phone_number varchar null
);

INSERT INTO users VALUES
(default, 'ivan', 'ivanov', 'mail@mail.ru', 'qwerty', '+78005553535'),
(default, 'petr', 'petrov', 'anymail@mail.ru', '123', '+71234567890');
