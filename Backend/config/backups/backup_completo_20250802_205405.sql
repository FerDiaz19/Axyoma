--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-08-02 20:54:05

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

ALTER TABLE IF EXISTS ONLY public.secciones_oficiales DROP CONSTRAINT IF EXISTS secciones_oficiales_evaluacion_oficial_i_713c3681_fk_evaluacio;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleados DROP CONSTRAINT IF EXISTS respuestas_empleados_pregunta_oficial_id_8dc43081_fk_preguntas;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleados DROP CONSTRAINT IF EXISTS respuestas_empleados_empleado_asignado_id_9ed2afaa_fk_empleados;
ALTER TABLE IF EXISTS ONLY public.preguntas_oficiales DROP CONSTRAINT IF EXISTS preguntas_oficiales_seccion_id_8fdcef8b_fk_secciones;
ALTER TABLE IF EXISTS ONLY public.preguntas_oficiales DROP CONSTRAINT IF EXISTS preguntas_oficiales_pregunta_padre_id_dd462c07_fk_preguntas;
ALTER TABLE IF EXISTS ONLY public.suscripciones DROP CONSTRAINT IF EXISTS fk_suscripciones_plan;
ALTER TABLE IF EXISTS ONLY public.suscripciones DROP CONSTRAINT IF EXISTS fk_suscripciones_empresa;
ALTER TABLE IF EXISTS ONLY public.secciones_eval DROP CONSTRAINT IF EXISTS fk_secciones_evaluacion;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS fk_seccion_preguntas_seccion;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS fk_seccion_preguntas_pregunta;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS fk_seccion_preguntas_conjunto;
ALTER TABLE IF EXISTS ONLY public.puestos DROP CONSTRAINT IF EXISTS fk_puestos_departamento;
ALTER TABLE IF EXISTS ONLY public.preguntas DROP CONSTRAINT IF EXISTS fk_pregunta_padre;
ALTER TABLE IF EXISTS ONLY public.plantas DROP CONSTRAINT IF EXISTS fk_plantas_empresa;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS fk_pagos_usuario;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS fk_pagos_suscripcion;
ALTER TABLE IF EXISTS ONLY public.opciones_conjunto DROP CONSTRAINT IF EXISTS fk_opciones_conjunto;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS fk_evaluaciones_tipo;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS fk_evaluaciones_empresa;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS fk_evaluaciones_creado_por;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS fk_empresas_administrador;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS fk_empleados_puesto;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS fk_departamentos_planta;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS fk_admin_empresa;
ALTER TABLE IF EXISTS ONLY public.empleados_asignados DROP CONSTRAINT IF EXISTS empleados_asignados_empleado_id_a1082f92_fk_empleados;
ALTER TABLE IF EXISTS ONLY public.empleados_asignados DROP CONSTRAINT IF EXISTS empleados_asignados_asignacion_id_96c473f3_fk_asignacio;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_user_id_35299eff_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluacion_planta_id_6db671c6_fk_plantas_planta_id;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluac_evaluacion_oficial_i_ce80dfa2_fk_evaluacio;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluac_empresa_id_456c4cf4_fk_empresas_;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluac_admin_asignador_id_b377164f_fk_auth_user;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_usuario_id_fkey;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_planta_id_fkey;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id;
DROP INDEX IF EXISTS public.secciones_oficiales_evaluacion_oficial_id_713c3681;
DROP INDEX IF EXISTS public.respuestas_empleados_pregunta_oficial_id_8dc43081;
DROP INDEX IF EXISTS public.respuestas_empleados_empleado_asignado_id_9ed2afaa;
DROP INDEX IF EXISTS public.preguntas_oficiales_seccion_id_8fdcef8b;
DROP INDEX IF EXISTS public.preguntas_oficiales_pregunta_padre_id_dd462c07;
DROP INDEX IF EXISTS public.idx_tipo_pregunta;
DROP INDEX IF EXISTS public.idx_tipo_evaluacion;
DROP INDEX IF EXISTS public.idx_suscripcion_pago;
DROP INDEX IF EXISTS public.idx_status_evaluacion;
DROP INDEX IF EXISTS public.idx_rfc;
DROP INDEX IF EXISTS public.idx_puesto_empleado;
DROP INDEX IF EXISTS public.idx_predefinido_conjunto;
DROP INDEX IF EXISTS public.idx_precio_plan;
DROP INDEX IF EXISTS public.idx_planta_depto;
DROP INDEX IF EXISTS public.idx_orden_seccion;
DROP INDEX IF EXISTS public.idx_orden_opciones;
DROP INDEX IF EXISTS public.idx_nombre_tipo_eval;
DROP INDEX IF EXISTS public.idx_nombre_plan;
DROP INDEX IF EXISTS public.idx_nombre_empresa;
DROP INDEX IF EXISTS public.idx_nombre_conjunto;
DROP INDEX IF EXISTS public.idx_nivel_usuario;
DROP INDEX IF EXISTS public.idx_fecha_pago;
DROP INDEX IF EXISTS public.idx_fecha_fin_suscripcion;
DROP INDEX IF EXISTS public.idx_evaluacion_seccion;
DROP INDEX IF EXISTS public.idx_estado_suscripcion;
DROP INDEX IF EXISTS public.idx_estado_pago;
DROP INDEX IF EXISTS public.idx_empresa_suscripcion;
DROP INDEX IF EXISTS public.idx_empresa_planta;
DROP INDEX IF EXISTS public.idx_empresa_evaluacion;
DROP INDEX IF EXISTS public.idx_email_empleado;
DROP INDEX IF EXISTS public.idx_departamento_puesto;
DROP INDEX IF EXISTS public.idx_correo;
DROP INDEX IF EXISTS public.idx_conjunto_opciones;
DROP INDEX IF EXISTS public.empleados_asignados_token_empleado_a8a54d8d_like;
DROP INDEX IF EXISTS public.empleados_asignados_empleado_id_a1082f92;
DROP INDEX IF EXISTS public.empleados_asignados_asignacion_id_96c473f3;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.authtoken_token_key_10f0b77e_like;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.asignaciones_evaluacion_token_sesion_c52ef540_like;
DROP INDEX IF EXISTS public.asignaciones_evaluacion_planta_id_6db671c6;
DROP INDEX IF EXISTS public.asignaciones_evaluacion_evaluacion_oficial_id_ce80dfa2;
DROP INDEX IF EXISTS public.asignaciones_evaluacion_empresa_id_456c4cf4;
DROP INDEX IF EXISTS public.asignaciones_evaluacion_admin_asignador_id_b377164f;
DROP INDEX IF EXISTS public.admin_bd_logrespaldo_usuario_id_17645f3a;
DROP INDEX IF EXISTS public.admin_bd_logrespaldo_empresa_id_61be407d;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_user_id_key;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_correo_key;
ALTER TABLE IF EXISTS ONLY public.tipos_evaluacion DROP CONSTRAINT IF EXISTS tipos_evaluacion_pkey;
ALTER TABLE IF EXISTS ONLY public.tipos_evaluacion DROP CONSTRAINT IF EXISTS tipos_evaluacion_nombre_key;
ALTER TABLE IF EXISTS ONLY public.suscripciones DROP CONSTRAINT IF EXISTS suscripciones_pkey;
ALTER TABLE IF EXISTS ONLY public.secciones_oficiales DROP CONSTRAINT IF EXISTS secciones_oficiales_pkey;
ALTER TABLE IF EXISTS ONLY public.secciones_eval DROP CONSTRAINT IF EXISTS secciones_eval_pkey;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_pkey;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleados DROP CONSTRAINT IF EXISTS respuestas_empleados_pkey;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleados DROP CONSTRAINT IF EXISTS respuestas_empleados_empleado_asignado_id_pre_2c08792d_uniq;
ALTER TABLE IF EXISTS ONLY public.puestos DROP CONSTRAINT IF EXISTS puestos_pkey;
ALTER TABLE IF EXISTS ONLY public.preguntas DROP CONSTRAINT IF EXISTS preguntas_pkey;
ALTER TABLE IF EXISTS ONLY public.preguntas_oficiales DROP CONSTRAINT IF EXISTS preguntas_oficiales_pkey;
ALTER TABLE IF EXISTS ONLY public.plantas DROP CONSTRAINT IF EXISTS plantas_pkey;
ALTER TABLE IF EXISTS ONLY public.planes DROP CONSTRAINT IF EXISTS planes_pkey;
ALTER TABLE IF EXISTS ONLY public.planes DROP CONSTRAINT IF EXISTS planes_nombre_key;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS pagos_pkey;
ALTER TABLE IF EXISTS ONLY public.opciones_conjunto DROP CONSTRAINT IF EXISTS opciones_conjunto_pkey;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS evaluaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.evaluaciones_oficiales DROP CONSTRAINT IF EXISTS evaluaciones_oficiales_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_rfc_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_nombre_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_administrador_key;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_pkey;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_email_key;
ALTER TABLE IF EXISTS ONLY public.empleados_asignados DROP CONSTRAINT IF EXISTS empleados_asignados_token_empleado_key;
ALTER TABLE IF EXISTS ONLY public.empleados_asignados DROP CONSTRAINT IF EXISTS empleados_asignados_pkey;
ALTER TABLE IF EXISTS ONLY public.empleados_asignados DROP CONSTRAINT IF EXISTS empleados_asignados_asignacion_id_empleado_id_fd4cc0ae_uniq;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_pkey;
ALTER TABLE IF EXISTS ONLY public.conjuntos_opciones DROP CONSTRAINT IF EXISTS conjuntos_opciones_pkey;
ALTER TABLE IF EXISTS ONLY public.conjuntos_opciones DROP CONSTRAINT IF EXISTS conjuntos_opciones_nombre_key;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_user_id_key;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluacion_token_sesion_key;
ALTER TABLE IF EXISTS ONLY public.asignaciones_evaluacion DROP CONSTRAINT IF EXISTS asignaciones_evaluacion_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_usuario_id_planta_id_key;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_bd_configuracionbd DROP CONSTRAINT IF EXISTS admin_bd_configuracionbd_pkey;
ALTER TABLE IF EXISTS public.usuarios ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.tipos_evaluacion ALTER COLUMN tipo_evaluacion_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.suscripciones ALTER COLUMN suscripcion_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.secciones_eval ALTER COLUMN seccion_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.puestos ALTER COLUMN puesto_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.preguntas ALTER COLUMN pregunta_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.plantas ALTER COLUMN planta_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.planes ALTER COLUMN plan_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.pagos ALTER COLUMN pago_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.opciones_conjunto ALTER COLUMN opcion_conjunto_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.evaluaciones ALTER COLUMN evaluacion_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.empresas ALTER COLUMN empresa_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.empleados ALTER COLUMN empleado_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.departamentos ALTER COLUMN departamento_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.conjuntos_opciones ALTER COLUMN conjunto_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.admin_plantas ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.usuarios_id_seq;
DROP TABLE IF EXISTS public.usuarios;
DROP SEQUENCE IF EXISTS public.tipos_evaluacion_tipo_evaluacion_id_seq;
DROP TABLE IF EXISTS public.tipos_evaluacion;
DROP SEQUENCE IF EXISTS public.suscripciones_suscripcion_id_seq;
DROP TABLE IF EXISTS public.suscripciones;
DROP TABLE IF EXISTS public.secciones_oficiales;
DROP SEQUENCE IF EXISTS public.secciones_eval_seccion_id_seq;
DROP TABLE IF EXISTS public.secciones_eval;
DROP TABLE IF EXISTS public.seccion_preguntas;
DROP TABLE IF EXISTS public.respuestas_empleados;
DROP SEQUENCE IF EXISTS public.puestos_puesto_id_seq;
DROP TABLE IF EXISTS public.puestos;
DROP SEQUENCE IF EXISTS public.preguntas_pregunta_id_seq;
DROP TABLE IF EXISTS public.preguntas_oficiales;
DROP TABLE IF EXISTS public.preguntas;
DROP SEQUENCE IF EXISTS public.plantas_planta_id_seq;
DROP TABLE IF EXISTS public.plantas;
DROP SEQUENCE IF EXISTS public.planes_plan_id_seq;
DROP TABLE IF EXISTS public.planes;
DROP SEQUENCE IF EXISTS public.pagos_pago_id_seq;
DROP TABLE IF EXISTS public.pagos;
DROP SEQUENCE IF EXISTS public.opciones_conjunto_opcion_conjunto_id_seq;
DROP TABLE IF EXISTS public.opciones_conjunto;
DROP TABLE IF EXISTS public.evaluaciones_oficiales;
DROP SEQUENCE IF EXISTS public.evaluaciones_evaluacion_id_seq;
DROP TABLE IF EXISTS public.evaluaciones;
DROP SEQUENCE IF EXISTS public.empresas_empresa_id_seq;
DROP TABLE IF EXISTS public.empresas;
DROP SEQUENCE IF EXISTS public.empleados_empleado_id_seq;
DROP TABLE IF EXISTS public.empleados_asignados;
DROP TABLE IF EXISTS public.empleados;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP SEQUENCE IF EXISTS public.departamentos_departamento_id_seq;
DROP TABLE IF EXISTS public.departamentos;
DROP SEQUENCE IF EXISTS public.conjuntos_opciones_conjunto_id_seq;
DROP TABLE IF EXISTS public.conjuntos_opciones;
DROP TABLE IF EXISTS public.authtoken_token;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.asignaciones_evaluacion;
DROP SEQUENCE IF EXISTS public.admin_plantas_id_seq;
DROP TABLE IF EXISTS public.admin_plantas;
DROP TABLE IF EXISTS public.admin_bd_logrespaldo;
DROP TABLE IF EXISTS public.admin_bd_configuracionbd;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 283 (class 1259 OID 204115)
-- Name: admin_bd_configuracionbd; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_bd_configuracionbd (
    id bigint NOT NULL,
    nombre_bd character varying(100) NOT NULL,
    host character varying(100) NOT NULL,
    puerto integer NOT NULL,
    usuario_admin character varying(100) NOT NULL,
    directorio_respaldos character varying(255) NOT NULL,
    max_respaldos_mantener integer NOT NULL,
    habilitar_respaldos_automaticos boolean NOT NULL,
    frecuencia_respaldo_dias integer NOT NULL
);


--
-- TOC entry 282 (class 1259 OID 204114)
-- Name: admin_bd_configuracionbd_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.admin_bd_configuracionbd ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_bd_configuracionbd_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 285 (class 1259 OID 204123)
-- Name: admin_bd_logrespaldo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_bd_logrespaldo (
    id bigint NOT NULL,
    tipo character varying(20) NOT NULL,
    archivo_nombre character varying(255) NOT NULL,
    archivo_ruta character varying(500),
    "archivo_tamaño" bigint,
    tablas_incluidas jsonb NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    exitoso boolean NOT NULL,
    detalles text NOT NULL,
    mensaje_error text NOT NULL,
    empresa_id integer,
    usuario_id integer NOT NULL
);


--
-- TOC entry 284 (class 1259 OID 204122)
-- Name: admin_bd_logrespaldo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.admin_bd_logrespaldo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_bd_logrespaldo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 203517)
-- Name: admin_plantas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_plantas (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    planta_id integer NOT NULL,
    fecha_asignacion timestamp with time zone DEFAULT now(),
    status boolean DEFAULT true,
    password_temporal character varying(128)
);


--
-- TOC entry 218 (class 1259 OID 203522)
-- Name: admin_plantas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.admin_plantas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5396 (class 0 OID 0)
-- Dependencies: 218
-- Name: admin_plantas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.admin_plantas_id_seq OWNED BY public.admin_plantas.id;


--
-- TOC entry 219 (class 1259 OID 203523)
-- Name: asignaciones_evaluacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asignaciones_evaluacion (
    id bigint NOT NULL,
    fecha_inicio timestamp with time zone NOT NULL,
    fecha_fin timestamp with time zone NOT NULL,
    duracion_dias integer NOT NULL,
    estado character varying(20) NOT NULL,
    token_sesion character varying(100) NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_modificacion timestamp with time zone NOT NULL,
    admin_asignador_id integer NOT NULL,
    empresa_id integer NOT NULL,
    planta_id integer,
    evaluacion_oficial_id bigint NOT NULL
);


--
-- TOC entry 220 (class 1259 OID 203526)
-- Name: asignaciones_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.asignaciones_evaluacion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.asignaciones_evaluacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 203527)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- TOC entry 222 (class 1259 OID 203530)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 203531)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 224 (class 1259 OID 203534)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 203535)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- TOC entry 226 (class 1259 OID 203538)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 203539)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- TOC entry 228 (class 1259 OID 203544)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- TOC entry 229 (class 1259 OID 203547)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 203548)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 231 (class 1259 OID 203549)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 232 (class 1259 OID 203552)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 203553)
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 234 (class 1259 OID 203556)
-- Name: conjuntos_opciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conjuntos_opciones (
    conjunto_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text,
    predefinido boolean DEFAULT false
);


--
-- TOC entry 235 (class 1259 OID 203562)
-- Name: conjuntos_opciones_conjunto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.conjuntos_opciones_conjunto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5397 (class 0 OID 0)
-- Dependencies: 235
-- Name: conjuntos_opciones_conjunto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.conjuntos_opciones_conjunto_id_seq OWNED BY public.conjuntos_opciones.conjunto_id;


--
-- TOC entry 236 (class 1259 OID 203563)
-- Name: departamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departamentos (
    departamento_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    descripcion text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true,
    planta integer NOT NULL
);


--
-- TOC entry 237 (class 1259 OID 203570)
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.departamentos_departamento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5398 (class 0 OID 0)
-- Dependencies: 237
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.departamentos_departamento_id_seq OWNED BY public.departamentos.departamento_id;


--
-- TOC entry 238 (class 1259 OID 203571)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- TOC entry 239 (class 1259 OID 203577)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 240 (class 1259 OID 203578)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- TOC entry 241 (class 1259 OID 203581)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 242 (class 1259 OID 203582)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- TOC entry 243 (class 1259 OID 203587)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 244 (class 1259 OID 203588)
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- TOC entry 245 (class 1259 OID 203593)
-- Name: empleados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.empleados (
    empleado_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    apellido_paterno character varying(64) NOT NULL,
    apellido_materno character varying(64),
    email character varying(255) NOT NULL,
    telefono character varying(15),
    fecha_ingreso date NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true,
    puesto integer NOT NULL
);


