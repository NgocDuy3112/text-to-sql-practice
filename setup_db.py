import sqlite3
import os

def run_sql_script(db_path, sql_path):
	with open(sql_path, 'r', encoding='utf-8') as f:
		sql_script = f.read()
	# Loại bỏ các dòng bắt đầu bằng -- (comment)
	sql_script = '\n'.join(line for line in sql_script.splitlines() if not line.strip().startswith('--'))
	# Tách các câu lệnh SQL bằng dấu chấm phẩy
	statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
	conn = sqlite3.connect(db_path)
	try:
		cur = conn.cursor()
		for stmt in statements:
			cur.execute(stmt)
		conn.commit()
		print(f"Đã chạy xong script {sql_path} trên database {db_path}")
	finally:
		conn.close()

if __name__ == "__main__":
	db_path = os.path.join(os.path.dirname(__file__), "db", "demo.db")
	sql_path = os.path.join(os.path.dirname(__file__), "db", "setup_demo.sql")
	run_sql_script(db_path, sql_path)
