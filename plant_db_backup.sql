PGDMP     '    .    	            {           plant_db    14.6 (Homebrew)    15.2                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    24577    plant_db    DATABASE     j   CREATE DATABASE plant_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE plant_db;
                wbabich    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                wbabich    false                       0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   wbabich    false    4            �            1259    24579    plants    TABLE     �  CREATE TABLE public.plants (
    id integer NOT NULL,
    common_name text NOT NULL,
    scientific_name text NOT NULL,
    sunlight_care text,
    water_care text,
    temperature_care text,
    humidity_care text,
    growing_tips text,
    propagation_tips text,
    common_pests text,
    "timestamp" timestamp without time zone DEFAULT now(),
    family text,
    genus text,
    year integer,
    edible boolean,
    edible_part text,
    edible_notes text,
    medicinal boolean,
    medicinal_notes text,
    toxicity text,
    synonyms text,
    native_status text,
    conservation_status text,
    image_url character varying(255)
);
    DROP TABLE public.plants;
       public         heap    postgres    false    4            �            1259    24578    plants_id_seq    SEQUENCE     �   CREATE SEQUENCE public.plants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.plants_id_seq;
       public          postgres    false    4    210                       0    0    plants_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.plants_id_seq OWNED BY public.plants.id;
          public          postgres    false    209            |           2604    24582 	   plants id    DEFAULT     f   ALTER TABLE ONLY public.plants ALTER COLUMN id SET DEFAULT nextval('public.plants_id_seq'::regclass);
 8   ALTER TABLE public.plants ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    210    209    210                      0    24579    plants 
   TABLE DATA           P  COPY public.plants (id, common_name, scientific_name, sunlight_care, water_care, temperature_care, humidity_care, growing_tips, propagation_tips, common_pests, "timestamp", family, genus, year, edible, edible_part, edible_notes, medicinal, medicinal_notes, toxicity, synonyms, native_status, conservation_status, image_url) FROM stdin;
    public          postgres    false    210   $                  0    0    plants_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.plants_id_seq', 9, true);
          public          postgres    false    209                       2606    24586    plants plants_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.plants DROP CONSTRAINT plants_pkey;
       public            postgres    false    210               s  x���n�0��ާ�H�*��~�[)�*@���l2I�:vd;��S��d����"+�.UJ�x<���<�{&.�����X�u[���Z�����H�KK���z��U���@:�m/�q��oo�DG��Tm-s�{���r��59@���T;�T�
���i�aI�U�d��R�[�FaF��ԭ�������P���tG���K-=9���<��(�A���d9���y����L��b�����L��q�\'J�nKʛ@
׺!�}�(���^�Q��ޜ�'�d���c��vL/,dt�T�[��cI�pF��ȯF36��h_Aކ<PZ����hd,y����~By��;�	��@5^M�Y����R��s�9�E�5�C�1�F�����'����'jȚZN�Fm{��'j�x3��5h�z.�?aè��[�ʔ%�����w�8Bu�JW.D������ �W#�g�����n4:���-#�`VIԸ�����e��(Y�����t�� �Pڱg2k��ѽ3�-�p�$#����	q�����/�-�*G,�ŮU�VA��҇��^S�U$h��������w:[�>��_��z� ����d�u>     