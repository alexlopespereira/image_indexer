--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.5

-- Started on 2016-12-27 06:19:18 PST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
-- SET row_security = off;

--
-- TOC entry 11 (class 2615 OID 32607)
-- Name: indice_imagens; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA indice_imagens;


SET search_path = indice_imagens, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 217 (class 1259 OID 34306)
-- Name: tb_imagem; Type: TABLE; Schema: indice_imagens; Owner: -
--

CREATE TABLE tb_imagem (
    co_seq_imagem integer NOT NULL,
    qt_banda integer,
    dt_coleta timestamp without time zone,
    nu_tamanho_pixel_x double precision,
    nu_tamanho_pixel_y double precision,
    no_unidade_celula_xy character varying(20),
    nu_near_range double precision,
    nu_far_range double precision,
    nu_angulo_near double precision,
    nu_angulo_far double precision,
    no_direcao_orbita character varying(20),
    no_lado_imageamento character varying(20),
    qt_looks integer,
    no_datum text,
    no_projecao text,
    qt_bits integer,
    no_id_cena character varying(50),
    no_id_orbita character varying(50),
    no_modo_imageamento character varying(100),
    tp_produto character varying(100),
    tp_extensao_arquivo character varying(5),
    dt_indexacao timestamp without time zone,
    no_caminho_arquivo character varying(800),
    qt_colunas integer,
    qt_linhas integer,
    no_caminho_metadados character varying(250),
    st_hh boolean,
    st_hv boolean,
    st_vv boolean,
    st_vh boolean,
    st_arquivado boolean,
    co_plataforma integer NOT NULL,
    co_sensor integer NOT NULL,
    geom public.geometry(Polygon,4674),
    ds_srs text,
    no_caminho_world character varying(250),
    nu_area_km2 double precision,
    co_servidor integer NOT NULL
);


--
-- TOC entry 189 (class 1259 OID 32610)
-- Name: tb_plataforma; Type: TABLE; Schema: indice_imagens; Owner: -
--

CREATE TABLE tb_plataforma (
    co_seq_plataforma integer NOT NULL,
    no_plataforma character varying(15) NOT NULL,
    ds_plataforma character varying(100),
    no_posicao character varying(16) NOT NULL
);


--
-- TOC entry 191 (class 1259 OID 32616)
-- Name: tb_sensor; Type: TABLE; Schema: indice_imagens; Owner: -
--

CREATE TABLE tb_sensor (
    co_seq_sensor integer NOT NULL,
    no_sensor character varying(15) NOT NULL,
    no_faixa_espectral character varying(10) NOT NULL
);


--
-- TOC entry 194 (class 1259 OID 32652)
-- Name: tb_servidor; Type: TABLE; Schema: indice_imagens; Owner: -
--

CREATE TABLE tb_servidor (
    co_seq_servidor integer NOT NULL,
    no_ip character(16) NOT NULL,
    no_usuario_processamento character varying(50) NOT NULL,
    no_diretorio_raiz_indice character varying(250) NOT NULL,
    no_os character varying(200) NOT NULL,
    co_centro_administrativo integer NOT NULL
);


--
-- TOC entry 192 (class 1259 OID 32635)
-- Name: rl_plataforma_sensor; Type: TABLE; Schema: indice_imagens; Owner: -
--

CREATE TABLE rl_plataforma_sensor (
    co_plataforma integer NOT NULL,
    co_sensor integer NOT NULL,
    dt_inicio date,
    dt_fim date
);


--
-- TOC entry 216 (class 1259 OID 34304)
-- Name: tb_imagem_co_seq_imagem_seq; Type: SEQUENCE; Schema: indice_imagens; Owner: -
--

CREATE SEQUENCE tb_imagem_co_seq_imagem_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5755 (class 0 OID 0)
-- Dependencies: 216
-- Name: tb_imagem_co_seq_imagem_seq; Type: SEQUENCE OWNED BY; Schema: indice_imagens; Owner: -
--

ALTER SEQUENCE tb_imagem_co_seq_imagem_seq OWNED BY tb_imagem.co_seq_imagem;


--
-- TOC entry 188 (class 1259 OID 32608)
-- Name: tb_plataforma_co_seq_plataforma_seq; Type: SEQUENCE; Schema: indice_imagens; Owner: -
--