--
-- TOC entry 246 (class 1259 OID 203600)
-- Name: empleados_asignados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.empleados_asignados (
    id bigint NOT NULL,
    token_empleado character varying(100) NOT NULL,
    estado character varying(20) NOT NULL,
    fecha_inicio_empleado timestamp with time zone,
    fecha_finalizacion timestamp with time zone,
    progreso_porcentaje integer NOT NULL,
    fecha_asignacion timestamp with time zone NOT NULL,
    ultimo_acceso timestamp with time zone,
    asignacion_id bigint NOT NULL,
    empleado_id integer NOT NULL
);


--
-- TOC entry 247 (class 1259 OID 203603)
-- Name: empleados_asignados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.empleados_asignados ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.empleados_asignados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 248 (class 1259 OID 203604)
-- Name: empleados_empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.empleados_empleado_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5399 (class 0 OID 0)
-- Dependencies: 248
-- Name: empleados_empleado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.empleados_empleado_id_seq OWNED BY public.empleados.empleado_id;


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
-- TOC entry 5400 (class 0 OID 0)
-- Dependencies: 250
-- Name: empresas_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.empresas_empresa_id_seq OWNED BY public.empresas.empresa_id;


--
-- TOC entry 251 (class 1259 OID 203613)
-- Name: evaluaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluaciones (
    evaluacion_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    descripcion text,
    instrucciones text,
    tiempo_limite integer,
    status boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tipo_evaluacion integer NOT NULL,
    empresa integer,
    creado_por integer NOT NULL
);


--
-- TOC entry 252 (class 1259 OID 203621)
-- Name: evaluaciones_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.evaluaciones_evaluacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5401 (class 0 OID 0)
-- Dependencies: 252
-- Name: evaluaciones_evaluacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.evaluaciones_evaluacion_id_seq OWNED BY public.evaluaciones.evaluacion_id;


--
-- TOC entry 253 (class 1259 OID 203622)
-- Name: evaluaciones_oficiales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluaciones_oficiales (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo_norma character varying(10) NOT NULL,
    descripcion text NOT NULL,
    instrucciones text NOT NULL,
    tiempo_limite integer,
    umbral_aprobacion integer,
    activa boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL
);


--
-- TOC entry 254 (class 1259 OID 203627)
-- Name: evaluaciones_oficiales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.evaluaciones_oficiales ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.evaluaciones_oficiales_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 255 (class 1259 OID 203628)
-- Name: opciones_conjunto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.opciones_conjunto (
    opcion_conjunto_id integer NOT NULL,
    texto_opcion character varying(256) NOT NULL,
    valor_booleano boolean,
    valor_numerico integer,
    puntuaje_escala integer,
    numero_orden integer NOT NULL,
    conjunto_opciones integer NOT NULL
);


--
-- TOC entry 256 (class 1259 OID 203631)
-- Name: opciones_conjunto_opcion_conjunto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.opciones_conjunto_opcion_conjunto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5402 (class 0 OID 0)
-- Dependencies: 256
-- Name: opciones_conjunto_opcion_conjunto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.opciones_conjunto_opcion_conjunto_id_seq OWNED BY public.opciones_conjunto.opcion_conjunto_id;


--
-- TOC entry 257 (class 1259 OID 203632)
-- Name: pagos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pagos (
    pago_id integer NOT NULL,
    suscripcion integer NOT NULL,
    monto numeric(10,2) NOT NULL,
    fecha_pago timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    metodo_pago character varying(50),
    estado_pago character varying(20) DEFAULT 'pendiente'::character varying,
    referencia_pago character varying(100),
    usuario integer NOT NULL,
    CONSTRAINT pagos_estado_pago_check CHECK (((estado_pago)::text = ANY (ARRAY[('pendiente'::character varying)::text, ('completado'::character varying)::text, ('fallido'::character varying)::text])))
);


--
-- TOC entry 258 (class 1259 OID 203638)
-- Name: pagos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pagos_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5403 (class 0 OID 0)
-- Dependencies: 258
-- Name: pagos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pagos_pago_id_seq OWNED BY public.pagos.pago_id;


--
-- TOC entry 259 (class 1259 OID 203639)
-- Name: planes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.planes (
    plan_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    descripcion text,
    precio numeric(10,2) NOT NULL,
    duracion integer NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true
);


--
-- TOC entry 260 (class 1259 OID 203646)
-- Name: planes_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.planes_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5404 (class 0 OID 0)
-- Dependencies: 260
-- Name: planes_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.planes_plan_id_seq OWNED BY public.planes.plan_id;


--
-- TOC entry 261 (class 1259 OID 203647)
-- Name: plantas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plantas (
    planta_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    direccion text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true,
    empresa integer NOT NULL
);


--
-- TOC entry 262 (class 1259 OID 203654)
-- Name: plantas_planta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.plantas_planta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5405 (class 0 OID 0)
-- Dependencies: 262
-- Name: plantas_planta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.plantas_planta_id_seq OWNED BY public.plantas.planta_id;


--
-- TOC entry 263 (class 1259 OID 203655)
-- Name: preguntas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.preguntas (
    pregunta_id integer NOT NULL,
    texto_pregunta text NOT NULL,
    tipo_pregunta character varying(20) NOT NULL,
    es_obligatoria boolean DEFAULT true,
    pregunta_padre integer,
    activador_padre character varying(255),
    CONSTRAINT preguntas_tipo_pregunta_check CHECK (((tipo_pregunta)::text = ANY (ARRAY[('Abierta'::character varying)::text, ('MÃºltiple'::character varying)::text, ('Escala'::character varying)::text, ('Bool'::character varying)::text])))
);


--
-- TOC entry 264 (class 1259 OID 203662)
-- Name: preguntas_oficiales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.preguntas_oficiales (
    id bigint NOT NULL,
    texto_pregunta text NOT NULL,
    tipo_pregunta character varying(20) NOT NULL,
    opciones_respuesta jsonb NOT NULL,
    es_obligatoria boolean NOT NULL,
    numero_orden integer NOT NULL,
    activador_padre character varying(100) NOT NULL,
    activa boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    pregunta_padre_id bigint,
    seccion_id bigint NOT NULL
);


--
-- TOC entry 265 (class 1259 OID 203667)
-- Name: preguntas_oficiales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.preguntas_oficiales ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.preguntas_oficiales_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 266 (class 1259 OID 203668)
-- Name: preguntas_pregunta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.preguntas_pregunta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5406 (class 0 OID 0)
-- Dependencies: 266
-- Name: preguntas_pregunta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.preguntas_pregunta_id_seq OWNED BY public.preguntas.pregunta_id;


--
-- TOC entry 267 (class 1259 OID 203669)
-- Name: puestos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.puestos (
    puesto_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    descripcion text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true,
    departamento integer NOT NULL
);


--
-- TOC entry 268 (class 1259 OID 203676)
-- Name: puestos_puesto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.puestos_puesto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5407 (class 0 OID 0)
-- Dependencies: 268
-- Name: puestos_puesto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.puestos_puesto_id_seq OWNED BY public.puestos.puesto_id;


--
-- TOC entry 269 (class 1259 OID 203677)
-- Name: respuestas_empleados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.respuestas_empleados (
    id bigint NOT NULL,
    respuesta_texto text NOT NULL,
    respuesta_numerica integer,
    respuesta_multiple jsonb NOT NULL,
    respuesta_booleana boolean,
    fecha_respuesta timestamp with time zone NOT NULL,
    tiempo_respuesta_segundos integer,
    es_respuesta_final boolean NOT NULL,
    empleado_asignado_id bigint NOT NULL,
    pregunta_oficial_id bigint NOT NULL
);


--
-- TOC entry 270 (class 1259 OID 203682)
-- Name: respuestas_empleados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.respuestas_empleados ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.respuestas_empleados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 271 (class 1259 OID 203683)
-- Name: seccion_preguntas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.seccion_preguntas (
    seccion integer NOT NULL,
    pregunta integer NOT NULL,
    conjunto_opciones integer
);


--
-- TOC entry 272 (class 1259 OID 203686)
-- Name: secciones_eval; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.secciones_eval (
    seccion_id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text,
    numero_orden integer NOT NULL,
    evaluacion integer NOT NULL
);


--
-- TOC entry 273 (class 1259 OID 203691)
-- Name: secciones_eval_seccion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.secciones_eval_seccion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5408 (class 0 OID 0)
-- Dependencies: 273
-- Name: secciones_eval_seccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.secciones_eval_seccion_id_seq OWNED BY public.secciones_eval.seccion_id;


--
-- TOC entry 274 (class 1259 OID 203692)
-- Name: secciones_oficiales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.secciones_oficiales (
    id bigint NOT NULL,
    nombre character varying(200) NOT NULL,
    descripcion text NOT NULL,
    numero_orden integer NOT NULL,
    es_evaluable boolean NOT NULL,
    evaluacion_oficial_id bigint NOT NULL
);


--
-- TOC entry 275 (class 1259 OID 203697)
-- Name: secciones_oficiales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.secciones_oficiales ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.secciones_oficiales_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 276 (class 1259 OID 203698)
-- Name: suscripciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.suscripciones (
    suscripcion_id integer NOT NULL,
    empresa integer NOT NULL,
    plan integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    estado character varying(20) DEFAULT 'activa'::character varying,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT suscripciones_estado_check CHECK (((estado)::text = ANY (ARRAY[('activa'::character varying)::text, ('vencida'::character varying)::text, ('cancelada'::character varying)::text])))
);


--
-- TOC entry 277 (class 1259 OID 203704)
-- Name: suscripciones_suscripcion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.suscripciones_suscripcion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5409 (class 0 OID 0)
-- Dependencies: 277
-- Name: suscripciones_suscripcion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.suscripciones_suscripcion_id_seq OWNED BY public.suscripciones.suscripcion_id;


--
-- TOC entry 278 (class 1259 OID 203705)
-- Name: tipos_evaluacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_evaluacion (
    tipo_evaluacion_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text
);


--
-- TOC entry 279 (class 1259 OID 203710)
-- Name: tipos_evaluacion_tipo_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_evaluacion_tipo_evaluacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5410 (class 0 OID 0)
-- Dependencies: 279
-- Name: tipos_evaluacion_tipo_evaluacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_evaluacion_tipo_evaluacion_id_seq OWNED BY public.tipos_evaluacion.tipo_evaluacion_id;


--
-- TOC entry 280 (class 1259 OID 203711)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
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
    CONSTRAINT usuarios_nivel_usuario_check CHECK (((nivel_usuario)::text = ANY (ARRAY[('superadmin'::character varying)::text, ('admin-empresa'::character varying)::text, ('admin-planta'::character varying)::text])))
);


--
-- TOC entry 281 (class 1259 OID 203719)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5411 (class 0 OID 0)
-- Dependencies: 281
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4914 (class 2604 OID 203720)
-- Name: admin_plantas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas ALTER COLUMN id SET DEFAULT nextval('public.admin_plantas_id_seq'::regclass);


