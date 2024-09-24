-- Adminer 4.8.1 PostgreSQL 16.4 (Debian 16.4-1.pgdg120+1) dump

\connect "loopai";

DROP TABLE IF EXISTS "loop";
DROP SEQUENCE IF EXISTS loop_id_seq;
CREATE SEQUENCE loop_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 2 CACHE 1;

CREATE TABLE "public"."loop" (
    "id" integer DEFAULT nextval('loop_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "name" character varying(80) NOT NULL,
    "yaml_file_name" character varying(120) NOT NULL,
    "py_file_name" character varying(120) NOT NULL,
    "env" character varying(120) NOT NULL,
    "project_id" integer NOT NULL,
    CONSTRAINT "loop_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

TRUNCATE "loop";
INSERT INTO "loop" ("id", "user_id", "name", "yaml_file_name", "py_file_name", "env", "project_id") VALUES
(1,	1,	'test_loop',	'test_loop.yaml',	'test_loop.py',	'loop_food.env',	1);

DROP TABLE IF EXISTS "product";
DROP SEQUENCE IF EXISTS product_id_seq;
CREATE SEQUENCE product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."product" (
    "id" integer DEFAULT nextval('product_id_seq') NOT NULL,
    "name" character varying(80) NOT NULL,
    "price" double precision NOT NULL,
    CONSTRAINT "product_name_key" UNIQUE ("name"),
    CONSTRAINT "product_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

TRUNCATE "product";

DROP TABLE IF EXISTS "project";
DROP SEQUENCE IF EXISTS project_id_seq;
CREATE SEQUENCE project_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."project" (
    "id" integer DEFAULT nextval('project_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "name" character varying(80) NOT NULL,
    "url" character varying(200),
    "login" character varying(80),
    "password" character varying(120),
    "api_key" character varying(120),
    CONSTRAINT "project_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

TRUNCATE "project";
INSERT INTO "project" ("id", "user_id", "name", "url", "login", "password", "api_key") VALUES
(1,	1,	'test_project',	'http://localhost',	'login',	'password',	NULL);

ALTER TABLE ONLY "public"."loop" ADD CONSTRAINT "loop_project_id_fkey" FOREIGN KEY (project_id) REFERENCES project(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."loop" ADD CONSTRAINT "loop_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."project" ADD CONSTRAINT "project_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) NOT DEFERRABLE;

-- 2024-09-24 09:35:36.878635+00