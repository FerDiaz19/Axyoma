--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-29 20:07:19

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
-- TOC entry 5032 (class 1262 OID 28935)
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
-- TOC entry 5033 (class 0 OID 0)
-- Dependencies: 219
-- Name: empresas_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.empresas_empresa_id_seq OWNED BY public.empresas.empresa_id;


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
-- TOC entry 5034 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4854 (class 2604 OID 28963)
-- Name: empresas empresa_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas ALTER COLUMN empresa_id SET DEFAULT nextval('public.empresas_empresa_id_seq'::regclass);


--
-- TOC entry 4851 (class 2604 OID 28940)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 5026 (class 0 OID 28960)
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
-- TOC entry 5024 (class 0 OID 28937)
-- Dependencies: 218
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, apellido_paterno, apellido_materno, correo, fecha_registro, nivel_usuario, status, admin_empresa, user_id) FROM stdin;
1	Ed	Rubio	\N	ed-rubio@axyoma.com	2025-07-21 18:10:06.589055	superadmin	t	\N	\N
3	Maria	Gomez	\N	maria.gomez@codewave.com	2025-07-21 18:10:06.589055	admin-planta	t	2	\N
4	Carlos	Ruiz	\N	carlos.ruiz@codewave.com	2025-07-21 18:10:06.589055	admin-planta	t	2	\N
5	Super	Administrator		superadmin@axyoma.com	2025-07-22 01:20:20.7492	superadmin	t	\N	1
8	Admin	Test	\N	admin@test.com	2025-07-22 02:10:18.685309	superadmin	t	\N	4
16	Admin Innovación	Administrador	Empresa	info@innovacion.mx	2025-07-22 02:58:18.520218	admin-empresa	t	\N	12
17	Admin TechSolutions	Planta	TechSolutions	admin.planta.21@techsolutionsméxico.com	2025-07-22 03:04:37.530508	admin-planta	t	\N	13
7	Admin	Planta		planta@codewave.com	2025-07-22 07:20:20.754321	admin-planta	f	\N	3
15	Admin TechSolutions	Administrador	Empresa	contacto@techsolutions.mx	2025-07-22 08:58:18.029643	admin-empresa	f	\N	11
6	Admin	Empresa		admin@codewave.com	2025-07-22 13:20:20.75244	admin-empresa	f	\N	2
2	Juan	Perez	\N	juan.perez@codewave.com	2025-07-22 00:10:06.589055	admin-empresa	f	\N	\N
18	Admin	EmpresaTest	\N	test@empresatest.com	2025-07-22 03:46:07.465875	admin-empresa	t	\N	16
19	Usuario	Frontend	\N	frontend@test.com	2025-07-22 03:48:52.36518	admin-empresa	t	\N	17
20	Admin	Frontend	1753156369	frontend1753156369@prueba.com	2025-07-22 03:52:52.438792	admin-empresa	t	\N	21
21	Administrador	Principal	1753156428	admin1753156428@minuevaempresa.com	2025-07-22 03:53:51.53462	admin-empresa	t	\N	22
22	Admin	Duplicado		admin_front_1753156431@empresa.com	2025-07-22 03:53:54.096184	admin-empresa	t	\N	23
23	Nuevo	Admin		nuevo_admin_1753156431@empresa.com	2025-07-22 03:53:56.662033	admin-empresa	t	\N	24
24	sda	asd	asd	axis@gmail.com	2025-07-22 03:54:27.848121	admin-empresa	t	\N	25
26	Administrador	Empresa	1753156708	admin1753156708@empresatest.com	2025-07-22 03:58:30.662177	admin-empresa	t	\N	27
28	Administrador	Empresa	1753156918	admin1753156918@empresatest.com	2025-07-22 04:02:01.271001	admin-empresa	t	\N	29
31	Admin Planta Debug 1753157233	Planta		planta_plantadebug1753157233_28@empresatestadmin1753156918.com	2025-07-22 04:07:15.732648	admin-planta	t	\N	32
32	Admin	Empresa	Test	admin1753157647@empresatest.com	2025-07-22 04:14:08.18453	admin-empresa	t	\N	33
33	Admin	Empresa	Debug	admin1753157663@empresatest.com	2025-07-22 04:14:23.543589	admin-empresa	t	\N	34
34	Admin	Empresa	Test	admin1753157689@empresatest.com	2025-07-22 04:14:49.739638	admin-empresa	t	\N	35
35	Admin Planta Sucursal 1753157690	Planta		planta_plantasucursal1753157690_32@empresatest1753157689.com	2025-07-22 04:14:50.88832	admin-planta	t	\N	36
36	Admin	Empresa	Test	admin1753157754@empresatest.com	2025-07-22 04:15:54.73527	admin-empresa	t	\N	37
37	Admin Planta Sucursal 1753157755	Planta		planta_plantasucursal1753157755_34@empresatest1753157754.com	2025-07-22 04:15:55.790247	admin-planta	t	\N	38
38	Admin	Empresa	Test	admin1753157773@empresatest.com	2025-07-22 04:16:14.447302	admin-empresa	t	\N	39
39	sadasd	afsdasdf	afafafsa	axis2@gmail.com	2025-07-22 04:16:15.230699	admin-empresa	t	\N	40
40	Admin Planta Sucursal 1753157775	Planta		planta_plantasucursal1753157775_36@empresatest1753157773.com	2025-07-22 04:16:15.656317	admin-planta	t	\N	41
41	Admin Planta API Test 1753158797	Planta		planta_plantaapitest1753158797_41@empresadebug1753157663.com	2025-07-22 04:33:19.579311	admin-planta	t	\N	42
42	Admin Planta Test 214400	Planta		planta_plantatest214400_42@testempresa214400.com	2025-07-22 04:44:01.323669	admin-planta	t	\N	43
43	Admin Planta Test 214653	Planta		planta_plantatest214653_43@empresadebug1753157663.com	2025-07-22 04:46:54.131329	admin-planta	t	\N	44
44	Admin Planta Test 214735	Planta		planta_plantatest214735_44@empresadebug1753157663.com	2025-07-22 04:47:35.986857	admin-planta	t	\N	45
45	Admin Planta Test 214816	Planta		planta_plantatest214816_45@empresadebug1753157663.com	2025-07-22 04:48:17.334943	admin-planta	t	\N	46
46	Admin Planta Frontend Test	Planta		planta_plantafrontendtest_46@empresadebug1753157663.com	2025-07-22 04:51:41.695814	admin-planta	t	\N	47
47	Admin Planta de Prueba API	Planta		planta_plantadepruebaapi_47@codewavetechnologies.com	2025-07-22 05:22:53.791357	admin-planta	t	\N	49
48	Usuario	Prueba	\N	test@axyoma.com	2025-07-29 04:17:10.38524	superadmin	t	\N	50
49	ernesto	garcia	sadcasdf	ernesto@gmail.com	2025-07-29 21:55:35.01761	superadmin	t	\N	51
\.


