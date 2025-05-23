CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    cpf VARCHAR(14)
);

-- Create indexes for frequently queried fields
CREATE INDEX IF NOT EXISTS idx_users_cpf ON users(cpf);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS passwords (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    password_hash BYTEA NOT NULL
);

-- Create patrimony table with user foreign key
CREATE TABLE IF NOT EXISTS patrimony (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    stocks DECIMAL(15, 2) DEFAULT 0,
    real_estate_funds DECIMAL(15, 2) DEFAULT 0,
    investment_funds DECIMAL(15, 2) DEFAULT 0,
    fixed_income DECIMAL(15, 2) DEFAULT 0,
    companies DECIMAL(15, 2) DEFAULT 0,
    real_estate DECIMAL(15, 2) DEFAULT 0,
    others DECIMAL(15, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Create index for faster lookups by user_id
CREATE INDEX IF NOT EXISTS idx_patrimony_user_id ON patrimony(user_id);

-- Trigger to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_patrimony_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_patrimony_timestamp_trigger
BEFORE UPDATE ON patrimony
FOR EACH ROW
EXECUTE FUNCTION update_patrimony_timestamp();

-- Add initial data
INSERT INTO users (user_id, name, username, email, cpf) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Rodrigo Lima', 'Rodrigo', 'rodrigo.lima@gmail.com', '40712345600');



-- Add password for initial user (strongpassword123)
INSERT INTO passwords (user_id, password_hash) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', decode('243262243132242e59497649576432756c697631564d6c63464d4d432e5968424d74704571476f34674d612e36436d796c56636252353930716f5975', 'hex'));

-- Add initial patrimony for initial user
INSERT INTO patrimony (user_id, stocks, real_estate_funds, investment_funds, fixed_income, companies, real_estate, others) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 10000.00, 5000.00, 7500.00, 25000.00, 0.00, 120000.00, 1000.00);