--
-- TOC entry 4917 (class 2604 OID 203721)
-- Name: conjuntos_opciones conjunto_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conjuntos_opciones ALTER COLUMN conjunto_id SET DEFAULT nextval('public.conjuntos_opciones_conjunto_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 203722)
-- Name: departamentos departamento_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos ALTER COLUMN departamento_id SET DEFAULT nextval('public.departamentos_departamento_id_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 203723)
-- Name: empleados empleado_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados ALTER COLUMN empleado_id SET DEFAULT nextval('public.empleados_empleado_id_seq'::regclass);


--
-- TOC entry 4925 (class 2604 OID 203724)
-- Name: empresas empresa_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas ALTER COLUMN empresa_id SET DEFAULT nextval('public.empresas_empresa_id_seq'::regclass);


--
-- TOC entry 4928 (class 2604 OID 203725)
-- Name: evaluaciones evaluacion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones ALTER COLUMN evaluacion_id SET DEFAULT nextval('public.evaluaciones_evaluacion_id_seq'::regclass);


--
-- TOC entry 4932 (class 2604 OID 203726)
-- Name: opciones_conjunto opcion_conjunto_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.opciones_conjunto ALTER COLUMN opcion_conjunto_id SET DEFAULT nextval('public.opciones_conjunto_opcion_conjunto_id_seq'::regclass);


--
-- TOC entry 4933 (class 2604 OID 203727)
-- Name: pagos pago_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos ALTER COLUMN pago_id SET DEFAULT nextval('public.pagos_pago_id_seq'::regclass);


--
-- TOC entry 4936 (class 2604 OID 203728)
-- Name: planes plan_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.planes ALTER COLUMN plan_id SET DEFAULT nextval('public.planes_plan_id_seq'::regclass);


--
-- TOC entry 4939 (class 2604 OID 203729)
-- Name: plantas planta_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plantas ALTER COLUMN planta_id SET DEFAULT nextval('public.plantas_planta_id_seq'::regclass);


--
-- TOC entry 4942 (class 2604 OID 203730)
-- Name: preguntas pregunta_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas ALTER COLUMN pregunta_id SET DEFAULT nextval('public.preguntas_pregunta_id_seq'::regclass);


--
-- TOC entry 4944 (class 2604 OID 203731)
-- Name: puestos puesto_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos ALTER COLUMN puesto_id SET DEFAULT nextval('public.puestos_puesto_id_seq'::regclass);


--
-- TOC entry 4947 (class 2604 OID 203732)
-- Name: secciones_eval seccion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval ALTER COLUMN seccion_id SET DEFAULT nextval('public.secciones_eval_seccion_id_seq'::regclass);


--
-- TOC entry 4948 (class 2604 OID 203733)
-- Name: suscripciones suscripcion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones ALTER COLUMN suscripcion_id SET DEFAULT nextval('public.suscripciones_suscripcion_id_seq'::regclass);


--
-- TOC entry 4951 (class 2604 OID 203734)
-- Name: tipos_evaluacion tipo_evaluacion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_evaluacion ALTER COLUMN tipo_evaluacion_id SET DEFAULT nextval('public.tipos_evaluacion_tipo_evaluacion_id_seq'::regclass);


--
-- TOC entry 4952 (class 2604 OID 203735)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 5388 (class 0 OID 204115)
-- Dependencies: 283
-- Data for Name: admin_bd_configuracionbd; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_bd_configuracionbd (id, nombre_bd, host, puerto, usuario_admin, directorio_respaldos, max_respaldos_mantener, habilitar_respaldos_automaticos, frecuencia_respaldo_dias) FROM stdin;
\.


--
-- TOC entry 5390 (class 0 OID 204123)
-- Dependencies: 285
-- Data for Name: admin_bd_logrespaldo; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_bd_logrespaldo (id, tipo, archivo_nombre, archivo_ruta, "archivo_tamaño", tablas_incluidas, fecha_creacion, exitoso, detalles, mensaje_error, empresa_id, usuario_id) FROM stdin;
\.


--
-- TOC entry 5322 (class 0 OID 203517)
-- Dependencies: 217
-- Data for Name: admin_plantas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_plantas (id, usuario_id, planta_id, fecha_asignacion, status, password_temporal) FROM stdin;
1	10	1	2025-08-01 20:54:28.302386-07	t	\N
2	11	2	2025-08-01 20:54:29.136104-07	t	\N
3	12	8	2025-08-01 20:58:39.005245-07	t	\N
4	13	12	2025-08-01 21:02:56.322235-07	t	R8gP6tyOeU0i
5	14	13	2025-08-01 21:03:51.032773-07	t	FhYXjCo4iAnz
7	17	17	2025-08-01 21:30:08.79524-07	t	\N
8	18	18	2025-08-01 21:31:06.899761-07	t	\N
\.


--
-- TOC entry 5324 (class 0 OID 203523)
-- Dependencies: 219
-- Data for Name: asignaciones_evaluacion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asignaciones_evaluacion (id, fecha_inicio, fecha_fin, duracion_dias, estado, token_sesion, fecha_creacion, fecha_modificacion, admin_asignador_id, empresa_id, planta_id, evaluacion_oficial_id) FROM stdin;
1	2025-07-31 23:00:00-07	2025-08-30 23:00:00-07	30	activa	SESION_1_3	2025-08-01 10:09:47.177929-07	2025-08-01 10:09:47.177937-07	1	3	5	1
\.


--
-- TOC entry 5326 (class 0 OID 203527)
-- Dependencies: 221
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 5328 (class 0 OID 203531)
-- Dependencies: 223
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5330 (class 0 OID 203535)
-- Dependencies: 225
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add Token	8	add_tokenproxy
30	Can change Token	8	change_tokenproxy
31	Can delete Token	8	delete_tokenproxy
32	Can view Token	8	view_tokenproxy
33	Can add Perfil de Usuario	9	add_perfilusuario
34	Can change Perfil de Usuario	9	change_perfilusuario
35	Can delete Perfil de Usuario	9	delete_perfilusuario
36	Can view Perfil de Usuario	9	view_perfilusuario
37	Can add Empresa	10	add_empresa
38	Can change Empresa	10	change_empresa
39	Can delete Empresa	10	delete_empresa
40	Can view Empresa	10	view_empresa
41	Can add Planta	11	add_planta
42	Can change Planta	11	change_planta
43	Can delete Planta	11	delete_planta
44	Can view Planta	11	view_planta
45	Can add Departamento	12	add_departamento
46	Can change Departamento	12	change_departamento
47	Can delete Departamento	12	delete_departamento
48	Can view Departamento	12	view_departamento
49	Can add Puesto	13	add_puesto
50	Can change Puesto	13	change_puesto
51	Can delete Puesto	13	delete_puesto
52	Can view Puesto	13	view_puesto
53	Can add Empleado	14	add_empleado
54	Can change Empleado	14	change_empleado
55	Can delete Empleado	14	delete_empleado
56	Can view Empleado	14	view_empleado
57	Can add Administrador de Planta	15	add_adminplanta
58	Can change Administrador de Planta	15	change_adminplanta
59	Can delete Administrador de Planta	15	delete_adminplanta
60	Can view Administrador de Planta	15	view_adminplanta
61	Can add Tipo de Evaluación	16	add_tipoevaluacion
62	Can change Tipo de Evaluación	16	change_tipoevaluacion
63	Can delete Tipo de Evaluación	16	delete_tipoevaluacion
64	Can view Tipo de Evaluación	16	view_tipoevaluacion
65	Can add Evaluación	17	add_evaluacion
66	Can change Evaluación	17	change_evaluacion
67	Can delete Evaluación	17	delete_evaluacion
68	Can view Evaluación	17	view_evaluacion
69	Can add Sección de Evaluación	18	add_seccioneval
70	Can change Sección de Evaluación	18	change_seccioneval
71	Can delete Sección de Evaluación	18	delete_seccioneval
72	Can view Sección de Evaluación	18	view_seccioneval
73	Can add Pregunta	19	add_pregunta
74	Can change Pregunta	19	change_pregunta
75	Can delete Pregunta	19	delete_pregunta
76	Can view Pregunta	19	view_pregunta
77	Can add Conjunto de Respuestas	20	add_conjuntorespuestas
78	Can change Conjunto de Respuestas	20	change_conjuntorespuestas
79	Can delete Conjunto de Respuestas	20	delete_conjuntorespuestas
80	Can view Conjunto de Respuestas	20	view_conjuntorespuestas
81	Can add Opción de Respuesta	21	add_posiblesrespuestas
82	Can change Opción de Respuesta	21	change_posiblesrespuestas
83	Can delete Opción de Respuesta	21	delete_posiblesrespuestas
84	Can view Opción de Respuesta	21	view_posiblesrespuestas
85	Can add Pregunta de Sección	22	add_seccionpregunta
86	Can change Pregunta de Sección	22	change_seccionpregunta
87	Can delete Pregunta de Sección	22	delete_seccionpregunta
88	Can view Pregunta de Sección	22	view_seccionpregunta
89	Can add Asignación de Evaluación	23	add_asignacion
90	Can change Asignación de Evaluación	23	change_asignacion
91	Can delete Asignación de Evaluación	23	delete_asignacion
92	Can view Asignación de Evaluación	23	view_asignacion
93	Can add Asignación de Empleado	24	add_asignacionempleado
94	Can change Asignación de Empleado	24	change_asignacionempleado
95	Can delete Asignación de Empleado	24	delete_asignacionempleado
96	Can view Asignación de Empleado	24	view_asignacionempleado
97	Can add Respuesta de Empleado	25	add_respuestaempleado
98	Can change Respuesta de Empleado	25	change_respuestaempleado
99	Can delete Respuesta de Empleado	25	delete_respuestaempleado
100	Can view Respuesta de Empleado	25	view_respuestaempleado
101	Can add Resultado de Evaluación	26	add_resultadoevaluacion
102	Can change Resultado de Evaluación	26	change_resultadoevaluacion
103	Can delete Resultado de Evaluación	26	delete_resultadoevaluacion
104	Can view Resultado de Evaluación	26	view_resultadoevaluacion
105	Can add Plan de Suscripción	27	add_plansuscripcion
106	Can change Plan de Suscripción	27	change_plansuscripcion
107	Can delete Plan de Suscripción	27	delete_plansuscripcion
108	Can view Plan de Suscripción	27	view_plansuscripcion
109	Can add Suscripción de Empresa	28	add_suscripcionempresa
110	Can change Suscripción de Empresa	28	change_suscripcionempresa
111	Can delete Suscripción de Empresa	28	delete_suscripcionempresa
112	Can view Suscripción de Empresa	28	view_suscripcionempresa
113	Can add Pago	29	add_pago
114	Can change Pago	29	change_pago
115	Can delete Pago	29	delete_pago
116	Can view Pago	29	view_pago
117	Can add suscripcion empresa export	30	add_suscripcionempresaexport
118	Can change suscripcion empresa export	30	change_suscripcionempresaexport
119	Can delete suscripcion empresa export	30	delete_suscripcionempresaexport
120	Can view suscripcion empresa export	30	view_suscripcionempresaexport
121	Can add pago export	31	add_pagoexport
122	Can change pago export	31	change_pagoexport
123	Can delete pago export	31	delete_pagoexport
124	Can view pago export	31	view_pagoexport
125	Can add Tipo de Evaluación	32	add_tipoevaluacion
126	Can change Tipo de Evaluación	32	change_tipoevaluacion
127	Can delete Tipo de Evaluación	32	delete_tipoevaluacion
128	Can view Tipo de Evaluación	32	view_tipoevaluacion
129	Can add Pregunta	33	add_pregunta
130	Can change Pregunta	33	change_pregunta
131	Can delete Pregunta	33	delete_pregunta
132	Can view Pregunta	33	view_pregunta
133	Can add Evaluación	34	add_evaluacioncompleta
134	Can change Evaluación	34	change_evaluacioncompleta
135	Can delete Evaluación	34	delete_evaluacioncompleta
136	Can view Evaluación	34	view_evaluacioncompleta
137	Can add evaluacion pregunta	35	add_evaluacionpregunta
138	Can change evaluacion pregunta	35	change_evaluacionpregunta
139	Can delete evaluacion pregunta	35	delete_evaluacionpregunta
140	Can view evaluacion pregunta	35	view_evaluacionpregunta
141	Can add Respuesta a Evaluación	36	add_respuestaevaluacion
142	Can change Respuesta a Evaluación	36	change_respuestaevaluacion
143	Can delete Respuesta a Evaluación	36	delete_respuestaevaluacion
144	Can view Respuesta a Evaluación	36	view_respuestaevaluacion
145	Can add Detalle de Respuesta	37	add_detallerespuesta
146	Can change Detalle de Respuesta	37	change_detallerespuesta
147	Can delete Detalle de Respuesta	37	delete_detallerespuesta
148	Can view Detalle de Respuesta	37	view_detallerespuesta
149	Can add Resultado de Evaluación	38	add_resultadoevaluacion
150	Can change Resultado de Evaluación	38	change_resultadoevaluacion
151	Can delete Resultado de Evaluación	38	delete_resultadoevaluacion
152	Can view Resultado de Evaluación	38	view_resultadoevaluacion
153	Can add seccion eval	39	add_seccioneval
154	Can change seccion eval	39	change_seccioneval
155	Can delete seccion eval	39	delete_seccioneval
156	Can view seccion eval	39	view_seccioneval
157	Can add seccion pregunta	40	add_seccionpregunta
158	Can change seccion pregunta	40	change_seccionpregunta
159	Can delete seccion pregunta	40	delete_seccionpregunta
160	Can view seccion pregunta	40	view_seccionpregunta
161	Can add Log de Respaldo	41	add_logrespaldo
162	Can change Log de Respaldo	41	change_logrespaldo
163	Can delete Log de Respaldo	41	delete_logrespaldo
164	Can view Log de Respaldo	41	view_logrespaldo
165	Can add Configuración de BD	42	add_configuracionbd
166	Can change Configuración de BD	42	change_configuracionbd
167	Can delete Configuración de BD	42	delete_configuracionbd
168	Can view Configuración de BD	42	view_configuracionbd
169	Can add Evaluación Oficial	43	add_evaluacionoficial
170	Can change Evaluación Oficial	43	change_evaluacionoficial
171	Can delete Evaluación Oficial	43	delete_evaluacionoficial
172	Can view Evaluación Oficial	43	view_evaluacionoficial
173	Can add Empleado Asignado	44	add_empleadoasignado
174	Can change Empleado Asignado	44	change_empleadoasignado
175	Can delete Empleado Asignado	44	delete_empleadoasignado
176	Can view Empleado Asignado	44	view_empleadoasignado
177	Can add Pregunta Oficial	45	add_preguntaoficial
178	Can change Pregunta Oficial	45	change_preguntaoficial
179	Can delete Pregunta Oficial	45	delete_preguntaoficial
180	Can view Pregunta Oficial	45	view_preguntaoficial
181	Can add Sección Oficial	46	add_seccionoficial
182	Can change Sección Oficial	46	change_seccionoficial
183	Can delete Sección Oficial	46	delete_seccionoficial
184	Can view Sección Oficial	46	view_seccionoficial
185	Can add Respuesta de Empleado	47	add_respuestaempleado
186	Can change Respuesta de Empleado	47	change_respuestaempleado
187	Can delete Respuesta de Empleado	47	delete_respuestaempleado
188	Can view Respuesta de Empleado	47	view_respuestaempleado
189	Can add Asignación de Evaluación	48	add_asignacionevaluacion
190	Can change Asignación de Evaluación	48	change_asignacionevaluacion
191	Can delete Asignación de Evaluación	48	delete_asignacionevaluacion
192	Can view Asignación de Evaluación	48	view_asignacionevaluacion
\.


--
-- TOC entry 5332 (class 0 OID 203539)
-- Dependencies: 227
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
19	pbkdf2_sha256$1000000$081Kg2m1F4RyIzEduT9P19$7+TaOMCRbkGnkw4dk4tYhJ7uiLjVvPXAq5a2fk6f2Yk=	\N	f	admin_planta_norte	Carlos	Rodriguez	admin.norte@techcorp.com	f	t	2025-08-01 20:51:24.542227-07
21	pbkdf2_sha256$1000000$KdTn928wdI0nNKglTTu3sE$rgaFspUtdgGTX6w1kS//sZbZ/yOLv4Gwah46il8Gfr4=	\N	f	admin_planta_sur	Maria	Lopez	admin.sur@techcorp.com	f	t	2025-08-01 20:54:28.309483-07
22	pbkdf2_sha256$1000000$Rvfho7HqQigBkbUodddNzI$q2bHNOdguFcX8n0H8ZVpKOQcN+Zx0LdZhWDAYlVF8MM=	\N	f	admin_planta_axis5	Pedro	Martinez	admin.planta@axis5.com	f	t	2025-08-01 20:58:38.157131-07
23	pbkdf2_sha256$1000000$ndJDaM2Mae4hg5SqaH8vdT$WQGRtfVC4e060TLnNqKGr76AzLpVTVtqngbn+d7d3x0=	\N	f	admin_planta_11	Admin	Planta Planta Prueba Automatica	admin.planta.11@axisdevelopment5.com	f	t	2025-08-01 21:01:39.641985-07
25	pbkdf2_sha256$1000000$qF0Csq97aIm1Crwqmy6ya5$MBdjpkohUWrPP4spW8PCPqwypyhQFU3D3jQG63EHmDw=	\N	f	admin_planta_13	Admin	Planta Planta Automatica Final	admin.planta.13@axisdevelopment5.com	f	t	2025-08-01 21:03:51.04637-07
26	pbkdf2_sha256$1000000$7H2I96PuqNuIaxO1h1jTHG$dU1T8l37YsNBu4qpnuDo+c3V7c23v6jaQvk2MQFw0ks=	\N	f	admin_planta_14	Admin	Planta Planta Test Usuario Auto	admin.planta.14@axisdevelopment5.com	f	t	2025-08-01 21:05:16.70825-07
27	pbkdf2_sha256$1000000$gjozBhNi92UgEyuM1Uh7XG$n8zKom11uOHIBmtFdJkMgKQbQEnvRc0CwraeHnV9tvA=	\N	f	planta_manager_1	Juan	García López	juan.garcia@techcorp.com	f	t	2025-08-01 21:15:14.605679-07
29	pbkdf2_sha256$1000000$VHOMJbFkDueN1RAf6rvJa2$RnRhFpu8RAQdN2hBLl7kMrCEO03ykP4ji/UOFdtWLGc=	\N	f	admin_planta_con_usuario_auto	Admin Planta Con Usuario Auto	Plant Manager	admin_planta_con_usuario_auto@techcorpsolutions.com	f	t	2025-08-01 21:31:06.91496-07
28	pbkdf2_sha256$1000000$Ne6KWlLsZ0Lro0w9jOLdzl$Mee+Vkk6ZSj0x+PrtAJFUbYhwlDrbQh7rIfV1YRc2gc=	\N	f	admin_planta_automatica_renovada	Admin Planta Automatica Renovada	Plant Manager	admin_planta_automatica_renovada@techcorpsolutions.com	f	t	2025-08-01 21:30:08.808928-07
2	pbkdf2_sha256$1000000$XkLkS1ejGukk4UtwVucAVW$yfKce37LL9tLRdv2lc0rLeI6xPA23oxpY72C5i2juiQ=	\N	f	admin_techcorpp	Admin	TechCorp	admin@techcorp.mx	f	t	2025-07-31 21:57:01.376967-07
24	pbkdf2_sha256$1000000$Kr3zb1Mvrcc0aDh5QHvRTK$nRVHzbYBSSDQ5e5GCHIStI7hafYRcXrxQy5qbjxdkSs=	\N	f	admin_planta_12	Admin	Planta Planta Automatica 2	admin.planta.12@axisdevelopment5.com	f	t	2025-08-01 21:02:56.338491-07
4	pbkdf2_sha256$1000000$cLsdZva8QvI4QJNlJqH2gH$J/9PokV+XPnmszt2spG7QdloQ65SplpeMyoQkga3pPE=	\N	f	admin_temp			admin_temp@axyoma.com	f	t	2025-07-31 23:40:53.382623-07
3	pbkdf2_sha256$1000000$RRtexn5eL0HKphLKsmYQvV$4m29NgPaVSGI3DFhzO1yDdg6ay++mY/we7/9OuaGjxw=	\N	f	admin_innovasoft	Admin	InnovaSoft	admin@innovasoft.mx	f	t	2025-07-31 21:57:02.243672-07
5	pbkdf2_sha256$1000000$OFio5F7N7DiYhZMvRIzTyt$BHW/s/pppUGIRfW0jH/1EQOoEgZy/m0mrXXLAl65vHM=	\N	f	ernesto			ernesto@axyoma.com	f	t	2025-08-01 00:59:35.804536-07
13	pbkdf2_sha256$1000000$huscBMAYjDZ7k4r4jiL8Cf$13YujsbJWNpIaRZAoDOE8THkNnuE4dd1d18rJTlr7mA=	\N	f	axis2			axis2@gmail.com	f	t	2025-08-01 01:20:14.777463-07
14	pbkdf2_sha256$1000000$Hu9obkzdLwRytUg0T9KYne$I0QLFPrsIENyy7MPETnkJInOYXCUrEYPv7F52k0NErw=	\N	f	axis3			axis3@gmail.com	f	t	2025-08-01 01:28:34.469042-07
15	pbkdf2_sha256$1000000$DhQGQhhyLCdkJEoyGOsxzt$SJocr4EA8GjZfMGYX8KxlmmW41roXFI5T+izGr5AI2Q=	\N	f	axis4			axis4@gmail.com	f	t	2025-08-01 01:41:49.680019-07
16	pbkdf2_sha256$1000000$K35Fgu4FQGBj8Ku036gNW6$3EDDDM1iJwUgESpJzjM7Lc7q+UEWSaoAC+uZiPwmdD8=	\N	f	axis5			axis5@gmail.com	f	t	2025-08-01 02:01:28.977445-07
17	pbkdf2_sha256$1000000$pE0ZZPa190rRHrxDh1ypF7$Nlyf9ahipVEM4Wz8CoORTFfQOeNv4STrVQy1g7Gstmk=	\N	f	admin_planta_9	Admin	Planta Planta 2	admin.planta.9@axisdevelopment2.com	f	t	2025-08-01 18:52:03.485455-07
18	pbkdf2_sha256$1000000$MrFEroQ5PEC06piZpscagk$uUyzOGPvW8p882DCg7PqpY7bHixDQa2f8I1DPkywZCc=	\N	f	admin_planta_10	Admin	Planta planta 3	admin.planta.10@axisdevelopment2.com	f	t	2025-08-01 19:53:27.237744-07
1	pbkdf2_sha256$1000000$OHvSjQOZ2pm4l0V8aYWOHh$xLV/Ag+YgR2cxJv/SE7iSPGuAZScJmAhcTTVSwdR1gQ=	2025-08-02 17:50:27.307886-07	t	superadmin	Super	Admin	superadmin@axyoma.com	t	t	2025-07-31 21:54:48.35281-07
32	pbkdf2_sha256$390000$xAu1wwLnv11k$CDEcEUk3h5lEeR8O4/GoiKchRvLqfWyEeRPNQ4pOGks=	\N	t	testuser	Super	Admin	testuser@axyoma.com	t	t	2025-08-02 18:51:13.941752-07
\.


--
-- TOC entry 5333 (class 0 OID 203544)
-- Dependencies: 228
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 5336 (class 0 OID 203549)
-- Dependencies: 231
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5338 (class 0 OID 203553)
-- Dependencies: 233
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
cf3aa920fb9ffc9e8a3b78a0e31423d174aefd78	2025-07-31 21:57:45.396623-07	1
afd5e109fa264421d1aa7f771189eef985869045	2025-08-01 01:27:47.033402-07	13
17e70020ea8897b00eed5e74f71b21cce5a03498	2025-08-01 02:08:29.512158-07	16
41a7d0b9d098094d0ca225b3164857d343a62d7f	2025-08-01 20:50:26.711778-07	2
9437f2721eefd9c33398ed4d7621c2660db2079d	2025-08-01 20:54:28.307717-07	19
e6110658e47625c177b1729cd3ff71488fd51a42	2025-08-01 20:54:29.136904-07	21
d032bb7cf793568de06db72d331b4cf4ad063347	2025-08-01 20:58:39.006153-07	22
cb39e1df596b7e79137de1028a9d3385eecf867b	2025-08-01 21:15:15.485414-07	27
2e168480b0ca28e262aa2f2c871f6eac30ab515b	2025-08-01 21:30:10.048221-07	28
e88a1d08222911dd20bede6e33b62ccd9c09fcef	2025-08-01 21:31:08.222656-07	29
a5b9e693071739e5ea71e63c4995905a56a1f478	2025-08-01 22:14:22.262358-07	24
dda278f2a1a26a66376eff4e54dc8ca1f0dc0fe7	2025-08-02 19:17:01.476851-07	32
\.


--
-- TOC entry 5339 (class 0 OID 203556)
-- Dependencies: 234
-- Data for Name: conjuntos_opciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.conjuntos_opciones (conjunto_id, nombre, descripcion, predefinido) FROM stdin;
\.


--
-- TOC entry 5341 (class 0 OID 203563)
-- Dependencies: 236
-- Data for Name: departamentos; Type: TABLE DATA; Schema: public; Owner: -
--

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
\.


--
-- TOC entry 5343 (class 0 OID 203571)
-- Dependencies: 238
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 5345 (class 0 OID 203578)
-- Dependencies: 240
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	authtoken	token
8	authtoken	tokenproxy
9	users	perfilusuario
10	users	empresa
11	users	planta
12	users	departamento
13	users	puesto
14	users	empleado
15	users	adminplanta
16	users	tipoevaluacion
17	users	evaluacion
18	users	seccioneval
19	users	pregunta
20	users	conjuntorespuestas
21	users	posiblesrespuestas
22	users	seccionpregunta
23	users	asignacion
24	users	asignacionempleado
25	users	respuestaempleado
26	users	resultadoevaluacion
27	subscriptions	plansuscripcion
28	subscriptions	suscripcionempresa
29	subscriptions	pago
30	subscriptions	suscripcionempresaexport
31	subscriptions	pagoexport
32	evaluaciones	tipoevaluacion
33	evaluaciones	pregunta
34	evaluaciones	evaluacioncompleta
35	evaluaciones	evaluacionpregunta
36	evaluaciones	respuestaevaluacion
37	evaluaciones	detallerespuesta
38	evaluaciones	resultadoevaluacion
39	evaluaciones	seccioneval
40	evaluaciones	seccionpregunta
41	admin_bd	logrespaldo
42	admin_bd	configuracionbd
43	evaluaciones	evaluacionoficial
44	evaluaciones	empleadoasignado
45	evaluaciones	preguntaoficial
46	evaluaciones	seccionoficial
47	evaluaciones	respuestaempleado
48	evaluaciones	asignacionevaluacion
\.


--
-- TOC entry 5347 (class 0 OID 203582)
-- Dependencies: 242
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-07-22 12:53:22.011-07
2	auth	0001_initial	2025-07-22 12:53:22.064833-07
3	admin	0001_initial	2025-07-22 12:53:22.082116-07
4	admin	0002_logentry_remove_auto_add	2025-07-22 12:53:22.08807-07
5	admin	0003_logentry_add_action_flag_choices	2025-07-22 12:53:22.094581-07
6	contenttypes	0002_remove_content_type_name	2025-07-22 12:53:22.106879-07
7	auth	0002_alter_permission_name_max_length	2025-07-22 12:53:22.11276-07
8	auth	0003_alter_user_email_max_length	2025-07-22 12:53:22.119562-07
9	auth	0004_alter_user_username_opts	2025-07-22 12:53:22.125443-07
10	auth	0005_alter_user_last_login_null	2025-07-22 12:53:22.13199-07
11	auth	0006_require_contenttypes_0002	2025-07-22 12:53:22.133093-07
12	auth	0007_alter_validators_add_error_messages	2025-07-22 12:53:22.138422-07
13	auth	0008_alter_user_username_max_length	2025-07-22 12:53:22.147327-07
14	auth	0009_alter_user_last_name_max_length	2025-07-22 12:53:22.153918-07
15	auth	0010_alter_group_name_max_length	2025-07-22 12:53:22.161203-07
16	auth	0011_update_proxy_permissions	2025-07-22 12:53:22.166755-07
17	auth	0012_alter_user_first_name_max_length	2025-07-22 12:53:22.173441-07
18	authtoken	0001_initial	2025-07-22 12:53:22.186101-07
19	authtoken	0002_auto_20160226_1747	2025-07-22 12:53:22.212177-07
20	authtoken	0003_tokenproxy	2025-07-22 12:53:22.213784-07
21	authtoken	0004_alter_tokenproxy_options	2025-07-22 12:53:22.217218-07
22	users	0001_initial	2025-07-30 07:51:15.981785-07
23	subscriptions	0001_initial	2025-07-30 07:51:30.731261-07
24	evaluaciones	0001_initial	2025-07-30 07:52:12.504555-07
26	sessions	0001_initial	2025-07-30 07:52:33.184174-07
27	evaluaciones	0002_seccioneval_seccionpregunta	2025-07-30 09:27:04.534393-07
28	users	0002_auto_20250730_1507	2025-07-30 17:20:10.139153-07
29	evaluaciones	0002_evaluacionoficial_asignacionevaluacion_and_more	2025-08-01 10:00:14.995498-07
30	admin_bd	0001_initial	2025-08-02 17:49:38.301144-07
\.


--
-- TOC entry 5349 (class 0 OID 203588)
-- Dependencies: 244
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
gbk62t9r1rvqaxg4awsyjifii9b9e4sp	.eJxVjEEOwiAQRe_C2hBBygwu3XsGMjCDVA1NSrsy3l2bdKHb_977LxVpXWpcu8xxZHVWRh1-t0T5IW0DfKd2m3Se2jKPSW-K3mnX14nledndv4NKvX7rgoN4TICJT0hgxBYDYMVZLx7I4cAhFPSO0LgMGIwLELj4Y2awuaj3B9YON38:1uiMvj:Rk2i_HsHX2Oh6M9OOAH5VFzH9QgLwiXE6ax6EZxuF1A	2025-08-16 17:50:27.310009-07
\.


--
-- TOC entry 5350 (class 0 OID 203593)
-- Dependencies: 245
-- Data for Name: empleados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empleados (empleado_id, nombre, apellido_paterno, apellido_materno, email, telefono, fecha_ingreso, fecha_registro, status, puesto) FROM stdin;
1	Empleado5647	Apellido5647	Test	emp5647@test.com	4426125315	2025-05-01	2025-08-01 04:57:03.016648	t	1
2	Empleado8656	Apellido8656	Test	emp8656@test.com	4423645328	2024-10-05	2025-08-01 04:57:03.018488	t	2
3	Empleado4859	Apellido4859	Test	emp4859@test.com	4421596926	2025-04-29	2025-08-01 04:57:03.020143	t	3
4	Empleado9139	Apellido9139	Test	emp9139@test.com	4421574844	2025-04-21	2025-08-01 04:57:03.021349	t	4
5	Empleado2856	Apellido2856	Test	emp2856@test.com	4423706395	2024-11-10	2025-08-01 04:57:03.022014	t	4
6	Empleado9436	Apellido9436	Test	emp9436@test.com	4421764635	2024-09-12	2025-08-01 04:57:03.023434	t	5
7	Empleado6744	Apellido6744	Test	emp6744@test.com	4423761261	2024-11-28	2025-08-01 04:57:03.024063	t	5
8	Empleado7013	Apellido7013	Test	emp7013@test.com	4423058053	2024-08-06	2025-08-01 04:57:03.027406	t	6
9	Empleado2488	Apellido2488	Test	emp2488@test.com	4425627863	2025-03-16	2025-08-01 04:57:03.02865	t	7
10	Empleado3976	Apellido3976	Test	emp3976@test.com	4424227724	2024-09-19	2025-08-01 04:57:03.029717	t	8
11	Empleado9662	Apellido9662	Test	emp9662@test.com	4427434336	2025-04-19	2025-08-01 04:57:03.030817	t	9
12	Empleado5760	Apellido5760	Test	emp5760@test.com	4426776548	2025-03-09	2025-08-01 04:57:03.031352	t	9
13	Empleado7741	Apellido7741	Test	emp7741@test.com	4429924733	2025-05-10	2025-08-01 04:57:03.032345	t	10
14	Empleado9290	Apellido9290	Test	emp9290@test.com	4424332978	2024-12-30	2025-08-01 04:57:03.03288	t	10
15	Empleado1450	Apellido1450	Test	emp1450@test.com	4423479435	2024-09-01	2025-08-01 04:57:03.035521	t	11
16	Empleado2365	Apellido2365	Test	emp2365@test.com	4426543101	2024-11-24	2025-08-01 04:57:03.036399	t	12
17	Empleado9391	Apellido9391	Test	emp9391@test.com	4421790504	2025-05-07	2025-08-01 04:57:03.037336	t	13
18	Empleado5168	Apellido5168	Test	emp5168@test.com	4423024732	2025-01-05	2025-08-01 04:57:03.038279	t	14
19	Empleado2078	Apellido2078	Test	emp2078@test.com	4429032001	2024-09-30	2025-08-01 04:57:03.03879	t	14
20	Empleado2257	Apellido2257	Test	emp2257@test.com	4428144964	2025-01-28	2025-08-01 04:57:03.039737	t	15
21	Empleado3527	Apellido3527	Test	emp3527@test.com	4427528925	2024-10-16	2025-08-01 04:57:03.040256	t	15
22	Empleado6725	Apellido6725	Test	emp6725@test.com	4426511910	2025-05-31	2025-08-01 04:57:03.042817	t	16
23	Empleado3789	Apellido3789	Test	emp3789@test.com	4427665761	2025-02-16	2025-08-01 04:57:03.044538	t	17
24	Empleado1602	Apellido1602	Test	emp1602@test.com	4427897324	2025-06-29	2025-08-01 04:57:03.04573	t	18
25	Empleado4735	Apellido4735	Test	emp4735@test.com	4421114599	2024-09-06	2025-08-01 04:57:03.046678	t	19
26	Empleado6117	Apellido6117	Test	emp6117@test.com	4426327238	2025-03-10	2025-08-01 04:57:03.047168	t	19
27	Empleado2957	Apellido2957	Test	emp2957@test.com	4426747565	2024-12-05	2025-08-01 04:57:03.048105	t	20
28	Empleado9602	Apellido9602	Test	emp9602@test.com	4429420706	2025-04-28	2025-08-01 04:57:03.048591	t	20
29	Empleado1587	Apellido1587	Test	emp1587@test.com	4425518612	2025-05-18	2025-08-01 04:57:03.051169	t	21
30	Empleado8064	Apellido8064	Test	emp8064@test.com	4426565656	2024-09-24	2025-08-01 04:57:03.052073	t	22
31	Empleado8804	Apellido8804	Test	emp8804@test.com	4426985030	2025-01-25	2025-08-01 04:57:03.053086	t	23
32	Empleado4028	Apellido4028	Test	emp4028@test.com	4423945986	2025-05-16	2025-08-01 04:57:03.054106	t	24
33	Empleado6839	Apellido6839	Test	emp6839@test.com	4421576664	2024-11-08	2025-08-01 04:57:03.054695	t	24
34	Empleado4605	Apellido4605	Test	emp4605@test.com	4421800630	2024-12-11	2025-08-01 04:57:03.055903	t	25
35	Empleado5197	Apellido5197	Test	emp5197@test.com	4423632719	2025-05-17	2025-08-01 04:57:03.0565	t	25
36	Empleado8732	Apellido8732	Test	emp8732@test.com	4426627712	2024-09-03	2025-08-01 04:57:03.059358	t	26
37	Empleado5198	Apellido5198	Test	emp5198@test.com	4425898739	2024-09-03	2025-08-01 04:57:03.060344	t	27
38	Empleado2871	Apellido2871	Test	emp2871@test.com	4421502827	2024-08-06	2025-08-01 04:57:03.061318	t	28
39	Empleado6864	Apellido6864	Test	emp6864@test.com	4422854615	2025-06-09	2025-08-01 04:57:03.062533	t	29
40	Empleado4000	Apellido4000	Test	emp4000@test.com	4428655634	2024-12-20	2025-08-01 04:57:03.063166	t	29
41	Empleado6355	Apellido6355	Test	emp6355@test.com	4426833833	2024-11-12	2025-08-01 04:57:03.064169	t	30
42	Empleado7309	Apellido7309	Test	emp7309@test.com	4428402960	2024-09-01	2025-08-01 04:57:03.064632	t	30
43	Empleado4259	Apellido4259	Test	emp4259@test.com	4429863604	2025-03-02	2025-08-01 04:57:03.067627	t	31
44	Empleado7668	Apellido7668	Test	emp7668@test.com	4423141314	2024-12-18	2025-08-01 04:57:03.068555	t	32
45	Empleado9617	Apellido9617	Test	emp9617@test.com	4425626939	2025-02-01	2025-08-01 04:57:03.069469	t	33
46	Empleado5740	Apellido5740	Test	emp5740@test.com	4424443969	2025-01-23	2025-08-01 04:57:03.070408	t	34
47	Empleado8264	Apellido8264	Test	emp8264@test.com	4422763748	2025-05-20	2025-08-01 04:57:03.070922	t	34
48	Empleado3849	Apellido3849	Test	emp3849@test.com	4424097565	2024-11-17	2025-08-01 04:57:03.071867	t	35
49	Empleado9145	Apellido9145	Test	emp9145@test.com	4427916483	2025-04-09	2025-08-01 04:57:03.072454	t	35
50	Empleado3700	Apellido3700	Test	emp3700@test.com	4426755563	2025-03-20	2025-08-01 04:57:03.074815	t	36
51	Empleado9701	Apellido9701	Test	emp9701@test.com	4423142270	2024-10-19	2025-08-01 04:57:03.075709	t	37
52	Empleado8980	Apellido8980	Test	emp8980@test.com	4428789901	2025-05-16	2025-08-01 04:57:03.076711	t	38
53	Empleado4324	Apellido4324	Test	emp4324@test.com	4425060943	2025-06-11	2025-08-01 04:57:03.077736	t	39
54	Empleado9256	Apellido9256	Test	emp9256@test.com	4425006958	2025-04-12	2025-08-01 04:57:03.078281	t	39
55	Empleado2845	Apellido2845	Test	emp2845@test.com	4426953311	2025-03-12	2025-08-01 04:57:03.079507	t	40
56	Empleado3055	Apellido3055	Test	emp3055@test.com	4424583548	2025-04-11	2025-08-01 04:57:03.080013	t	40
57	Empleado7033	Apellido7033	Test	emp7033@test.com	4428725747	2025-02-15	2025-08-01 04:57:03.08247	t	41
58	Empleado4318	Apellido4318	Test	emp4318@test.com	4423357848	2025-05-12	2025-08-01 04:57:03.0834	t	42
59	Empleado5309	Apellido5309	Test	emp5309@test.com	4425898683	2025-06-07	2025-08-01 04:57:03.08435	t	43
60	Empleado5876	Apellido5876	Test	emp5876@test.com	4426151521	2025-06-24	2025-08-01 04:57:03.085312	t	44
61	Empleado4736	Apellido4736	Test	emp4736@test.com	4429673946	2025-02-12	2025-08-01 04:57:03.085776	t	44
62	Empleado3449	Apellido3449	Test	emp3449@test.com	4421444599	2024-12-14	2025-08-01 04:57:03.086864	t	45
63	Empleado8807	Apellido8807	Test	emp8807@test.com	4428786448	2024-08-02	2025-08-01 04:57:03.087886	t	45
64	Empleado7959	Apellido7959	Test	emp7959@test.com	4428710083	2025-03-03	2025-08-01 04:57:03.090561	t	46
65	Empleado3334	Apellido3334	Test	emp3334@test.com	4425883843	2024-11-26	2025-08-01 04:57:03.091673	t	47
66	Empleado6865	Apellido6865	Test	emp6865@test.com	4424313749	2024-11-26	2025-08-01 04:57:03.092713	t	48
67	Empleado7189	Apellido7189	Test	emp7189@test.com	4423376414	2025-02-10	2025-08-01 04:57:03.093671	t	49
68	Empleado2017	Apellido2017	Test	emp2017@test.com	4428860551	2024-08-16	2025-08-01 04:57:03.094207	t	49
69	Empleado4496	Apellido4496	Test	emp4496@test.com	4426398884	2024-08-25	2025-08-01 04:57:03.095301	t	50
70	Empleado5004	Apellido5004	Test	emp5004@test.com	4428638644	2025-05-10	2025-08-01 04:57:03.09587	t	50
71	Empleado9601	Apellido9601	Test	emp9601@test.com	4421393566	2025-06-05	2025-08-01 04:57:03.098512	t	51
72	Empleado1245	Apellido1245	Test	emp1245@test.com	4422629376	2025-05-12	2025-08-01 04:57:03.100071	t	52
73	Empleado7463	Apellido7463	Test	emp7463@test.com	4427124326	2024-09-15	2025-08-01 04:57:03.101032	t	53
74	Empleado1746	Apellido1746	Test	emp1746@test.com	4427792413	2025-03-05	2025-08-01 04:57:03.102113	t	54
75	Empleado1683	Apellido1683	Test	emp1683@test.com	4425954697	2025-04-12	2025-08-01 04:57:03.102587	t	54
77	Empleado7924	Apellido7924	Test	emp7924@test.com	4427078742	2025-02-24	2025-08-01 04:57:03.103984	t	55
78	Empleado6390	Apellido6390	Test	emp6390@test.com	4424069765	2024-07-31	2025-08-01 04:57:03.106506	t	56
79	Empleado4139	Apellido4139	Test	emp4139@test.com	4422288982	2025-04-18	2025-08-01 04:57:03.107465	t	57
80	Empleado6183	Apellido6183	Test	emp6183@test.com	4426675606	2024-08-19	2025-08-01 04:57:03.108386	t	58
81	Empleado6249	Apellido6249	Test	emp6249@test.com	4423986167	2025-04-19	2025-08-01 04:57:03.109274	t	59
82	Empleado6206	Apellido6206	Test	emp6206@test.com	4429396267	2024-10-21	2025-08-01 04:57:03.109752	t	59
83	Empleado2092	Apellido2092	Test	emp2092@test.com	4422509086	2024-10-23	2025-08-01 04:57:03.110704	t	60
84	Empleado1703	Apellido1703	Test	emp1703@test.com	4429814747	2024-10-25	2025-08-01 04:57:03.111261	t	60
85	Empleado4679	Apellido4679	Test	emp4679@test.com	4424086424	2025-05-19	2025-08-01 04:57:03.113906	t	61
86	Empleado7998	Apellido7998	Test	emp7998@test.com	4422233202	2024-11-06	2025-08-01 04:57:03.114784	t	62
87	Empleado6960	Apellido6960	Test	emp6960@test.com	4422354573	2024-09-18	2025-08-01 04:57:03.115699	t	63
88	Empleado5763	Apellido5763	Test	emp5763@test.com	4428758373	2025-04-05	2025-08-01 04:57:03.116707	t	64
89	Empleado9458	Apellido9458	Test	emp9458@test.com	4421915373	2025-01-27	2025-08-01 04:57:03.117277	t	64
90	Empleado1145	Apellido1145	Test	emp1145@test.com	4424815040	2024-12-31	2025-08-01 04:57:03.118146	t	65
91	Empleado1550	Apellido1550	Test	emp1550@test.com	4428464971	2024-08-29	2025-08-01 04:57:03.118622	t	65
92	Empleado7334	Apellido7334	Test	emp7334@test.com	4421703769	2024-12-06	2025-08-01 04:57:03.121039	t	66
93	Empleado9302	Apellido9302	Test	emp9302@test.com	4423697569	2025-06-29	2025-08-01 04:57:03.121933	t	67
94	Empleado6276	Apellido6276	Test	emp6276@test.com	4423215047	2024-12-21	2025-08-01 04:57:03.122921	t	68
95	Empleado8474	Apellido8474	Test	emp8474@test.com	4422523418	2024-10-28	2025-08-01 04:57:03.123845	t	69
96	Empleado5774	Apellido5774	Test	emp5774@test.com	4422638334	2024-09-10	2025-08-01 04:57:03.124341	t	69
97	Empleado4792	Apellido4792	Test	emp4792@test.com	4421296696	2025-01-22	2025-08-01 04:57:03.125241	t	70
98	Empleado2433	Apellido2433	Test	emp2433@test.com	4422300833	2024-11-03	2025-08-01 04:57:03.125712	t	70
99	Empleado6722	Apellido6722	Test	emp6722@test.com	4428152915	2025-06-20	2025-08-01 04:57:03.128459	t	71
100	Empleado2942	Apellido2942	Test	emp2942@test.com	4429148089	2025-06-21	2025-08-01 04:57:03.129556	t	72
101	Empleado7864	Apellido7864	Test	emp7864@test.com	4427866590	2024-09-03	2025-08-01 04:57:03.13058	t	73
102	Empleado5091	Apellido5091	Test	emp5091@test.com	4427045156	2024-11-22	2025-08-01 04:57:03.131527	t	74
103	Empleado6048	Apellido6048	Test	emp6048@test.com	4429118601	2025-04-20	2025-08-01 04:57:03.132026	t	74
104	Empleado8288	Apellido8288	Test	emp8288@test.com	4425492330	2024-12-26	2025-08-01 04:57:03.132916	t	75
105	Empleado2926	Apellido2926	Test	emp2926@test.com	4427122190	2025-02-01	2025-08-01 04:57:03.133377	t	75
106	Empleado7960	Apellido7960	Test	emp7960@test.com	4424217093	2025-01-28	2025-08-01 04:57:03.135829	t	76
107	Empleado6376	Apellido6376	Test	emp6376@test.com	4421767606	2025-02-26	2025-08-01 04:57:03.136702	t	77
108	Empleado7492	Apellido7492	Test	emp7492@test.com	4429307053	2025-06-18	2025-08-01 04:57:03.137658	t	78
109	Empleado5921	Apellido5921	Test	emp5921@test.com	4423269768	2025-06-23	2025-08-01 04:57:03.13854	t	79
110	Empleado4708	Apellido4708	Test	emp4708@test.com	4427105238	2024-10-23	2025-08-01 04:57:03.139036	t	79
111	Empleado8337	Apellido8337	Test	emp8337@test.com	4426708404	2025-04-13	2025-08-01 04:57:03.139963	t	80
112	Empleado8582	Apellido8582	Test	emp8582@test.com	4428987486	2025-02-25	2025-08-01 04:57:03.140466	t	80
113	Empleado1566	Apellido1566	Test	emp1566@test.com	4429001763	2025-04-06	2025-08-01 04:57:03.142834	t	81
114	Empleado1472	Apellido1472	Test	emp1472@test.com	4428971586	2025-05-11	2025-08-01 04:57:03.143746	t	82
115	Empleado5742	Apellido5742	Test	emp5742@test.com	4427212858	2024-12-05	2025-08-01 04:57:03.144716	t	83
116	Empleado4111	Apellido4111	Test	emp4111@test.com	4427554517	2024-10-20	2025-08-01 04:57:03.145776	t	84
117	Empleado1134	Apellido1134	Test	emp1134@test.com	4423711857	2025-06-20	2025-08-01 04:57:03.146286	t	84
118	Empleado6076	Apellido6076	Test	emp6076@test.com	4426020336	2024-10-15	2025-08-01 04:57:03.147252	t	85
119	Empleado5211	Apellido5211	Test	emp5211@test.com	4428495837	2025-03-13	2025-08-01 04:57:03.147718	t	85
120	Empleado5708	Apellido5708	Test	emp5708@test.com	4426598807	2025-03-20	2025-08-01 04:57:03.150389	t	86
121	Empleado2916	Apellido2916	Test	emp2916@test.com	4429237986	2025-04-28	2025-08-01 04:57:03.151355	t	87
122	Empleado1844	Apellido1844	Test	emp1844@test.com	4421879828	2024-12-06	2025-08-01 04:57:03.152279	t	88
123	Empleado2701	Apellido2701	Test	emp2701@test.com	4429203786	2024-10-27	2025-08-01 04:57:03.15391	t	89
124	Empleado4543	Apellido4543	Test	emp4543@test.com	4423546844	2025-01-06	2025-08-01 04:57:03.154511	t	89
125	Empleado8635	Apellido8635	Test	emp8635@test.com	4427043714	2025-06-01	2025-08-01 04:57:03.155504	t	90
126	Empleado8916	Apellido8916	Test	emp8916@test.com	4422244687	2025-05-24	2025-08-01 04:57:03.155976	t	90
127	Empleado8833	Apellido8833	Test	emp8833@test.com	4426938429	2025-01-17	2025-08-01 04:57:03.158443	t	91
128	Empleado5000	Apellido5000	Test	emp5000@test.com	4424965734	2025-06-15	2025-08-01 04:57:03.159331	t	92
129	Empleado4664	Apellido4664	Test	emp4664@test.com	4424777353	2024-12-18	2025-08-01 04:57:03.160275	t	93
130	Empleado7550	Apellido7550	Test	emp7550@test.com	4429373488	2025-01-29	2025-08-01 04:57:03.161223	t	94
131	Empleado3508	Apellido3508	Test	emp3508@test.com	4425917328	2025-04-07	2025-08-01 04:57:03.161715	t	94
132	Empleado7107	Apellido7107	Test	emp7107@test.com	4422668462	2024-09-26	2025-08-01 04:57:03.162834	t	95
133	Empleado8122	Apellido8122	Test	emp8122@test.com	4428608612	2025-03-28	2025-08-01 04:57:03.163318	t	95
134	Empleado4874	Apellido4874	Test	emp4874@test.com	4422534313	2025-01-09	2025-08-01 04:57:03.16572	t	96
135	Empleado1169	Apellido1169	Test	emp1169@test.com	4428218082	2025-02-10	2025-08-01 04:57:03.166614	t	97
136	Empleado2052	Apellido2052	Test	emp2052@test.com	4423485602	2024-12-25	2025-08-01 04:57:03.167611	t	98
137	Empleado4880	Apellido4880	Test	emp4880@test.com	4426348953	2024-10-07	2025-08-01 04:57:03.168522	t	99
138	Empleado2028	Apellido2028	Test	emp2028@test.com	4422498169	2025-02-01	2025-08-01 04:57:03.169008	t	99
139	Empleado9294	Apellido9294	Test	emp9294@test.com	4423250701	2024-11-16	2025-08-01 04:57:03.169946	t	100
140	Empleado6689	Apellido6689	Test	emp6689@test.com	4428427861	2024-12-24	2025-08-01 04:57:03.17042	t	100
76	Empleado1103	Apellido1103	Test	emp1103@test.com	4424373115	2025-03-26	2025-08-01 04:57:03.10351	f	55
149	Ernesto	Garcia	Valenzuela	ernesto.garcia@empresa.com	\N	2025-08-01	2025-08-02 02:41:21.8503	t	165
150	Ernesto	Garcia	Valenzuela	ernesto.garcia1@empresa.com	\N	2025-08-01	2025-08-02 03:17:45.287424	t	149
151	Ernest	Bautista	Reyes	ernest.bautista@empresa.com	6644798476	2025-08-01	2025-08-02 03:24:12.747703	t	160
152	Misael	Rubio	Contreras	misael@planta12.com	6641230659	2025-09-05	2025-08-02 05:16:38.899482	t	166
153	Efrain	Rubio	Contreras	efrain@planta12.com	665365467	2025-09-05	2025-08-02 05:52:10.429936	t	166
\.


--
-- TOC entry 5351 (class 0 OID 203600)
-- Dependencies: 246
-- Data for Name: empleados_asignados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empleados_asignados (id, token_empleado, estado, fecha_inicio_empleado, fecha_finalizacion, progreso_porcentaje, fecha_asignacion, ultimo_acceso, asignacion_id, empleado_id) FROM stdin;
1	EMP3_EVAL1_EMP76_TEST1	pendiente	\N	\N	0	2025-08-01 10:09:47.182816-07	\N	1	76
2	EMP3_EVAL1_EMP117_TEST2	pendiente	\N	\N	0	2025-08-01 10:10:30.333613-07	\N	1	117
3	EMP3_EVAL1_EMP90_TEST3	pendiente	\N	\N	0	2025-08-01 10:10:30.337191-07	\N	1	90
\.


--
-- TOC entry 5354 (class 0 OID 203605)
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
-- TOC entry 5356 (class 0 OID 203613)
-- Dependencies: 251
-- Data for Name: evaluaciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.evaluaciones (evaluacion_id, nombre, descripcion, instrucciones, tiempo_limite, status, fecha_registro, fecha_actualizacion, tipo_evaluacion, empresa, creado_por) FROM stdin;
\.


--
-- TOC entry 5358 (class 0 OID 203622)
-- Dependencies: 253
-- Data for Name: evaluaciones_oficiales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.evaluaciones_oficiales (id, nombre, tipo_norma, descripcion, instrucciones, tiempo_limite, umbral_aprobacion, activa, fecha_creacion) FROM stdin;
1	Evaluación NOM-035 Oficial	NOM-035	Evaluación oficial de factores de riesgo psicosocial según NOM-035-STPS-2018	Complete todas las preguntas de manera honesta y reflexiva.	\N	\N	t	2025-08-01 10:08:28.937168-07
2	Evaluaci??n NOM-030 Oficial	NOM-030	Evaluaci??n oficial de servicios preventivos de seguridad y salud en el trabajo	Complete todas las secciones relacionadas con los servicios preventivos.	45	\N	t	2025-08-01 10:17:28.107988-07
\.


--
-- TOC entry 5360 (class 0 OID 203628)
-- Dependencies: 255
-- Data for Name: opciones_conjunto; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.opciones_conjunto (opcion_conjunto_id, texto_opcion, valor_booleano, valor_numerico, puntuaje_escala, numero_orden, conjunto_opciones) FROM stdin;
\.


--
-- TOC entry 5362 (class 0 OID 203632)
-- Dependencies: 257
-- Data for Name: pagos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pagos (pago_id, suscripcion, monto, fecha_pago, metodo_pago, estado_pago, referencia_pago, usuario) FROM stdin;
\.


--
-- TOC entry 5364 (class 0 OID 203639)
-- Dependencies: 259
-- Data for Name: planes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.planes (plan_id, nombre, descripcion, precio, duracion, fecha_registro, status) FROM stdin;
2	Plan Profesional	Plan profesional para empresas medianas	599.00	30	2025-07-31 06:00:00	t
3	Plan Empresarial	Plan empresarial para grandes organizaciones	1299.00	30	2025-07-31 06:00:00	t
4	Plan de prueba	Este plan se borrara	50000.00	500	\N	f
1	Plan Básico	Plan básico para empresas chicas	299.00	30	2025-08-01 12:00:00	t
\.


--
-- TOC entry 5366 (class 0 OID 203647)
-- Dependencies: 261
-- Data for Name: plantas; Type: TABLE DATA; Schema: public; Owner: -
--

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
11	Planta Prueba Automatica	Direccion de prueba 123	2025-08-02 04:01:39.627258	t	6
13	Planta Automatica Final	Direccion final 789	2025-08-02 04:03:51.032773	t	6
15	Planta Prueba Manual	Direccion manual 123	2025-08-02 04:13:19.223776	t	1
17	Planta Automatica Renovada	Zona Industrial Nueva	2025-08-02 04:30:08.79524	t	1
18	Planta Con Usuario Auto	Industrial	2025-08-02 04:31:06.899761	t	1
12	Planta Automatica	Direccion automatica 456	2025-08-02 04:02:56.322235	t	6
\.


--
-- TOC entry 5368 (class 0 OID 203655)
-- Dependencies: 263
-- Data for Name: preguntas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.preguntas (pregunta_id, texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) FROM stdin;
\.


--
-- TOC entry 5369 (class 0 OID 203662)
-- Dependencies: 264
-- Data for Name: preguntas_oficiales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.preguntas_oficiales (id, texto_pregunta, tipo_pregunta, opciones_respuesta, es_obligatoria, numero_orden, activador_padre, activa, fecha_creacion, pregunta_padre_id, seccion_id) FROM stdin;
1	¿Cuál es su edad?	Múltiple	["18-25", "26-35", "36-45", "46-55", "Más de 55"]	t	1		t	2025-08-01 10:08:28.944523-07	\N	1
2	¿Cuál es su sexo?	Múltiple	["Masculino", "Femenino", "Prefiero no decir"]	t	2		t	2025-08-01 10:08:28.947989-07	\N	1
3	¿Su trabajo le exige realizar tareas muy intensas o que requieren gran rapidez?	Escala	["1", "2", "3", "4", "5"]	t	1		t	2025-08-01 10:08:28.949514-07	\N	2
4	¿Considera que su trabajo es estresante?	Si/No	[]	t	2		t	2025-08-01 10:08:28.951049-07	\N	2
5	??La empresa cuenta con servicios preventivos de seguridad y salud?	Si/No	[]	t	1		t	2025-08-01 10:17:28.113168-07	\N	3
6	??Qu?? tipo de servicios preventivos considera m??s importantes?	M??ltiple	["Medicina del trabajo", "Higiene industrial", "Seguridad en el trabajo", "Ergonom??a", "Psicosociolog??a aplicada"]	t	2		t	2025-08-01 10:17:28.11414-07	\N	3
7	??Con qu?? frecuencia recibe capacitaci??n en seguridad?	M??ltiple	["Mensual", "Trimestral", "Semestral", "Anual", "Nunca"]	t	1		t	2025-08-01 10:17:28.114805-07	\N	4
8	El espacio donde trabajo me permite realizar mis actividades de manera segura e higiénica	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	1		t	2025-08-01 11:28:12.005407-07	\N	5
9	Mi trabajo me exige hacer mucho esfuerzo físico	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	2		t	2025-08-01 11:28:12.007059-07	\N	5
10	Me preocupa sufrir un accidente en mi trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	3		t	2025-08-01 11:28:12.008254-07	\N	5
11	Considero que en mi trabajo se aplican las normas de seguridad y salud en el trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	4		t	2025-08-01 11:28:12.009405-07	\N	5
12	Considero que las actividades que realizo son peligrosas	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	5		t	2025-08-01 11:28:12.010698-07	\N	5
13	Por la cantidad de trabajo que tengo debo quedarme tiempo adicional a mi turno	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	6		t	2025-08-01 11:28:12.012116-07	\N	6
14	Por la cantidad de trabajo que tengo debo trabajar sin parar	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	7		t	2025-08-01 11:28:12.013534-07	\N	6
15	Considero que es necesario mantener un ritmo de trabajo acelerado	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	8		t	2025-08-01 11:28:12.014997-07	\N	6
16	Mi trabajo exige que esté muy concentrado	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	9		t	2025-08-01 11:28:12.016477-07	\N	7
17	Mi trabajo requiere que memorice mucha información	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	10		t	2025-08-01 11:28:12.018031-07	\N	7
18	En mi trabajo tengo que tomar decisiones difíciles muy rápido	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	11		t	2025-08-01 11:28:12.019287-07	\N	7
19	Mi trabajo exige que atienda varios asuntos al mismo tiempo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	12		t	2025-08-01 11:28:12.020567-07	\N	7
20	En mi trabajo soy responsable de cosas de mucho valor	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	13		t	2025-08-01 11:28:12.021754-07	\N	8
21	Respondo ante mi jefe por los resultados de toda mi área de trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	14		t	2025-08-01 11:28:12.02292-07	\N	8
22	En el trabajo me dan órdenes contradictorias	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	15		t	2025-08-01 11:28:12.024067-07	\N	8
23	Considero que en mi trabajo me piden hacer cosas innecesarias	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	16		t	2025-08-01 11:28:12.025561-07	\N	8
24	Mi jefe ayuda a organizar mejor el trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	33		t	2025-08-01 11:28:12.026945-07	\N	13
25	Mi jefe tiene en cuenta mis puntos de vista y opiniones	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	34		t	2025-08-01 11:28:12.028285-07	\N	13
26	Mi jefe me comunica a tiempo la información relacionada con el trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	35		t	2025-08-01 11:28:12.029633-07	\N	13
27	En mi trabajo puedo expresarme libremente sin interrupciones	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	57		t	2025-08-01 11:28:12.031038-07	\N	16
28	Recibo críticas constantes a mi persona y/o trabajo	Escala	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	58		t	2025-08-01 11:28:12.032559-07	\N	16
29	En mi trabajo debo brindar servicio a clientes o usuarios	Si/No	["Sí", "No"]	t	65		t	2025-08-01 11:28:12.034177-07	\N	17
30	Soy jefe de otros trabajadores	Si/No	["Sí", "No"]	t	70		t	2025-08-01 11:28:12.035638-07	\N	18
31	¿Qué debe demostrar el patrón referente al personal de la empresa que forma parte de los servicios preventivos de seguridad y salud en el trabajo?	Múltiple	["Que es capacitado en las funciones y actividades", "Que no se han presentado accidentes recientes", "Que tienen conocimiento acerca de las funciones y actividades a realizar", "Que es actualizado constantemente dentro del centro de trabajo"]	t	75		t	2025-08-01 11:28:12.051557-07	\N	19
32	El patrón cumple cuando presenta mediante una entrevista que asume funciones y actividades de seguridad y ______	Múltiple	["Preventivas - Salud", "Seguras - Prevención", "Funcionales - Salud", "Esenciales - Prevención"]	t	76		t	2025-08-01 11:28:12.052884-07	\N	19
33	¿Cuál es el fin de orientar al patrón y a los trabajadores de las funciones y actividades a desarrollar por los servicios preventivos y salud en el trabajo?	Múltiple	["Cumplir con la obligación de brindar capacitación", "Prever que los trabajadores desarrollen sus actividades en condiciones seguras", "Prever que los trabajadores no tengan accidentes y esto produzca costos adicionales", "Fortalecer una cultura de reacción ante accidentes"]	t	80		t	2025-08-01 11:28:12.054239-07	\N	20
34	¿Cuáles son las características que el botiquín debe cumplir?	Múltiple	["Ser de fácil transporte, visible y de fácil acceso, que contenga material suficiente, identificable con una cruz roja, de peso no excesivo", "Ser de fácil transporte, visible y de fácil acceso, identificable con una cruz roja, de peso no excesivo, sin candados o dispositivos que dificulten el acceso a su contenido", "Ser de fácil transporte, colocado en un lugar donde todos tengan acceso a él, identificable con una cruz roja, de material resistente y sin candados o dispositivos que dificulten el acceso a su contenido", "Ser de fácil transporte y de fácil acceso, en una ubicación fácil para los trabajadores, con contenido suficiente para todos, sin candados que dificulten el acceso a su contenido"]	t	81		t	2025-08-01 11:28:12.055348-07	\N	21
35	El programa de seguridad y salud en el trabajo, deberá tener las fechas de inicio y término programadas para instrumentar las acciones preventivas o correctivas y para la atención de emergencias	Si/No	["Sí", "No"]	t	82		t	2025-08-01 11:28:12.056432-07	\N	21
36	¿En qué situaciones se brindará atención de consulta médica?	Múltiple	["Por enfermedad general y por enfermedad de trabajo", "Por enfermedad de trabajo y por una situación de emergencia en el trabajo", "Por enfermedad general y por accidente de trabajo", "Por enfermedad general y por lesiones graves de trabajo"]	t	84		t	2025-08-01 11:28:12.058216-07	\N	21
37	¿Cómo se realiza la capacitación para mandos superiores?	Múltiple	["Brindándoles asesoramiento sobre las dudas que tengan respecto a la seguridad y salud en el trabajo", "Mediante el asesoramiento sobre los temas que los especialistas en seguridad y salud deben conocer", "A través del asesoramiento para enseñarles como realizar un programa y normas internas de salud en el trabajo", "Mediante el asesoramiento para el establecimiento de políticas y normas internas de salud en el trabajo"]	t	85		t	2025-08-01 11:28:12.059474-07	\N	22
38	Cuando las unidades de verificación evalúan el cumplimiento de esta norma, ¿Qué documento se debe emitir?	Múltiple	["Acta", "Dictamen", "Recibo", "Reglamento"]	t	88		t	2025-08-01 11:28:12.061032-07	\N	23
39	En las acciones recomendadas se deben considerar aspectos como la planeación y dirección; la capacitación e información a los trabajadores y las medidas de prevención. Se deben exceptuar las medidas de protección y las políticas temporales	Si/No	["Sí", "No"]	t	93		t	2025-08-01 11:28:12.062147-07	\N	23
40	Esta es una pregunta de prueba?	Multiple	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	71		t	2025-08-01 16:29:17.090501-07	\N	1
41	Esta es una pregunta de prueba desde PowerShell?	Multiple	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	72		t	2025-08-01 16:31:06.761092-07	\N	1
42	Pregunta de prueba	Multiple	["Opcion 1", "Opcion 2"]	t	73		t	2025-08-01 16:33:07.553164-07	\N	1
43	Esto es una prueba	Multiple	["si", "no"]	t	43		t	2025-08-01 16:36:49.230416-07	\N	1
44	La gente esta?	Si_no	["Sí", "No"]	t	44		t	2025-08-01 16:37:25.844108-07	\N	1
45	Prueba prueba	Si_no	["Sí", "No"]	t	45		t	2025-08-01 16:41:04.144957-07	\N	1
46	Pregunta de prueba desde PowerShell 2?	Multiple	["Siempre", "Casi siempre", "Algunas veces", "Casi nunca", "Nunca"]	t	74		t	2025-08-01 16:45:50.555691-07	\N	1
47	Pregunta de prueba 3	Multiple	["Si", "No"]	t	75		t	2025-08-01 16:46:07.275457-07	\N	1
48	¿Pregunta de diagnóstico?	Multiple	["Sí", "No"]	t	76		t	2025-08-01 16:54:48.756846-07	\N	1
49	Probando probando edicion	Escala	["1 - Totalmente en desacuerdo", "2 - En desacuerdo", "3 - Neutral", "4 - De acuerdo", "5 - Totalmente de acuerdo"]	t	49		t	2025-08-01 16:59:18.847499-07	\N	3
\.


--
-- TOC entry 5372 (class 0 OID 203669)
-- Dependencies: 267
-- Data for Name: puestos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.puestos (puesto_id, nombre, descripcion, fecha_registro, status, departamento) FROM stdin;
1	Director	Puesto de Director	2025-08-01 04:57:03.014747	t	1
2	Gerente	Puesto de Gerente	2025-08-01 04:57:03.017839	t	1
3	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.019539	t	1
4	Operador	Puesto de Operador	2025-08-01 04:57:03.020733	t	1
5	Técnico	Puesto de Técnico	2025-08-01 04:57:03.022693	t	1
6	Director	Puesto de Director	2025-08-01 04:57:03.026768	t	2
7	Gerente	Puesto de Gerente	2025-08-01 04:57:03.028077	t	2
8	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.029187	t	2
9	Operador	Puesto de Operador	2025-08-01 04:57:03.030265	t	2
10	Técnico	Puesto de Técnico	2025-08-01 04:57:03.031842	t	2
11	Director	Puesto de Director	2025-08-01 04:57:03.035054	t	3
12	Gerente	Puesto de Gerente	2025-08-01 04:57:03.03596	t	3
13	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.036856	t	3
14	Operador	Puesto de Operador	2025-08-01 04:57:03.037777	t	3
15	Técnico	Puesto de Técnico	2025-08-01 04:57:03.039249	t	3
16	Director	Puesto de Director	2025-08-01 04:57:03.042326	t	4
17	Gerente	Puesto de Gerente	2025-08-01 04:57:03.043953	t	4
18	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.045186	t	4
19	Operador	Puesto de Operador	2025-08-01 04:57:03.046207	t	4
20	Técnico	Puesto de Técnico	2025-08-01 04:57:03.047594	t	4
21	Director	Puesto de Director	2025-08-01 04:57:03.050692	t	5
22	Gerente	Puesto de Gerente	2025-08-01 04:57:03.051603	t	5
23	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.052523	t	5
24	Operador	Puesto de Operador	2025-08-01 04:57:03.053645	t	5
25	Técnico	Puesto de Técnico	2025-08-01 04:57:03.055335	t	5
26	Director	Puesto de Director	2025-08-01 04:57:03.058868	t	6
27	Gerente	Puesto de Gerente	2025-08-01 04:57:03.059807	t	6
28	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.060786	t	6
29	Operador	Puesto de Operador	2025-08-01 04:57:03.061908	t	6
30	Técnico	Puesto de Técnico	2025-08-01 04:57:03.063673	t	6
31	Director	Puesto de Director	2025-08-01 04:57:03.067107	t	7
32	Gerente	Puesto de Gerente	2025-08-01 04:57:03.068105	t	7
33	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.068992	t	7
34	Operador	Puesto de Operador	2025-08-01 04:57:03.06994	t	7
35	Técnico	Puesto de Técnico	2025-08-01 04:57:03.071385	t	7
36	Director	Puesto de Director	2025-08-01 04:57:03.074368	t	8
37	Gerente	Puesto de Gerente	2025-08-01 04:57:03.075254	t	8
38	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.076207	t	8
39	Operador	Puesto de Operador	2025-08-01 04:57:03.07719	t	8
40	Técnico	Puesto de Técnico	2025-08-01 04:57:03.078883	t	8
41	Director	Puesto de Director	2025-08-01 04:57:03.082011	t	9
42	Gerente	Puesto de Gerente	2025-08-01 04:57:03.082906	t	9
43	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.083853	t	9
44	Operador	Puesto de Operador	2025-08-01 04:57:03.084826	t	9
45	Técnico	Puesto de Técnico	2025-08-01 04:57:03.086352	t	9
46	Director	Puesto de Director	2025-08-01 04:57:03.090109	t	10
47	Gerente	Puesto de Gerente	2025-08-01 04:57:03.091109	t	10
48	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.092198	t	10
49	Operador	Puesto de Operador	2025-08-01 04:57:03.093196	t	10
50	Técnico	Puesto de Técnico	2025-08-01 04:57:03.094733	t	10
51	Director	Puesto de Director	2025-08-01 04:57:03.098042	t	11
52	Gerente	Puesto de Gerente	2025-08-01 04:57:03.099546	t	11
53	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.100542	t	11
54	Operador	Puesto de Operador	2025-08-01 04:57:03.101621	t	11
55	Técnico	Puesto de Técnico	2025-08-01 04:57:03.103042	t	11
56	Director	Puesto de Director	2025-08-01 04:57:03.10603	t	12
57	Gerente	Puesto de Gerente	2025-08-01 04:57:03.10697	t	12
58	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.107908	t	12
59	Operador	Puesto de Operador	2025-08-01 04:57:03.108834	t	12
60	Técnico	Puesto de Técnico	2025-08-01 04:57:03.110221	t	12
61	Director	Puesto de Director	2025-08-01 04:57:03.11345	t	13
62	Gerente	Puesto de Gerente	2025-08-01 04:57:03.114352	t	13
63	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.115195	t	13
64	Operador	Puesto de Operador	2025-08-01 04:57:03.116139	t	13
65	Técnico	Puesto de Técnico	2025-08-01 04:57:03.117703	t	13
66	Director	Puesto de Director	2025-08-01 04:57:03.120563	t	14
67	Gerente	Puesto de Gerente	2025-08-01 04:57:03.121483	t	14
68	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.122419	t	14
69	Operador	Puesto de Operador	2025-08-01 04:57:03.123364	t	14
70	Técnico	Puesto de Técnico	2025-08-01 04:57:03.124776	t	14
71	Director	Puesto de Director	2025-08-01 04:57:03.127892	t	15
72	Gerente	Puesto de Gerente	2025-08-01 04:57:03.129006	t	15
73	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.1301	t	15
74	Operador	Puesto de Operador	2025-08-01 04:57:03.131026	t	15
75	Técnico	Puesto de Técnico	2025-08-01 04:57:03.132467	t	15
76	Director	Puesto de Director	2025-08-01 04:57:03.135356	t	16
77	Gerente	Puesto de Gerente	2025-08-01 04:57:03.136261	t	16
78	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.137164	t	16
79	Operador	Puesto de Operador	2025-08-01 04:57:03.138099	t	16
80	Técnico	Puesto de Técnico	2025-08-01 04:57:03.139511	t	16
81	Director	Puesto de Director	2025-08-01 04:57:03.142397	t	17
82	Gerente	Puesto de Gerente	2025-08-01 04:57:03.143292	t	17
83	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.14423	t	17
84	Operador	Puesto de Operador	2025-08-01 04:57:03.14525	t	17
85	Técnico	Puesto de Técnico	2025-08-01 04:57:03.146782	t	17
86	Director	Puesto de Director	2025-08-01 04:57:03.149891	t	18
87	Gerente	Puesto de Gerente	2025-08-01 04:57:03.150867	t	18
88	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.151795	t	18
89	Operador	Puesto de Operador	2025-08-01 04:57:03.15333	t	18
90	Técnico	Puesto de Técnico	2025-08-01 04:57:03.15505	t	18
91	Director	Puesto de Director	2025-08-01 04:57:03.157978	t	19
92	Gerente	Puesto de Gerente	2025-08-01 04:57:03.158874	t	19
93	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.159793	t	19
94	Operador	Puesto de Operador	2025-08-01 04:57:03.160748	t	19
95	Técnico	Puesto de Técnico	2025-08-01 04:57:03.1623	t	19
96	Director	Puesto de Director	2025-08-01 04:57:03.165279	t	20
97	Gerente	Puesto de Gerente	2025-08-01 04:57:03.16617	t	20
98	Supervisor	Puesto de Supervisor	2025-08-01 04:57:03.167118	t	20
99	Operador	Puesto de Operador	2025-08-01 04:57:03.168058	t	20
100	Técnico	Puesto de Técnico	2025-08-01 04:57:03.169468	t	20
101	Gerente General	\N	2025-08-01 08:20:14.729674	t	21
102	Asistente Administrativo	\N	2025-08-01 08:20:14.729674	t	21
103	Gerente de RRHH	\N	2025-08-01 08:20:14.729674	t	22
104	Especialista en Nómina	\N	2025-08-01 08:20:14.729674	t	22
105	Reclutador	\N	2025-08-01 08:20:14.729674	t	22
106	Contador	\N	2025-08-01 08:20:14.729674	t	23
107	Analista Financiero	\N	2025-08-01 08:20:14.729674	t	23
108	Supervisor de Producción	\N	2025-08-01 08:20:14.729674	t	24
109	Operador de Máquina	\N	2025-08-01 08:20:14.729674	t	24
110	Técnico de Proceso	\N	2025-08-01 08:20:14.729674	t	24
111	Inspector de Calidad	\N	2025-08-01 08:20:14.729674	t	25
112	Auditor Interno	\N	2025-08-01 08:20:14.729674	t	25
113	Técnico de Mantenimiento	\N	2025-08-01 08:20:14.729674	t	26
114	Electricista Industrial	\N	2025-08-01 08:20:14.729674	t	26
115	Coordinador de Almacén	\N	2025-08-01 08:20:14.729674	t	27
116	Montacarguista	\N	2025-08-01 08:20:14.729674	t	27
117	Gerente General	\N	2025-08-01 08:28:34.466153	t	28
118	Asistente Administrativo	\N	2025-08-01 08:28:34.466153	t	28
119	Gerente de RRHH	\N	2025-08-01 08:28:34.466153	t	29
120	Especialista en Nómina	\N	2025-08-01 08:28:34.466153	t	29
121	Reclutador	\N	2025-08-01 08:28:34.466153	t	29
122	Contador	\N	2025-08-01 08:28:34.466153	t	30
123	Analista Financiero	\N	2025-08-01 08:28:34.466153	t	30
124	Supervisor de Producción	\N	2025-08-01 08:28:34.466153	t	31
125	Operador de Máquina	\N	2025-08-01 08:28:34.466153	t	31
126	Técnico de Proceso	\N	2025-08-01 08:28:34.466153	t	31
127	Inspector de Calidad	\N	2025-08-01 08:28:34.466153	t	32
128	Auditor Interno	\N	2025-08-01 08:28:34.466153	t	32
129	Técnico de Mantenimiento	\N	2025-08-01 08:28:34.466153	t	33
130	Electricista Industrial	\N	2025-08-01 08:28:34.466153	t	33
131	Coordinador de Almacén	\N	2025-08-01 08:28:34.466153	t	34
132	Montacarguista	\N	2025-08-01 08:28:34.466153	t	34
133	Gerente General	\N	2025-08-01 08:41:49.627754	t	35
134	Asistente Administrativo	\N	2025-08-01 08:41:49.627754	t	35
135	Gerente de RRHH	\N	2025-08-01 08:41:49.627754	t	36
136	Especialista en Nómina	\N	2025-08-01 08:41:49.627754	t	36
137	Reclutador	\N	2025-08-01 08:41:49.627754	t	36
138	Contador	\N	2025-08-01 08:41:49.627754	t	37
139	Analista Financiero	\N	2025-08-01 08:41:49.627754	t	37
140	Supervisor de Producción	\N	2025-08-01 08:41:49.627754	t	38
141	Operador de Máquina	\N	2025-08-01 08:41:49.627754	t	38
142	Técnico de Proceso	\N	2025-08-01 08:41:49.627754	t	38
143	Inspector de Calidad	\N	2025-08-01 08:41:49.627754	t	39
144	Auditor Interno	\N	2025-08-01 08:41:49.627754	t	39
145	Técnico de Mantenimiento	\N	2025-08-01 08:41:49.627754	t	40
146	Electricista Industrial	\N	2025-08-01 08:41:49.627754	t	40
147	Coordinador de Almacén	\N	2025-08-01 08:41:49.627754	t	41
148	Montacarguista	\N	2025-08-01 08:41:49.627754	t	41
149	Gerente General	\N	2025-08-01 09:01:28.925834	t	42
150	Asistente Administrativo	\N	2025-08-01 09:01:28.925834	t	42
151	Gerente de RRHH	\N	2025-08-01 09:01:28.925834	t	43
152	Especialista en Nómina	\N	2025-08-01 09:01:28.925834	t	43
153	Reclutador	\N	2025-08-01 09:01:28.925834	t	43
154	Contador	\N	2025-08-01 09:01:28.925834	t	44
155	Analista Financiero	\N	2025-08-01 09:01:28.925834	t	44
156	Supervisor de Producción	\N	2025-08-01 09:01:28.925834	t	45
157	Operador de Máquina	\N	2025-08-01 09:01:28.925834	t	45
158	Técnico de Proceso	\N	2025-08-01 09:01:28.925834	t	45
159	Inspector de Calidad	\N	2025-08-01 09:01:28.925834	t	46
160	Auditor Interno	\N	2025-08-01 09:01:28.925834	t	46
161	Técnico de Mantenimiento	\N	2025-08-01 09:01:28.925834	t	47
162	Electricista Industrial	\N	2025-08-01 09:01:28.925834	t	47
163	Coordinador de Almacén	\N	2025-08-01 09:01:28.925834	t	48
164	Montacarguista	\N	2025-08-01 09:01:28.925834	t	48
165	Puesto para prueba	Pruebaa	2025-08-02 01:52:48.523482	t	49
166	Director General	Director en RRHH	2025-08-02 05:16:02.300646	t	50
\.


--
-- TOC entry 5374 (class 0 OID 203677)
-- Dependencies: 269
-- Data for Name: respuestas_empleados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.respuestas_empleados (id, respuesta_texto, respuesta_numerica, respuesta_multiple, respuesta_booleana, fecha_respuesta, tiempo_respuesta_segundos, es_respuesta_final, empleado_asignado_id, pregunta_oficial_id) FROM stdin;
1		\N	"26-35"	\N	2025-08-01 10:09:47.186341-07	15	t	1	1
2		\N	"Masculino"	\N	2025-08-01 10:09:47.188823-07	8	t	1	2
\.


--
-- TOC entry 5376 (class 0 OID 203683)
-- Dependencies: 271
-- Data for Name: seccion_preguntas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.seccion_preguntas (seccion, pregunta, conjunto_opciones) FROM stdin;
\.


--
-- TOC entry 5377 (class 0 OID 203686)
-- Dependencies: 272
-- Data for Name: secciones_eval; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.secciones_eval (seccion_id, nombre, descripcion, numero_orden, evaluacion) FROM stdin;
\.


--
-- TOC entry 5379 (class 0 OID 203692)
-- Dependencies: 274
-- Data for Name: secciones_oficiales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.secciones_oficiales (id, nombre, descripcion, numero_orden, es_evaluable, evaluacion_oficial_id) FROM stdin;
1	Datos Generales	Información general del empleado	1	t	1
2	Factores de Riesgo Psicosocial	Evaluación de factores de riesgo psicosocial en el trabajo	2	t	1
3	Servicios Preventivos	Evaluaci??n de servicios preventivos disponibles	1	t	2
4	Capacitaci??n y Entrenamiento	Evaluaci??n de programas de capacitaci??n	2	t	2
5	Condiciones en el ambiente de trabajo	Preguntas relacionadas con condiciones en el ambiente de trabajo	1	t	1
6	Cantidad y ritmo de trabajo	Preguntas relacionadas con cantidad y ritmo de trabajo	2	t	1
7	Esfuerzo mental	Preguntas relacionadas con esfuerzo mental	3	t	1
8	Actividades y responsabilidades	Preguntas relacionadas con actividades y responsabilidades	4	t	1
9	Jornada de trabajo	Preguntas relacionadas con jornada de trabajo	5	t	1
10	Decisiones en el trabajo	Preguntas relacionadas con decisiones en el trabajo	6	t	1
11	Cambios en el trabajo	Preguntas relacionadas con cambios en el trabajo	7	t	1
12	Capacitación e información	Preguntas relacionadas con capacitación e información	8	t	1
13	Relación con los jefes	Preguntas relacionadas con relación con los jefes	9	t	1
14	Relaciones con los compañeros	Preguntas relacionadas con relaciones con los compañeros	10	t	1
15	Rendimiento, reconocimiento, pertenencia y estabilidad	Preguntas relacionadas con rendimiento, reconocimiento, pertenencia y estabilidad	11	t	1
16	Actos de violencia laboral	Preguntas relacionadas con actos de violencia laboral	12	t	1
17	Atención a clientes y usuarios	Preguntas relacionadas con atención a clientes y usuarios	13	t	1
18	Jefe de otros trabajadores	Preguntas relacionadas con jefe de otros trabajadores	14	t	1
19	Servicios preventivos	Preguntas sobre servicios preventivos	1	t	2
20	Diagnóstico y programa de seguridad y salud	Preguntas sobre diagnóstico y programa de seguridad y salud	2	t	2
21	Medidas de prevención y atención de emergencias	Preguntas sobre medidas de prevención y atención de emergencias	3	t	2
22	Capacitación y promoción de la salud	Preguntas sobre capacitación y promoción de la salud	4	t	2
23	Reportes, investigación y adecuaciones	Preguntas sobre reportes, investigación y adecuaciones	5	t	2
\.


--
-- TOC entry 5381 (class 0 OID 203698)
-- Dependencies: 276
-- Data for Name: suscripciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.suscripciones (suscripcion_id, empresa, plan, fecha_inicio, fecha_fin, estado, fecha_registro) FROM stdin;
1	2	2	2025-07-31	2025-08-30	activa	\N
2	1	3	2025-07-31	2025-08-30	activa	\N
5	6	2	2025-08-01	2025-08-31	activa	\N
\.


--
-- TOC entry 5383 (class 0 OID 203705)
-- Dependencies: 278
-- Data for Name: tipos_evaluacion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_evaluacion (tipo_evaluacion_id, nombre, descripcion) FROM stdin;
\.


--
-- TOC entry 5385 (class 0 OID 203711)
-- Dependencies: 280
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id, nombre, apellido_paterno, apellido_materno, correo, fecha_registro, nivel_usuario, status, admin_empresa, user_id) FROM stdin;
1	Super	Admin	\N	superadmin@axyoma.com	2025-08-01 04:54:49.200658	superadmin	t	\N	1
3	Admin	InnovaSoft	\N	admin@innovasoft.mx	2025-08-01 04:57:02.994473	admin-empresa	t	\N	3
2	TechCorp	Inc		admin@techcorp.mx	2025-08-01 04:57:02.242881	admin-empresa	t	\N	2
4	Fernando	Olivares	Mata	admin_temp@axyoma.com	2025-08-01 06:40:54.239468	admin-empresa	t	\N	4
5	Ernesto	Garcia	Valenzuela	ernesto@axyoma.com	2025-08-01 07:59:35.800593	superadmin	t	\N	5
6	Jose	Padilal	Torres	axis2@gmail.com	2025-08-01 08:20:14.729674	admin-empresa	t	\N	13
7	Jose	Padilal	Torres	axis3@gmail.com	2025-08-01 08:28:34.466153	admin-empresa	t	\N	14
8	Jose	Padilal	Torres	axis4@gmail.com	2025-08-01 08:41:49.627754	admin-empresa	t	\N	15
9	Miguel	Mendoza	Torres	axis5@gmail.com	2025-08-01 09:01:28.925834	admin-empresa	t	\N	16
10	Carlos	Rodriguez	Gomez	admin.norte@techcorp.com	2025-08-02 03:51:25.403261	admin-planta	t	2	19
11	Maria	Lopez	Martinez	admin.sur@techcorp.com	2025-08-02 03:54:29.132115	admin-planta	t	2	21
12	Pedro	Martinez	Sanchez	admin.planta@axis5.com	2025-08-02 03:58:39.000871	admin-planta	t	9	22
13	Admin	Planta	Planta Automatica 2	admin.planta.12@axisdevelopment5.com	2025-08-02 04:02:56.322235	admin-planta	t	9	24
14	Admin	Planta	Planta Automatica Final	admin.planta.13@axisdevelopment5.com	2025-08-02 04:03:51.032773	admin-planta	t	9	25
15	Admin	Planta	Planta Test Usuario Auto	admin.planta.14@axisdevelopment5.com	2025-08-02 04:05:16.692011	admin-planta	t	9	26
16	Juan	García	López	juan.garcia@techcorp.com	2025-08-02 04:15:14.593013	admin-planta	t	2	27
17	Admin Planta Automatica Renovada	Plant	Manager	admin_planta_automatica_renovada@techcorpsolutions.com	2025-08-02 04:30:08.79524	admin-planta	t	2	28
18	Admin Planta Con Usuario Auto	Plant	Manager	admin_planta_con_usuario_auto@techcorpsolutions.com	2025-08-02 04:31:06.899761	admin-planta	t	2	29
21	Super	Admin	Sistema	testuser@axyoma.com	2025-08-02 18:51:13.942755	superadmin	t	\N	32
\.


--
-- TOC entry 5412 (class 0 OID 0)
-- Dependencies: 282
-- Name: admin_bd_configuracionbd_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_bd_configuracionbd_id_seq', 1, false);


--
-- TOC entry 5413 (class 0 OID 0)
-- Dependencies: 284
-- Name: admin_bd_logrespaldo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_bd_logrespaldo_id_seq', 1, false);


--
-- TOC entry 5414 (class 0 OID 0)
-- Dependencies: 218
-- Name: admin_plantas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_plantas_id_seq', 8, true);


--
-- TOC entry 5415 (class 0 OID 0)
-- Dependencies: 220
-- Name: asignaciones_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asignaciones_evaluacion_id_seq', 1, true);


--
-- TOC entry 5416 (class 0 OID 0)
-- Dependencies: 222
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5417 (class 0 OID 0)
-- Dependencies: 224
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5418 (class 0 OID 0)
-- Dependencies: 226
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 192, true);


