--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-08-04 03:57:23

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
-- TOC entry 5026 (class 0 OID 203647)
-- Dependencies: 260
-- Data for Name: plantas; Type: TABLE DATA; Schema: public; Owner: -
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.plantas DISABLE TRIGGER ALL;

COPY public.plantas (planta_id, nombre, direccion, fecha_registro, status, empresa) FROM stdin;
1	Planta Norte	Zona Norte	2025-08-01 04:57:03.004552	t	1
2	Planta Sur	Zona Sur	2025-08-01 04:57:03.005659	t	1
3	Planta Central	Zona Central	2025-08-01 04:57:03.006336	t	2
4	Planta Satelite	Zona Satelite	2025-08-01 04:57:03.007021	t	2
5	Planta Principal		2025-08-01 08:20:14.729674	t	3
6	Planta Principal	Ciudad Juarez	2025-08-01 08:28:34.466153	t	4
7	Planta Principal	Ciudad de Puebal	2025-08-01 08:41:49.627754	t	5
8	Planta Principal	Colonia Altiplano Rogelio Mendoza #150	2025-08-01 09:01:28.925834	t	6
9	Planta 2	Prueba de direccion	2025-08-02 01:52:03.477564	t	3
10	planta 3	jje	2025-08-02 02:53:27.232782	t	3
13	Planta Automatica Final	Direccion final 789	2025-08-02 04:03:51.032773	t	6
15	Planta Prueba Manual	Direccion manual 123	2025-08-02 04:13:19.223776	t	1
17	Planta Automatica Renovada	Zona Industrial Nueva	2025-08-02 04:30:08.79524	t	1
18	Planta Con Usuario Auto	Industrial	2025-08-02 04:31:06.899761	t	1
12	Planta Automatica	Direccion automatica 456	2025-08-02 04:02:56.322235	t	6
19	Planta Principal	Aqui en casa	2025-08-03 22:38:14.663847	t	1
20	Planta Principal	bajijasjdiasjdw	2025-08-03 23:28:13.471544	t	7
21	Planta Principal	asdfghgfcxcvbhgfds	2025-08-04 05:27:14.097477	t	7
22	Planta Principal	qwerty	2025-08-04 05:34:56.235837	t	8
11	Planta Prueba Automatica	Direccion de prueba 123	2025-08-02 04:01:39.627258	t	5
23	Una extra	AQUI	2025-08-04 10:32:57.611063	t	6
\.


ALTER TABLE public.plantas ENABLE TRIGGER ALL;

--
-- TOC entry 5033 (class 0 OID 0)
-- Dependencies: 261
-- Name: plantas_planta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.plantas_planta_id_seq', 23, true);


-- Completed on 2025-08-04 03:57:23

--
-- PostgreSQL database dump complete
--

