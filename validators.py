
def get_sql(dimension, field, rule_cfg):
    
    
    if dimension == "complete":
        return f"CASE WHEN {field} IS NOT NULL AND {field} != '' THEN 1.0 ELSE 0 END"

    if dimension == "accuracy":
        if "list" in rule_cfg:
            vals = ", ".join([f"'{v}'" for v in rule_cfg['list']])
            return f"CASE WHEN {field} IN ({vals}) THEN 1.0 ELSE 0 END"
        return "1.0"

    if dimension == "validity":
        if "val" in rule_cfg:
            limit = rule_cfg['val']
                # Rule: Must be > 10. We use COALESCE to handle NULLs safely as 0.
            return f"CASE WHEN COALESCE(CAST({field} AS FLOAT), 0) > {limit} THEN 1.0 ELSE 0 END"
        

    if dimension == "unique":
        #in db.py
        return "1.0"

    if dimension == "timeliness":
        if rule_cfg.get("rule") == "greater_than_or_equal":
            return f"CASE WHEN {field} >= {rule_cfg['compare_to']} THEN 1.0 ELSE 0 END"
        return "1.0"

    if dimension == "consistent":
        if rule_cfg.get("rule") == "consistency_inactive":
            return f"CASE WHEN status = 'Inactive' AND CAST({field} AS FLOAT) <= {rule_cfg['max_inactive']} THEN 1.0 ELSE 0 END"
        return "1.0"
    
    return "1.0"