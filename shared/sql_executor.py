import sqlite3
import pandas as pd
from typing import List
from shared.messages import ChatbotMessage

# Hàm thực thi SQL và trả về DataFrame
def execute_sql_to_df(sql: str, db_path: str) -> pd.DataFrame:
	"""
	Thực thi câu lệnh SQL và trả về kết quả dạng pandas DataFrame.
	:param sql: Chuỗi truy vấn SQL
	:param db_path: Đường dẫn file database SQLite
	:return: pandas.DataFrame
	"""
	conn = sqlite3.connect(db_path)
	try:
		df = pd.read_sql_query(sql, conn)
	finally:
		conn.close()
	return df

# Thành phần lưu lịch sử trò chuyện
class ChatHistory:
	def __init__(self, db_path: str, conversation_id: str):
		self.db_path = db_path
		self.conversation_id = conversation_id
		self._ensure_table()

	def _ensure_table(self):
		conn = sqlite3.connect(self.db_path)
		try:
			# Bảng lưu metadata của conversations
			conn.execute('''
				CREATE TABLE IF NOT EXISTS conversations (
					id TEXT PRIMARY KEY,
					title TEXT NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)
			''')
			# Bảng lưu messages
			conn.execute('''
				CREATE TABLE IF NOT EXISTS chat_history (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					conversation_id TEXT NOT NULL,
					msg_type TEXT NOT NULL,
					content TEXT NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					debug_info TEXT,
					FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
				)
			''')
			# Tạo index để tăng tốc query
			conn.execute('''
				CREATE INDEX IF NOT EXISTS idx_chat_history_conversation_id 
				ON chat_history(conversation_id)
			''')
			conn.commit()
		finally:
			conn.close()

	def add(self, message: ChatbotMessage):
		conn = sqlite3.connect(self.db_path)
		try:
			# Chuyển debug dict thành JSON string
			import json
			debug_str = json.dumps(message.debug, ensure_ascii=False) if message.debug else None
			
			conn.execute(
				'INSERT INTO chat_history (conversation_id, msg_type, content, debug_info) VALUES (?, ?, ?, ?)',
				(self.conversation_id, message.type.name, message.content, debug_str)
			)
			# Cập nhật updated_at của conversation
			conn.execute(
				'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
				(self.conversation_id,)
			)
			conn.commit()
		finally:
			conn.close()

	def get(self) -> List[ChatbotMessage]:
		conn = sqlite3.connect(self.db_path)
		try:
			rows = conn.execute(
				'SELECT msg_type, content, debug_info FROM chat_history WHERE conversation_id = ? ORDER BY id',
				(self.conversation_id,)
			).fetchall()
			messages = []
			from shared.messages import MESSAGE_TYPE
			import json
			for msg_type, content, debug_info in rows:
				debug_dict = json.loads(debug_info) if debug_info else {}
				messages.append(ChatbotMessage(type=MESSAGE_TYPE[msg_type], content=content, debug=debug_dict))
			return messages
		finally:
			conn.close()

	def clear(self):
		conn = sqlite3.connect(self.db_path)
		try:
			conn.execute(
				'DELETE FROM chat_history WHERE conversation_id = ?',
				(self.conversation_id,)
			)
			conn.commit()
		finally:
			conn.close()


	@staticmethod
	def _ensure_table_static(db_path: str):
		conn = sqlite3.connect(db_path)
		try:
			# Bảng lưu metadata của conversations
			conn.execute('''
				CREATE TABLE IF NOT EXISTS conversations (
					id TEXT PRIMARY KEY,
					title TEXT NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				)
			''')
			# Bảng lưu messages
			conn.execute('''
				CREATE TABLE IF NOT EXISTS chat_history (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					conversation_id TEXT NOT NULL,
					msg_type TEXT NOT NULL,
					content TEXT NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					debug_info TEXT,
					FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
				)
			''')
			# Tạo index để tăng tốc query
			conn.execute('''
				CREATE INDEX IF NOT EXISTS idx_chat_history_conversation_id 
				ON chat_history(conversation_id)
			''')
			conn.commit()
		finally:
			conn.close()

	@staticmethod
	def delete_conversation(db_path: str, conversation_id: str):
		ChatHistory._ensure_table_static(db_path)
		conn = sqlite3.connect(db_path)
		try:
			# Xóa conversation từ bảng conversations (messages sẽ tự động xóa nhờ CASCADE)
			conn.execute(
				'DELETE FROM conversations WHERE id = ?',
				(conversation_id,)
			)
			# Xóa messages (để chắc chắn nếu CASCADE không hoạt động)
			conn.execute(
				'DELETE FROM chat_history WHERE conversation_id = ?',
				(conversation_id,)
			)
			conn.commit()
		finally:
			conn.close()

	@staticmethod
	def create_conversation(db_path: str, conversation_id: str, title: str):
		"""Tạo một conversation mới với title"""
		ChatHistory._ensure_table_static(db_path)
		conn = sqlite3.connect(db_path)
		try:
			conn.execute(
				'INSERT INTO conversations (id, title) VALUES (?, ?)',
				(conversation_id, title)
			)
			conn.commit()
		finally:
			conn.close()

	@staticmethod
	def get_conversation_title(db_path: str, conversation_id: str) -> str:
		"""Lấy title của conversation"""
		ChatHistory._ensure_table_static(db_path)
		conn = sqlite3.connect(db_path)
		try:
			row = conn.execute(
				'SELECT title FROM conversations WHERE id = ?',
				(conversation_id,)
			).fetchone()
			return row[0] if row else None
		finally:
			conn.close()

	@staticmethod
	def update_conversation_title(db_path: str, conversation_id: str, new_title: str):
		"""Cập nhật title của conversation"""
		ChatHistory._ensure_table_static(db_path)
		conn = sqlite3.connect(db_path)
		try:
			conn.execute(
				'UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
				(new_title, conversation_id)
			)
			conn.commit()
		finally:
			conn.close()

	@staticmethod
	def list_conversations(db_path: str) -> List[str]:
		"""Lấy danh sách conversation IDs, sắp xếp theo updated_at giảm dần (mới nhất trước)"""
		ChatHistory._ensure_table_static(db_path)
		conn = sqlite3.connect(db_path)
		try:
			rows = conn.execute(
				'SELECT id FROM conversations ORDER BY updated_at DESC'
			).fetchall()
			return [row[0] for row in rows]
		finally:
			conn.close()