--
-- TOC entry 5035 (class 0 OID 0)
-- Dependencies: 219
-- Name: empresas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.empresas_empresa_id_seq', 28, true);


--
-- TOC entry 5036 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 49, true);


--
-- TOC entry 4867 (class 2606 OID 28975)
-- Name: empresas empresas_administrador_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_key UNIQUE (administrador);


--
-- TOC entry 4869 (class 2606 OID 28971)
-- Name: empresas empresas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nombre_key UNIQUE (nombre);


--
-- TOC entry 4871 (class 2606 OID 28969)
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (empresa_id);


--
-- TOC entry 4873 (class 2606 OID 28973)
-- Name: empresas empresas_rfc_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rfc_key UNIQUE (rfc);


--
-- TOC entry 4861 (class 2606 OID 28949)
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- TOC entry 4863 (class 2606 OID 28947)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4865 (class 2606 OID 28951)
-- Name: usuarios usuarios_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_user_id_key UNIQUE (user_id);


--
-- TOC entry 4858 (class 1259 OID 28958)
-- Name: idx_correo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_correo ON public.usuarios USING btree (correo);


--
-- TOC entry 4859 (class 1259 OID 28957)
-- Name: idx_nivel_usuario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_nivel_usuario ON public.usuarios USING btree (nivel_usuario);


--
-- TOC entry 4874 (class 1259 OID 28981)
-- Name: idx_nombre_empresa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_nombre_empresa ON public.empresas USING btree (nombre);


--
-- TOC entry 4875 (class 1259 OID 28982)
-- Name: idx_rfc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rfc ON public.empresas USING btree (rfc);


--
-- TOC entry 4876 (class 2606 OID 28952)
-- Name: usuarios fk_admin_empresa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_admin_empresa FOREIGN KEY (admin_empresa) REFERENCES public.usuarios(id);


--
-- TOC entry 4877 (class 2606 OID 28976)
-- Name: empresas fk_empresas_administrador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT fk_empresas_administrador FOREIGN KEY (administrador) REFERENCES public.usuarios(id);


-- Completed on 2025-07-29 20:07:20

--
-- PostgreSQL database dump complete
--

