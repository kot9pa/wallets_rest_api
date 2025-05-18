CREATE TABLE IF NOT EXISTS wallets (
        wallet_uuid VARCHAR NOT NULL,
        balance INTEGER NOT NULL,
        id SERIAL NOT NULL,
        PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS operations (
        operation_type operationtype NOT NULL,
        amount INTEGER NOT NULL,
        wallet_id INTEGER NOT NULL,
        id SERIAL NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(wallet_id) REFERENCES wallets (id)
);