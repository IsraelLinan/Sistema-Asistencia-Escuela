--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2026-04-09 20:52:51

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
-- TOC entry 218 (class 1259 OID 16720)
-- Name: docentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.docentes (
    id integer NOT NULL,
    nombre character varying(100),
    codigo_barras character varying(50)
);


ALTER TABLE public.docentes OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16719)
-- Name: docentes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.docentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.docentes_id_seq OWNER TO postgres;

--
-- TOC entry 4858 (class 0 OID 0)
-- Dependencies: 217
-- Name: docentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.docentes_id_seq OWNED BY public.docentes.id;


--
-- TOC entry 220 (class 1259 OID 16737)
-- Name: estudiantes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estudiantes (
    id integer NOT NULL,
    nombre character varying(100),
    codigo_barras character varying(50)
);


ALTER TABLE public.estudiantes OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16736)
-- Name: estudiantes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estudiantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estudiantes_id_seq OWNER TO postgres;

--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 219
-- Name: estudiantes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estudiantes_id_seq OWNED BY public.estudiantes.id;


--
-- TOC entry 222 (class 1259 OID 16746)
-- Name: ingresos_docentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingresos_docentes (
    id integer NOT NULL,
    docente_id integer,
    hora_ingreso timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    hora_salida timestamp without time zone
);


ALTER TABLE public.ingresos_docentes OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16745)
-- Name: ingresos_docentes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingresos_docentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingresos_docentes_id_seq OWNER TO postgres;

--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 221
-- Name: ingresos_docentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingresos_docentes_id_seq OWNED BY public.ingresos_docentes.id;


--
-- TOC entry 224 (class 1259 OID 16759)
-- Name: ingresos_estudiantes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingresos_estudiantes (
    id integer NOT NULL,
    estudiante_id integer,
    hora_ingreso timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    hora_salida timestamp without time zone
);


ALTER TABLE public.ingresos_estudiantes OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16758)
-- Name: ingresos_estudiantes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingresos_estudiantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingresos_estudiantes_id_seq OWNER TO postgres;

--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingresos_estudiantes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingresos_estudiantes_id_seq OWNED BY public.ingresos_estudiantes.id;


--
-- TOC entry 226 (class 1259 OID 16774)
-- Name: personas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.personas (
    id integer NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    codigo_barras character varying(255) NOT NULL,
    tipo_persona character varying(50) NOT NULL
);


ALTER TABLE public.personas OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16773)
-- Name: personas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.personas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.personas_id_seq OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 225
-- Name: personas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.personas_id_seq OWNED BY public.personas.id;


--
-- TOC entry 228 (class 1259 OID 16786)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16785)
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
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 227
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4666 (class 2604 OID 16723)
-- Name: docentes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes ALTER COLUMN id SET DEFAULT nextval('public.docentes_id_seq'::regclass);


--
-- TOC entry 4667 (class 2604 OID 16740)
-- Name: estudiantes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes ALTER COLUMN id SET DEFAULT nextval('public.estudiantes_id_seq'::regclass);


--
-- TOC entry 4668 (class 2604 OID 16749)
-- Name: ingresos_docentes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_docentes ALTER COLUMN id SET DEFAULT nextval('public.ingresos_docentes_id_seq'::regclass);


--
-- TOC entry 4670 (class 2604 OID 16762)
-- Name: ingresos_estudiantes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_estudiantes ALTER COLUMN id SET DEFAULT nextval('public.ingresos_estudiantes_id_seq'::regclass);


--
-- TOC entry 4672 (class 2604 OID 16777)
-- Name: personas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas ALTER COLUMN id SET DEFAULT nextval('public.personas_id_seq'::regclass);


--
-- TOC entry 4673 (class 2604 OID 16789)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 4842 (class 0 OID 16720)
-- Dependencies: 218
-- Data for Name: docentes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.docentes (id, nombre, codigo_barras) FROM stdin;
1	David Quispe	424512568
2	Pablo Quispe	41112aaa6ea97521aaaf044f4029ae55
3	Erlis Aquino	2a31f81c988efe06382261bc19209a18
4	FERNANDO MANTILLA	c483ab792c8bc1ac8d8285697fee9444
5	LINAN CARMONA ISRAEL ISAAC	bc2c30064fad13711e69cf8537aa3a6f
6	MAMANI QUISPE MARTIN	f421c4754c4e5cfc31b04aff94829d10
7	QUISPE CONDORI PABLO	824cb9fdb960e60427a7547ad9102d85
8	Merrill Tucker	22bddd92d2bb8a5f0f5283e65174a456
9	Susie Clarke	0edb60c94b9140d9a2a1deb1749dc66d
10	Camille Mccormick	63450c493fa80eeadcfa05432d8828ca
11	Sylvester Holder	b32c10be1c9b3c064e7bcd546d97a749
\.


