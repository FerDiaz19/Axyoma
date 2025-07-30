--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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

ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_user_id_560ecfb6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_admin_empresa_42f4b2d2_fk_usuarios_id;
ALTER TABLE IF EXISTS ONLY public.suscripciones_empresa DROP CONSTRAINT IF EXISTS suscripciones_empres_plan_id_52beaa74_fk_planes_su;
ALTER TABLE IF EXISTS ONLY public.suscripciones_empresa DROP CONSTRAINT IF EXISTS suscripciones_empres_empresa_id_c4b3c4fb_fk_empresas_;
ALTER TABLE IF EXISTS ONLY public.secciones_eval DROP CONSTRAINT IF EXISTS secciones_eval_evaluacion_id_9491cf53_fk_evaluacio;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_seccion_id_d01463b5_fk_secciones;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_respuesta_correcta_i_6bb7046d_fk_posibles_;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_pregunta_id_9ea6a022_fk_preguntas_pregunta_id;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_conjunto_respuestas__8736e887_fk_conjunto_;
ALTER TABLE IF EXISTS ONLY public.resultados_evaluacion DROP CONSTRAINT IF EXISTS resultados_evaluacio_asignacion_empleado__8b357c01_fk_asignacio;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleado DROP CONSTRAINT IF EXISTS respuestas_empleado_seccion_pregunta_id_8774b443_fk_seccion_p;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleado DROP CONSTRAINT IF EXISTS respuestas_empleado_opcion_seleccionada__549d0943_fk_posibles_;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleado DROP CONSTRAINT IF EXISTS respuestas_empleado_asignacion_empleado__d871f5df_fk_asignacio;
ALTER TABLE IF EXISTS ONLY public.puestos DROP CONSTRAINT IF EXISTS puestos_departamento_f7a3d642_fk_departamentos_departamento_id;
ALTER TABLE IF EXISTS ONLY public.preguntas DROP CONSTRAINT IF EXISTS preguntas_pregunta_padre_2d67e8ba_fk_preguntas_pregunta_id;
ALTER TABLE IF EXISTS ONLY public.posibles_respuestas DROP CONSTRAINT IF EXISTS posibles_respuestas_conjunto_respuestas_610d1979_fk_conjunto_;
ALTER TABLE IF EXISTS ONLY public.plantas DROP CONSTRAINT IF EXISTS plantas_empresa_28c08c98_fk_empresas_empresa_id;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS pagos_usuario_id_eba921fa_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS pagos_suscripcion_id_99dc8463_fk_suscripci;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS evaluaciones_tipo_evaluacion_id_70bc7bfe_fk_tipos_eva;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS evaluaciones_empresa_id_9402d5a5_fk_empresas_empresa_id;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS evaluaciones_creado_por_id_0c8f3e58_fk_usuarios_id;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_administrador_82543b62_fk_usuarios_id;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_puesto_id_3b6f3d91_fk_puestos_puesto_id;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_empresa_id_17428638_fk_empresas_empresa_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_planta_87b189b3_fk_plantas_planta_id;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_user_id_35299eff_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.asignaciones DROP CONSTRAINT IF EXISTS asignaciones_evaluacion_id_8b3fa956_fk_evaluacio;
ALTER TABLE IF EXISTS ONLY public.asignaciones DROP CONSTRAINT IF EXISTS asignaciones_empleado_evaluado_id_6b1b750c_fk_empleados;
ALTER TABLE IF EXISTS ONLY public.asignaciones_empleado DROP CONSTRAINT IF EXISTS asignaciones_emplead_empleado_id_f10d9740_fk_empleados;
ALTER TABLE IF EXISTS ONLY public.asignaciones_empleado DROP CONSTRAINT IF EXISTS asignaciones_emplead_asignacion_id_4d2e2a85_fk_asignacio;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_usuario_id_370be9ba_fk_usuarios_id;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_planta_id_e107f2b3_fk_plantas_planta_id;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id;
DROP INDEX IF EXISTS public.usuarios_correo_02971567_like;
DROP INDEX IF EXISTS public.usuarios_admin_empresa_42f4b2d2;
DROP INDEX IF EXISTS public.tipos_evaluacion_nombre_26ea7ca7_like;
DROP INDEX IF EXISTS public.suscripciones_empresa_plan_id_52beaa74;
DROP INDEX IF EXISTS public.suscripciones_empresa_empresa_id_c4b3c4fb;
DROP INDEX IF EXISTS public.secciones_eval_evaluacion_id_9491cf53;
DROP INDEX IF EXISTS public.seccion_preguntas_seccion_id_d01463b5;
DROP INDEX IF EXISTS public.seccion_preguntas_respuesta_correcta_id_6bb7046d;
DROP INDEX IF EXISTS public.seccion_preguntas_pregunta_id_9ea6a022;
DROP INDEX IF EXISTS public.seccion_preguntas_conjunto_respuestas_id_8736e887;
DROP INDEX IF EXISTS public.respuestas_empleado_seccion_pregunta_id_8774b443;
DROP INDEX IF EXISTS public.respuestas_empleado_opcion_seleccionada_id_549d0943;
DROP INDEX IF EXISTS public.respuestas_empleado_asignacion_empleado_id_d871f5df;
DROP INDEX IF EXISTS public.puestos_departamento_f7a3d642;
DROP INDEX IF EXISTS public.preguntas_pregunta_padre_2d67e8ba;
DROP INDEX IF EXISTS public.posibles_respuestas_conjunto_respuestas_610d1979;
DROP INDEX IF EXISTS public.plantas_empresa_28c08c98;
DROP INDEX IF EXISTS public.planes_suscripcion_nombre_e2e7f579_like;
DROP INDEX IF EXISTS public.pagos_usuario_id_eba921fa;
DROP INDEX IF EXISTS public.pagos_suscripcion_id_99dc8463;
DROP INDEX IF EXISTS public.evaluaciones_tipo_evaluacion_id_70bc7bfe;
DROP INDEX IF EXISTS public.evaluaciones_empresa_id_9402d5a5;
DROP INDEX IF EXISTS public.evaluaciones_creado_por_id_0c8f3e58;
DROP INDEX IF EXISTS public.empresas_rfc_6169650d_like;
DROP INDEX IF EXISTS public.empresas_nombre_5a4759a9_like;
DROP INDEX IF EXISTS public.empleados_puesto_id_3b6f3d91;
DROP INDEX IF EXISTS public.empleados_empresa_id_17428638;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.departamentos_planta_87b189b3;
DROP INDEX IF EXISTS public.conjunto_respuestas_nombre_1bddfe85_like;
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
DROP INDEX IF EXISTS public.asignaciones_evaluacion_id_8b3fa956;
DROP INDEX IF EXISTS public.asignaciones_empleado_evaluado_id_6b1b750c;
DROP INDEX IF EXISTS public.asignaciones_empleado_empleado_id_f10d9740;
DROP INDEX IF EXISTS public.asignaciones_empleado_asignacion_id_4d2e2a85;
DROP INDEX IF EXISTS public.admin_plantas_usuario_id_370be9ba;
DROP INDEX IF EXISTS public.admin_plantas_planta_id_e107f2b3;
DROP INDEX IF EXISTS public.admin_bd_logrespaldo_usuario_id_17645f3a;
DROP INDEX IF EXISTS public.admin_bd_logrespaldo_empresa_id_61be407d;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_user_id_key;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_correo_key;
ALTER TABLE IF EXISTS ONLY public.secciones_eval DROP CONSTRAINT IF EXISTS unique_section_orden;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS unique_seccion_pregunta;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS unique_seccion_orden;
ALTER TABLE IF EXISTS ONLY public.posibles_respuestas DROP CONSTRAINT IF EXISTS unique_opcion_orden;
ALTER TABLE IF EXISTS ONLY public.tipos_evaluacion DROP CONSTRAINT IF EXISTS tipos_evaluacion_pkey;
ALTER TABLE IF EXISTS ONLY public.tipos_evaluacion DROP CONSTRAINT IF EXISTS tipos_evaluacion_nombre_key;
ALTER TABLE IF EXISTS ONLY public.suscripciones_empresa DROP CONSTRAINT IF EXISTS suscripciones_empresa_pkey;
ALTER TABLE IF EXISTS ONLY public.secciones_eval DROP CONSTRAINT IF EXISTS secciones_eval_pkey;
ALTER TABLE IF EXISTS ONLY public.seccion_preguntas DROP CONSTRAINT IF EXISTS seccion_preguntas_pkey;
ALTER TABLE IF EXISTS ONLY public.resultados_evaluacion DROP CONSTRAINT IF EXISTS resultados_evaluacion_pkey;
ALTER TABLE IF EXISTS ONLY public.resultados_evaluacion DROP CONSTRAINT IF EXISTS resultados_evaluacion_asignacion_empleado_id_key;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleado DROP CONSTRAINT IF EXISTS respuestas_empleado_pkey;
ALTER TABLE IF EXISTS ONLY public.respuestas_empleado DROP CONSTRAINT IF EXISTS respuestas_empleado_asignacion_empleado_id_s_c3e48c83_uniq;
ALTER TABLE IF EXISTS ONLY public.puestos DROP CONSTRAINT IF EXISTS puestos_pkey;
ALTER TABLE IF EXISTS ONLY public.puestos DROP CONSTRAINT IF EXISTS puestos_nombre_departamento_4c6581db_uniq;
ALTER TABLE IF EXISTS ONLY public.preguntas DROP CONSTRAINT IF EXISTS preguntas_pkey;
ALTER TABLE IF EXISTS ONLY public.posibles_respuestas DROP CONSTRAINT IF EXISTS posibles_respuestas_pkey;
ALTER TABLE IF EXISTS ONLY public.plantas DROP CONSTRAINT IF EXISTS plantas_pkey;
ALTER TABLE IF EXISTS ONLY public.planes_suscripcion DROP CONSTRAINT IF EXISTS planes_suscripcion_pkey;
ALTER TABLE IF EXISTS ONLY public.planes_suscripcion DROP CONSTRAINT IF EXISTS planes_suscripcion_nombre_key;
ALTER TABLE IF EXISTS ONLY public.pagos DROP CONSTRAINT IF EXISTS pagos_pkey;
ALTER TABLE IF EXISTS ONLY public.evaluaciones DROP CONSTRAINT IF EXISTS evaluaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_rfc_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_nombre_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_administrador_key;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_pkey;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_nombre_planta_94271a14_uniq;
ALTER TABLE IF EXISTS ONLY public.conjunto_respuestas DROP CONSTRAINT IF EXISTS conjunto_respuestas_pkey;
ALTER TABLE IF EXISTS ONLY public.conjunto_respuestas DROP CONSTRAINT IF EXISTS conjunto_respuestas_nombre_key;
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
ALTER TABLE IF EXISTS ONLY public.asignaciones DROP CONSTRAINT IF EXISTS asignaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.asignaciones_empleado DROP CONSTRAINT IF EXISTS asignaciones_empleado_token_acceso_key;
ALTER TABLE IF EXISTS ONLY public.asignaciones_empleado DROP CONSTRAINT IF EXISTS asignaciones_empleado_pkey;
ALTER TABLE IF EXISTS ONLY public.asignaciones_empleado DROP CONSTRAINT IF EXISTS asignaciones_empleado_asignacion_id_empleado_id_2bd96fc9_uniq;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_usuario_id_planta_id_f206071a_uniq;
ALTER TABLE IF EXISTS ONLY public.admin_plantas DROP CONSTRAINT IF EXISTS admin_plantas_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_bd_logrespaldo DROP CONSTRAINT IF EXISTS admin_bd_logrespaldo_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_bd_configuracionbd DROP CONSTRAINT IF EXISTS admin_bd_configuracionbd_pkey;
DROP TABLE IF EXISTS public.usuarios;
DROP TABLE IF EXISTS public.tipos_evaluacion;
DROP TABLE IF EXISTS public.suscripciones_empresa;
DROP TABLE IF EXISTS public.secciones_eval;
DROP TABLE IF EXISTS public.seccion_preguntas;
DROP TABLE IF EXISTS public.resultados_evaluacion;
DROP TABLE IF EXISTS public.respuestas_empleado;
DROP TABLE IF EXISTS public.puestos;
DROP TABLE IF EXISTS public.preguntas;
DROP TABLE IF EXISTS public.posibles_respuestas;
DROP TABLE IF EXISTS public.plantas;
DROP TABLE IF EXISTS public.planes_suscripcion;
DROP TABLE IF EXISTS public.pagos;
DROP TABLE IF EXISTS public.evaluaciones;
DROP TABLE IF EXISTS public.empresas;
DROP TABLE IF EXISTS public.empleados;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.departamentos;
DROP TABLE IF EXISTS public.conjunto_respuestas;
DROP TABLE IF EXISTS public.authtoken_token;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.asignaciones_empleado;
DROP TABLE IF EXISTS public.asignaciones;
DROP TABLE IF EXISTS public.admin_plantas;
DROP TABLE IF EXISTS public.admin_bd_logrespaldo;
DROP TABLE IF EXISTS public.admin_bd_configuracionbd;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
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
-- Name: admin_plantas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_plantas (
    id bigint NOT NULL,
    fecha_asignacion timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    password_temporal character varying(128),
    usuario_id integer NOT NULL,
    planta_id integer NOT NULL
);


