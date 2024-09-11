CREATE TABLE public.movies (
	id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	title varchar NOT NULL,
	overview varchar NOT NULL,
	"year" int NOT NULL,
	rating float4 NOT NULL,
	category varchar NOT NULL,
	CONSTRAINT movies_pk PRIMARY KEY (id)
);
