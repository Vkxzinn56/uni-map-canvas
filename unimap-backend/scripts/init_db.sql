-- UniMap 3.0 - Database Initialization
-- Runs once on first PostgreSQL container start

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";   -- for LIKE/ILIKE performance
CREATE EXTENSION IF NOT EXISTS "unaccent";   -- for accent-insensitive search

-- Test database (for CI/CD)
CREATE DATABASE unimap_test_db OWNER unimap;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE unimap_db TO unimap;
GRANT ALL PRIVILEGES ON DATABASE unimap_test_db TO unimap;