--
-- Name: admin_plantas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.admin_plantas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_plantas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: asignaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asignaciones (
    asignacion_id integer NOT NULL,
    fecha_inicio timestamp with time zone NOT NULL,
    fecha_fin timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    puesto character varying(64),
    departamento character varying(64),
    empleado_evaluado_id integer,
    evaluacion_id integer NOT NULL
);


--
-- Name: asignaciones_asignacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.asignaciones ALTER COLUMN asignacion_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.asignaciones_asignacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: asignaciones_empleado; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asignaciones_empleado (
    asignacion_empleado_id integer NOT NULL,
    token_acceso uuid NOT NULL,
    status character varying(16) NOT NULL,
    fecha_asignacion timestamp with time zone NOT NULL,
    fecha_completado timestamp with time zone,
    asignacion_id integer NOT NULL,
    empleado_id integer NOT NULL
);


--
-- Name: asignaciones_empleado_asignacion_empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.asignaciones_empleado ALTER COLUMN asignacion_empleado_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.asignaciones_empleado_asignacion_empleado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
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
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
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
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
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
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
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
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
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
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: conjunto_respuestas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conjunto_respuestas (
    conjunto_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text,
    predefinido boolean NOT NULL
);


--
-- Name: conjunto_respuestas_conjunto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.conjunto_respuestas ALTER COLUMN conjunto_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.conjunto_respuestas_conjunto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: departamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departamentos (
    departamento_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text,
    fecha_registro timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    planta integer NOT NULL
);


--
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.departamentos ALTER COLUMN departamento_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.departamentos_departamento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
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
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
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
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
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
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: empleados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.empleados (
    empleado_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    apellido_paterno character varying(64) NOT NULL,
    apellido_materno character varying(64),
    email character varying(255),
    telefono character varying(20),
    fecha_ingreso date,
    fecha_registro timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    empresa_id integer,
    puesto_id integer
);


--
-- Name: empleados_empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.empleados ALTER COLUMN empleado_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.empleados_empleado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
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
    fecha_registro timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    administrador integer NOT NULL
);


--
-- Name: empresas_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.empresas ALTER COLUMN empresa_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.empresas_empresa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: evaluaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluaciones (
    evaluacion_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    descripcion text,
    instrucciones text,
    tiempo_limite integer,
    umbral_aprobacion integer,
    status boolean NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    creado_por_id integer,
    empresa_id integer,
    tipo_evaluacion_id integer NOT NULL
);


--
-- Name: evaluaciones_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.evaluaciones ALTER COLUMN evaluacion_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.evaluaciones_evaluacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pagos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pagos (
    pago_id integer NOT NULL,
    costo numeric(10,2) NOT NULL,
    monto_pago numeric(10,2) NOT NULL,
    estado_pago character varying(20) NOT NULL,
    fecha_pago timestamp with time zone NOT NULL,
    fecha_vencimiento date,
    transaccion_id character varying(50),
    comprobante character varying(255),
    usuario_id integer,
    suscripcion_id integer NOT NULL
);


--
-- Name: pagos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.pagos ALTER COLUMN pago_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.pagos_pago_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: planes_suscripcion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.planes_suscripcion (
    plan_id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text,
    precio numeric(10,2) NOT NULL,
    duracion integer NOT NULL,
    limite_empleados integer,
    limite_plantas integer,
    caracteristicas text,
    status boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL
);


--
-- Name: planes_suscripcion_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.planes_suscripcion ALTER COLUMN plan_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.planes_suscripcion_plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: plantas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plantas (
    planta_id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    direccion text,
    fecha_registro timestamp with time zone NOT NULL,
    status boolean NOT NULL,
    empresa integer NOT NULL
);


--
-- Name: plantas_planta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.plantas ALTER COLUMN planta_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.plantas_planta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: posibles_respuestas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.posibles_respuestas (
    opcion_conjunto_id integer NOT NULL,
    texto_opcion character varying(256) NOT NULL,
    valor_booleano boolean,
    valor_int integer,
    valor_decimal numeric(16,2),
    numero_orden integer NOT NULL,
    conjunto_respuestas integer NOT NULL
);


--
-- Name: posibles_respuestas_opcion_conjunto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.posibles_respuestas ALTER COLUMN opcion_conjunto_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.posibles_respuestas_opcion_conjunto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: preguntas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.preguntas (
    pregunta_id integer NOT NULL,
    texto_pregunta text NOT NULL,
    tipo_pregunta character varying(20) NOT NULL,
    es_obligatoria boolean NOT NULL,
    activador_padre character varying(255),
    pregunta_padre integer
);


--
-- Name: preguntas_pregunta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.preguntas ALTER COLUMN pregunta_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.preguntas_pregunta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: puestos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.puestos (
    puesto_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text,
    status boolean NOT NULL,
    departamento integer NOT NULL
);


--
-- Name: puestos_puesto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.puestos ALTER COLUMN puesto_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.puestos_puesto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: respuestas_empleado; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.respuestas_empleado (
    respuesta_empleado_id integer NOT NULL,
    respuesta_texto text,
    respuesta_valor_numerico integer,
    respuesta_valor_decimal numeric(16,2),
    es_correcta boolean NOT NULL,
    fecha_respuesta timestamp with time zone NOT NULL,
    asignacion_empleado_id integer NOT NULL,
    opcion_seleccionada_id integer,
    seccion_pregunta_id integer NOT NULL
);


--
-- Name: respuestas_empleado_respuesta_empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.respuestas_empleado ALTER COLUMN respuesta_empleado_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.respuestas_empleado_respuesta_empleado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: resultados_evaluacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resultados_evaluacion (
    resultado_id integer NOT NULL,
    puntaje_total numeric(6,2),
    num_respuestas_correctas integer NOT NULL,
    num_preguntas_evaluables integer NOT NULL,
    porcentaje_correctas numeric(5,2),
    fecha_calculo timestamp with time zone NOT NULL,
    aprobado boolean,
    asignacion_empleado_id integer NOT NULL
);


--
-- Name: resultados_evaluacion_resultado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.resultados_evaluacion ALTER COLUMN resultado_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.resultados_evaluacion_resultado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: seccion_preguntas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.seccion_preguntas (
    seccion_pregunta_id integer NOT NULL,
    numero_orden integer NOT NULL,
    conjunto_respuestas_id integer,
    pregunta_id integer NOT NULL,
    respuesta_correcta_id integer,
    seccion_id integer NOT NULL
);


--
-- Name: seccion_preguntas_seccion_pregunta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.seccion_preguntas ALTER COLUMN seccion_pregunta_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.seccion_preguntas_seccion_pregunta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: secciones_eval; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.secciones_eval (
    seccion_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    descripcion text,
    numero_orden integer NOT NULL,
    es_evaluable boolean NOT NULL,
    evaluacion_id integer NOT NULL
);


--
-- Name: secciones_eval_seccion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.secciones_eval ALTER COLUMN seccion_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.secciones_eval_seccion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: suscripciones_empresa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.suscripciones_empresa (
    suscripcion_id integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    estado character varying(20) NOT NULL,
    status boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    empresa_id integer NOT NULL,
    plan_id integer NOT NULL
);


--
-- Name: suscripciones_empresa_suscripcion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.suscripciones_empresa ALTER COLUMN suscripcion_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.suscripciones_empresa_suscripcion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tipos_evaluacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_evaluacion (
    tipo_evaluacion_id integer NOT NULL,
    nombre character varying(32) NOT NULL,
    descripcion text
);


--
-- Name: tipos_evaluacion_tipo_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.tipos_evaluacion ALTER COLUMN tipo_evaluacion_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipos_evaluacion_tipo_evaluacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(128) NOT NULL,
    apellido_paterno character varying(64) NOT NULL,
    apellido_materno character varying(64),
    correo character varying(255) NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    nivel_usuario character varying(20) NOT NULL,
    status boolean NOT NULL,
    admin_empresa integer,
    user_id integer NOT NULL
);


--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.usuarios ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuarios_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: admin_bd_configuracionbd; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_bd_configuracionbd (id, nombre_bd, host, puerto, usuario_admin, directorio_respaldos, max_respaldos_mantener, habilitar_respaldos_automaticos, frecuencia_respaldo_dias) FROM stdin;
\.


--
-- Data for Name: admin_bd_logrespaldo; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_bd_logrespaldo (id, tipo, archivo_nombre, archivo_ruta, "archivo_tamaño", tablas_incluidas, fecha_creacion, exitoso, detalles, mensaje_error, empresa_id, usuario_id) FROM stdin;
\.


--
-- Data for Name: admin_plantas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_plantas (id, fecha_asignacion, status, password_temporal, usuario_id, planta_id) FROM stdin;
1	2025-07-30 14:36:41.973657-07	t	\N	2	1
2	2025-07-30 14:49:55.119446-07	t	\N	2	2
\.


--
-- Data for Name: asignaciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asignaciones (asignacion_id, fecha_inicio, fecha_fin, status, fecha_registro, fecha_actualizacion, puesto, departamento, empleado_evaluado_id, evaluacion_id) FROM stdin;
\.


