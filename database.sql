DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE NOT NULL
);

DROP TABLE IF EXISTS url_checks;
CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER NOT NULL,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at DATE NOT NULL,
    CONSTRAINT fk_url
        FOREIGN KEY(url_id) 
        REFERENCES urls(id)
        ON DELETE CASCADE
);