CREATE SEQUENCE tb_plataforma_co_seq_plataforma_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5756 (class 0 OID 0)
-- Dependencies: 188
-- Name: tb_plataforma_co_seq_plataforma_seq; Type: SEQUENCE OWNED BY; Schema: indice_imagens; Owner: -
--

ALTER SEQUENCE tb_plataforma_co_seq_plataforma_seq OWNED BY tb_plataforma.co_seq_plataforma;


--
-- TOC entry 190 (class 1259 OID 32614)
-- Name: tb_sensor_co_seq_sensor_seq; Type: SEQUENCE; Schema: indice_imagens; Owner: -
--

CREATE SEQUENCE tb_sensor_co_seq_sensor_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5757 (class 0 OID 0)
-- Dependencies: 190
-- Name: tb_sensor_co_seq_sensor_seq; Type: SEQUENCE OWNED BY; Schema: indice_imagens; Owner: -
--

ALTER SEQUENCE tb_sensor_co_seq_sensor_seq OWNED BY tb_sensor.co_seq_sensor;


--
-- TOC entry 193 (class 1259 OID 32650)
-- Name: tb_servidor_co_seq_servidor_seq; Type: SEQUENCE; Schema: indice_imagens; Owner: -
--

CREATE SEQUENCE tb_servidor_co_seq_servidor_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5758 (class 0 OID 0)
-- Dependencies: 193
-- Name: tb_servidor_co_seq_servidor_seq; Type: SEQUENCE OWNED BY; Schema: indice_imagens; Owner: -
--

ALTER SEQUENCE tb_servidor_co_seq_servidor_seq OWNED BY tb_servidor.co_seq_servidor;


--
-- TOC entry 596 (class 1259 OID 946096)
-- Name: vw_indice_imagens; Type: VIEW; Schema: indice_imagens; Owner: -
--

