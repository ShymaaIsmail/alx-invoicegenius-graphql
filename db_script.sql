-- psql
CREATE DATABASE invoicesgenius_db;
CREATE USER invoicesgenius_user WITH PASSWORD 'super_secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE invoicesgenius_db TO invoicesgenius_user;