--
-- TOC entry 5419 (class 0 OID 0)
-- Dependencies: 229
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- TOC entry 5420 (class 0 OID 0)
-- Dependencies: 230
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 32, true);


--
-- TOC entry 5421 (class 0 OID 0)
-- Dependencies: 232
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 5422 (class 0 OID 0)
-- Dependencies: 235
-- Name: conjuntos_opciones_conjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.conjuntos_opciones_conjunto_id_seq', 1, false);


--
-- TOC entry 5423 (class 0 OID 0)
-- Dependencies: 237
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departamentos_departamento_id_seq', 50, true);


--
-- TOC entry 5424 (class 0 OID 0)
-- Dependencies: 239
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- TOC entry 5425 (class 0 OID 0)
-- Dependencies: 241
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 48, true);


--
-- TOC entry 5426 (class 0 OID 0)
-- Dependencies: 243
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 30, true);


--
-- TOC entry 5427 (class 0 OID 0)
-- Dependencies: 247
-- Name: empleados_asignados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empleados_asignados_id_seq', 3, true);


--
-- TOC entry 5428 (class 0 OID 0)
-- Dependencies: 248
-- Name: empleados_empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empleados_empleado_id_seq', 153, true);


--
-- TOC entry 5429 (class 0 OID 0)
-- Dependencies: 250
-- Name: empresas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empresas_empresa_id_seq', 6, true);


