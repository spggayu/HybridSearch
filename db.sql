CREATE TABLE magazine_information (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publication_date DATE NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE magazine_content (
    id SERIAL PRIMARY KEY,
    magazine_id INT REFERENCES magazine_information(id),
    content TEXT NOT NULL,
    vector_representation FLOAT8[] -- Replace with your desired vector type
);