--
-- Data for Name: asignaciones_empleado; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asignaciones_empleado (asignacion_empleado_id, token_acceso, status, fecha_asignacion, fecha_completado, asignacion_id, empleado_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
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
33	Can add perfil usuario	9	add_perfilusuario
34	Can change perfil usuario	9	change_perfilusuario
35	Can delete perfil usuario	9	delete_perfilusuario
36	Can view perfil usuario	9	view_perfilusuario
37	Can add empresa	10	add_empresa
38	Can change empresa	10	change_empresa
39	Can delete empresa	10	delete_empresa
40	Can view empresa	10	view_empresa
41	Can add planta	11	add_planta
42	Can change planta	11	change_planta
43	Can delete planta	11	delete_planta
44	Can view planta	11	view_planta
45	Can add departamento	12	add_departamento
46	Can change departamento	12	change_departamento
47	Can delete departamento	12	delete_departamento
48	Can view departamento	12	view_departamento
49	Can add puesto	13	add_puesto
50	Can change puesto	13	change_puesto
51	Can delete puesto	13	delete_puesto
52	Can view puesto	13	view_puesto
53	Can add empleado	14	add_empleado
54	Can change empleado	14	change_empleado
55	Can delete empleado	14	delete_empleado
56	Can view empleado	14	view_empleado
57	Can add admin planta	15	add_adminplanta
58	Can change admin planta	15	change_adminplanta
59	Can delete admin planta	15	delete_adminplanta
60	Can view admin planta	15	view_adminplanta
61	Can add pago export	16	add_pagoexport
62	Can change pago export	16	change_pagoexport
63	Can delete pago export	16	delete_pagoexport
64	Can view pago export	16	view_pagoexport
65	Can add suscripcion empresa export	17	add_suscripcionempresaexport
66	Can change suscripcion empresa export	17	change_suscripcionempresaexport
67	Can delete suscripcion empresa export	17	delete_suscripcionempresaexport
68	Can view suscripcion empresa export	17	view_suscripcionempresaexport
69	Can add Plan de Suscripción	18	add_plansuscripcion
70	Can change Plan de Suscripción	18	change_plansuscripcion
71	Can delete Plan de Suscripción	18	delete_plansuscripcion
72	Can view Plan de Suscripción	18	view_plansuscripcion
73	Can add Suscripción de Empresa	19	add_suscripcionempresa
74	Can change Suscripción de Empresa	19	change_suscripcionempresa
75	Can delete Suscripción de Empresa	19	delete_suscripcionempresa
76	Can view Suscripción de Empresa	19	view_suscripcionempresa
77	Can add Pago	20	add_pago
78	Can change Pago	20	change_pago
79	Can delete Pago	20	delete_pago
80	Can view Pago	20	view_pago
81	Can add conjunto respuestas	21	add_conjuntorespuestas
82	Can change conjunto respuestas	21	change_conjuntorespuestas
83	Can delete conjunto respuestas	21	delete_conjuntorespuestas
84	Can view conjunto respuestas	21	view_conjuntorespuestas
85	Can add tipo evaluacion	22	add_tipoevaluacion
86	Can change tipo evaluacion	22	change_tipoevaluacion
87	Can delete tipo evaluacion	22	delete_tipoevaluacion
88	Can view tipo evaluacion	22	view_tipoevaluacion
89	Can add asignacion	23	add_asignacion
90	Can change asignacion	23	change_asignacion
91	Can delete asignacion	23	delete_asignacion
92	Can view asignacion	23	view_asignacion
93	Can add asignacion empleado	24	add_asignacionempleado
94	Can change asignacion empleado	24	change_asignacionempleado
95	Can delete asignacion empleado	24	delete_asignacionempleado
96	Can view asignacion empleado	24	view_asignacionempleado
97	Can add evaluacion	25	add_evaluacion
98	Can change evaluacion	25	change_evaluacion
99	Can delete evaluacion	25	delete_evaluacion
100	Can view evaluacion	25	view_evaluacion
101	Can add posibles respuestas	26	add_posiblesrespuestas
102	Can change posibles respuestas	26	change_posiblesrespuestas
103	Can delete posibles respuestas	26	delete_posiblesrespuestas
104	Can view posibles respuestas	26	view_posiblesrespuestas
105	Can add pregunta	27	add_pregunta
106	Can change pregunta	27	change_pregunta
107	Can delete pregunta	27	delete_pregunta
108	Can view pregunta	27	view_pregunta
109	Can add resultado evaluacion	28	add_resultadoevaluacion
110	Can change resultado evaluacion	28	change_resultadoevaluacion
111	Can delete resultado evaluacion	28	delete_resultadoevaluacion
112	Can view resultado evaluacion	28	view_resultadoevaluacion
113	Can add seccion eval	29	add_seccioneval
114	Can change seccion eval	29	change_seccioneval
115	Can delete seccion eval	29	delete_seccioneval
116	Can view seccion eval	29	view_seccioneval
117	Can add seccion pregunta	30	add_seccionpregunta
118	Can change seccion pregunta	30	change_seccionpregunta
119	Can delete seccion pregunta	30	delete_seccionpregunta
120	Can view seccion pregunta	30	view_seccionpregunta
121	Can add respuesta empleado	31	add_respuestaempleado
122	Can change respuesta empleado	31	change_respuestaempleado
123	Can delete respuesta empleado	31	delete_respuestaempleado
124	Can view respuesta empleado	31	view_respuestaempleado
125	Can add Configuración de BD	32	add_configuracionbd
126	Can change Configuración de BD	32	change_configuracionbd
127	Can delete Configuración de BD	32	delete_configuracionbd
128	Can view Configuración de BD	32	view_configuracionbd
129	Can add Log de Respaldo	33	add_logrespaldo
130	Can change Log de Respaldo	33	change_logrespaldo
131	Can delete Log de Respaldo	33	delete_logrespaldo
132	Can view Log de Respaldo	33	view_logrespaldo
133	Can add asignacion	34	add_asignacion
134	Can change asignacion	34	change_asignacion
135	Can delete asignacion	34	delete_asignacion
136	Can view asignacion	34	view_asignacion
137	Can add conjunto respuestas	35	add_conjuntorespuestas
138	Can change conjunto respuestas	35	change_conjuntorespuestas
139	Can delete conjunto respuestas	35	delete_conjuntorespuestas
140	Can view conjunto respuestas	35	view_conjuntorespuestas
141	Can add tipo evaluacion	36	add_tipoevaluacion
142	Can change tipo evaluacion	36	change_tipoevaluacion
143	Can delete tipo evaluacion	36	delete_tipoevaluacion
144	Can view tipo evaluacion	36	view_tipoevaluacion
145	Can add asignacion empleado	37	add_asignacionempleado
146	Can change asignacion empleado	37	change_asignacionempleado
147	Can delete asignacion empleado	37	delete_asignacionempleado
148	Can view asignacion empleado	37	view_asignacionempleado
149	Can add evaluacion	38	add_evaluacion
150	Can change evaluacion	38	change_evaluacion
151	Can delete evaluacion	38	delete_evaluacion
152	Can view evaluacion	38	view_evaluacion
153	Can add posibles respuestas	39	add_posiblesrespuestas
154	Can change posibles respuestas	39	change_posiblesrespuestas
155	Can delete posibles respuestas	39	delete_posiblesrespuestas
156	Can view posibles respuestas	39	view_posiblesrespuestas
157	Can add pregunta	40	add_pregunta
158	Can change pregunta	40	change_pregunta
159	Can delete pregunta	40	delete_pregunta
160	Can view pregunta	40	view_pregunta
161	Can add resultado evaluacion	41	add_resultadoevaluacion
162	Can change resultado evaluacion	41	change_resultadoevaluacion
163	Can delete resultado evaluacion	41	delete_resultadoevaluacion
164	Can view resultado evaluacion	41	view_resultadoevaluacion
165	Can add seccion eval	42	add_seccioneval
166	Can change seccion eval	42	change_seccioneval
167	Can delete seccion eval	42	delete_seccioneval
168	Can view seccion eval	42	view_seccioneval
169	Can add seccion pregunta	43	add_seccionpregunta
170	Can change seccion pregunta	43	change_seccionpregunta
171	Can delete seccion pregunta	43	delete_seccionpregunta
172	Can view seccion pregunta	43	view_seccionpregunta
173	Can add respuesta empleado	44	add_respuestaempleado
174	Can change respuesta empleado	44	change_respuestaempleado
175	Can delete respuesta empleado	44	delete_respuestaempleado
176	Can view respuesta empleado	44	view_respuestaempleado
177	Can add Evaluación	45	add_evaluacioncompleta
178	Can change Evaluación	45	change_evaluacioncompleta
179	Can delete Evaluación	45	delete_evaluacioncompleta
180	Can view Evaluación	45	view_evaluacioncompleta
181	Can add evaluacion pregunta	46	add_evaluacionpregunta
182	Can change evaluacion pregunta	46	change_evaluacionpregunta
183	Can delete evaluacion pregunta	46	delete_evaluacionpregunta
184	Can view evaluacion pregunta	46	view_evaluacionpregunta
185	Can add Respuesta a Evaluación	47	add_respuestaevaluacion
186	Can change Respuesta a Evaluación	47	change_respuestaevaluacion
187	Can delete Respuesta a Evaluación	47	delete_respuestaevaluacion
188	Can view Respuesta a Evaluación	47	view_respuestaevaluacion
189	Can add Detalle de Respuesta	48	add_detallerespuesta
190	Can change Detalle de Respuesta	48	change_detallerespuesta
191	Can delete Detalle de Respuesta	48	delete_detallerespuesta
192	Can view Detalle de Respuesta	48	view_detallerespuesta
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$1000000$a1UUieta6zPC2Kkj7GcFAn$MHnLPGuMsYwv+AT9WnuC1J8TaPNnLI/oph4ea0fx+qI=	\N	t	superadmin			superadmin@axyoma.com	t	t	2025-07-30 14:34:12.743368-07
4	pbkdf2_sha256$1000000$sg2Q3KVQOtCcpJmRANFrZo$KAi6lQG/zMeHPHHPBn87sGG9kPyT+GYHg3autVdAeMs=	\N	f	axis22			axissssssss@gmail.com	f	t	2025-07-30 14:59:42.776558-07
2	pbkdf2_sha256$1000000$Lp9PRfWKUr6pSjUvsPJbNn$764YP8JSgqHf3d1pX6nd4AdtOj4Q09CG5KWhv2MmUS0=	\N	f	admin_empresa	Admin	Empresa	admin@empresa.com	t	t	2025-07-30 14:36:41.085477-07
3	pbkdf2_sha256$1000000$WuC1ItySMk31pXbIybU3xj$CWsX0zy49NY01OuLoHHeDNSVkUKBqE355mDoQ7LVzb4=	\N	f	admin_planta	Admin	Planta	admin@planta.com	t	t	2025-07-30 14:36:41.533309-07
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
68b325708c606f3299aaf21e7bb7fc60ba80921b	2025-07-30 14:38:53.157906-07	2
0d681a39ae4dbced4c2a2f40a42251ce4815b66f	2025-07-30 14:39:50.465151-07	3
19f5ff2698683a9e92956ef79326a58d9ce285ae	2025-07-30 14:46:16.69811-07	1
d478b3511a258140ad12698612b3d5b7d8894734	2025-07-30 14:59:52.60841-07	4
\.


--
-- Data for Name: conjunto_respuestas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.conjunto_respuestas (conjunto_id, nombre, descripcion, predefinido) FROM stdin;
\.


--
-- Data for Name: departamentos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.departamentos (departamento_id, nombre, descripcion, fecha_registro, status, planta) FROM stdin;
1	Recursos Humanos	Gestión del talento humano y desarrollo organizacional	2025-07-30 14:49:54.8852-07	t	2
2	Producción	Operaciones de manufactura y control de calidad	2025-07-30 14:49:54.887578-07	t	2
3	Mantenimiento	Mantenimiento preventivo y correctivo de equipos	2025-07-30 14:49:54.888926-07	t	2
4	Calidad	Control de calidad y sistemas de gestión	2025-07-30 14:49:54.890401-07	t	2
5	Almacén	Logística, inventarios y distribución	2025-07-30 14:49:54.891758-07	t	2
6	Administración	Finanzas, contabilidad y administración general	2025-07-30 14:49:54.893244-07	t	2
7	Sistemas	Tecnologías de información y automatización	2025-07-30 14:49:54.894556-07	t	2
8	Recursos Humanos	Gestión del talento humano y desarrollo organizacional	2025-07-30 14:49:54.89606-07	t	3
9	Producción	Operaciones de manufactura y control de calidad	2025-07-30 14:49:54.897869-07	t	3
10	Mantenimiento	Mantenimiento preventivo y correctivo de equipos	2025-07-30 14:49:54.899312-07	t	3
11	Calidad	Control de calidad y sistemas de gestión	2025-07-30 14:49:54.900606-07	t	3
12	Almacén	Logística, inventarios y distribución	2025-07-30 14:49:54.901937-07	t	3
13	Administración	Finanzas, contabilidad y administración general	2025-07-30 14:49:54.903366-07	t	3
14	Sistemas	Tecnologías de información y automatización	2025-07-30 14:49:54.904698-07	t	3
15	Recursos Humanos	Gestión del talento humano y desarrollo organizacional	2025-07-30 14:49:54.906121-07	t	4
16	Producción	Operaciones de manufactura y control de calidad	2025-07-30 14:49:54.907351-07	t	4
17	Mantenimiento	Mantenimiento preventivo y correctivo de equipos	2025-07-30 14:49:54.90865-07	t	4
18	Calidad	Control de calidad y sistemas de gestión	2025-07-30 14:49:54.909867-07	t	4
19	Almacén	Logística, inventarios y distribución	2025-07-30 14:49:54.911033-07	t	4
20	Administración	Finanzas, contabilidad y administración general	2025-07-30 14:49:54.912366-07	t	4
21	Sistemas	Tecnologías de información y automatización	2025-07-30 14:49:54.914144-07	t	4
22	Administración	Gestión administrativa general	2025-07-30 14:59:43.224564-07	t	5
23	Recursos Humanos	Gestión del personal y nómina	2025-07-30 14:59:43.225327-07	t	5
24	Finanzas	Gestión financiera y contable	2025-07-30 14:59:43.225791-07	t	5
25	Producción	Operaciones de manufactura	2025-07-30 14:59:43.226196-07	t	5
26	Calidad	Control y aseguramiento de calidad	2025-07-30 14:59:43.226583-07	t	5
27	Mantenimiento	Mantenimiento de equipos e instalaciones	2025-07-30 14:59:43.226945-07	t	5
28	Logística	Almacén y distribución	2025-07-30 14:59:43.227279-07	t	5
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
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
16	subscriptions	pagoexport
17	subscriptions	suscripcionempresaexport
18	subscriptions	plansuscripcion
19	subscriptions	suscripcionempresa
20	subscriptions	pago
21	evaluaciones	conjuntorespuestas
22	evaluaciones	tipoevaluacion
23	evaluaciones	asignacion
24	evaluaciones	asignacionempleado
25	evaluaciones	evaluacion
26	evaluaciones	posiblesrespuestas
27	evaluaciones	pregunta
28	evaluaciones	resultadoevaluacion
29	evaluaciones	seccioneval
30	evaluaciones	seccionpregunta
31	evaluaciones	respuestaempleado
32	admin_bd	configuracionbd
33	admin_bd	logrespaldo
34	users	asignacion
35	users	conjuntorespuestas
36	users	tipoevaluacion
37	users	asignacionempleado
38	users	evaluacion
39	users	posiblesrespuestas
40	users	pregunta
41	users	resultadoevaluacion
42	users	seccioneval
43	users	seccionpregunta
44	users	respuestaempleado
45	evaluaciones	evaluacioncompleta
46	evaluaciones	evaluacionpregunta
47	evaluaciones	respuestaevaluacion
48	evaluaciones	detallerespuesta
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-07-30 14:33:01.615049-07
2	auth	0001_initial	2025-07-30 14:33:01.678458-07
3	admin	0001_initial	2025-07-30 14:33:01.696686-07
4	admin	0002_logentry_remove_auto_add	2025-07-30 14:33:01.702246-07
5	admin	0003_logentry_add_action_flag_choices	2025-07-30 14:33:01.708251-07
6	users	0001_initial	2025-07-30 14:33:01.842331-07
7	admin_bd	0001_initial	2025-07-30 14:33:01.869701-07
8	contenttypes	0002_remove_content_type_name	2025-07-30 14:33:01.886824-07
9	auth	0002_alter_permission_name_max_length	2025-07-30 14:33:01.897095-07
10	auth	0003_alter_user_email_max_length	2025-07-30 14:33:01.903798-07
11	auth	0004_alter_user_username_opts	2025-07-30 14:33:01.910299-07
12	auth	0005_alter_user_last_login_null	2025-07-30 14:33:01.917902-07
13	auth	0006_require_contenttypes_0002	2025-07-30 14:33:01.918787-07
14	auth	0007_alter_validators_add_error_messages	2025-07-30 14:33:01.924991-07
15	auth	0008_alter_user_username_max_length	2025-07-30 14:33:01.936815-07
16	auth	0009_alter_user_last_name_max_length	2025-07-30 14:33:01.944659-07
17	auth	0010_alter_group_name_max_length	2025-07-30 14:33:01.955253-07
18	auth	0011_update_proxy_permissions	2025-07-30 14:33:01.970613-07
19	auth	0012_alter_user_first_name_max_length	2025-07-30 14:33:01.977794-07
20	authtoken	0001_initial	2025-07-30 14:33:01.995278-07
21	authtoken	0002_auto_20160226_1747	2025-07-30 14:33:02.020842-07
22	authtoken	0003_tokenproxy	2025-07-30 14:33:02.022582-07
23	authtoken	0004_alter_tokenproxy_options	2025-07-30 14:33:02.02612-07
24	evaluaciones	0001_initial	2025-07-30 14:33:02.281217-07
25	sessions	0001_initial	2025-07-30 14:33:02.291649-07
26	subscriptions	0001_initial	2025-07-30 14:33:02.352864-07
27	users	0002_auto_20250730_1507	2025-07-30 15:08:18.257889-07
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: empleados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empleados (empleado_id, nombre, apellido_paterno, apellido_materno, email, telefono, fecha_ingreso, fecha_registro, status, empresa_id, puesto_id) FROM stdin;
1	Sergio	Pérez	Gómez	sergio.pérez@technomex.com.mx	4421850199	2021-06-29	2025-07-30 14:50:52.117023-07	t	\N	1
2	Francisco	Romero	Castillo	francisco.romero@technomex.com.mx	4429995462	2024-03-04	2025-07-30 14:50:52.120532-07	t	\N	2
3	María Elena	Martínez	Romero	maría.elena.martínez@technomex.com.mx	4422614362	2022-12-28	2025-07-30 14:50:52.122766-07	t	\N	3
4	Silvia	Rodríguez	Ortiz	silvia.rodríguez@technomex.com.mx	4422715773	2022-03-15	2025-07-30 14:50:52.125046-07	t	\N	4
5	Andrés	Ortiz	Vargas	andrés.ortiz@technomex.com.mx	4423988287	2020-12-01	2025-07-30 14:50:52.127228-07	t	\N	4
6	Fernando	Gutiérrez	Pérez	fernando.gutiérrez@technomex.com.mx	4428805788	2022-06-16	2025-07-30 14:50:52.128502-07	t	\N	4
7	Ana Patricia	Ruiz	López	ana.patricia.ruiz@technomex.com.mx	4429952586	2021-12-15	2025-07-30 14:50:52.129923-07	t	\N	5
8	Eduardo	Ruiz	Castillo	eduardo.ruiz@technomex.com.mx	4428835797	2021-06-10	2025-07-30 14:50:52.132378-07	t	\N	6
9	Raúl	Romero	Rodríguez	raúl.romero@technomex.com.mx	4429900399	2021-06-11	2025-07-30 14:50:52.134594-07	t	\N	7
10	Claudia	García	Ruiz	claudia.garcía@technomex.com.mx	4423562439	2023-05-25	2025-07-30 14:50:52.136748-07	t	\N	8
11	Adriana	Ruiz	López	adriana.ruiz@technomex.com.mx	4421945351	2024-09-13	2025-07-30 14:50:52.138738-07	t	\N	8
12	Beatriz	González	Romero	beatriz.gonzález@technomex.com.mx	4427244061	2021-04-15	2025-07-30 14:50:52.139836-07	t	\N	8
13	Raúl	Torres	Torres	raúl.torres@technomex.com.mx	4426743189	2023-01-25	2025-07-30 14:50:52.14116-07	t	\N	8
14	Sandra	Gutiérrez	Castillo	sandra.gutiérrez@technomex.com.mx	4427107486	2022-11-04	2025-07-30 14:50:52.142454-07	t	\N	9
15	Claudia	Martínez	Medina	claudia.martínez@technomex.com.mx	4427104993	2021-06-22	2025-07-30 14:50:52.144536-07	t	\N	9
16	Gabriela	Ruiz	Sánchez	gabriela.ruiz@technomex.com.mx	4425637167	2023-09-10	2025-07-30 14:50:52.145743-07	t	\N	9
17	Carlos	Cruz	González	carlos.cruz@technomex.com.mx	4429093480	2024-06-11	2025-07-30 14:50:52.14724-07	t	\N	10
18	Verónica	Pérez	Cruz	verónica.pérez@technomex.com.mx	4426898651	2021-09-19	2025-07-30 14:50:52.149889-07	t	\N	10
19	Juan Carlos	Rodríguez	Rivera	juan.carlos.rodríguez@technomex.com.mx	4426272792	2022-02-14	2025-07-30 14:50:52.151189-07	t	\N	10
20	Beatriz	Cruz	Rivera	beatriz.cruz@technomex.com.mx	4427935217	2022-04-06	2025-07-30 14:50:52.152455-07	t	\N	10
21	Verónica	González	Rodríguez	verónica.gonzález@technomex.com.mx	4422142344	2022-12-28	2025-07-30 14:50:52.153699-07	t	\N	11
22	Mónica	Rivera	Torres	mónica.rivera@technomex.com.mx	4423337122	2025-05-19	2025-07-30 14:50:52.15584-07	t	\N	12
23	Francisco	Gómez	López	francisco.gómez@technomex.com.mx	4429364542	2022-06-16	2025-07-30 14:50:52.158117-07	t	\N	12
24	Raúl	Hernández	Romero	raúl.hernández@technomex.com.mx	4428266316	2024-11-29	2025-07-30 14:50:52.159249-07	t	\N	13
25	Mónica	Martínez	Ortiz	mónica.martínez@technomex.com.mx	4423394094	2022-07-24	2025-07-30 14:50:52.161288-07	t	\N	13
26	José Luis	Cruz	Ortiz	josé.luis.cruz@technomex.com.mx	4424356195	2022-12-21	2025-07-30 14:50:52.162834-07	t	\N	14
27	José Luis	Vargas	Torres	josé.luis.vargas@technomex.com.mx	4429528790	2024-06-30	2025-07-30 14:50:52.165709-07	t	\N	15
28	Andrés	Pérez	Martínez	andrés.pérez@technomex.com.mx	4429441163	2023-03-10	2025-07-30 14:50:52.168269-07	t	\N	16
29	Alejandro	Vargas	González	alejandro.vargas@technomex.com.mx	4429160349	2025-06-29	2025-07-30 14:50:52.170525-07	t	\N	17
30	David	Rodríguez	Pérez	david.rodríguez@technomex.com.mx	4421541184	2020-10-15	2025-07-30 14:50:52.17273-07	t	\N	17
31	Mónica	Romero	González	mónica.romero@technomex.com.mx	4424273292	2023-12-09	2025-07-30 14:50:52.173869-07	t	\N	17
32	Verónica	Rodríguez	Ruiz	verónica.rodríguez@technomex.com.mx	4426295832	2025-02-09	2025-07-30 14:50:52.175096-07	t	\N	17
33	Verónica	Ruiz	García	verónica.ruiz@technomex.com.mx	4424267200	2022-05-07	2025-07-30 14:50:52.176205-07	t	\N	18
34	Verónica	López	Torres	verónica.lópez@technomex.com.mx	4426306690	2024-08-03	2025-07-30 14:50:52.178175-07	t	\N	19
35	Rosa María	Castillo	Ortiz	rosa.maría.castillo@technomex.com.mx	4425903355	2021-08-04	2025-07-30 14:50:52.180535-07	t	\N	19
36	Fernando	Cruz	Rivera	fernando.cruz@technomex.com.mx	4423964941	2022-05-15	2025-07-30 14:50:52.182049-07	t	\N	19
37	Ana Patricia	Torres	Herrera	ana.patricia.torres@technomex.com.mx	4427261075	2023-09-02	2025-07-30 14:50:52.183356-07	t	\N	19
38	Fernando	Medina	Ruiz	fernando.medina@technomex.com.mx	4421059759	2024-02-11	2025-07-30 14:50:52.184516-07	t	\N	19
39	Mónica	Sánchez	Herrera	mónica.sánchez@technomex.com.mx	4421066062	2024-07-30	2025-07-30 14:50:52.185637-07	t	\N	20
40	María Elena	Díaz	García	maría.elena.díaz@technomex.com.mx	4423864967	2022-02-25	2025-07-30 14:50:52.18789-07	t	\N	21
41	Daniel	Torres	Herrera	daniel.torres@technomex.com.mx	4423742853	2022-03-26	2025-07-30 14:50:52.190186-07	t	\N	22
42	José Luis	Ruiz	Martínez	josé.luis.ruiz@technomex.com.mx	4428958226	2023-06-08	2025-07-30 14:50:52.192277-07	t	\N	23
43	Silvia	Castillo	Ruiz	silvia.castillo@technomex.com.mx	4427440780	2022-01-21	2025-07-30 14:50:52.19429-07	t	\N	23
44	Carlos	Ramírez	Ruiz	carlos.ramírez@technomex.com.mx	4423342030	2024-09-24	2025-07-30 14:50:52.195458-07	t	\N	24
45	Miguel Ángel	Gutiérrez	Castillo	miguel.ángel.gutiérrez@technomex.com.mx	4421137074	2023-06-09	2025-07-30 14:50:52.198185-07	t	\N	25
46	Lucía	Díaz	García	lucía.díaz@technomex.com.mx	4429595671	2025-03-10	2025-07-30 14:50:52.200457-07	t	\N	26
47	Mónica	García	Flores	mónica.garcía@technomex.com.mx	4423021720	2024-02-19	2025-07-30 14:50:52.202545-07	t	\N	27
48	Carmen	Rodríguez	Gómez	carmen.rodríguez@technomex.com.mx	4424541208	2023-04-05	2025-07-30 14:50:52.204639-07	t	\N	27
49	Fernando	Torres	Martínez	fernando.torres@technomex.com.mx	4425841931	2022-10-28	2025-07-30 14:50:52.205768-07	t	\N	27
50	Daniel	Morales	Hernández	daniel.morales@technomex.com.mx	4428353325	2022-03-08	2025-07-30 14:50:52.206903-07	t	\N	27
51	Raúl	Flores	Gómez	raúl.flores@technomex.com.mx	4428329513	2023-02-02	2025-07-30 14:50:52.207978-07	t	\N	28
52	David	Sánchez	Romero	david.sánchez@technomex.com.mx	4421511247	2021-10-14	2025-07-30 14:50:52.20993-07	t	\N	29
53	Beatriz	Flores	González	beatriz.flores@technomex.com.mx	4428971516	2021-11-18	2025-07-30 14:50:52.211995-07	t	\N	30
54	David	Herrera	Pérez	david.herrera@technomex.com.mx	4421025756	2025-02-10	2025-07-30 14:50:52.214605-07	t	\N	31
55	Leticia	Sánchez	Vargas	leticia.sánchez@technomex.com.mx	4428254964	2022-11-29	2025-07-30 14:50:52.21692-07	t	\N	31
56	Sandra	Ruiz	Castillo	sandra.ruiz@technomex.com.mx	4423369090	2021-12-14	2025-07-30 14:50:52.218144-07	t	\N	31
57	Gabriela	Cruz	Ramírez	gabriela.cruz@technomex.com.mx	4424699156	2023-05-09	2025-07-30 14:50:52.219456-07	t	\N	32
58	José Luis	Medina	Díaz	josé.luis.medina@technomex.com.mx	4421720723	2023-02-20	2025-07-30 14:50:52.221528-07	t	\N	33
59	Alejandro	Ruiz	Rivera	alejandro.ruiz@technomex.com.mx	4421465238	2024-10-25	2025-07-30 14:50:52.223556-07	t	\N	34
60	Sandra	Herrera	Romero	sandra.herrera@technomex.com.mx	4421286418	2023-11-18	2025-07-30 14:50:52.225624-07	t	\N	35
61	Francisco	Hernández	Castillo	francisco.hernández@technomex.com.mx	4424904937	2023-07-09	2025-07-30 14:50:52.227647-07	t	\N	35
62	Beatriz	Rivera	Díaz	beatriz.rivera@technomex.com.mx	4429674947	2024-05-09	2025-07-30 14:50:52.228889-07	t	\N	35
63	Fernando	Flores	Castillo	fernando.flores@technomex.com.mx	4423986981	2021-09-17	2025-07-30 14:50:52.231399-07	t	\N	35
64	Sergio	Sánchez	Herrera	sergio.sánchez@technomex.com.mx	4428292995	2021-05-19	2025-07-30 14:50:52.232818-07	t	\N	36
65	Rosa María	García	Pérez	rosa.maría.garcía@technomex.com.mx	4422646477	2024-05-29	2025-07-30 14:50:52.235151-07	t	\N	36
66	Verónica	Medina	Morales	verónica.medina@technomex.com.mx	4426017876	2024-04-01	2025-07-30 14:50:52.236426-07	t	\N	37
67	Lucía	González	Rodríguez	lucía.gonzález@technomex.com.mx	4424174239	2023-07-14	2025-07-30 14:50:52.238553-07	t	\N	37
68	Leticia	Ortiz	Jiménez	leticia.ortiz@technomex.com.mx	4423821111	2023-09-05	2025-07-30 14:50:52.239757-07	t	\N	37
69	Eduardo	Díaz	Sánchez	eduardo.díaz@technomex.com.mx	4426007140	2025-02-13	2025-07-30 14:50:52.241012-07	t	\N	37
70	Lucía	Herrera	Romero	lucía.herrera@technomex.com.mx	4427254090	2021-07-14	2025-07-30 14:50:52.242251-07	t	\N	38
71	Silvia	Gómez	Martínez	silvia.gómez@technomex.com.mx	4421602851	2022-09-01	2025-07-30 14:50:52.24434-07	t	\N	39
72	Ricardo	Martínez	Ramírez	ricardo.martínez@technomex.com.mx	4425958113	2023-04-06	2025-07-30 14:50:52.246747-07	t	\N	39
73	Daniel	Pérez	Herrera	daniel.pérez@technomex.com.mx	4425335940	2023-12-29	2025-07-30 14:50:52.248354-07	t	\N	39
74	Juan Carlos	Vargas	Jiménez	juan.carlos.vargas@technomex.com.mx	4428439250	2023-02-17	2025-07-30 14:50:52.249816-07	t	\N	40
75	Claudia	González	Morales	claudia.gonzález@technomex.com.mx	4422295585	2021-06-29	2025-07-30 14:50:52.252169-07	t	\N	40
76	Rosa María	Cruz	Castillo	rosa.maría.cruz@technomex.com.mx	4423749605	2024-11-29	2025-07-30 14:50:52.253486-07	t	\N	40
77	Lucía	Cruz	González	lucía.cruz@technomex.com.mx	4426348563	2023-11-18	2025-07-30 14:50:52.254906-07	t	\N	41
78	Carmen	González	Ruiz	carmen.gonzález@technomex.com.mx	4426274984	2021-03-01	2025-07-30 14:50:52.256994-07	t	\N	42
79	Sandra	Rivera	García	sandra.rivera@technomex.com.mx	4423550832	2023-07-13	2025-07-30 14:50:52.259072-07	t	\N	43
80	José Luis	Díaz	Rivera	josé.luis.díaz@technomex.com.mx	4424514271	2020-12-16	2025-07-30 14:50:52.26114-07	t	\N	44
81	Fernando	Gómez	Ruiz	fernando.gómez@technomex.com.mx	4429690245	2022-05-10	2025-07-30 14:50:52.263754-07	t	\N	44
82	Sergio	Martínez	Ortiz	sergio.martínez@technomex.com.mx	4425184346	2024-12-13	2025-07-30 14:50:52.265763-07	t	\N	44
83	Adriana	Vargas	Rodríguez	adriana.vargas@technomex.com.mx	4428883690	2023-12-03	2025-07-30 14:50:52.267009-07	t	\N	45
84	Raúl	López	Torres	raúl.lópez@technomex.com.mx	4428021925	2022-07-04	2025-07-30 14:50:52.269144-07	t	\N	46
85	Leticia	Jiménez	Torres	leticia.jiménez@technomex.com.mx	4426354797	2021-11-30	2025-07-30 14:50:52.272084-07	t	\N	47
86	María Elena	Rivera	Torres	maría.elena.rivera@technomex.com.mx	4427075911	2020-10-18	2025-07-30 14:50:52.274198-07	t	\N	48
87	Fernando	Vargas	García	fernando.vargas@technomex.com.mx	4421979784	2023-02-17	2025-07-30 14:50:52.276218-07	t	\N	49
88	Mónica	Gómez	Romero	mónica.gómez@technomex.com.mx	4428175900	2024-12-23	2025-07-30 14:50:52.278261-07	t	\N	50
89	David	Ortiz	López	david.ortiz@technomex.com.mx	4424513677	2023-03-04	2025-07-30 14:50:52.280948-07	t	\N	51
90	Lucía	Rodríguez	Gómez	lucía.rodríguez@technomex.com.mx	4427481172	2020-09-24	2025-07-30 14:50:52.283425-07	t	\N	52
91	Juan Carlos	Gómez	Medina	juan.carlos.gómez@technomex.com.mx	4422837749	2024-03-20	2025-07-30 14:50:52.285485-07	t	\N	53
92	Silvia	López	Sánchez	silvia.lópez@technomex.com.mx	4424376610	2021-02-04	2025-07-30 14:50:52.287542-07	t	\N	54
93	María Elena	González	Jiménez	maría.elena.gonzález@technomex.com.mx	4426806536	2023-09-10	2025-07-30 14:50:52.290049-07	t	\N	54
94	María Elena	Ruiz	Pérez	maría.elena.ruiz@technomex.com.mx	4428889758	2024-11-09	2025-07-30 14:50:52.29118-07	t	\N	54
95	Carlos	Sánchez	Jiménez	carlos.sánchez@technomex.com.mx	4424370541	2025-05-08	2025-07-30 14:50:52.292365-07	t	\N	55
96	Verónica	Ortiz	Hernández	verónica.ortiz@technomex.com.mx	4423206762	2025-02-13	2025-07-30 14:50:52.294432-07	t	\N	56
97	Claudia	Ramírez	Herrera	claudia.ramírez@technomex.com.mx	4425352718	2021-07-13	2025-07-30 14:50:52.297093-07	t	\N	57
98	Francisco	Sánchez	Romero	francisco.sánchez@technomex.com.mx	4423010696	2021-03-18	2025-07-30 14:50:52.299524-07	t	\N	58
99	Adriana	Morales	Vargas	adriana.morales@technomex.com.mx	4425494179	2022-01-08	2025-07-30 14:50:52.301817-07	t	\N	58
100	Mónica	Rodríguez	Herrera	mónica.rodríguez@technomex.com.mx	4424739544	2024-11-23	2025-07-30 14:50:52.303057-07	t	\N	59
101	Ana Patricia	Rodríguez	Morales	ana.patricia.rodríguez@technomex.com.mx	4422781610	2021-08-25	2025-07-30 14:50:52.305172-07	t	\N	60
102	Roberto	Sánchez	Vargas	roberto.sánchez@technomex.com.mx	4429716984	2021-12-23	2025-07-30 14:50:52.307692-07	t	\N	62
103	Roberto	Rodríguez	González	roberto.rodríguez@technomex.com.mx	4425179113	2024-05-08	2025-07-30 14:50:52.3097-07	t	\N	62
104	Andrés	Hernández	Medina	andrés.hernández@technomex.com.mx	4422705687	2024-03-10	2025-07-30 14:50:52.310808-07	t	\N	62
105	Eduardo	Vargas	González	eduardo.vargas@technomex.com.mx	4422861999	2021-06-11	2025-07-30 14:50:52.312086-07	t	\N	62
106	Miguel Ángel	Gómez	Hernández	miguel.ángel.gómez@technomex.com.mx	4422055307	2025-05-14	2025-07-30 14:50:52.313955-07	t	\N	62
107	Fernando	García	Rivera	fernando.garcía@technomex.com.mx	4423278078	2021-03-23	2025-07-30 14:50:52.315609-07	t	\N	63
108	Miguel Ángel	Cruz	Gómez	miguel.ángel.cruz@technomex.com.mx	4424972179	2025-05-13	2025-07-30 14:50:52.317938-07	t	\N	63
109	Andrés	Flores	Ruiz	andrés.flores@technomex.com.mx	4426643355	2022-08-14	2025-07-30 14:50:52.319118-07	t	\N	63
110	Andrés	García	Hernández	andrés.garcía@technomex.com.mx	4422854086	2020-12-12	2025-07-30 14:50:52.320249-07	t	\N	64
111	Ana Patricia	García	Medina	ana.patricia.garcía@technomex.com.mx	4428679466	2024-08-25	2025-07-30 14:50:52.322408-07	t	\N	64
112	Alejandro	Flores	Ortiz	alejandro.flores@technomex.com.mx	4427228753	2024-02-09	2025-07-30 14:50:52.323601-07	t	\N	64
113	Leticia	Ramírez	Ramírez	leticia.ramírez@technomex.com.mx	4421077539	2024-10-18	2025-07-30 14:50:52.324927-07	t	\N	64
114	Carmen	Jiménez	Ruiz	carmen.jiménez@technomex.com.mx	4426869059	2020-11-16	2025-07-30 14:50:52.326016-07	t	\N	65
115	Patricia	Rivera	Pérez	patricia.rivera@technomex.com.mx	4428635235	2022-06-15	2025-07-30 14:50:52.328182-07	t	\N	66
116	José Luis	Martínez	García	josé.luis.martínez@technomex.com.mx	4422055936	2024-04-04	2025-07-30 14:50:52.330896-07	t	\N	66
117	Gabriela	Morales	Ruiz	gabriela.morales@technomex.com.mx	4425625533	2023-05-22	2025-07-30 14:50:52.332871-07	t	\N	66
118	Sergio	Rodríguez	Cruz	sergio.rodríguez@technomex.com.mx	4424151116	2023-09-15	2025-07-30 14:50:52.335184-07	t	\N	67
119	Carmen	Romero	Vargas	carmen.romero@technomex.com.mx	4429441791	2025-03-28	2025-07-30 14:50:52.337349-07	t	\N	67
120	Andrés	Rodríguez	González	andrés.rodríguez@technomex.com.mx	4424634101	2021-06-16	2025-07-30 14:50:52.338521-07	t	\N	68
121	Adriana	Hernández	Sánchez	adriana.hernández@technomex.com.mx	4428693735	2021-09-30	2025-07-30 14:50:52.340662-07	t	\N	69
122	Miguel Ángel	Castillo	Herrera	miguel.ángel.castillo@technomex.com.mx	4425802543	2024-12-22	2025-07-30 14:50:52.342852-07	t	\N	70
123	David	Pérez	Romero	david.pérez@technomex.com.mx	4428900502	2023-06-19	2025-07-30 14:50:52.345024-07	t	\N	71
124	Patricia	Castillo	García	patricia.castillo@technomex.com.mx	4429429208	2024-12-20	2025-07-30 14:50:52.347578-07	t	\N	71
125	Raúl	Ortiz	Medina	raúl.ortiz@technomex.com.mx	4426393863	2021-07-28	2025-07-30 14:50:52.348985-07	t	\N	71
126	Francisco	Cruz	Sánchez	francisco.cruz@technomex.com.mx	4425140898	2022-12-08	2025-07-30 14:50:52.350256-07	t	\N	72
127	Lucía	García	García	lucía.garcía@technomex.com.mx	4427673944	2025-06-16	2025-07-30 14:50:52.352375-07	t	\N	73
128	Gabriela	García	Medina	gabriela.garcía@technomex.com.mx	4428878689	2024-05-30	2025-07-30 14:50:52.354422-07	t	\N	73
129	Ana Patricia	Díaz	Rivera	ana.patricia.díaz@technomex.com.mx	4428239892	2024-03-11	2025-07-30 14:50:52.355592-07	t	\N	73
130	Patricia	Medina	Romero	patricia.medina@technomex.com.mx	4425592438	2024-06-08	2025-07-30 14:50:52.356767-07	t	\N	73
131	Lucía	Martínez	Romero	lucía.martínez@technomex.com.mx	4426322985	2023-10-11	2025-07-30 14:50:52.358375-07	t	\N	73
132	Daniel	Herrera	González	daniel.herrera@technomex.com.mx	4421814033	2023-04-15	2025-07-30 14:50:52.359503-07	t	\N	74
133	Juan Carlos	Torres	Castillo	juan.carlos.torres@technomex.com.mx	4425645807	2021-03-10	2025-07-30 14:50:52.361622-07	t	\N	75
134	Silvia	Ortiz	Vargas	silvia.ortiz@technomex.com.mx	4426246052	2024-10-17	2025-07-30 14:50:52.364074-07	t	\N	76
135	Gabriela	González	Ramírez	gabriela.gonzález@technomex.com.mx	4424247960	2025-06-23	2025-07-30 14:50:52.366962-07	t	\N	77
136	Juan Carlos	Hernández	Pérez	juan.carlos.hernández@technomex.com.mx	4427980587	2022-06-11	2025-07-30 14:50:52.369182-07	t	\N	78
137	Ricardo	Romero	Medina	ricardo.romero@technomex.com.mx	4421578522	2025-03-27	2025-07-30 14:50:52.371387-07	t	\N	79
138	Patricia	Gutiérrez	Morales	patricia.gutiérrez@technomex.com.mx	4424693503	2021-06-24	2025-07-30 14:50:52.374458-07	t	\N	81
\.


--
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empresas (empresa_id, nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, fecha_registro, status, administrador) FROM stdin;
1	TechnoMex Industries	TMI950815AB2	Blvd. Tecnológico #2000, Parque Industrial Norte, Querétaro, Qro. 76120	\N	contacto@technomex.com.mx	4421234567	2025-07-30 14:36:41.528404-07	t	1
3	axis	asdasdasdff3r4	wdfwsedfsdf	\N	axissssssss@gmail.com	5345345	2025-07-30 14:59:43.222745-07	t	4
\.


--
-- Data for Name: evaluaciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.evaluaciones (evaluacion_id, nombre, descripcion, instrucciones, tiempo_limite, umbral_aprobacion, status, fecha_registro, fecha_actualizacion, creado_por_id, empresa_id, tipo_evaluacion_id) FROM stdin;
\.


--
-- Data for Name: pagos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pagos (pago_id, costo, monto_pago, estado_pago, fecha_pago, fecha_vencimiento, transaccion_id, comprobante, usuario_id, suscripcion_id) FROM stdin;
1	499.00	499.00	Completado	2025-07-30 14:59:43.241072-07	\N	AUTO-3-20250730215943	\N	4	1
2	499.00	499.00	Completado	2025-07-30 15:15:16.008061-07	\N	SUB-2-20250730221516	\N	2	2
\.


--
-- Data for Name: planes_suscripcion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.planes_suscripcion (plan_id, nombre, descripcion, precio, duracion, limite_empleados, limite_plantas, caracteristicas, status, fecha_creacion) FROM stdin;
1	Básico	Plan básico para empresas nuevas	499.00	30	\N	\N	\N	t	2025-07-30 14:59:43.236672-07
2	Intermedio	Plan intermedio con mas opciones	600.00	60	\N	\N	\N	t	2025-07-30 15:23:37.679743-07
\.


--
-- Data for Name: plantas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.plantas (planta_id, nombre, direccion, fecha_registro, status, empresa) FROM stdin;
1	Planta Demo	Calle Industrial #456, Parque Industrial	2025-07-30 14:36:41.971232-07	t	1
2	Planta Querétaro Centro	Av. Constituyentes #850, Centro Histórico, Querétaro, Qro. 76000	2025-07-30 14:49:54.877616-07	t	1
3	Planta El Marqués	Carr. Querétaro-México Km. 45, El Marqués, Qro. 76240	2025-07-30 14:49:54.879835-07	t	1
4	Planta San Juan del Río	Zona Industrial La Noria, San Juan del Río, Qro. 76800	2025-07-30 14:49:54.881527-07	t	1
5	Planta Principal	wdfwsedfsdf	2025-07-30 14:59:43.223574-07	t	3
\.


--
-- Data for Name: posibles_respuestas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.posibles_respuestas (opcion_conjunto_id, texto_opcion, valor_booleano, valor_int, valor_decimal, numero_orden, conjunto_respuestas) FROM stdin;
\.


--
-- Data for Name: preguntas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.preguntas (pregunta_id, texto_pregunta, tipo_pregunta, es_obligatoria, activador_padre, pregunta_padre) FROM stdin;
\.


--
-- Data for Name: puestos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.puestos (puesto_id, nombre, descripcion, status, departamento) FROM stdin;
1	Director de RH	Dirección estratégica de recursos humanos	t	1
2	Gerente de RH	Gestión operativa de recursos humanos	t	1
3	Especialista en Reclutamiento	Reclutamiento y selección de personal	t	1
4	Analista de Nómina	Procesamiento de nómina y beneficios	t	1
5	Capacitador	Desarrollo y capacitación del personal	t	1
6	Gerente de Producción	Coordinación general de producción	t	2
7	Supervisor de Línea	Supervisión directa de líneas productivas	t	2
8	Operador de Máquina	Operación de maquinaria industrial	t	2
9	Técnico de Proceso	Optimización de procesos productivos	t	2
10	Inspector de Calidad	Control de calidad en línea	t	2
11	Jefe de Mantenimiento	Coordinación de mantenimiento general	t	3
12	Técnico Mecánico	Mantenimiento mecánico de equipos	t	3
13	Técnico Eléctrico	Mantenimiento eléctrico e instrumentación	t	3
14	Soldador	Trabajos de soldadura y reparación	t	3
15	Gerente de Calidad	Gestión del sistema de calidad	t	4
16	Auditor Interno	Auditorías internas de calidad	t	4
17	Técnico de Laboratorio	Análisis de laboratorio y pruebas	t	4
18	Jefe de Almacén	Coordinación de almacén y logística	t	5
19	Almacenista	Manejo de inventarios y materiales	t	5
20	Montacarguista	Operación de montacargas y equipo	t	5
21	Gerente Administrativo	Gestión administrativa general	t	6
22	Contador	Contabilidad y estados financieros	t	6
23	Auxiliar Contable	Apoyo en procesos contables	t	6
24	Recepcionista	Atención al público y recepción	t	6
25	Jefe de Sistemas	Coordinación de TI y automatización	t	7
26	Programador	Desarrollo de software y sistemas	t	7
27	Soporte Técnico	Soporte técnico a usuarios	t	7
28	Director de RH	Dirección estratégica de recursos humanos	t	8
29	Gerente de RH	Gestión operativa de recursos humanos	t	8
30	Especialista en Reclutamiento	Reclutamiento y selección de personal	t	8
31	Analista de Nómina	Procesamiento de nómina y beneficios	t	8
32	Capacitador	Desarrollo y capacitación del personal	t	8
33	Gerente de Producción	Coordinación general de producción	t	9
34	Supervisor de Línea	Supervisión directa de líneas productivas	t	9
35	Operador de Máquina	Operación de maquinaria industrial	t	9
36	Técnico de Proceso	Optimización de procesos productivos	t	9
37	Inspector de Calidad	Control de calidad en línea	t	9
38	Jefe de Mantenimiento	Coordinación de mantenimiento general	t	10
39	Técnico Mecánico	Mantenimiento mecánico de equipos	t	10
40	Técnico Eléctrico	Mantenimiento eléctrico e instrumentación	t	10
41	Soldador	Trabajos de soldadura y reparación	t	10
42	Gerente de Calidad	Gestión del sistema de calidad	t	11
43	Auditor Interno	Auditorías internas de calidad	t	11
44	Técnico de Laboratorio	Análisis de laboratorio y pruebas	t	11
45	Jefe de Almacén	Coordinación de almacén y logística	t	12
46	Almacenista	Manejo de inventarios y materiales	t	12
47	Montacarguista	Operación de montacargas y equipo	t	12
48	Gerente Administrativo	Gestión administrativa general	t	13
49	Contador	Contabilidad y estados financieros	t	13
50	Auxiliar Contable	Apoyo en procesos contables	t	13
51	Recepcionista	Atención al público y recepción	t	13
52	Jefe de Sistemas	Coordinación de TI y automatización	t	14
53	Programador	Desarrollo de software y sistemas	t	14
54	Soporte Técnico	Soporte técnico a usuarios	t	14
55	Director de RH	Dirección estratégica de recursos humanos	t	15
56	Gerente de RH	Gestión operativa de recursos humanos	t	15
57	Especialista en Reclutamiento	Reclutamiento y selección de personal	t	15
58	Analista de Nómina	Procesamiento de nómina y beneficios	t	15
59	Capacitador	Desarrollo y capacitación del personal	t	15
60	Gerente de Producción	Coordinación general de producción	t	16
61	Supervisor de Línea	Supervisión directa de líneas productivas	t	16
62	Operador de Máquina	Operación de maquinaria industrial	t	16
63	Técnico de Proceso	Optimización de procesos productivos	t	16
64	Inspector de Calidad	Control de calidad en línea	t	16
65	Jefe de Mantenimiento	Coordinación de mantenimiento general	t	17
66	Técnico Mecánico	Mantenimiento mecánico de equipos	t	17
67	Técnico Eléctrico	Mantenimiento eléctrico e instrumentación	t	17
68	Soldador	Trabajos de soldadura y reparación	t	17
69	Gerente de Calidad	Gestión del sistema de calidad	t	18
70	Auditor Interno	Auditorías internas de calidad	t	18
71	Técnico de Laboratorio	Análisis de laboratorio y pruebas	t	18
72	Jefe de Almacén	Coordinación de almacén y logística	t	19
73	Almacenista	Manejo de inventarios y materiales	t	19
74	Montacarguista	Operación de montacargas y equipo	t	19
75	Gerente Administrativo	Gestión administrativa general	t	20
76	Contador	Contabilidad y estados financieros	t	20
77	Auxiliar Contable	Apoyo en procesos contables	t	20
78	Recepcionista	Atención al público y recepción	t	20
79	Jefe de Sistemas	Coordinación de TI y automatización	t	21
80	Programador	Desarrollo de software y sistemas	t	21
81	Soporte Técnico	Soporte técnico a usuarios	t	21
82	Gerente General	\N	t	22
83	Asistente Administrativo	\N	t	22
84	Gerente de RRHH	\N	t	23
85	Especialista en Nómina	\N	t	23
86	Reclutador	\N	t	23
87	Contador	\N	t	24
88	Analista Financiero	\N	t	24
89	Supervisor de Producción	\N	t	25
90	Operador de Máquina	\N	t	25
91	Técnico de Proceso	\N	t	25
92	Inspector de Calidad	\N	t	26
93	Auditor Interno	\N	t	26
94	Técnico de Mantenimiento	\N	t	27
95	Electricista Industrial	\N	t	27
96	Coordinador de Almacén	\N	t	28
97	Montacarguista	\N	t	28
\.


--
-- Data for Name: respuestas_empleado; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.respuestas_empleado (respuesta_empleado_id, respuesta_texto, respuesta_valor_numerico, respuesta_valor_decimal, es_correcta, fecha_respuesta, asignacion_empleado_id, opcion_seleccionada_id, seccion_pregunta_id) FROM stdin;
\.


--
-- Data for Name: resultados_evaluacion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.resultados_evaluacion (resultado_id, puntaje_total, num_respuestas_correctas, num_preguntas_evaluables, porcentaje_correctas, fecha_calculo, aprobado, asignacion_empleado_id) FROM stdin;
\.


--
-- Data for Name: seccion_preguntas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.seccion_preguntas (seccion_pregunta_id, numero_orden, conjunto_respuestas_id, pregunta_id, respuesta_correcta_id, seccion_id) FROM stdin;
\.


--
-- Data for Name: secciones_eval; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.secciones_eval (seccion_id, nombre, descripcion, numero_orden, es_evaluable, evaluacion_id) FROM stdin;
\.


--
-- Data for Name: suscripciones_empresa; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.suscripciones_empresa (suscripcion_id, fecha_inicio, fecha_fin, estado, status, fecha_creacion, empresa_id, plan_id) FROM stdin;
1	2025-07-30	2025-08-29	Activa	t	2025-07-30 14:59:43.238146-07	3	1
2	2025-07-30	2025-08-29	Activa	t	2025-07-30 15:15:16.00523-07	1	1
\.


--
-- Data for Name: tipos_evaluacion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_evaluacion (tipo_evaluacion_id, nombre, descripcion) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id, nombre, apellido_paterno, apellido_materno, correo, fecha_registro, nivel_usuario, status, admin_empresa, user_id) FROM stdin;
1	Admin	Empresa	\N	admin@empresa.com	2025-07-30 14:36:41.52401-07	admin-empresa	t	\N	2
2	Admin	Planta	\N	admin@planta.com	2025-07-30 14:36:41.969727-07	admin-planta	t	\N	3
3	Super	Admin	\N	superadmin@axyoma.com	2025-07-30 14:41:15.508153-07	superadmin	t	\N	1
4	asdasd	asdasd	asda	axissssssss@gmail.com	2025-07-30 14:59:43.22181-07	admin-empresa	t	\N	4
\.