--
-- TOC entry 4844 (class 0 OID 16737)
-- Dependencies: 220
-- Data for Name: estudiantes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estudiantes (id, nombre, codigo_barras) FROM stdin;
1	Israel Linan	424512567
2	Juan Pérez	424512569
3	Alba Bella Ferrari	7247946126e45d0cc2ebf14a24053686
4	ana maria carmona	11c0a2e96477177e5f63217f1e05d744
5	javier chavez montesinos	0b69860371a32a09403ecbce4fba2bfd
6	Alejandro Sulca Martinez	4738fb520b40018aeea768b407847f56
7	maria angelica quispe	0bba7bf973bdb721358c8f680009c23c
8	eduardo quispe	6f09092cf1a4bd1ddcef7dd7f9926b6f
9	CORONADO OCAMPO WILDER LATINO	6e89bb3f918f1e75b7256761213e423a
10	CARMONA MORALES LUIS ALBERTO	7a20005640a01f8d227bc21f8f75ec6f
11	LINAN CARMONA RUTH	5867ab0feec21546b3bc50d1aaf44da0
12	CHAVEZ MONTESINOS JAVIER	7811ee071283da1714300f94f4ff0fae
13	Linan Carmona Israel Isaac	8f6f3c1663c5e0a0ee63a10c007794e4
14	Palmer Duarte	f87fc5ebeb0ed2e13f16a58127ce711a
15	Rosalinda Trevino	6f0ae4b8687a9d081ada1b7f35897b78
16	Earle Newton	7b2899547715047a4bcdfe77ba8d1472
17	Mathew Mccoy	87b687810308cf15669acbfb022ad397
\.


--
-- TOC entry 4846 (class 0 OID 16746)
-- Dependencies: 222
-- Data for Name: ingresos_docentes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingresos_docentes (id, docente_id, hora_ingreso, hora_salida) FROM stdin;
1	1	2025-07-18 12:58:22.414302	\N
2	2	2025-07-23 18:42:37.404691	\N
3	4	2025-07-23 22:21:26.661593	\N
4	5	2025-09-09 02:29:37.978396	2025-09-09 02:32:51.031336
5	6	2025-09-10 17:35:21.145548	2025-09-10 17:36:03.930191
6	7	2025-09-10 17:47:57.097233	2025-09-10 17:48:20.44355
7	8	2026-02-24 11:32:02.119514	2026-02-24 11:39:55.311249
8	9	2026-02-24 11:32:08.864996	2026-02-24 11:40:01.936715
9	10	2026-02-24 11:32:16.790976	2026-02-24 11:40:08.926349
10	11	2026-02-24 11:32:24.824884	2026-02-24 11:40:16.649219
\.


--
-- TOC entry 4848 (class 0 OID 16759)
-- Dependencies: 224
-- Data for Name: ingresos_estudiantes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingresos_estudiantes (id, estudiante_id, hora_ingreso, hora_salida) FROM stdin;
1	1	2025-07-17 18:30:47.386562	\N
2	2	2025-07-20 23:18:12.467687	\N
3	3	2025-07-23 01:50:27.369219	\N
4	8	2025-07-26 14:49:45.297815	\N
5	9	2025-09-09 00:59:42.891211	\N
6	10	2025-09-10 02:08:15.953845	2025-09-10 02:11:44.659306
7	11	2025-09-10 17:33:23.081641	2025-09-10 17:34:15.093297
8	12	2025-09-10 17:49:32.369121	2025-09-10 17:49:49.29002
9	13	2026-02-24 00:45:19.381908	2026-02-24 00:58:04.045296
10	14	2026-02-24 11:31:05.958717	2026-02-24 11:38:48.199962
11	15	2026-02-24 11:31:16.432022	2026-02-24 11:38:56.887294
12	16	2026-02-24 11:31:24.727037	2026-02-24 11:39:04.439767
13	17	2026-02-24 11:31:35.991196	2026-02-24 11:39:11.656618
\.


