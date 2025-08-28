import azure.functions as func
import json
from datetime import datetime
import os
import urllib.parse
import pg8000
import ssl


def get_db_params_from_url(conn_str: str):
	parsed = urllib.parse.urlparse(conn_str)
	username = urllib.parse.unquote(parsed.username) if parsed.username else None
	password = urllib.parse.unquote(parsed.password) if parsed.password else None
	return {
		"host": parsed.hostname,
		"port": parsed.port or 5432,
		"user": username,
		"password": password,
		"database": parsed.path[1:] if parsed.path else "postgres",
		"ssl_context": ssl.create_default_context(),
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
	"""POST endpoint to save chat memory to PostgreSQL using pg8000"""
	try:
		# Parse request body
		req_body = req.get_json()

		# Validate required fields
		required_fields = ["tenant_id", "user_id", "session_id", "content"]
		for field in required_fields:
			if field not in req_body:
				return func.HttpResponse(
					json.dumps({
						"status": "error",
						"message": f"Missing required field: {field}"
					}),
					status_code=400,
					mimetype="application/json",
				)

		# Connection string from app settings
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

			# Ensure table exists
			ensure_memory_table(cursor)

			# Prepare insert
			memory_id = req_body.get("id") or req_body.get("uuid") or __import__("uuid").uuid4().hex
			message_type = req_body.get("message_type", "chat")
			metadata = req_body.get("metadata") or {}

			cursor.execute(
				"""
				INSERT INTO chat_memory (
					id, tenant_id, user_id, session_id, content, message_type, created_at, metadata
				) VALUES (
					%s, %s, %s, %s, %s, %s, %s, %s::jsonb
				)
				""",
				[
					memory_id,
					req_body["tenant_id"],
					req_body["user_id"],
					req_body["session_id"],
					req_body["content"],
					message_type,
					datetime.utcnow(),
					json.dumps(metadata),
				],
			)
			conn.commit()
		finally:
			try:
				cursor.close()
			except Exception:
				pass
			conn.close()

		response = {
			"status": "success",
			"message": "Memory saved successfully",
			"data": {
				"id": memory_id,
				"tenant_id": req_body["tenant_id"],
				"user_id": req_body["user_id"],
				"session_id": req_body["session_id"],
				"content": req_body["content"],
				"message_type": message_type,
				"created_at": datetime.utcnow().isoformat(),
				"metadata": metadata,
			},
		}

		return func.HttpResponse(
			json.dumps(response), status_code=201, mimetype="application/json"
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