--
-- Name: admin_bd_configuracionbd_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_bd_configuracionbd_id_seq', 1, false);


--
-- Name: admin_bd_logrespaldo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_bd_logrespaldo_id_seq', 1, false);


--
-- Name: admin_plantas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_plantas_id_seq', 2, true);


--
-- Name: asignaciones_asignacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asignaciones_asignacion_id_seq', 1, false);


--
-- Name: asignaciones_empleado_asignacion_empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asignaciones_empleado_asignacion_empleado_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 192, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 4, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: conjunto_respuestas_conjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.conjunto_respuestas_conjunto_id_seq', 1, false);


--
-- Name: departamentos_departamento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departamentos_departamento_id_seq', 28, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 48, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 27, true);


--
-- Name: empleados_empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empleados_empleado_id_seq', 138, true);


--
-- Name: empresas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.empresas_empresa_id_seq', 3, true);


--
-- Name: evaluaciones_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.evaluaciones_evaluacion_id_seq', 1, false);


--
-- Name: pagos_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pagos_pago_id_seq', 2, true);


--
-- Name: planes_suscripcion_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.planes_suscripcion_plan_id_seq', 2, true);


--
-- Name: plantas_planta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.plantas_planta_id_seq', 5, true);


--
-- Name: posibles_respuestas_opcion_conjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.posibles_respuestas_opcion_conjunto_id_seq', 1, false);


