--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-29 22:52:41

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
-- TOC entry 5025 (class 1262 OID 28935)
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
-- TOC entry 220 (class 1259 OID 28960)
-- Name: empresas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.empresas (
    empresa_id integer NOT NULL,
    nombre character varying(65) NOT NULL,
    rfc character varying(16) NOT NULL,
    direccion text,
    logotipo character varying(128),
    email_contacto character varying(128),
    telefono_contacto character varying(15),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true,
    administrador integer NOT NULL
);


ALTER TABLE public.empresas OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 28959)
-- Name: empresas_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.empresas_empresa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.empresas_empresa_id_seq OWNER TO postgres;

--
-- TOC entry 5026 (class 0 OID 0)
-- Dependencies: 219
-- Name: empresas_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.empresas_empresa_id_seq OWNED BY public.empresas.empresa_id;


--
-- TOC entry 4859 (class 2604 OID 28963)
-- Name: empresas empresa_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas ALTER COLUMN empresa_id SET DEFAULT nextval('public.empresas_empresa_id_seq'::regclass);


--
-- TOC entry 5019 (class 0 OID 28960)
-- Dependencies: 220
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.empresas (empresa_id, nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, fecha_registro, status, administrador) FROM stdin;
21	Empresa Debug 1753157663	EMP1753157663	Av. Debug 1753157663	\N	admin1753157663@empresatest.com	5551234567	2025-07-22 04:14:23.545032	t	33
22	Empresa Test 1753157689	EMP1753157689	Av. Administración 1753157689	\N	admin1753157689@empresatest.com	5551234567	2025-07-22 04:14:49.741071	t	34
23	Empresa Test 1753157754	EMP1753157754	Av. Administración 1753157754	\N	admin1753157754@empresatest.com	5551234567	2025-07-22 04:15:54.737304	t	36
24	Empresa Test 1753157773	EMP1753157773	Av. Administración 1753157773	\N	admin1753157773@empresatest.com	5551234567	2025-07-22 04:16:14.448828	t	38
25	axis2	asdasdaasdfsdf	asdasdasd	\N	axis2@gmail.com	356456546	2025-07-22 04:16:15.232221	t	39
26	Test Empresa 214400	TEST214400ABC	Dirección de prueba 123	\N	\N	\N	2025-07-22 04:44:00.777463	t	8
1	CodeWave Technologies	CWTECH920314ABC	Dirección actualizada por prueba CRUD	https://example.com/codewave-logo.png	contacto@codewave.com	6641234567	2025-07-23 00:10:06.609258	t	2
9	aaaxdddddddd	IDS920815CD2	Blvd. Innovación 456, Monterrey, Nuevo León	\N	info@innovacion.mx	81-3333-4444	2025-07-24 20:58:18.520843	t	16
8	TechSolutions México	TSM850623AB1	Nueva Dirección Editada	\N	nuevo_email@empresa.com	33-1111-2222	2025-07-24 08:58:18.032769	t	15
11	Mi Empresa Test Completa	TEST53155965	Calle Test 123, Ciudad Test	\N	\N	\N	2025-07-22 03:46:07.471836	t	18
12	Mi Empresa Frontend	FRONT123456789	Dirección de prueba frontend	\N	\N	\N	2025-07-22 03:48:52.371593	t	19
13	Empresa Frontend 1753156369	FRONT56369	Calle Frontend 123, Col. Prueba	\N	frontend1753156369@prueba.com	5551234567	2025-07-22 03:52:52.440466	t	20
14	Mi Nueva Empresa 1753156428	MNE428123456	Av. Principal 456, Col. Centro	\N	admin1753156428@minuevaempresa.com	5555678901	2025-07-22 03:53:51.536474	t	21
15	Empresa Duplicada	DUP123456789		\N			2025-07-22 03:53:54.097679	t	22
16	Otra Empresa	MNE431123456		\N			2025-07-22 03:53:56.663534	t	23
17	axis	GAVE010630AY0	asdad	\N	axis@gmail.com	42324234234	2025-07-22 03:54:27.849588	t	24
18	Empresa Test Admin 1753156708	ETA708123456	Av. Empresarial 123, Col. Corporativo	\N	admin1753156708@empresatest.com	5551234567	2025-07-22 03:58:30.66451	t	26
19	Empresa Test Admin 1753156918	ETA918123456	Av. Empresarial 123, Col. Corporativo	\N	admin1753156918@empresatest.com	5551234567	2025-07-22 04:02:01.272632	t	28
20	Empresa Test 1753157647	EMP1753157647	Av. Administración 1753157647	\N	admin1753157647@empresatest.com	5551234567	2025-07-22 04:14:08.186917	t	32
\.


--
-- TOC entry 5027 (class 0 OID 0)
-- Dependencies: 219
-- Name: empresas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.empresas_empresa_id_seq', 28, true);


--
-- TOC entry 4863 (class 2606 OID 28975)
-- Name: empresas empresas_administrador_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_key UNIQUE (administrador);


--
-- TOC entry 4865 (class 2606 OID 28971)
-- Name: empresas empresas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nombre_key UNIQUE (nombre);


--
-- TOC entry 4867 (class 2606 OID 28969)
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (empresa_id);


--
-- TOC entry 4869 (class 2606 OID 28973)
-- Name: empresas empresas_rfc_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rfc_key UNIQUE (rfc);


--
-- TOC entry 4870 (class 1259 OID 28981)
-- Name: idx_nombre_empresa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_nombre_empresa ON public.empresas USING btree (nombre);


--
-- TOC entry 4871 (class 1259 OID 28982)
-- Name: idx_rfc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rfc ON public.empresas USING btree (rfc);


--
-- TOC entry 4872 (class 2606 OID 28976)
-- Name: empresas fk_empresas_administrador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT fk_empresas_administrador FOREIGN KEY (administrador) REFERENCES public.usuarios(id);


-- Completed on 2025-07-29 22:52:41

--
-- PostgreSQL database dump complete
--

