CREATE TABLE model (
   id SERIAL PRIMARY KEY,
   name      TEXT    not null,
   fieldType TEXT    not null,
   foot      TEXT   not null,
   path      TEXT    not null,
   isDaily   BOOLEAN not null DEFAULT false,
   timeFormat TEXT   not null DEFAULT '%Y%m%d_%H%M',
   timeRegex  TEXT   not null DEFAULT '.*?_(\d+_\d+)_.*'
);

CREATE TABLE colorscale (
   id SERIAL PRIMARY KEY,
   name       TEXT not null,
   domains    TEXT not null,
   palette    TEXT not null
);

CREATE TABLE field (
   name       TEXT  not null,
   alias      TEXT  not null,
   colorscale_id INTEGER references colorscale(id) ,
   model_id      INTEGER references model(id),
   PRIMARY KEY (model_id, name)
);

