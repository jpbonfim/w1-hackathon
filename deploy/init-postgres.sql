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

-- Add initial data
INSERT INTO users (user_id, name, username, email, cpf) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Rodrigo Lima', 'Rodrigo', 'rodrigo.lima@gmail.com', '40712345600');