--
-- Name: preguntas_pregunta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.preguntas_pregunta_id_seq', 1, false);


--
-- Name: puestos_puesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.puestos_puesto_id_seq', 97, true);


--
-- Name: respuestas_empleado_respuesta_empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.respuestas_empleado_respuesta_empleado_id_seq', 1, false);


--
-- Name: resultados_evaluacion_resultado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.resultados_evaluacion_resultado_id_seq', 1, false);


--
-- Name: seccion_preguntas_seccion_pregunta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.seccion_preguntas_seccion_pregunta_id_seq', 1, false);


--
-- Name: secciones_eval_seccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.secciones_eval_seccion_id_seq', 1, false);


--
-- Name: suscripciones_empresa_suscripcion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.suscripciones_empresa_suscripcion_id_seq', 2, true);


--
-- Name: tipos_evaluacion_tipo_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_evaluacion_tipo_evaluacion_id_seq', 1, false);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 4, true);


--
-- Name: admin_bd_configuracionbd admin_bd_configuracionbd_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_configuracionbd
    ADD CONSTRAINT admin_bd_configuracionbd_pkey PRIMARY KEY (id);


--
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_pkey PRIMARY KEY (id);


--
-- Name: admin_plantas admin_plantas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_pkey PRIMARY KEY (id);


