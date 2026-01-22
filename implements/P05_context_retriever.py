import os
import yaml
from shared import get_cosine_sim, THRESHOLD_SIMILARITY


class ColumnDescription:
    table_name: str = None
    column_name: str = None
    column_description: str = None

    def __init__(self, table_name: str, column_name: str, column_description: str):
        self.table_name = table_name
        self.column_name = column_name
        self.column_description = column_description


class TableDescription:
    name: str = None
    description: str = None
    table_columns: list[ColumnDescription] = None

    def __init__(self,name: str, description: str, table_columns: list[ColumnDescription]):
        self.name = name
        self.description = description
        self.table_columns = table_columns

    @classmethod
    def from_data(cls, table_name: str, data: dict) -> "TableDescription":
        description = data['description']
        table_columns = []
        for col in data['columns']:
            table_columns.append(ColumnDescription(table_name, col['name'], col['description']))
        return cls(name=table_name, description=description, table_columns=table_columns)


# Đọc mô tả từ file
with open(os.path.join(os.path.dirname(__file__), "P05_metadata.yml")) as stream:
    try:
        metadata: dict = yaml.safe_load(stream)
        TABLE_DESCRIPTIONS: list[TableDescription] = []
        for table_name, data in metadata.items():
            table = TableDescription.from_data(table_name, data)
            TABLE_DESCRIPTIONS.append(table)
    except Exception as e:
        print(f"Lỗi đọc mô tả: {e}. Mô tả được mặc định về rỗng.")
        TABLE_DESCRIPTIONS: list[TableDescription] = []


def retrieve_context(question: str, k: int = 3) -> list[TableDescription]:
    """
    Truy vấn tương đồng mô tả bảng.
    
    :param question: Yêu cầu người dùng.
    :type question: str
    :param k: Giới hạn số lượng bảng được chọn.
    :type k: int
    :return: Danh sách đối tượng mô tả bảng theo thứ tự giảm dần tương đồng.
    :rtype: list[TableDescription]
    """
    
    table_descriptions_texts: list[str] = []
    for table in TABLE_DESCRIPTIONS:
        table_descriptions_texts.append(
            f"Tên bảng: {table.name}. Mô tả: {table.description}."
        )
        # for col in table.table_columns:
        #     table_descriptions_texts[-1] += f" Tên cột: {col.column_name}. Mô tả: {col.column_description}."

    selected_metadata = []
    
    cos_sims = get_cosine_sim(question, table_descriptions_texts)
    for item in cos_sims[:k]:
        if item['score'] > THRESHOLD_SIMILARITY:
            selected_metadata.append(
                TABLE_DESCRIPTIONS[item['old_idx']]
            )

    # ====== TODO: Thực hiện cài đặt dưới đây ======
    # Hàm hỗ trợ gọi tạo sinh LLM: chat_model.generate()
    # Hàm hỗ trợ gọi tạo sinh LLM có ràng buộc cấu trúc: chat_model.generate_structured()
    # Hàm hỗ trợ tạo embed câu hỏi: embed_model.generate_query_embeddings()
    # Hàm hỗ trợ tạo embed tài liệu: embed_model.generate_doc_embeddings()
    # Hàm hỗ trợ tính điểm cosine tương đồng: get_cosine_sim()
    
    # ====== README: Về mô tả bảng/cột ======
    # Mã nguồn đọc mô tả bảng/cột từ `implements\P05_metadata.yml`,
    # sau đó khởi tạo các đối tượng `TableDescription` tương ứng
    # phần lập trình sẽ xử lý trên `TableDescription`.

    # ====== Hết phần cài đặt ======
    
    assert isinstance(selected_metadata, list), "Kết quả trả về phải là list"
    
    return selected_metadata