--
-- TOC entry 4850 (class 0 OID 16774)
-- Dependencies: 226
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personas (id, nombre_completo, codigo_barras, tipo_persona) FROM stdin;
1	elias isaias linan carmona	71a5336ffbc8539e879362408274c5d8	Estudiante
2	julio cesar linan guiterrez	b3618da2ce65f324c99ee44d63232392	Docente
3	Alba Bella Ferrari	7247946126e45d0cc2ebf14a24053686	Estudiante
4	Pablo Quispe	41112aaa6ea97521aaaf044f4029ae55	Docente
5	ana maria carmona	11c0a2e96477177e5f63217f1e05d744	Estudiante
6	Erlis Aquino	2a31f81c988efe06382261bc19209a18	Docente
7	javier chavez montesinos	0b69860371a32a09403ecbce4fba2bfd	Estudiante
8	Alejandro Sulca Martinez	4738fb520b40018aeea768b407847f56	Estudiante
9	FERNANDO MANTILLA	c483ab792c8bc1ac8d8285697fee9444	Docente
10	maria angelica quispe	0bba7bf973bdb721358c8f680009c23c	Estudiante
11	eduardo quispe	6f09092cf1a4bd1ddcef7dd7f9926b6f	Estudiante
12	CORONADO OCAMPO WILDER LATINO	6e89bb3f918f1e75b7256761213e423a	Estudiante
13	LINAN CARMONA ISRAEL ISAAC	bc2c30064fad13711e69cf8537aa3a6f	Docente
14	CARMONA MORALES LUIS ALBERTO	7a20005640a01f8d227bc21f8f75ec6f	Estudiante
15	LINAN CARMONA RUTH	5867ab0feec21546b3bc50d1aaf44da0	Estudiante
16	MAMANI QUISPE MARTIN	f421c4754c4e5cfc31b04aff94829d10	Docente
17	QUISPE CONDORI PABLO	824cb9fdb960e60427a7547ad9102d85	Docente
18	CHAVEZ MONTESINOS JAVIER	7811ee071283da1714300f94f4ff0fae	Estudiante
19	Linan Carmona Israel Isaac	8f6f3c1663c5e0a0ee63a10c007794e4	Estudiante
20	Palmer Duarte	f87fc5ebeb0ed2e13f16a58127ce711a	Estudiante
21	Rosalinda Trevino	6f0ae4b8687a9d081ada1b7f35897b78	Estudiante
22	Earle Newton	7b2899547715047a4bcdfe77ba8d1472	Estudiante
23	Mathew Mccoy	87b687810308cf15669acbfb022ad397	Estudiante
24	Merrill Tucker	22bddd92d2bb8a5f0f5283e65174a456	Docente
25	Susie Clarke	0edb60c94b9140d9a2a1deb1749dc66d	Docente
26	Camille Mccormick	63450c493fa80eeadcfa05432d8828ca	Docente
27	Sylvester Holder	b32c10be1c9b3c064e7bcd546d97a749	Docente
\.


--
-- TOC entry 4852 (class 0 OID 16786)
-- Dependencies: 228
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, username, password) FROM stdin;
1	admin	123456
\.


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 217
-- Name: docentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.docentes_id_seq', 11, true);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 219
-- Name: estudiantes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estudiantes_id_seq', 17, true);


--
-- TOC entry 4866 (class 0 OID 0)
-- Dependencies: 221
-- Name: ingresos_docentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingresos_docentes_id_seq', 10, true);


--
-- TOC entry 4867 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingresos_estudiantes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingresos_estudiantes_id_seq', 13, true);


--
-- TOC entry 4868 (class 0 OID 0)
-- Dependencies: 225
-- Name: personas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.personas_id_seq', 27, true);


--
-- TOC entry 4869 (class 0 OID 0)
-- Dependencies: 227
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);


--
-- TOC entry 4675 (class 2606 OID 16727)
-- Name: docentes docentes_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 4677 (class 2606 OID 16725)
-- Name: docentes docentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_pkey PRIMARY KEY (id);


--
-- TOC entry 4679 (class 2606 OID 16744)
-- Name: estudiantes estudiantes_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes
    ADD CONSTRAINT estudiantes_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 4681 (class 2606 OID 16742)
-- Name: estudiantes estudiantes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudiantes
    ADD CONSTRAINT estudiantes_pkey PRIMARY KEY (id);


--
-- TOC entry 4683 (class 2606 OID 16752)
-- Name: ingresos_docentes ingresos_docentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_docentes
    ADD CONSTRAINT ingresos_docentes_pkey PRIMARY KEY (id);


--
-- TOC entry 4685 (class 2606 OID 16765)
-- Name: ingresos_estudiantes ingresos_estudiantes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_estudiantes
    ADD CONSTRAINT ingresos_estudiantes_pkey PRIMARY KEY (id);


--
-- TOC entry 4687 (class 2606 OID 16783)
-- Name: personas personas_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 4689 (class 2606 OID 16781)
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id);


--
-- TOC entry 4691 (class 2606 OID 16791)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4693 (class 2606 OID 16793)
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- TOC entry 4694 (class 2606 OID 16753)
-- Name: ingresos_docentes ingresos_docentes_docente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_docentes
    ADD CONSTRAINT ingresos_docentes_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES public.docentes(id);


--
-- TOC entry 4695 (class 2606 OID 16766)
-- Name: ingresos_estudiantes ingresos_estudiantes_estudiante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos_estudiantes
    ADD CONSTRAINT ingresos_estudiantes_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES public.estudiantes(id);


-- Completed on 2026-04-09 20:52:52

--
-- PostgreSQL database dump complete
--

