-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample users
INSERT INTO users (email, name) VALUES
('mishi@example.com', 'mishi'),
('mahi@example.com', 'mahi'),
('ali@example.com', 'ali'),
('asif@example.com', 'asif'),
('inshal@example.com', 'inshal');


