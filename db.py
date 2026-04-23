import sqlite3
from src.validators import get_sql

def fetch_calculated_data(config):
    db_path = config.get('system', {}).get('db_path', 'data/project_details.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    dimensions = ["complete", "accuracy", "validity", "uniqueness", "timeliness", "consistent"]
    query_parts = []
    
    for key, cat in config['categories'].items():
        # Only include if toggle is true
        if cat.get('include') is not True:
            continue
        
        fields = cat.get('fields', {})
        if not fields:
            continue 
            
        dim_sql = []
        for dim in dimensions:
            if dim == "unique":
               
                primary = list(fields.keys())[0]
                dim_sql.append(f"(CAST(COUNT(DISTINCT {primary}) AS FLOAT) / COUNT(*)) * 100 as {dim}")
            else:
                snippets = [get_sql(dim, f, cfg) for f, cfg in fields.items()]
                
                combined = " + ".join(snippets)
                dim_sql.append(f"AVG(({combined}) / {len(snippets)}) * 100 as {dim}")

        table_name = cat.get('table', 'project_details')
        sql = f"SELECT '{cat['display_name']}' as row_name, COUNT(*) as qty, {', '.join(dim_sql)} FROM {table_name}"
        query_parts.append(sql)

    #If no categories are selected, return empty instead of executing bad SQL
    if not query_parts:
        return []

    # Join with UNION ALL and strip any accidental whitespace
    final_query = " UNION ALL ".join(query_parts).strip()
    
    try:
        cursor.execute(final_query)
        results = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {e}")
        print(f"Failed Query: {final_query}") #the exact syntax error
        results = []
    finally:
        conn.close()
        
    return results