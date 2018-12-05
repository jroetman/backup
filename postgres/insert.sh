psql -c "truncate products_colorscale CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_product CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_field CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_level CASCADE" --user=postgres --db=aerosol
psql -c "truncate products_leveltype CASCADE " --user=postgres --db=aerosol
psql -c "truncate products_field_levels" --user=postgres --db=aerosol

psql -c "\copy products_colorscale(id,name,domains,palette) FROM 'colors.csv' delimiter '|'  csv" --user=postgres --db=aerosol

psql -c "\copy products_product(id,name, alias, fieldtype, isdaily, path, foot,  time_format, time_regex) FROM 'products.csv' delimiter '|'  csv header" --user=postgres --db=aerosol

psql -c "\copy products_leveltype(id,type_id, name, description) FROM 'level_types.csv' delimiter '|' csv header " --user=postgres --db=aerosol

psql -c "\copy products_field(id,varname,alias,model_id) FROM 'fields.csv' delimiter '|'  csv header" --user=postgres --db=aerosol

psql -c "\copy products_level(color_scale_id,level_type_id, id, level, display_name) FROM 'levels.csv' delimiter '|'  csv header" --user=postgres --db=aerosol

psql -c "\copy products_field_levels(field_id,level_id) FROM 'field_levels.csv' delimiter '|'  csv header" --user=postgres --db=aerosol