--
-- Name: admin_plantas admin_plantas_usuario_id_planta_id_f206071a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_usuario_id_planta_id_f206071a_uniq UNIQUE (usuario_id, planta_id);


--
-- Name: asignaciones_empleado asignaciones_empleado_asignacion_id_empleado_id_2bd96fc9_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_empleado
    ADD CONSTRAINT asignaciones_empleado_asignacion_id_empleado_id_2bd96fc9_uniq UNIQUE (asignacion_id, empleado_id);


--
-- Name: asignaciones_empleado asignaciones_empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_empleado
    ADD CONSTRAINT asignaciones_empleado_pkey PRIMARY KEY (asignacion_empleado_id);


--
-- Name: asignaciones_empleado asignaciones_empleado_token_acceso_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_empleado
    ADD CONSTRAINT asignaciones_empleado_token_acceso_key UNIQUE (token_acceso);


--
-- Name: asignaciones asignaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones
    ADD CONSTRAINT asignaciones_pkey PRIMARY KEY (asignacion_id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: conjunto_respuestas conjunto_respuestas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conjunto_respuestas
    ADD CONSTRAINT conjunto_respuestas_nombre_key UNIQUE (nombre);


--
-- Name: conjunto_respuestas conjunto_respuestas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conjunto_respuestas
    ADD CONSTRAINT conjunto_respuestas_pkey PRIMARY KEY (conjunto_id);


--
-- Name: departamentos departamentos_nombre_planta_94271a14_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_nombre_planta_94271a14_uniq UNIQUE (nombre, planta);


--
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_pkey PRIMARY KEY (departamento_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: empleados empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_pkey PRIMARY KEY (empleado_id);


--
-- Name: empresas empresas_administrador_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_key UNIQUE (administrador);


--
-- Name: empresas empresas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nombre_key UNIQUE (nombre);


--
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (empresa_id);


--
-- Name: empresas empresas_rfc_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rfc_key UNIQUE (rfc);


--
-- Name: evaluaciones evaluaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT evaluaciones_pkey PRIMARY KEY (evaluacion_id);


--
-- Name: pagos pagos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_pkey PRIMARY KEY (pago_id);


--
-- Name: planes_suscripcion planes_suscripcion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.planes_suscripcion
    ADD CONSTRAINT planes_suscripcion_nombre_key UNIQUE (nombre);


--
-- Name: planes_suscripcion planes_suscripcion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.planes_suscripcion
    ADD CONSTRAINT planes_suscripcion_pkey PRIMARY KEY (plan_id);


--
-- Name: plantas plantas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plantas
    ADD CONSTRAINT plantas_pkey PRIMARY KEY (planta_id);


--
-- Name: posibles_respuestas posibles_respuestas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posibles_respuestas
    ADD CONSTRAINT posibles_respuestas_pkey PRIMARY KEY (opcion_conjunto_id);


--
-- Name: preguntas preguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT preguntas_pkey PRIMARY KEY (pregunta_id);


--
-- Name: puestos puestos_nombre_departamento_4c6581db_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos
    ADD CONSTRAINT puestos_nombre_departamento_4c6581db_uniq UNIQUE (nombre, departamento);


--
-- Name: puestos puestos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos
    ADD CONSTRAINT puestos_pkey PRIMARY KEY (puesto_id);


--
-- Name: respuestas_empleado respuestas_empleado_asignacion_empleado_id_s_c3e48c83_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleado
    ADD CONSTRAINT respuestas_empleado_asignacion_empleado_id_s_c3e48c83_uniq UNIQUE (asignacion_empleado_id, seccion_pregunta_id);


--
-- Name: respuestas_empleado respuestas_empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleado
    ADD CONSTRAINT respuestas_empleado_pkey PRIMARY KEY (respuesta_empleado_id);


--
-- Name: resultados_evaluacion resultados_evaluacion_asignacion_empleado_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_evaluacion
    ADD CONSTRAINT resultados_evaluacion_asignacion_empleado_id_key UNIQUE (asignacion_empleado_id);


--
-- Name: resultados_evaluacion resultados_evaluacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_evaluacion
    ADD CONSTRAINT resultados_evaluacion_pkey PRIMARY KEY (resultado_id);


--
-- Name: seccion_preguntas seccion_preguntas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_pkey PRIMARY KEY (seccion_pregunta_id);


--
-- Name: secciones_eval secciones_eval_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval
    ADD CONSTRAINT secciones_eval_pkey PRIMARY KEY (seccion_id);


--
-- Name: suscripciones_empresa suscripciones_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones_empresa
    ADD CONSTRAINT suscripciones_empresa_pkey PRIMARY KEY (suscripcion_id);


--
-- Name: tipos_evaluacion tipos_evaluacion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_evaluacion
    ADD CONSTRAINT tipos_evaluacion_nombre_key UNIQUE (nombre);


--
-- Name: tipos_evaluacion tipos_evaluacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_evaluacion
    ADD CONSTRAINT tipos_evaluacion_pkey PRIMARY KEY (tipo_evaluacion_id);


--
-- Name: posibles_respuestas unique_opcion_orden; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posibles_respuestas
    ADD CONSTRAINT unique_opcion_orden UNIQUE (conjunto_respuestas, numero_orden);


--
-- Name: seccion_preguntas unique_seccion_orden; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT unique_seccion_orden UNIQUE (seccion_id, numero_orden);


--
-- Name: seccion_preguntas unique_seccion_pregunta; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT unique_seccion_pregunta UNIQUE (seccion_id, pregunta_id);


--
-- Name: secciones_eval unique_section_orden; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval
    ADD CONSTRAINT unique_section_orden UNIQUE (evaluacion_id, numero_orden);


--
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_user_id_key UNIQUE (user_id);


--
-- Name: admin_bd_logrespaldo_empresa_id_61be407d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_bd_logrespaldo_empresa_id_61be407d ON public.admin_bd_logrespaldo USING btree (empresa_id);


--
-- Name: admin_bd_logrespaldo_usuario_id_17645f3a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_bd_logrespaldo_usuario_id_17645f3a ON public.admin_bd_logrespaldo USING btree (usuario_id);


--
-- Name: admin_plantas_planta_id_e107f2b3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_plantas_planta_id_e107f2b3 ON public.admin_plantas USING btree (planta_id);


--
-- Name: admin_plantas_usuario_id_370be9ba; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_plantas_usuario_id_370be9ba ON public.admin_plantas USING btree (usuario_id);


--
-- Name: asignaciones_empleado_asignacion_id_4d2e2a85; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_empleado_asignacion_id_4d2e2a85 ON public.asignaciones_empleado USING btree (asignacion_id);


--
-- Name: asignaciones_empleado_empleado_id_f10d9740; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_empleado_empleado_id_f10d9740 ON public.asignaciones_empleado USING btree (empleado_id);


--
-- Name: asignaciones_empleado_evaluado_id_6b1b750c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_empleado_evaluado_id_6b1b750c ON public.asignaciones USING btree (empleado_evaluado_id);


--
-- Name: asignaciones_evaluacion_id_8b3fa956; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX asignaciones_evaluacion_id_8b3fa956 ON public.asignaciones USING btree (evaluacion_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: conjunto_respuestas_nombre_1bddfe85_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX conjunto_respuestas_nombre_1bddfe85_like ON public.conjunto_respuestas USING btree (nombre varchar_pattern_ops);


--
-- Name: departamentos_planta_87b189b3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX departamentos_planta_87b189b3 ON public.departamentos USING btree (planta);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: empleados_empresa_id_17428638; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empleados_empresa_id_17428638 ON public.empleados USING btree (empresa_id);


--
-- Name: empleados_puesto_id_3b6f3d91; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empleados_puesto_id_3b6f3d91 ON public.empleados USING btree (puesto_id);


--
-- Name: empresas_nombre_5a4759a9_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empresas_nombre_5a4759a9_like ON public.empresas USING btree (nombre varchar_pattern_ops);


--
-- Name: empresas_rfc_6169650d_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX empresas_rfc_6169650d_like ON public.empresas USING btree (rfc varchar_pattern_ops);


--
-- Name: evaluaciones_creado_por_id_0c8f3e58; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluaciones_creado_por_id_0c8f3e58 ON public.evaluaciones USING btree (creado_por_id);


--
-- Name: evaluaciones_empresa_id_9402d5a5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluaciones_empresa_id_9402d5a5 ON public.evaluaciones USING btree (empresa_id);


--
-- Name: evaluaciones_tipo_evaluacion_id_70bc7bfe; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluaciones_tipo_evaluacion_id_70bc7bfe ON public.evaluaciones USING btree (tipo_evaluacion_id);


--
-- Name: pagos_suscripcion_id_99dc8463; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX pagos_suscripcion_id_99dc8463 ON public.pagos USING btree (suscripcion_id);


--
-- Name: pagos_usuario_id_eba921fa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX pagos_usuario_id_eba921fa ON public.pagos USING btree (usuario_id);


--
-- Name: planes_suscripcion_nombre_e2e7f579_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX planes_suscripcion_nombre_e2e7f579_like ON public.planes_suscripcion USING btree (nombre varchar_pattern_ops);


--
-- Name: plantas_empresa_28c08c98; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX plantas_empresa_28c08c98 ON public.plantas USING btree (empresa);


--
-- Name: posibles_respuestas_conjunto_respuestas_610d1979; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posibles_respuestas_conjunto_respuestas_610d1979 ON public.posibles_respuestas USING btree (conjunto_respuestas);


--
-- Name: preguntas_pregunta_padre_2d67e8ba; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX preguntas_pregunta_padre_2d67e8ba ON public.preguntas USING btree (pregunta_padre);


--
-- Name: puestos_departamento_f7a3d642; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX puestos_departamento_f7a3d642 ON public.puestos USING btree (departamento);


--
-- Name: respuestas_empleado_asignacion_empleado_id_d871f5df; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX respuestas_empleado_asignacion_empleado_id_d871f5df ON public.respuestas_empleado USING btree (asignacion_empleado_id);


--
-- Name: respuestas_empleado_opcion_seleccionada_id_549d0943; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX respuestas_empleado_opcion_seleccionada_id_549d0943 ON public.respuestas_empleado USING btree (opcion_seleccionada_id);


--
-- Name: respuestas_empleado_seccion_pregunta_id_8774b443; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX respuestas_empleado_seccion_pregunta_id_8774b443 ON public.respuestas_empleado USING btree (seccion_pregunta_id);


--
-- Name: seccion_preguntas_conjunto_respuestas_id_8736e887; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX seccion_preguntas_conjunto_respuestas_id_8736e887 ON public.seccion_preguntas USING btree (conjunto_respuestas_id);


--
-- Name: seccion_preguntas_pregunta_id_9ea6a022; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX seccion_preguntas_pregunta_id_9ea6a022 ON public.seccion_preguntas USING btree (pregunta_id);


--
-- Name: seccion_preguntas_respuesta_correcta_id_6bb7046d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX seccion_preguntas_respuesta_correcta_id_6bb7046d ON public.seccion_preguntas USING btree (respuesta_correcta_id);


--
-- Name: seccion_preguntas_seccion_id_d01463b5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX seccion_preguntas_seccion_id_d01463b5 ON public.seccion_preguntas USING btree (seccion_id);


--
-- Name: secciones_eval_evaluacion_id_9491cf53; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX secciones_eval_evaluacion_id_9491cf53 ON public.secciones_eval USING btree (evaluacion_id);


--
-- Name: suscripciones_empresa_empresa_id_c4b3c4fb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX suscripciones_empresa_empresa_id_c4b3c4fb ON public.suscripciones_empresa USING btree (empresa_id);


--
-- Name: suscripciones_empresa_plan_id_52beaa74; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX suscripciones_empresa_plan_id_52beaa74 ON public.suscripciones_empresa USING btree (plan_id);


--
-- Name: tipos_evaluacion_nombre_26ea7ca7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tipos_evaluacion_nombre_26ea7ca7_like ON public.tipos_evaluacion USING btree (nombre varchar_pattern_ops);


--
-- Name: usuarios_admin_empresa_42f4b2d2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_admin_empresa_42f4b2d2 ON public.usuarios USING btree (admin_empresa);


--
-- Name: usuarios_correo_02971567_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_correo_02971567_like ON public.usuarios USING btree (correo varchar_pattern_ops);


--
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_empresa_id_61be407d_fk_empresas_empresa_id FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: admin_bd_logrespaldo admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_bd_logrespaldo
    ADD CONSTRAINT admin_bd_logrespaldo_usuario_id_17645f3a_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: admin_plantas admin_plantas_planta_id_e107f2b3_fk_plantas_planta_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_planta_id_e107f2b3_fk_plantas_planta_id FOREIGN KEY (planta_id) REFERENCES public.plantas(planta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: admin_plantas admin_plantas_usuario_id_370be9ba_fk_usuarios_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_plantas
    ADD CONSTRAINT admin_plantas_usuario_id_370be9ba_fk_usuarios_id FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: asignaciones_empleado asignaciones_emplead_asignacion_id_4d2e2a85_fk_asignacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_empleado
    ADD CONSTRAINT asignaciones_emplead_asignacion_id_4d2e2a85_fk_asignacio FOREIGN KEY (asignacion_id) REFERENCES public.asignaciones(asignacion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: asignaciones_empleado asignaciones_emplead_empleado_id_f10d9740_fk_empleados; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones_empleado
    ADD CONSTRAINT asignaciones_emplead_empleado_id_f10d9740_fk_empleados FOREIGN KEY (empleado_id) REFERENCES public.empleados(empleado_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: asignaciones asignaciones_empleado_evaluado_id_6b1b750c_fk_empleados; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones
    ADD CONSTRAINT asignaciones_empleado_evaluado_id_6b1b750c_fk_empleados FOREIGN KEY (empleado_evaluado_id) REFERENCES public.empleados(empleado_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: asignaciones asignaciones_evaluacion_id_8b3fa956_fk_evaluacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asignaciones
    ADD CONSTRAINT asignaciones_evaluacion_id_8b3fa956_fk_evaluacio FOREIGN KEY (evaluacion_id) REFERENCES public.evaluaciones(evaluacion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: departamentos departamentos_planta_87b189b3_fk_plantas_planta_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_planta_87b189b3_fk_plantas_planta_id FOREIGN KEY (planta) REFERENCES public.plantas(planta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empleados empleados_empresa_id_17428638_fk_empresas_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_empresa_id_17428638_fk_empresas_empresa_id FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empleados empleados_puesto_id_3b6f3d91_fk_puestos_puesto_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_puesto_id_3b6f3d91_fk_puestos_puesto_id FOREIGN KEY (puesto_id) REFERENCES public.puestos(puesto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empresas empresas_administrador_82543b62_fk_usuarios_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_administrador_82543b62_fk_usuarios_id FOREIGN KEY (administrador) REFERENCES public.usuarios(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: evaluaciones evaluaciones_creado_por_id_0c8f3e58_fk_usuarios_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT evaluaciones_creado_por_id_0c8f3e58_fk_usuarios_id FOREIGN KEY (creado_por_id) REFERENCES public.usuarios(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: evaluaciones evaluaciones_empresa_id_9402d5a5_fk_empresas_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT evaluaciones_empresa_id_9402d5a5_fk_empresas_empresa_id FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: evaluaciones evaluaciones_tipo_evaluacion_id_70bc7bfe_fk_tipos_eva; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluaciones
    ADD CONSTRAINT evaluaciones_tipo_evaluacion_id_70bc7bfe_fk_tipos_eva FOREIGN KEY (tipo_evaluacion_id) REFERENCES public.tipos_evaluacion(tipo_evaluacion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pagos pagos_suscripcion_id_99dc8463_fk_suscripci; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_suscripcion_id_99dc8463_fk_suscripci FOREIGN KEY (suscripcion_id) REFERENCES public.suscripciones_empresa(suscripcion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pagos pagos_usuario_id_eba921fa_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_usuario_id_eba921fa_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plantas plantas_empresa_28c08c98_fk_empresas_empresa_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plantas
    ADD CONSTRAINT plantas_empresa_28c08c98_fk_empresas_empresa_id FOREIGN KEY (empresa) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: posibles_respuestas posibles_respuestas_conjunto_respuestas_610d1979_fk_conjunto_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.posibles_respuestas
    ADD CONSTRAINT posibles_respuestas_conjunto_respuestas_610d1979_fk_conjunto_ FOREIGN KEY (conjunto_respuestas) REFERENCES public.conjunto_respuestas(conjunto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: preguntas preguntas_pregunta_padre_2d67e8ba_fk_preguntas_pregunta_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.preguntas
    ADD CONSTRAINT preguntas_pregunta_padre_2d67e8ba_fk_preguntas_pregunta_id FOREIGN KEY (pregunta_padre) REFERENCES public.preguntas(pregunta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: puestos puestos_departamento_f7a3d642_fk_departamentos_departamento_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.puestos
    ADD CONSTRAINT puestos_departamento_f7a3d642_fk_departamentos_departamento_id FOREIGN KEY (departamento) REFERENCES public.departamentos(departamento_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: respuestas_empleado respuestas_empleado_asignacion_empleado__d871f5df_fk_asignacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleado
    ADD CONSTRAINT respuestas_empleado_asignacion_empleado__d871f5df_fk_asignacio FOREIGN KEY (asignacion_empleado_id) REFERENCES public.asignaciones_empleado(asignacion_empleado_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: respuestas_empleado respuestas_empleado_opcion_seleccionada__549d0943_fk_posibles_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleado
    ADD CONSTRAINT respuestas_empleado_opcion_seleccionada__549d0943_fk_posibles_ FOREIGN KEY (opcion_seleccionada_id) REFERENCES public.posibles_respuestas(opcion_conjunto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: respuestas_empleado respuestas_empleado_seccion_pregunta_id_8774b443_fk_seccion_p; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.respuestas_empleado
    ADD CONSTRAINT respuestas_empleado_seccion_pregunta_id_8774b443_fk_seccion_p FOREIGN KEY (seccion_pregunta_id) REFERENCES public.seccion_preguntas(seccion_pregunta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: resultados_evaluacion resultados_evaluacio_asignacion_empleado__8b357c01_fk_asignacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_evaluacion
    ADD CONSTRAINT resultados_evaluacio_asignacion_empleado__8b357c01_fk_asignacio FOREIGN KEY (asignacion_empleado_id) REFERENCES public.asignaciones_empleado(asignacion_empleado_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: seccion_preguntas seccion_preguntas_conjunto_respuestas__8736e887_fk_conjunto_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_conjunto_respuestas__8736e887_fk_conjunto_ FOREIGN KEY (conjunto_respuestas_id) REFERENCES public.conjunto_respuestas(conjunto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: seccion_preguntas seccion_preguntas_pregunta_id_9ea6a022_fk_preguntas_pregunta_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_pregunta_id_9ea6a022_fk_preguntas_pregunta_id FOREIGN KEY (pregunta_id) REFERENCES public.preguntas(pregunta_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: seccion_preguntas seccion_preguntas_respuesta_correcta_i_6bb7046d_fk_posibles_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_respuesta_correcta_i_6bb7046d_fk_posibles_ FOREIGN KEY (respuesta_correcta_id) REFERENCES public.posibles_respuestas(opcion_conjunto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: seccion_preguntas seccion_preguntas_seccion_id_d01463b5_fk_secciones; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seccion_preguntas
    ADD CONSTRAINT seccion_preguntas_seccion_id_d01463b5_fk_secciones FOREIGN KEY (seccion_id) REFERENCES public.secciones_eval(seccion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: secciones_eval secciones_eval_evaluacion_id_9491cf53_fk_evaluacio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.secciones_eval
    ADD CONSTRAINT secciones_eval_evaluacion_id_9491cf53_fk_evaluacio FOREIGN KEY (evaluacion_id) REFERENCES public.evaluaciones(evaluacion_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suscripciones_empresa suscripciones_empres_empresa_id_c4b3c4fb_fk_empresas_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones_empresa
    ADD CONSTRAINT suscripciones_empres_empresa_id_c4b3c4fb_fk_empresas_ FOREIGN KEY (empresa_id) REFERENCES public.empresas(empresa_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: suscripciones_empresa suscripciones_empres_plan_id_52beaa74_fk_planes_su; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suscripciones_empresa
    ADD CONSTRAINT suscripciones_empres_plan_id_52beaa74_fk_planes_su FOREIGN KEY (plan_id) REFERENCES public.planes_suscripcion(plan_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios usuarios_admin_empresa_42f4b2d2_fk_usuarios_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_admin_empresa_42f4b2d2_fk_usuarios_id FOREIGN KEY (admin_empresa) REFERENCES public.usuarios(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios usuarios_user_id_560ecfb6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_user_id_560ecfb6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

