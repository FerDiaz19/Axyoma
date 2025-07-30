--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-29 20:20:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE axyomadb;
--
-- TOC entry 5014 (class 1262 OID 28935)
-- Name: axyomadb; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE axyomadb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_United States.1252';


ALTER DATABASE axyomadb OWNER TO postgres;

\connect axyomadb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 28937)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    apellido_paterno character varying(64) NOT NULL,
    apellido_materno character varying(64),
    correo character varying(255) NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    nivel_usuario character varying(20) NOT NULL,
    status boolean DEFAULT true,
    admin_empresa integer,
    user_id integer,
    CONSTRAINT usuarios_nivel_usuario_check CHECK (((nivel_usuario)::text = ANY ((ARRAY['superadmin'::character varying, 'admin-empresa'::character varying, 'admin-planta'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 28936)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- TOC entry 5015 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4851 (class 2604 OID 28940)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 4858 (class 2606 OID 28949)
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- TOC entry 4860 (class 2606 OID 28947)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4862 (class 2606 OID 28951)
-- Name: usuarios usuarios_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_user_id_key UNIQUE (user_id);


--
-- TOC entry 4855 (class 1259 OID 28958)
-- Name: idx_correo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_correo ON public.usuarios USING btree (correo);


--
-- TOC entry 4856 (class 1259 OID 28957)
-- Name: idx_nivel_usuario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_nivel_usuario ON public.usuarios USING btree (nivel_usuario);


--
-- TOC entry 4863 (class 2606 OID 28952)
-- Name: usuarios fk_admin_empresa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_admin_empresa FOREIGN KEY (admin_empresa) REFERENCES public.usuarios(id);


-- Completed on 2025-07-29 20:20:31

--
-- PostgreSQL database dump complete
--

