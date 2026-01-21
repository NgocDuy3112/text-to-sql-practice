# Thực hành chatbot

> Hiện nội dung thực hành được chuẩn bị đến phần **P03: Router - Phân định luồng xử lý**.

## Yêu cầu

- Python >= 3.10
- Ollama

## Mô hình Ollama sử dụng trong demo

Chạy lệnh `ollama pull model-id` với các model ID bên dưới:

- gemma3:1b
- bge-m3

## Cấu trúc thư mục

- `/db`: Chứa file `.sql` khởi tạo CSDL mẫu và file lưu trữ CSDL `.db` sau khi được khởi tạo.
- `/implements`: Thư mục chứa các file nội dung thực hành cần triển khai.
- `/implements_ref`: Thư mục chứa phần lập trình tham khảo tương ứng với từng nội dung thực hành.
- `/shared`: Thư mục chứa các phần lập trình dùng chung được cài đặt sẵn.
- `/test`: Thư mục chứa các file script để kiểm thử từng phần nội dung lập trình.
- `app.py`: Script khởi chạy giao diện chatbot hoàn chỉnh khi đã hoàn thiện pipeline.
- `setup_db.py`: Script khởi chạy CSDL mẫu.
- `mo-ta-thuc-hanh.png`: Ảnh mô tả pipeline vận hành của chatbot và các nội dung thực hành đơn lập. Các nội dung *xanh lá* là các nội dung *lập trình*, các nội dung *màu vàng* là các nội dung *prompt engineering*.

## Cài đặt thực hành

### 1. Tạo môi trường ảo python venv

```bash
# Khởi tạo môi trường ảo
python -m venv .venv

# Truy cập vào môi trường ảo
.venv/Scripts/Activate.ps1

# Để thoát môi trường ảo, chạy lệnh
# deactivate
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 3. Khởi tạo CSDL mẫu

```bash
python setup_db.py
```

Khi này, bộ CSDL với dữ liệu mẫu đã được tạo tại `/db/demo.db`.

**Schema của CSDL mẫu:**

```sql
-- =========================
-- TABLE: hoc_vien
-- =========================
CREATE TABLE hoc_vien (
    id TEXT PRIMARY KEY,
    ten TEXT NOT NULL,
    nam_sinh INTEGER,
    so_dien_thoai TEXT,
    email TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- =========================
-- TABLE: chuong_trinh
-- =========================
CREATE TABLE chuong_trinh (
    id TEXT PRIMARY KEY,
    ten TEXT NOT NULL,
    tong_so_gio INTEGER,
    hoc_phi INTEGER,
    ghi_chu TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- =========================
-- TABLE: lop_hoc
-- =========================
CREATE TABLE lop_hoc (
    id TEXT PRIMARY KEY,
    ten_lop TEXT NOT NULL,
    chuong_trinh_id TEXT NOT NULL,
    thoi_gian_hoc TEXT,
    dia_diem_hoc TEXT,
    thoi_gian_bat_dau DATE,
    thoi_gian_ket_thuc DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_lop_chuong_trinh FOREIGN KEY (chuong_trinh_id) REFERENCES chuong_trinh(id)
);

-- =========================
-- TABLE: giang_vien
-- =========================
CREATE TABLE giang_vien (
    id TEXT PRIMARY KEY,
    ten TEXT NOT NULL,
    so_dien_thoai TEXT,
    email TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- =========================
-- TABLE: dang_ky_lop
-- =========================
CREATE TABLE dang_ky_lop (
    id TEXT PRIMARY KEY,
    hoc_vien_id TEXT NOT NULL,
    lop_hoc_id TEXT NOT NULL,
    trang_thai TEXT NOT NULL CHECK (trang_thai IN ('dang_hoc', 'hoan_tat', 'huy')),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_dk_hoc_vien FOREIGN KEY (hoc_vien_id) REFERENCES hoc_vien(id),
    CONSTRAINT fk_dk_lop_hoc FOREIGN KEY (lop_hoc_id) REFERENCES lop_hoc(id)
);

-- =========================
-- TABLE: giang_vien_phu_trach
-- =========================
CREATE TABLE giang_vien_phu_trach (
    id TEXT PRIMARY KEY,
    giang_vien_id TEXT NOT NULL,
    lop_hoc_id TEXT NOT NULL,
    vai_tro TEXT NOT NULL CHECK (vai_tro IN ('giang_day_chinh', 'tro_giang', 'thuc_hanh')),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_pc_giang_vien FOREIGN KEY (giang_vien_id) REFERENCES giang_vien(id),
    CONSTRAINT fk_pc_lop_hoc FOREIGN KEY (lop_hoc_id) REFERENCES lop_hoc(id)
);

-- =========================
-- TABLE: diem_cuoi_khoa
-- =========================
CREATE TABLE diem_cuoi_khoa (
    id TEXT PRIMARY KEY,
    lop_hoc_id TEXT NOT NULL,
    hoc_vien_id TEXT NOT NULL,
    diem NUMERIC(4,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_diem_lop_hoc FOREIGN KEY (lop_hoc_id) REFERENCES lop_hoc(id),
    CONSTRAINT fk_diem_hoc_vien FOREIGN KEY (hoc_vien_id) REFERENCES hoc_vien(id)
);
```

### 4. Lập trình nội dung thực hành

Các nội dung thực hành được đặt ở thư mục `/implements`.

Nội dung thực hành được đặt tên chỉ mục theo `Pxx` với `xx` tương ứng với số chỉ mục của phần nội dung trình bày.

### 5. Kiểm thử phần lập trình

Sau khi hoàn tất lập trình các phần `Pxx`, chạy các script `Txx` tương ứng ở thư mục `/tests` để kiểm thử phần cài đặt.

### 6. Khởi chạy giao diện chatbot hoàn chỉnh

Sau khi ***hoàn thiện toàn bộ các phần thực hành***, khởi chạy giao diện chatbot với lệnh `streamlit run app.py` để trải nghiệm pipeline chatbot hoàn chỉnh.