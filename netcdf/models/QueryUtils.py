import os
import json, psycopg2
import psycopg2.extras
import traceback
from flask import jsonify

conn = None
def getConn():
    global conn 
    if (conn is None or conn.closed > 0):
        conn = psycopg2.connect("host=db dbname=aerosol user=postgres")

    return conn

def getModelInstance(modelName, dtg, varname=None, level=None):
    #if defined in lib meta with a path, then we can use the existing model classes
    print(modelName, dtg, varname, level)
    nw = None
    res = {'ncfile' : None }
    cur = None
    path = ""

    try:
        cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
        SELECT p.path,p.name,p.alias, p.time_regex, p.time_format, pf.alias field_alias, pf.varname,
               cs.name color_name, cs.id color_id, cs.domains,
               cs.palette, lvl.level, lvl.id lvlid, p.isDaily
        FROM products_colorscale cs,
		     products_field pf , 
		     products_level lvl,
		     products_product p
        WHERE p.id = pf.model_id
		AND p.name = '%s'
		AND lvl.color_scale_id = cs.id

        """ % (modelName)
        if varname is not None:
            query += "AND pf.varname ='" + varname + "' "

        if level is not None:
            print("get model with level")
            query += " AND lvl.id = %s;" % level
            cur.execute(query)

        else:
            print("get model no level")
            query += ";"
            cur.execute(query)

        #print(query)
        c = cur.fetchall()
        if c is not None and len(c) > 0:
           rec = c[0]
           path = rec['path']
           if path is not None:
               res = rec
               res['dtg'] = dtg
               dir_out = ""
               filepath = res['path']
               if('isdaily' in res and  res['isdaily'] == True):
                   dir_out = filepath.replace('dtg', dtg[:6])
                   dir_out += dtg[6:8] + "/"

               else:
                   dir_out = filepath.replace('dtg', dtg[:6])

               res['dir_out'] = dir_out
               res['ncfile']  = getProductFile(res['dir_out'], dtg)
               res['varname']  = varname

        cur.close()
    except:
        print("Model %s Not Found at %s" % (modelName, path))
        print(query)
        if cur is not None:
           cur.close()
        pass;

    return res

def getColors(): 
  cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute( """
   SELECT cs.*
     FROM products_colorscale cs
  """)

  res = cur.fetchall()
  cur.close()
  return {'colors' : res}

def getProducts(filterStr=None, filterType=None): 

  pfilter = ""
  if filterStr is not None:
    pfilter = "AND varname like '%%" + filterStr.lower() + "%%' "

  cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  query = """
    SELECT p.id, p.name, p.alias, json_agg(sub) fields
      FROM products_product p,
     (Select pf.model_id, pf.varname, pf.alias, json_agg(pl) as levels, pf.options
        from products_field pf, 
    	   (SELECT pl2.id as plid, pl2.field_id as fid, pl2.level, cs.id as color_id
    		  FROM products_level pl2, 
    	           products_colorscale cs
    		 WHERE cs.id  = pl2.color_scale_id		
    		) pl
         where pf.id = pl.fid
    """

  query += pfilter
  query += """
    	GROUP BY  pf.model_id, pf.varname, pf.alias, pf.options ORDER BY pf.alias
     ) sub
      WHERE sub.model_id = p.id
   """ 
  query +=  "GROUP BY p.id, p.name,p.alias ORDER BY p.alias;"

  #print(query)
  cur.execute(query, pfilter)
  res = cur.fetchall()
  cur.close()

  return jsonify(res)

def getProductFile(dir_out, dtg):
    ncfile = "" 
    try:
       for file in os.listdir(dir_out):
           if dtg[:8] in file:
              if file.endswith(".nc") and dtg[:8] in file:
                  ncfile = file
                  break;
    except Exception as e:
        print("File Not Found %s %s" % (dir_out, dtg[:8])) 
        print(e)

    return (dir_out +  ncfile);

def removeColorbar(cid):
  cur = getConn().cursor()
  try:
      query = """
              DELETE FROM products_colorscale
               WHERE id = %s;
            """
      cur.execute(query, (cid,))
      getConn().commit()

  except Exception as e:
    print(e) 
    pass

  cur.close()

def assignColorbar(cid, plid):
  cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  try:
      query = """
                UPDATE products_level
                  SET color_scale_id = %s
                WHERE id = %s
              """

     # print(query)
      cur.execute(query, (cid, plid))
  except Exception as e:
    print(e) 
    pass

  cur.close()

def updateColor(colorId, name, domains=None, palette=None, maxc=None):
  cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cid = -1
  try:

      query = """
                UPDATE products_colorscale
                  SET domains = %s,
                      palette = %s,
                      name = %s
                  WHERE id = %s;
              """

      if 'new' in str(colorId):
          query = "INSERT into products_colorscale(id, name,  domains, palette) values (DEFAULT, %s, %s, %s) RETURNING id;"

      domains = ",".join(domains)
      palette  = ",".join(palette)

     # print(query)
      
      if 'new' in str(colorId):
          cur.execute(query, (name, domains, palette))
          cid = cur.fetchone()['id']

      else:
          cur.execute(query, (domains, palette, name, colorId))

      print(query)
      print(name,domains,palette)
  except Exception as e:
    print(e) 
    print(traceback.format_exc())
    pass

  cur.close()
  return cid 

def saveMap(mapId, props):
  cur = getConn().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  try:
      query = "INSERT into products_maps(mapId, props) value(%s,%s) ON CONFLICT DO UPDATE"
      #print(query, mapId, props)
      cur.execute(query)
         # cid = cur.fetchone()[0]
  except Exception as e:
    print(e) 
    pass

  cur.close()

