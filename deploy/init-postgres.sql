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


CREATE TABLE patrimony_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    month VARCHAR(10) NOT NULL,
    patrimony DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE economy_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    month VARCHAR(10) NOT NULL,
    economy DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- Index for faster lookups by user_id
CREATE INDEX idx_patrimony_history_user_id ON patrimony_history(user_id);

-- Add initial data
INSERT INTO users (user_id, name, username, email, cpf) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Rodrigo Lima', 'Rodrigo', 'rodrigo.lima@gmail.com', '40712345600');

-- Add password for initial user (strongpassword123)
INSERT INTO passwords (user_id, password_hash) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', decode('243262243132242e59497649576432756c697631564d6c63464d4d432e5968424d74704571476f34674d612e36436d796c56636252353930716f5975', 'hex'));

-- Add initial patrimony for initial user
INSERT INTO patrimony (user_id, stocks, real_estate_funds, investment_funds, fixed_income, companies, real_estate, others) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 10000.00, 5000.00, 7500.00, 25000.00, 0.00, 120000.00, 1000.00);

-- Add one year of patrimony history records for initial user
INSERT INTO patrimony_history (user_id, month, patrimony) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jan', 160000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Fev', 162500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Mar', 165000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Abr', 164200.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Mai', 166800.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jun', 169500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jul', 171200.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Ago', 173000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Set', 172500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Out', 174800.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Nov', 176500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Dez', 178500.00);


INSERT INTO economy_history (user_id, month, economy) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jan', 1000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Fev', 2500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Mar', 5000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Abr', 9500.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Mai', 17000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jun', 31000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Jul', 56000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Ago', 101000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Set', 180000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Out', 320000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Nov', 570000.00),
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Dez', 670000.00);


--
