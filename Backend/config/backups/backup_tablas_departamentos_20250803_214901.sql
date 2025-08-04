--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-08-03 21:49:01

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
1	RRHH	Departamento de RRHH	2025-08-01 04:57:03.013493	t	3
2	Producción	Departamento de Producción	2025-08-01 04:57:03.026031	t	3
3	Mantenimiento	Departamento de Mantenimiento	2025-08-01 04:57:03.034559	t	3
4	Calidad	Departamento de Calidad	2025-08-01 04:57:03.041816	t	3
5	Logística	Departamento de Logística	2025-08-01 04:57:03.050213	t	3
6	RRHH	Departamento de RRHH	2025-08-01 04:57:03.058329	t	4
7	Producción	Departamento de Producción	2025-08-01 04:57:03.066241	t	4
8	Mantenimiento	Departamento de Mantenimiento	2025-08-01 04:57:03.073951	t	4
9	Calidad	Departamento de Calidad	2025-08-01 04:57:03.081574	t	4
10	Logística	Departamento de Logística	2025-08-01 04:57:03.089674	t	4
11	RRHH	Departamento de RRHH	2025-08-01 04:57:03.097575	t	1
12	Producción	Departamento de Producción	2025-08-01 04:57:03.105572	t	1
13	Mantenimiento	Departamento de Mantenimiento	2025-08-01 04:57:03.113004	t	1
14	Calidad	Departamento de Calidad	2025-08-01 04:57:03.120157	t	1
15	Logística	Departamento de Logística	2025-08-01 04:57:03.127364	t	1
16	RRHH	Departamento de RRHH	2025-08-01 04:57:03.134923	t	2
17	Producción	Departamento de Producción	2025-08-01 04:57:03.141978	t	2
18	Mantenimiento	Departamento de Mantenimiento	2025-08-01 04:57:03.149422	t	2
19	Calidad	Departamento de Calidad	2025-08-01 04:57:03.157533	t	2
20	Logística	Departamento de Logística	2025-08-01 04:57:03.16487	t	2
21	Administración	Gestión administrativa general	2025-08-01 08:20:14.729674	t	5
22	Recursos Humanos	Gestión del personal y nómina	2025-08-01 08:20:14.729674	t	5
23	Finanzas	Gestión financiera y contable	2025-08-01 08:20:14.729674	t	5
24	Producción	Operaciones de manufactura	2025-08-01 08:20:14.729674	t	5
25	Calidad	Control y aseguramiento de calidad	2025-08-01 08:20:14.729674	t	5
26	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-01 08:20:14.729674	t	5
27	Logística	Almacén y distribución	2025-08-01 08:20:14.729674	t	5
28	Administración	Gestión administrativa general	2025-08-01 08:28:34.466153	t	6
29	Recursos Humanos	Gestión del personal y nómina	2025-08-01 08:28:34.466153	t	6
30	Finanzas	Gestión financiera y contable	2025-08-01 08:28:34.466153	t	6
31	Producción	Operaciones de manufactura	2025-08-01 08:28:34.466153	t	6
32	Calidad	Control y aseguramiento de calidad	2025-08-01 08:28:34.466153	t	6
33	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-01 08:28:34.466153	t	6
34	Logística	Almacén y distribución	2025-08-01 08:28:34.466153	t	6
35	Administración	Gestión administrativa general	2025-08-01 08:41:49.627754	t	7
36	Recursos Humanos	Gestión del personal y nómina	2025-08-01 08:41:49.627754	t	7
37	Finanzas	Gestión financiera y contable	2025-08-01 08:41:49.627754	t	7
38	Producción	Operaciones de manufactura	2025-08-01 08:41:49.627754	t	7
39	Calidad	Control y aseguramiento de calidad	2025-08-01 08:41:49.627754	t	7
40	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-01 08:41:49.627754	t	7
41	Logística	Almacén y distribución	2025-08-01 08:41:49.627754	t	7
42	Administración	Gestión administrativa general	2025-08-01 09:01:28.925834	t	8
43	Recursos Humanos	Gestión del personal y nómina	2025-08-01 09:01:28.925834	t	8
44	Finanzas	Gestión financiera y contable	2025-08-01 09:01:28.925834	t	8
45	Producción	Operaciones de manufactura	2025-08-01 09:01:28.925834	t	8
46	Calidad	Control y aseguramiento de calidad	2025-08-01 09:01:28.925834	t	8
47	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-01 09:01:28.925834	t	8
48	Logística	Almacén y distribución	2025-08-01 09:01:28.925834	t	8
49	Prueba departamento	Prueba	2025-08-02 01:52:35.521467	t	9
50	RRHH	Recursos Humanoides	2025-08-02 05:14:57.381589	t	12
51	Administración	Gestión administrativa general	2025-08-03 22:38:14.663847	t	19
52	Recursos Humanos	Gestión del personal y nómina	2025-08-03 22:38:14.663847	t	19
53	Finanzas	Gestión financiera y contable	2025-08-03 22:38:14.663847	t	19
54	Producción	Operaciones de manufactura	2025-08-03 22:38:14.663847	t	19
55	Calidad	Control y aseguramiento de calidad	2025-08-03 22:38:14.663847	t	19
56	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-03 22:38:14.663847	t	19
57	Logística	Almacén y distribución	2025-08-03 22:38:14.663847	t	19
58	Administración	Gestión administrativa general	2025-08-03 23:28:13.471544	t	20
59	Recursos Humanos	Gestión del personal y nómina	2025-08-03 23:28:13.471544	t	20
60	Finanzas	Gestión financiera y contable	2025-08-03 23:28:13.471544	t	20
61	Producción	Operaciones de manufactura	2025-08-03 23:28:13.471544	t	20
62	Calidad	Control y aseguramiento de calidad	2025-08-03 23:28:13.471544	t	20
63	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-08-03 23:28:13.471544	t	20
64	Logística	Almacén y distribución	2025-08-03 23:28:13.471544	t	20
\.


ALTER TABLE public.departamentos ENABLE TRIGGER ALL;

--
-- TOC entry 5034 (class 0 OID 0)
-- Dependencies: 237
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departamentos_departamento_id_seq', 64, true);


-- Completed on 2025-08-03 21:49:01

--
-- PostgreSQL database dump complete
--

