--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-08-03 14:35:16

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

ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS fk_empresas_administrador;
DROP INDEX IF EXISTS public.idx_rfc;
DROP INDEX IF EXISTS public.idx_nombre_empresa;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_rfc_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_nombre_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_administrador_key;
ALTER TABLE IF EXISTS public.empresas ALTER COLUMN empresa_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.empresas_empresa_id_seq;
DROP TABLE IF EXISTS public.empresas;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 249 (class 1259 OID 203605)
-- Name: empresas; Type: TABLE; Schema: public; Owner: -
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


--
-- TOC entry 250 (class 1259 OID 203612)
-- Name: empresas_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.empresas_empresa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5044 (class 0 OID 0)
-- Dependencies: 250
-- Name: empresas_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.empresas_empresa_id_seq OWNED BY public.empresas.empresa_id;


--
-- TOC entry 4878 (class 2604 OID 203724)
-- Name: empresas empresa_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas ALTER COLUMN empresa_id SET DEFAULT nextval('public.empresas_empresa_id_seq'::regclass);


--
-- TOC entry 5037 (class 0 OID 203605)
-- Dependencies: 249
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empresas (empresa_id, nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, fecha_registro, status, administrador) FROM stdin;
1	TechCorp Solutions	TCS950815MX3	Av. Tecnológico 1500	\N	contacto@techcorp.mx	4421234567	2025-08-01 04:57:02.99782	t	2
2	InnovaSoft Industrie	ISI980320QR	Blvd. Bernardo Quintana 2000	\N	info@innovasoft.mx	4427654321	2025-08-01 04:57:03.001902	t	3
3	Axis Development 2	GAVE0106SDF3		\N	axis2@gmail.com	4354345345	2025-08-01 08:20:14.729674	t	6
4	Axis Development 3	GAVE0104324FF	Ciudad Juarez	\N	axis3@gmail.com	4354345345	2025-08-01 08:28:34.466153	t	7
5	Axis Development 4	HSD98FDSFSD	Ciudad de Puebal	\N	axis4@gmail.com	664120432	2025-08-01 08:41:49.627754	t	8
6	Axis Development 5	HSD98FDSDAAA	Colonia Altiplano Rogelio Mendoza #150	\N	axis5@gmail.com	6642343481	2025-08-01 09:01:28.925834	t	9
\.


--
-- TOC entry 5045 (class 0 OID 0)
-- Dependencies: 250
-- Name: empresas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empresas_empresa_id_seq', 6, true);


--
-- TOC entry 4882 (class 2606 OID 203799)
-- Name: empresas empresas_administrador_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_key UNIQUE (administrador);


--
-- TOC entry 4884 (class 2606 OID 203801)
-- Name: empresas empresas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nombre_key UNIQUE (nombre);


--
-- TOC entry 4886 (class 2606 OID 203803)
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (empresa_id);


--
-- TOC entry 4888 (class 2606 OID 203805)
-- Name: empresas empresas_rfc_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rfc_key UNIQUE (rfc);


--
-- TOC entry 4889 (class 1259 OID 203884)
-- Name: idx_nombre_empresa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nombre_empresa ON public.empresas USING btree (nombre);


--
-- TOC entry 4890 (class 1259 OID 203893)
-- Name: idx_rfc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rfc ON public.empresas USING btree (rfc);


--
-- TOC entry 4891 (class 2606 OID 204008)
-- Name: empresas fk_empresas_administrador; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT fk_empresas_administrador FOREIGN KEY (administrador) REFERENCES public.usuarios(id);


-- Completed on 2025-08-03 14:35:16

--
-- PostgreSQL database dump complete
--

