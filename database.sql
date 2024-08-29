DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATE NOT NULL
);

DROP TABLE IF EXISTS url_checks;
CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id integer NOT NULL,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at DATE NOT NULL
);