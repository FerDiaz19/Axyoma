--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-08-04 17:56:01

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

--
-- TOC entry 5027 (class 0 OID 203563)
-- Dependencies: 236
-- Data for Name: departamentos; Type: TABLE DATA; Schema: public; Owner: -
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.departamentos DISABLE TRIGGER ALL;

COPY public.departamentos (departamento_id, nombre, descripcion, fecha_registro, status, planta) FROM stdin;
96	RRH	ALGO MAS	2025-08-05 00:52:57.045172	t	22
\.


ALTER TABLE public.departamentos ENABLE TRIGGER ALL;

--
-- TOC entry 5034 (class 0 OID 0)
-- Dependencies: 237
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departamentos_departamento_id_seq', 96, true);


-- Completed on 2025-08-04 17:56:01

--
-- PostgreSQL database dump complete
--

