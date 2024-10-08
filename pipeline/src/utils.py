import logging
from datetime import datetime


def log_pipeline_run(conn, run_type, status, source_name="api_data"):
    """Log the pipeline run details to the database."""
    pipeline_log = {
        "run_type": run_type,
        "source_name": source_name,
        "status": status,
        "created_timestamp": datetime.now(),
    }

    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO pipeline_logs (run_type, source_name, status, created_timestamp)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    pipeline_log["run_type"],
                    pipeline_log["source_name"],
                    pipeline_log["status"],
                    pipeline_log["created_timestamp"],
                ),
            )

        conn.commit()
    except Exception as e:
        logging.error(f"Error logging pipeline run: {e}")
        conn.rollback()