--
-- TOC entry 5430 (class 0 OID 0)
-- Dependencies: 252
-- Name: evaluaciones_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.evaluaciones_evaluacion_id_seq', 1, false);


--
-- TOC entry 5431 (class 0 OID 0)
-- Dependencies: 254
-- Name: evaluaciones_oficiales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.evaluaciones_oficiales_id_seq', 2, true);


--
-- TOC entry 5432 (class 0 OID 0)
-- Dependencies: 256
-- Name: opciones_conjunto_opcion_conjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.opciones_conjunto_opcion_conjunto_id_seq', 1, false);


--
-- TOC entry 5433 (class 0 OID 0)
-- Dependencies: 258
-- Name: pagos_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pagos_pago_id_seq', 1, false);


--
-- TOC entry 5434 (class 0 OID 0)
-- Dependencies: 260
-- Name: planes_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.planes_plan_id_seq', 4, true);


--
-- TOC entry 5435 (class 0 OID 0)
-- Dependencies: 262
-- Name: plantas_planta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.plantas_planta_id_seq', 18, true);


--
-- TOC entry 5436 (class 0 OID 0)
-- Dependencies: 265
-- Name: preguntas_oficiales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.preguntas_oficiales_id_seq', 49, true);


--
-- TOC entry 5437 (class 0 OID 0)
-- Dependencies: 266
-- Name: preguntas_pregunta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.preguntas_pregunta_id_seq', 1, false);


