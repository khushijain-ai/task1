import statistics

def get_color(score, thresholds):
    if score >= thresholds['high']: return "green"
    if score >= thresholds['medium']: return "yellow"
    return "red"

def run_calculation_engine(sql_results, config):
    table_rows = []
    global_scores = []
    thresholds = config['thresholds']
    
    for row in sql_results:
        metrics = {}
        for dim in ["complete", "accuracy", "validity", "uniqueness", "timeliness", "consistent"]:
            metrics[dim] = {
                "value": round(row[dim]),
                "color": get_color(row[dim], thresholds)
            }
        
        row_avg = statistics.mean([m['value'] for m in metrics.values()])
        global_scores.append(row_avg)

        table_rows.append({
            "row": row['row_name'],
            "metrics": metrics,
            "average": round(row_avg),
            "include": True,
            "qty": row['qty']
        })

    return {
        "header": {
            "data_quality_confidence": round(statistics.mean(global_scores)) if global_scores else 0,
            "projects_selected": f"{len(global_scores)}/8",
            "prediction_confidence": 90,
            "trend": -4
        },
        "rows": table_rows
    }