CREATE VIEW vw_indice_imagens AS
 SELECT i.co_seq_imagem,
    p.co_seq_plataforma,
    p.no_plataforma,
    p.ds_plataforma,
    p.no_posicao,
    s.co_seq_sensor,
    s.no_sensor,
    s.no_faixa_espectral,
    i.qt_banda,
    i.dt_coleta,
    i.nu_tamanho_pixel_x,
    i.nu_tamanho_pixel_y,
    i.no_unidade_celula_xy,
    i.nu_near_range,
    i.nu_far_range,
    i.nu_angulo_near,
    i.nu_angulo_far,
    i.no_direcao_orbita,
    i.no_lado_imageamento,
    i.qt_looks,
    i.no_datum,
    i.no_projecao,
    i.qt_bits,
    i.no_id_cena,
    i.no_id_orbita,
    i.no_modo_imageamento,
    i.tp_produto,
    i.tp_extensao_arquivo,
    i.dt_indexacao,
    i.no_caminho_arquivo,
    i.qt_colunas,
    i.qt_linhas,
    i.no_caminho_metadados,
    i.st_hh,
    i.st_hv,
    i.st_vv,
    i.st_vh,
    i.st_arquivado,
    i.geom,
    i.ds_srs,
    i.no_caminho_world,
    i.nu_area_km2,
    (('\\'::text || (srv.no_ip)::text) || replace((i.no_caminho_arquivo)::text, '/'::text, '\'::text)) AS no_caminho_windows,
    (('smb://'::text || (srv.no_ip)::text) || (i.no_caminho_arquivo)::text) AS no_caminho_linux
   FROM (((tb_imagem i
     JOIN tb_plataforma p ON ((i.co_plataforma = p.co_seq_plataforma)))
     JOIN tb_sensor s ON ((i.co_sensor = s.co_seq_sensor)))
     JOIN tb_servidor srv ON ((i.co_servidor = srv.co_seq_servidor)));


--
-- TOC entry 5592 (class 2604 OID 34309)
-- Name: co_seq_imagem; Type: DEFAULT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_imagem ALTER COLUMN co_seq_imagem SET DEFAULT nextval('tb_imagem_co_seq_imagem_seq'::regclass);


--
-- TOC entry 5589 (class 2604 OID 32613)
-- Name: co_seq_plataforma; Type: DEFAULT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_plataforma ALTER COLUMN co_seq_plataforma SET DEFAULT nextval('tb_plataforma_co_seq_plataforma_seq'::regclass);


--
-- TOC entry 5590 (class 2604 OID 32619)
-- Name: co_seq_sensor; Type: DEFAULT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_sensor ALTER COLUMN co_seq_sensor SET DEFAULT nextval('tb_sensor_co_seq_sensor_seq'::regclass);


--
-- TOC entry 5591 (class 2604 OID 32655)
-- Name: co_seq_servidor; Type: DEFAULT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_servidor ALTER COLUMN co_seq_servidor SET DEFAULT nextval('tb_servidor_co_seq_servidor_seq'::regclass);


--
-- TOC entry 5605 (class 2606 OID 34314)
-- Name: pk_imagem; Type: CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_imagem
    ADD CONSTRAINT pk_imagem PRIMARY KEY (co_seq_imagem);


--
-- TOC entry 5594 (class 2606 OID 32621)
-- Name: pk_plataforma; Type: CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_plataforma
    ADD CONSTRAINT pk_plataforma PRIMARY KEY (co_seq_plataforma);


--
-- TOC entry 5598 (class 2606 OID 32639)
-- Name: pk_rl_plataforma_sensor; Type: CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY rl_plataforma_sensor
    ADD CONSTRAINT pk_rl_plataforma_sensor PRIMARY KEY (co_plataforma, co_sensor);


--
-- TOC entry 5596 (class 2606 OID 32623)
-- Name: pk_sensor; Type: CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_sensor
    ADD CONSTRAINT pk_sensor PRIMARY KEY (co_seq_sensor);


--
-- TOC entry 5600 (class 2606 OID 32657)
-- Name: pk_servidor; Type: CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_servidor
    ADD CONSTRAINT pk_servidor PRIMARY KEY (co_seq_servidor);


--
-- TOC entry 5601 (class 1259 OID 965211)
-- Name: idx_imagens_geom; Type: INDEX; Schema: indice_imagens; Owner: -
--

CREATE INDEX idx_imagens_geom ON tb_imagem USING gist (geom);


--
-- TOC entry 5602 (class 1259 OID 965213)
-- Name: idx_imagens_geom2; Type: INDEX; Schema: indice_imagens; Owner: -
--

CREATE INDEX idx_imagens_geom2 ON tb_imagem USING gist (public.st_centroid(geom));


--
-- TOC entry 5603 (class 1259 OID 965212)
-- Name: idx_imagens_pk; Type: INDEX; Schema: indice_imagens; Owner: -
--

CREATE UNIQUE INDEX idx_imagens_pk ON tb_imagem USING btree (co_seq_imagem);


--
-- TOC entry 5608 (class 2606 OID 34315)
-- Name: fk_rel_plataforma_sensor_imagem; Type: FK CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_imagem
    ADD CONSTRAINT fk_rel_plataforma_sensor_imagem FOREIGN KEY (co_plataforma, co_sensor) REFERENCES rl_plataforma_sensor(co_plataforma, co_sensor);


--
-- TOC entry 5606 (class 2606 OID 32640)
-- Name: fk_rl_plataforma_sensor_plataforma; Type: FK CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY rl_plataforma_sensor
    ADD CONSTRAINT fk_rl_plataforma_sensor_plataforma FOREIGN KEY (co_plataforma) REFERENCES tb_plataforma(co_seq_plataforma);


--
-- TOC entry 5607 (class 2606 OID 32645)
-- Name: fk_rl_plataforma_sensor_sensor; Type: FK CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY rl_plataforma_sensor
    ADD CONSTRAINT fk_rl_plataforma_sensor_sensor FOREIGN KEY (co_sensor) REFERENCES tb_sensor(co_seq_sensor);


--
-- TOC entry 5609 (class 2606 OID 946116)
-- Name: fk_servidor_imagem; Type: FK CONSTRAINT; Schema: indice_imagens; Owner: -
--

ALTER TABLE ONLY tb_imagem
    ADD CONSTRAINT fk_servidor_imagem FOREIGN KEY (co_servidor) REFERENCES tb_servidor(co_seq_servidor);


-- Completed on 2016-12-27 06:19:30 PST

--
-- PostgreSQL database dump complete
--