--
-- TOC entry 5438 (class 0 OID 0)
-- Dependencies: 268
-- Name: puestos_puesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.puestos_puesto_id_seq', 168, true);


--
-- TOC entry 5439 (class 0 OID 0)
-- Dependencies: 270
-- Name: respuestas_empleados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.respuestas_empleados_id_seq', 3, true);


--
-- TOC entry 5440 (class 0 OID 0)
-- Dependencies: 273
-- Name: secciones_eval_seccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.secciones_eval_seccion_id_seq', 1, false);


--
-- TOC entry 5441 (class 0 OID 0)
-- Dependencies: 275
-- Name: secciones_oficiales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.secciones_oficiales_id_seq', 23, true);


--
-- TOC entry 5442 (class 0 OID 0)
-- Dependencies: 277
-- Name: suscripciones_suscripcion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.suscripciones_suscripcion_id_seq', 5, true);


--
-- TOC entry 5443 (class 0 OID 0)
-- Dependencies: 279
-- Name: tipos_evaluacion_tipo_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_evaluacion_tipo_evaluacion_id_seq', 1, false);


--
-- TOC entry 5444 (class 0 OID 0)
-- Dependencies: 281
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 21, true);


--
-- TOC entry 5128 (class 2606 OID 204121)
-- Name: admin_bd_configuracionbd admin_bd_configuracionbd_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_configuracionbd
    ADD CONSTRAINT admin_bd_configuracionbd_pkey PRIMARY KEY (id);


