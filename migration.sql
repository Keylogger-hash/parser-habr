CREATE TABLE IF NOT EXISTS posts (id SERIAL PRIMARY KEY, text text,title text, date text, url text,
                                       author text, author_url text, hub text);
CREATE TABLE IF NOT EXISTS hubs(id serial,hub text);
