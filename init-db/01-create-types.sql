DO $$
BEGIN
    CREATE TYPE operationtype AS ENUM ('DEPOSIT', 'WITHDRAW');
    RAISE NOTICE 'Created operationtype enum';
EXCEPTION WHEN duplicate_object THEN
    RAISE NOTICE 'operationtype enum already exists';
END
$$;