--
-- TOC entry 5131 (class 2606 OID 204129)
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_pkey PRIMARY KEY (id);


--
-- TOC entry 4961 (class 2606 OID 203737)
-- Name: admin_plantas admin_plantas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_pkey PRIMARY KEY (id);


--
-- TOC entry 4963 (class 2606 OID 203739)
-- Name: admin_plantas admin_plantas_usuario_id_planta_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_usuario_id_planta_id_key UNIQUE (usuario_id, planta_id);


--
-- TOC entry 4968 (class 2606 OID 203741)
-- Name: asignaciones_evaluacion asignaciones_evaluacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluacion_pkey PRIMARY KEY (id);


--
-- TOC entry 4972 (class 2606 OID 203743)
-- Name: asignaciones_evaluacion asignaciones_evaluacion_token_sesion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluacion_token_sesion_key UNIQUE (token_sesion);


--
-- TOC entry 4975 (class 2606 OID 203745)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 4980 (class 2606 OID 203747)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 4983 (class 2606 OID 203749)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4977 (class 2606 OID 203751)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 4986 (class 2606 OID 203753)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 4988 (class 2606 OID 203755)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 4996 (class 2606 OID 203757)
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 4999 (class 2606 OID 203759)
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 4990 (class 2606 OID 203761)
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 5002 (class 2606 OID 203763)
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5005 (class 2606 OID 203765)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 4993 (class 2606 OID 203767)
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 5008 (class 2606 OID 203769)
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- TOC entry 5010 (class 2606 OID 203771)
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- TOC entry 5012 (class 2606 OID 203773)
-- Name: conjuntos_opciones conjuntos_opciones_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conjuntos_opciones
    ADD CONSTRAINT conjuntos_opciones_nombre_key UNIQUE (nombre);


--
-- TOC entry 5014 (class 2606 OID 203775)
-- Name: conjuntos_opciones conjuntos_opciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conjuntos_opciones
    ADD CONSTRAINT conjuntos_opciones_pkey PRIMARY KEY (conjunto_id);


--
-- TOC entry 5018 (class 2606 OID 203777)
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_pkey PRIMARY KEY (departamento_id);


--
-- TOC entry 5022 (class 2606 OID 203779)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5025 (class 2606 OID 203781)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 5027 (class 2606 OID 203783)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5029 (class 2606 OID 203785)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5032 (class 2606 OID 203787)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5042 (class 2606 OID 203789)
-- Name: empleados_asignados empleados_asignados_asignacion_id_empleado_id_fd4cc0ae_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados_asignados
    ADD CONSTRAINT empleados_asignados_asignacion_id_empleado_id_fd4cc0ae_uniq UNIQUE (asignacion_id, empleado_id);


--
-- TOC entry 5045 (class 2606 OID 203791)
-- Name: empleados_asignados empleados_asignados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados_asignados
    ADD CONSTRAINT empleados_asignados_pkey PRIMARY KEY (id);


--
-- TOC entry 5048 (class 2606 OID 203793)
-- Name: empleados_asignados empleados_asignados_token_empleado_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados_asignados
    ADD CONSTRAINT empleados_asignados_token_empleado_key UNIQUE (token_empleado);


--
-- TOC entry 5035 (class 2606 OID 203795)
-- Name: empleados empleados_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_email_key UNIQUE (email);


--
-- TOC entry 5037 (class 2606 OID 203797)
-- Name: empleados empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_pkey PRIMARY KEY (empleado_id);


--
-- TOC entry 5050 (class 2606 OID 203799)
-- Name: empresas empresas_administrador_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_key UNIQUE (administrador);


--
-- TOC entry 5052 (class 2606 OID 203801)
-- Name: empresas empresas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nombre_key UNIQUE (nombre);


--
-- TOC entry 5054 (class 2606 OID 203803)
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (empresa_id);


--
-- TOC entry 5056 (class 2606 OID 203805)
-- Name: empresas empresas_rfc_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rfc_key UNIQUE (rfc);


--
-- TOC entry 5065 (class 2606 OID 203807)
-- Name: evaluaciones_oficiales evaluaciones_oficiales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones_oficiales
    ADD CONSTRAINT evaluaciones_oficiales_pkey PRIMARY KEY (id);


--
-- TOC entry 5060 (class 2606 OID 203809)
-- Name: evaluaciones evaluaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT evaluaciones_pkey PRIMARY KEY (evaluacion_id);


--
-- TOC entry 5069 (class 2606 OID 203811)
-- Name: opciones_conjunto opciones_conjunto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.opciones_conjunto
    ADD CONSTRAINT opciones_conjunto_pkey PRIMARY KEY (opcion_conjunto_id);


--
-- TOC entry 5074 (class 2606 OID 203813)
-- Name: pagos pagos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_pkey PRIMARY KEY (pago_id);


--
-- TOC entry 5078 (class 2606 OID 203815)
-- Name: planes planes_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.planes
    ADD CONSTRAINT planes_nombre_key UNIQUE (nombre);


--
-- TOC entry 5080 (class 2606 OID 203817)
-- Name: planes planes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.planes
    ADD CONSTRAINT planes_pkey PRIMARY KEY (plan_id);


--
-- TOC entry 5083 (class 2606 OID 203819)
-- Name: plantas plantas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plantas
    ADD CONSTRAINT plantas_pkey PRIMARY KEY (planta_id);


--
-- TOC entry 5088 (class 2606 OID 203821)
-- Name: preguntas_oficiales preguntas_oficiales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas_oficiales
    ADD CONSTRAINT preguntas_oficiales_pkey PRIMARY KEY (id);


--
-- TOC entry 5086 (class 2606 OID 203823)
-- Name: preguntas preguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT preguntas_pkey PRIMARY KEY (pregunta_id);


--
-- TOC entry 5093 (class 2606 OID 203825)
-- Name: puestos puestos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos
    ADD CONSTRAINT puestos_pkey PRIMARY KEY (puesto_id);


--
-- TOC entry 5096 (class 2606 OID 203827)
-- Name: respuestas_empleados respuestas_empleados_empleado_asignado_id_pre_2c08792d_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleados
    ADD CONSTRAINT respuestas_empleados_empleado_asignado_id_pre_2c08792d_uniq UNIQUE (empleado_asignado_id, pregunta_oficial_id);


--
-- TOC entry 5098 (class 2606 OID 203829)
-- Name: respuestas_empleados respuestas_empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleados
    ADD CONSTRAINT respuestas_empleados_pkey PRIMARY KEY (id);


--
-- TOC entry 5101 (class 2606 OID 203831)
-- Name: seccion_preguntas seccion_preguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_pkey PRIMARY KEY (seccion, pregunta);


--
-- TOC entry 5105 (class 2606 OID 203833)
-- Name: secciones_eval secciones_eval_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval
    ADD CONSTRAINT secciones_eval_pkey PRIMARY KEY (seccion_id);


--
-- TOC entry 5108 (class 2606 OID 203835)
-- Name: secciones_oficiales secciones_oficiales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_oficiales
    ADD CONSTRAINT secciones_oficiales_pkey PRIMARY KEY (id);


--
-- TOC entry 5113 (class 2606 OID 203837)
-- Name: suscripciones suscripciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones
    ADD CONSTRAINT suscripciones_pkey PRIMARY KEY (suscripcion_id);


--
-- TOC entry 5116 (class 2606 OID 203839)
-- Name: tipos_evaluacion tipos_evaluacion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_evaluacion
    ADD CONSTRAINT tipos_evaluacion_nombre_key UNIQUE (nombre);


--
-- TOC entry 5118 (class 2606 OID 203841)
-- Name: tipos_evaluacion tipos_evaluacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_evaluacion
    ADD CONSTRAINT tipos_evaluacion_pkey PRIMARY KEY (tipo_evaluacion_id);


--
-- TOC entry 5122 (class 2606 OID 203843)
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- TOC entry 5124 (class 2606 OID 203845)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 5126 (class 2606 OID 203847)
-- Name: usuarios usuarios_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_user_id_key UNIQUE (user_id);


--
-- TOC entry 5129 (class 1259 OID 204140)
-- Name: admin_bd_logrespaldo_empresa_id_61be407d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_bd_logrespaldo_empresa_id_61be407d ON public.admin_bd_logrespaldo USING btree (empresa_id);


