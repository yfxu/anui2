CREATE TABLE IF NOT EXISTS sneks
(
    snek_id         SERIAL PRIMARY KEY,
    user_id_snekker BIGINT,
    user_id_snekked BIGINT
);