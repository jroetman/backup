psql -c "truncate products_colorscale CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_product CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_field CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_level CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_leveltype CASCADE " --user=postgres --db=aerosol
psql -c "truncate products_leveltypelevels" --user=postgres --db=aerosol

psql -c "\copy products_colorscale(name,domains,palette) FROM 'colors.csv' delimiter '|'  csv" --user=postgres --db=aerosol

psql -c "\copy products_product(id,name, alias, fieldtype, isdaily, path, foot,  time_format, time_regex) FROM 'products.csv' delimiter '|'  csv header" --user=postgres --db=aerosol

psql -c "\copy products_leveltype(id,level_type_id, name, description) FROM 'level_types.csv' delimiter '|' csv header " --user=postgres --db=aerosol

psql -c "\copy products_field(varname,alias,model_id, options, level_type_id) 
               FROM 'fields.csv' WITH QUOTE '$' delimiter '|'  csv header" --user=postgres --db=aerosol

#psql -c "\copy products_level(id,color_scale_id,level_type_id,level, display_name) FROM 'levels.csv' delimiter '|'  csv header" --user=postgres --db=aerosol

psql -c "\copy products_leveltypelevels(level_type_id,level) FROM 'level_types_levels.csv' delimiter '|'  csv header" --user=postgres --db=aerosol


psql -U "postgres" -d "aerosol"  -c  "insert into products_level(field_id, color_scale_id, level_type_id, level, display_name)
                                      select  f.id, cs.id, lt.id, ltl.level, ltl.level
                                       from products_field f,
                                            products_leveltypelevels ltl,
                                            products_leveltype lt,
                                      	    products_colorscale cs
                                      where ltl.level_type_id = lt.id
                                        and f.level_type_id  = lt.id
                                        and cs.name = concat(f.varname, ' ', ltl.level)
                                      "