--
-- TOC entry 5132 (class 1259 OID 204141)
-- Name: admin_bd_logrespaldo_usuario_id_17645f3a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_bd_logrespaldo_usuario_id_17645f3a ON public.admin_bd_logrespaldo USING btree (usuario_id);


--
-- TOC entry 4964 (class 1259 OID 203848)
-- Name: asignaciones_evaluacion_admin_asignador_id_b377164f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_admin_asignador_id_b377164f ON public.asignaciones_evaluacion USING btree (admin_asignador_id);


--
-- TOC entry 4965 (class 1259 OID 203849)
-- Name: asignaciones_evaluacion_empresa_id_456c4cf4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_empresa_id_456c4cf4 ON public.asignaciones_evaluacion USING btree (empresa_id);


--
-- TOC entry 4966 (class 1259 OID 203850)
-- Name: asignaciones_evaluacion_evaluacion_oficial_id_ce80dfa2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_evaluacion_oficial_id_ce80dfa2 ON public.asignaciones_evaluacion USING btree (evaluacion_oficial_id);


--
-- TOC entry 4969 (class 1259 OID 203851)
-- Name: asignaciones_evaluacion_planta_id_6db671c6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_planta_id_6db671c6 ON public.asignaciones_evaluacion USING btree (planta_id);


--
-- TOC entry 4970 (class 1259 OID 203852)
-- Name: asignaciones_evaluacion_token_sesion_c52ef540_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_token_sesion_c52ef540_like ON public.asignaciones_evaluacion USING btree (token_sesion varchar_pattern_ops);


--
-- TOC entry 4973 (class 1259 OID 203853)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 4978 (class 1259 OID 203854)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 4981 (class 1259 OID 203855)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 4984 (class 1259 OID 203856)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 4994 (class 1259 OID 203857)
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- TOC entry 4997 (class 1259 OID 203858)
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- TOC entry 5000 (class 1259 OID 203859)
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 5003 (class 1259 OID 203860)
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 4991 (class 1259 OID 203861)
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 5006 (class 1259 OID 203862)
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- TOC entry 5020 (class 1259 OID 203863)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 5023 (class 1259 OID 203864)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 5030 (class 1259 OID 203865)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 5033 (class 1259 OID 203866)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 5040 (class 1259 OID 203867)
-- Name: empleados_asignados_asignacion_id_96c473f3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empleados_asignados_asignacion_id_96c473f3 ON public.empleados_asignados USING btree (asignacion_id);


--
-- TOC entry 5043 (class 1259 OID 203868)
-- Name: empleados_asignados_empleado_id_a1082f92; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empleados_asignados_empleado_id_a1082f92 ON public.empleados_asignados USING btree (empleado_id);


--
-- TOC entry 5046 (class 1259 OID 203869)
-- Name: empleados_asignados_token_empleado_a8a54d8d_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empleados_asignados_token_empleado_a8a54d8d_like ON public.empleados_asignados USING btree (token_empleado varchar_pattern_ops);


--
-- TOC entry 5066 (class 1259 OID 203870)
-- Name: idx_conjunto_opciones; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_conjunto_opciones ON public.opciones_conjunto USING btree (conjunto_opciones);


--
-- TOC entry 5119 (class 1259 OID 203871)
-- Name: idx_correo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_correo ON public.usuarios USING btree (correo);


--
-- TOC entry 5091 (class 1259 OID 203872)
-- Name: idx_departamento_puesto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_departamento_puesto ON public.puestos USING btree (departamento);


--
-- TOC entry 5038 (class 1259 OID 203873)
-- Name: idx_email_empleado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_empleado ON public.empleados USING btree (email);


--
-- TOC entry 5061 (class 1259 OID 203874)
-- Name: idx_empresa_evaluacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_empresa_evaluacion ON public.evaluaciones USING btree (empresa);


--
-- TOC entry 5081 (class 1259 OID 203875)
-- Name: idx_empresa_planta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_empresa_planta ON public.plantas USING btree (empresa);


--
-- TOC entry 5109 (class 1259 OID 203876)
-- Name: idx_empresa_suscripcion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_empresa_suscripcion ON public.suscripciones USING btree (empresa);


--
-- TOC entry 5070 (class 1259 OID 203877)
-- Name: idx_estado_pago; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_estado_pago ON public.pagos USING btree (estado_pago);


--
-- TOC entry 5110 (class 1259 OID 203878)
-- Name: idx_estado_suscripcion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_estado_suscripcion ON public.suscripciones USING btree (estado);


--
-- TOC entry 5102 (class 1259 OID 203879)
-- Name: idx_evaluacion_seccion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_evaluacion_seccion ON public.secciones_eval USING btree (evaluacion);


--
-- TOC entry 5111 (class 1259 OID 203880)
-- Name: idx_fecha_fin_suscripcion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fecha_fin_suscripcion ON public.suscripciones USING btree (fecha_fin);


--
-- TOC entry 5071 (class 1259 OID 203881)
-- Name: idx_fecha_pago; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fecha_pago ON public.pagos USING btree (fecha_pago);


--
-- TOC entry 5120 (class 1259 OID 203882)
-- Name: idx_nivel_usuario; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nivel_usuario ON public.usuarios USING btree (nivel_usuario);


--
-- TOC entry 5015 (class 1259 OID 203883)
-- Name: idx_nombre_conjunto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nombre_conjunto ON public.conjuntos_opciones USING btree (nombre);


--
-- TOC entry 5057 (class 1259 OID 203884)
-- Name: idx_nombre_empresa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nombre_empresa ON public.empresas USING btree (nombre);


--
-- TOC entry 5075 (class 1259 OID 203885)
-- Name: idx_nombre_plan; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nombre_plan ON public.planes USING btree (nombre);


--
-- TOC entry 5114 (class 1259 OID 203886)
-- Name: idx_nombre_tipo_eval; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_nombre_tipo_eval ON public.tipos_evaluacion USING btree (nombre);


--
-- TOC entry 5067 (class 1259 OID 203887)
-- Name: idx_orden_opciones; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_orden_opciones ON public.opciones_conjunto USING btree (numero_orden);


--
-- TOC entry 5103 (class 1259 OID 203888)
-- Name: idx_orden_seccion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_orden_seccion ON public.secciones_eval USING btree (numero_orden);


--
-- TOC entry 5019 (class 1259 OID 203889)
-- Name: idx_planta_depto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_planta_depto ON public.departamentos USING btree (planta);


--
-- TOC entry 5076 (class 1259 OID 203890)
-- Name: idx_precio_plan; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_precio_plan ON public.planes USING btree (precio);


--
-- TOC entry 5016 (class 1259 OID 203891)
-- Name: idx_predefinido_conjunto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_predefinido_conjunto ON public.conjuntos_opciones USING btree (predefinido);


--
-- TOC entry 5039 (class 1259 OID 203892)
-- Name: idx_puesto_empleado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_puesto_empleado ON public.empleados USING btree (puesto);


--
-- TOC entry 5058 (class 1259 OID 203893)
-- Name: idx_rfc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rfc ON public.empresas USING btree (rfc);


--
-- TOC entry 5062 (class 1259 OID 203894)
-- Name: idx_status_evaluacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_status_evaluacion ON public.evaluaciones USING btree (status);


--
-- TOC entry 5072 (class 1259 OID 203895)
-- Name: idx_suscripcion_pago; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_suscripcion_pago ON public.pagos USING btree (suscripcion);


--
-- TOC entry 5063 (class 1259 OID 203896)
-- Name: idx_tipo_evaluacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tipo_evaluacion ON public.evaluaciones USING btree (tipo_evaluacion);


--
-- TOC entry 5084 (class 1259 OID 203897)
-- Name: idx_tipo_pregunta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tipo_pregunta ON public.preguntas USING btree (tipo_pregunta);


--
-- TOC entry 5089 (class 1259 OID 203898)
-- Name: preguntas_oficiales_pregunta_padre_id_dd462c07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX preguntas_oficiales_pregunta_padre_id_dd462c07 ON public.preguntas_oficiales USING btree (pregunta_padre_id);


--
-- TOC entry 5090 (class 1259 OID 203899)
-- Name: preguntas_oficiales_seccion_id_8fdcef8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX preguntas_oficiales_seccion_id_8fdcef8b ON public.preguntas_oficiales USING btree (seccion_id);


--
-- TOC entry 5094 (class 1259 OID 203900)
-- Name: respuestas_empleados_empleado_asignado_id_9ed2afaa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX respuestas_empleados_empleado_asignado_id_9ed2afaa ON public.respuestas_empleados USING btree (empleado_asignado_id);


--
-- TOC entry 5099 (class 1259 OID 203901)
-- Name: respuestas_empleados_pregunta_oficial_id_8dc43081; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX respuestas_empleados_pregunta_oficial_id_8dc43081 ON public.respuestas_empleados USING btree (pregunta_oficial_id);


--
-- TOC entry 5106 (class 1259 OID 203902)
-- Name: secciones_oficiales_evaluacion_oficial_id_713c3681; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX secciones_oficiales_evaluacion_oficial_id_713c3681 ON public.secciones_oficiales USING btree (evaluacion_oficial_id);


--
-- TOC entry 5175 (class 2606 OID 204130)
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5176 (class 2606 OID 204135)
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5133 (class 2606 OID 203903)
-- Name: admin_plantas admin_plantas_planta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_planta_id_fkey FOREIGN KEY (planta_id) REFERENCES public.plantas(planta_id) ON DELETE CASCADE;


--
-- TOC entry 5134 (class 2606 OID 203908)
-- Name: admin_plantas admin_plantas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 5135 (class 2606 OID 203913)
-- Name: asignaciones_evaluacion asignaciones_evaluac_admin_asignador_id_b377164f_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluac_admin_asignador_id_b377164f_fk_auth_user FOREIGN KEY (admin_asignador_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5136 (class 2606 OID 203918)
-- Name: asignaciones_evaluacion asignaciones_evaluac_empresa_id_456c4cf4_fk_empresas_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluac_empresa_id_456c4cf4_fk_empresas_ FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5137 (class 2606 OID 203923)
-- Name: asignaciones_evaluacion asignaciones_evaluac_evaluacion_oficial_i_ce80dfa2_fk_evaluacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluac_evaluacion_oficial_i_ce80dfa2_fk_evaluacio FOREIGN KEY (evaluacion_oficial_id) REFERENCES public.evaluaciones_oficiales(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5138 (class 2606 OID 203928)
-- Name: asignaciones_evaluacion asignaciones_evaluacion_planta_id_6db671c6_fk_plantas_planta_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_evaluacion
    ADD CONSTRAINT asignaciones_evaluacion_planta_id_6db671c6_fk_plantas_planta_id FOREIGN KEY (planta_id) REFERENCES public.plantas(planta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5139 (class 2606 OID 203933)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5140 (class 2606 OID 203938)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5141 (class 2606 OID 203943)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5142 (class 2606 OID 203948)
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5143 (class 2606 OID 203953)
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5144 (class 2606 OID 203958)
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5145 (class 2606 OID 203963)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5146 (class 2606 OID 203968)
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5148 (class 2606 OID 203973)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5149 (class 2606 OID 203978)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5151 (class 2606 OID 203983)
-- Name: empleados_asignados empleados_asignados_asignacion_id_96c473f3_fk_asignacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados_asignados
    ADD CONSTRAINT empleados_asignados_asignacion_id_96c473f3_fk_asignacio FOREIGN KEY (asignacion_id) REFERENCES public.asignaciones_evaluacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5152 (class 2606 OID 203988)
-- Name: empleados_asignados empleados_asignados_empleado_id_a1082f92_fk_empleados; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados_asignados
    ADD CONSTRAINT empleados_asignados_empleado_id_a1082f92_fk_empleados FOREIGN KEY (empleado_id) REFERENCES public.empleados(empleado_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5174 (class 2606 OID 203993)
-- Name: usuarios fk_admin_empresa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_admin_empresa FOREIGN KEY (admin_empresa) REFERENCES public.usuarios(id);


--
-- TOC entry 5147 (class 2606 OID 203998)
-- Name: departamentos fk_departamentos_planta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT fk_departamentos_planta FOREIGN KEY (planta) REFERENCES public.plantas(planta_id);


--
-- TOC entry 5150 (class 2606 OID 204003)
-- Name: empleados fk_empleados_puesto; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT fk_empleados_puesto FOREIGN KEY (puesto) REFERENCES public.puestos(puesto_id);


--
-- TOC entry 5153 (class 2606 OID 204008)
-- Name: empresas fk_empresas_administrador; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT fk_empresas_administrador FOREIGN KEY (administrador) REFERENCES public.usuarios(id);


--
-- TOC entry 5154 (class 2606 OID 204013)
-- Name: evaluaciones fk_evaluaciones_creado_por; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT fk_evaluaciones_creado_por FOREIGN KEY (creado_por) REFERENCES public.usuarios(id);


--
-- TOC entry 5155 (class 2606 OID 204018)
-- Name: evaluaciones fk_evaluaciones_empresa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT fk_evaluaciones_empresa FOREIGN KEY (empresa) REFERENCES public.empresas(empresa_id);


--
-- TOC entry 5156 (class 2606 OID 204023)
-- Name: evaluaciones fk_evaluaciones_tipo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT fk_evaluaciones_tipo FOREIGN KEY (tipo_evaluacion) REFERENCES public.tipos_evaluacion(tipo_evaluacion_id);


--
-- TOC entry 5157 (class 2606 OID 204028)
-- Name: opciones_conjunto fk_opciones_conjunto; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.opciones_conjunto
    ADD CONSTRAINT fk_opciones_conjunto FOREIGN KEY (conjunto_opciones) REFERENCES public.conjuntos_opciones(conjunto_id);


--
-- TOC entry 5158 (class 2606 OID 204033)
-- Name: pagos fk_pagos_suscripcion; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT fk_pagos_suscripcion FOREIGN KEY (suscripcion) REFERENCES public.suscripciones(suscripcion_id);


--
-- TOC entry 5159 (class 2606 OID 204038)
-- Name: pagos fk_pagos_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT fk_pagos_usuario FOREIGN KEY (usuario) REFERENCES public.usuarios(id);


--
-- TOC entry 5160 (class 2606 OID 204043)
-- Name: plantas fk_plantas_empresa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plantas
    ADD CONSTRAINT fk_plantas_empresa FOREIGN KEY (empresa) REFERENCES public.empresas(empresa_id);


--
-- TOC entry 5161 (class 2606 OID 204048)
-- Name: preguntas fk_pregunta_padre; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT fk_pregunta_padre FOREIGN KEY (pregunta_padre) REFERENCES public.preguntas(pregunta_id);


--
-- TOC entry 5164 (class 2606 OID 204053)
-- Name: puestos fk_puestos_departamento; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos
    ADD CONSTRAINT fk_puestos_departamento FOREIGN KEY (departamento) REFERENCES public.departamentos(departamento_id);


--
-- TOC entry 5167 (class 2606 OID 204058)
-- Name: seccion_preguntas fk_seccion_preguntas_conjunto; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT fk_seccion_preguntas_conjunto FOREIGN KEY (conjunto_opciones) REFERENCES public.conjuntos_opciones(conjunto_id);


--
-- TOC entry 5168 (class 2606 OID 204063)
-- Name: seccion_preguntas fk_seccion_preguntas_pregunta; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT fk_seccion_preguntas_pregunta FOREIGN KEY (pregunta) REFERENCES public.preguntas(pregunta_id);


--
-- TOC entry 5169 (class 2606 OID 204068)
-- Name: seccion_preguntas fk_seccion_preguntas_seccion; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT fk_seccion_preguntas_seccion FOREIGN KEY (seccion) REFERENCES public.secciones_eval(seccion_id);


--
-- TOC entry 5170 (class 2606 OID 204073)
-- Name: secciones_eval fk_secciones_evaluacion; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval
    ADD CONSTRAINT fk_secciones_evaluacion FOREIGN KEY (evaluacion) REFERENCES public.evaluaciones(evaluacion_id);


--
-- TOC entry 5172 (class 2606 OID 204078)
-- Name: suscripciones fk_suscripciones_empresa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones
    ADD CONSTRAINT fk_suscripciones_empresa FOREIGN KEY (empresa) REFERENCES public.empresas(empresa_id);


--
-- TOC entry 5173 (class 2606 OID 204083)
-- Name: suscripciones fk_suscripciones_plan; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones
    ADD CONSTRAINT fk_suscripciones_plan FOREIGN KEY (plan) REFERENCES public.planes(plan_id);


--
-- TOC entry 5162 (class 2606 OID 204088)
-- Name: preguntas_oficiales preguntas_oficiales_pregunta_padre_id_dd462c07_fk_preguntas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas_oficiales
    ADD CONSTRAINT preguntas_oficiales_pregunta_padre_id_dd462c07_fk_preguntas FOREIGN KEY (pregunta_padre_id) REFERENCES public.preguntas_oficiales(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5163 (class 2606 OID 204093)
-- Name: preguntas_oficiales preguntas_oficiales_seccion_id_8fdcef8b_fk_secciones; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas_oficiales
    ADD CONSTRAINT preguntas_oficiales_seccion_id_8fdcef8b_fk_secciones FOREIGN KEY (seccion_id) REFERENCES public.secciones_oficiales(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5165 (class 2606 OID 204098)
-- Name: respuestas_empleados respuestas_empleados_empleado_asignado_id_9ed2afaa_fk_empleados; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleados
    ADD CONSTRAINT respuestas_empleados_empleado_asignado_id_9ed2afaa_fk_empleados FOREIGN KEY (empleado_asignado_id) REFERENCES public.empleados_asignados(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5166 (class 2606 OID 204103)
-- Name: respuestas_empleados respuestas_empleados_pregunta_oficial_id_8dc43081_fk_preguntas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleados
    ADD CONSTRAINT respuestas_empleados_pregunta_oficial_id_8dc43081_fk_preguntas FOREIGN KEY (pregunta_oficial_id) REFERENCES public.preguntas_oficiales(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5171 (class 2606 OID 204108)
-- Name: secciones_oficiales secciones_oficiales_evaluacion_oficial_i_713c3681_fk_evaluacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_oficiales
    ADD CONSTRAINT secciones_oficiales_evaluacion_oficial_i_713c3681_fk_evaluacio FOREIGN KEY (evaluacion_oficial_id) REFERENCES public.evaluaciones_oficiales(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2025-08-02 20:54:05

--
-- PostgreSQL database dump complete
--

