-- Script para crear la base de datos en PostgreSQL con configuracion UTF-8
-- Ejecuta este script desde pgAdmin o psql como usuario postgres

-- Terminar conexiones existentes a la base de datos si existe
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'axyoma';

-- Eliminar base de datos si existe
DROP DATABASE IF EXISTS axyoma;

-- Crear la base de datos con configuracion UTF-8 correcta
CREATE DATABASE axyoma
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE = template0;

-- Conectarse a la base de datos
\c axyoma;

-- Configurar la sesion para UTF-8
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- Verificar la configuracion
SELECT current_database(), pg_encoding_to_char(encoding) as encoding 
FROM pg_database WHERE datname = current_database();

-- Crear extension si es necesaria
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

COMMENT ON DATABASE axyoma IS 'Base de datos para sistema Axyoma';
