CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    cpf VARCHAR(14) NOT NULL UNIQUE
);

-- Create indexes for frequently queried fields
CREATE INDEX IF NOT EXISTS idx_users_cpf ON users(cpf);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Add initial data
 INSERT INTO users (user_id, name, nickname, email, cpf) VALUES
    ('fc9dfa83-4a94-4090-a8ce-3110799bf690', 'Rodrigo Lima', 'Rodrigo', 'rodrigo.lima@gmail.com', '40712345600');