import azure.functions as func
import json
from datetime import datetime
import os
import urllib.parse
import pg8000


def get_db_params_from_url(conn_str: str):
	parsed = urllib.parse.urlparse(conn_str)
	return {
		"host": parsed.hostname,
		"port": parsed.port or 5432,
		"user": parsed.username,
		"password": parsed.password,
		"database": parsed.path[1:] if parsed.path else "postgres",
	}


def ensure_memory_table(cursor) -> None:
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS chat_memory (
			id VARCHAR(36) PRIMARY KEY,
			tenant_id VARCHAR(255) NOT NULL,
			user_id VARCHAR(255) NOT NULL,
			session_id VARCHAR(255) NOT NULL,
			content TEXT NOT NULL,
			message_type VARCHAR(50) NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			metadata JSONB
		)
		"""
	)


def main(req: func.HttpRequest) -> func.HttpResponse:
	"""GET endpoint to retrieve chat memory from PostgreSQL using pg8000"""
	try:
		# Query parameters
		tenant_id = req.params.get("tenant_id")
		user_id = req.params.get("user_id")
		session_id = req.params.get("session_id")
		limit = int(req.params.get("limit", "100"))

		if not tenant_id:
			return func.HttpResponse(
				json.dumps({"status": "error", "message": "tenant_id is required"}),
				status_code=400,
				mimetype="application/json",
			)

		conn_str = os.environ.get("POSTGRES_CONNECTION")
		if not conn_str:
			return func.HttpResponse(
				json.dumps({"status": "error", "message": "POSTGRES_CONNECTION not set"}),
				status_code=500,
				mimetype="application/json",
			)

		params = get_db_params_from_url(conn_str)
		conn = pg8000.connect(**params)
		try:
			cursor = conn.cursor()
			# Ensure table exists so GET does not fail on fresh DB
			ensure_memory_table(cursor)

			query = (
				"SELECT id, tenant_id, user_id, session_id, content, message_type, created_at, metadata "
				"FROM chat_memory WHERE tenant_id = %s"
			)
			q_params = [tenant_id]
			if user_id:
				query += " AND user_id = %s"
				q_params.append(user_id)
			if session_id:
				query += " AND session_id = %s"
				q_params.append(session_id)
			query += " ORDER BY created_at DESC LIMIT %s"
			q_params.append(limit)

			cursor.execute(query, q_params)
			rows = cursor.fetchall()

			data = []
			for r in rows:
				data.append(
					{
						"id": r[0],
						"tenant_id": r[1],
						"user_id": r[2],
						"session_id": r[3],
						"content": r[4],
						"message_type": r[5],
						"created_at": (r[6].isoformat() if r[6] else None),
						"metadata": r[7] if r[7] else {},
					}
				)
		finally:
			try:
				cursor.close()
			except Exception:
				pass
			conn.close()

		return func.HttpResponse(
			json.dumps({"status": "success", "count": len(data), "data": data}),
			status_code=200,
			mimetype="application/json",
		)

	except Exception as e:
		return func.HttpResponse(
			json.dumps({
				"status": "error",
				"message": str(e),
				"timestamp": datetime.utcnow().isoformat(),
			}),
			status_code=500,
			mimetype="application/json",
		)
