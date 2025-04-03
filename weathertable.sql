CREATE TABLE IF NOT EXISTS weather_data(
    id SERIAL PRIMARY KEY,
    city varchar(25) NOT NULL,
    date date NOT NULL,
    weather varchar(30) NOT NULL,
    temp_high float NOT NULL,
    temp_low float NOT NULL,
    temp_avg float NOT NULL,
    humidity int NOT NULL
);
TRUNCATE weather_data RESTART IDENTITY;