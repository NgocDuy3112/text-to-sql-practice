-- psql -U postgres -h localhost -d chatbot_demo -a -f ./demo.sql
-- TODO: sqlite

-- =========================
-- DROP TABLE (optional)
-- =========================
DROP TABLE IF EXISTS diem_cuoi_khoa;
DROP TABLE IF EXISTS dang_ky_lop;
DROP TABLE IF EXISTS giang_vien_phu_trach;
DROP TABLE IF EXISTS lop_hoc;
DROP TABLE IF EXISTS hoc_vien;
DROP TABLE IF EXISTS giang_vien;
DROP TABLE IF EXISTS chuong_trinh;

DROP TABLE IF EXISTS conversations;

DROP TABLE IF EXISTS chat_history;

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
    CONSTRAINT fk_lop_chuong_trinh
        FOREIGN KEY (chuong_trinh_id)
        REFERENCES chuong_trinh(id)
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
    trang_thai TEXT NOT NULL
        CHECK (trang_thai IN ('dang_hoc', 'hoan_tat', 'huy')),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_dk_hoc_vien
        FOREIGN KEY (hoc_vien_id)
        REFERENCES hoc_vien(id),
    CONSTRAINT fk_dk_lop_hoc
        FOREIGN KEY (lop_hoc_id)
        REFERENCES lop_hoc(id)
);

-- =========================
-- TABLE: giang_vien_phu_trach
-- =========================
CREATE TABLE giang_vien_phu_trach (
    id TEXT PRIMARY KEY,
    giang_vien_id TEXT NOT NULL,
    lop_hoc_id TEXT NOT NULL,
    vai_tro TEXT NOT NULL
        CHECK (vai_tro IN ('giang_day_chinh', 'tro_giang', 'thuc_hanh')),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_pc_giang_vien
        FOREIGN KEY (giang_vien_id)
        REFERENCES giang_vien(id),
    CONSTRAINT fk_pc_lop_hoc
        FOREIGN KEY (lop_hoc_id)
        REFERENCES lop_hoc(id)
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
    CONSTRAINT fk_diem_lop_hoc
        FOREIGN KEY (lop_hoc_id)
        REFERENCES lop_hoc(id),
    CONSTRAINT fk_diem_hoc_vien
        FOREIGN KEY (hoc_vien_id)
        REFERENCES hoc_vien(id)
);

-- =========================
-- INSERT DATA
-- =========================

-- hoc_vien
INSERT INTO hoc_vien (
    id, ten, nam_sinh, so_dien_thoai, email, created_at, updated_at
) VALUES
('HV1', 'Nguyễn Văn An', 1995, '0901000001', 'an.nguyen@example.com', '2024-12-01 09:00:00', '2025-01-05 10:00:00'),
('HV2', 'Trần Thị Bình', 1998, '0901000002', 'binh.tran@example.com', '2024-12-05 09:30:00', '2025-01-10 11:00:00'),
('HV3', 'Lê Hoàng Cường', 1990, '0901000003', 'cuong.le@example.com', '2024-12-10 10:00:00', '2025-02-01 08:30:00'),
('HV4', 'Phạm Thu Dung', 2000, '0901000004', 'dung.pham@example.com', '2025-01-01 14:00:00', '2025-02-20 09:00:00'),
('HV5', 'Võ Minh Đức', 1997, '0901000005', 'duc.vo@example.com', '2025-01-10 15:00:00', '2025-02-18 16:00:00');

-- chuong_trinh
INSERT INTO chuong_trinh (
    id, ten, tong_so_gio, hoc_phi, ghi_chu, created_at, updated_at
) VALUES
('CT1', 'Tin học văn phòng cơ bản', 40, 1500000, 'Chương trình nền tảng', '2024-11-01 08:00:00', '2024-12-01 09:00:00'),
('CT2', 'Excel nâng cao', 30, 1800000, 'Yêu cầu đã biết Excel cơ bản', '2024-11-05 08:30:00', '2024-12-10 10:00:00'),
('CT3', 'Lập trình Python cơ bản', 60, 2500000, 'Không yêu cầu nền tảng lập trình', '2024-11-10 09:00:00', '2025-01-01 08:00:00'),
('CT4', 'Phân tích dữ liệu với Python', 50, 3000000, 'Học tiếp sau Python cơ bản', '2024-12-01 10:00:00', '2025-01-15 09:00:00'),
('CT5', 'SQL cho người mới bắt đầu', 25, 1200000, 'Dành cho người chưa biết SQL', '2024-12-15 11:00:00', '2025-01-20 10:30:00');

-- lop_hoc
INSERT INTO lop_hoc (
    id, ten_lop, chuong_trinh_id, thoi_gian_hoc, dia_diem_hoc,
    thoi_gian_bat_dau, thoi_gian_ket_thuc, created_at, updated_at
) VALUES
('LH1', 'VP01', 'CT1', 'Tối 2-4-6', 'Phòng A1', '2025-01-10', '2025-03-10', '2024-12-20 09:00:00', '2025-01-05 08:00:00'),
('LH2', 'EX02', 'CT2', 'Tối 3-5',   'Phòng A2', '2025-02-05', '2025-03-20', '2025-01-05 10:00:00', '2025-02-01 09:00:00'),
('LH3', 'PY01', 'CT3', 'Thứ 7-CN',  'Phòng B1', '2025-01-15', '2025-04-15', '2024-12-25 14:00:00', '2025-01-10 10:00:00'),
('LH4', 'DA01', 'CT4', 'Tối 2-4',   'Phòng B2', '2025-03-01', '2025-05-01', '2025-01-20 15:00:00', '2025-02-20 09:00:00'),
('LH5', 'SQL01','CT5', 'Tối 6',     'Phòng A3', '2025-02-20', '2025-03-25', '2025-01-25 16:00:00', '2025-02-15 10:00:00');

-- giang_vien
INSERT INTO giang_vien (
    id, ten, so_dien_thoai, email, created_at, updated_at
) VALUES
('GV1', 'Nguyễn Thị Trang', '0912000001', 'trang.nguyen@example.com', '2024-10-01 09:00:00', '2025-01-01 08:00:00'),
('GV2', 'Trần Quang Minh', '0912000002', 'minh.tran@example.com', '2024-10-05 09:30:00', '2025-01-05 08:30:00'),
('GV3', 'Lê Thanh Sơn', '0912000003', 'son.le@example.com', '2024-10-10 10:00:00', '2025-01-10 09:00:00'),
('GV4', 'Phạm Quốc Bảo', '0912000004', 'bao.pham@example.com', '2024-10-15 10:30:00', '2025-01-15 09:30:00'),
('GV5', 'Vũ Thị Lan', '0912000005', 'lan.vu@example.com', '2024-10-20 11:00:00', '2025-01-20 10:00:00');

-- giang_vien_phu_trach
INSERT INTO giang_vien_phu_trach (
    id, giang_vien_id, lop_hoc_id, vai_tro, created_at, updated_at
) VALUES
('PC1', 'GV1', 'LH1', 'giang_day_chinh', '2024-12-25 09:00:00', '2025-01-01 08:00:00'),
('PC2', 'GV2', 'LH2', 'giang_day_chinh', '2025-01-10 09:00:00', '2025-01-15 08:30:00'),
('PC3', 'GV3', 'LH3', 'giang_day_chinh', '2024-12-30 14:00:00', '2025-01-05 09:00:00'),
('PC4', 'GV4', 'LH4', 'tro_giang',      '2025-02-01 10:00:00', '2025-02-10 09:00:00'),
('PC5', 'GV5', 'LH5', 'thuc_hanh',      '2025-02-05 11:00:00', '2025-02-15 10:00:00'),
('PC6', 'GV2', 'LH3', 'tro_giang',      '2025-01-05 15:00:00', '2025-01-10 10:00:00'),
('PC7', 'GV4', 'LH3', 'thuc_hanh',      '2025-01-06 16:00:00', '2025-01-12 11:00:00');

-- dang_ky_lop
INSERT INTO dang_ky_lop (
    id, hoc_vien_id, lop_hoc_id, trang_thai, created_at, updated_at
) VALUES
('DK1', 'HV1', 'LH1', 'hoan_tat', '2025-01-10 08:00:00', '2025-03-10 18:00:00'),
('DK2', 'HV2', 'LH1', 'hoan_tat', '2025-01-12 09:00:00', '2025-03-10 18:00:00'),
('DK3', 'HV3', 'LH3', 'dang_hoc', '2025-01-15 10:00:00', '2025-02-20 09:00:00'),
('DK4', 'HV4', 'LH4', 'dang_hoc', '2025-03-01 08:30:00', '2025-03-10 09:00:00'),
('DK5', 'HV5', 'LH5', 'huy',      '2025-02-18 14:00:00', '2025-02-19 10:00:00');

-- diem_cuoi_khoa
INSERT INTO diem_cuoi_khoa (
    id, lop_hoc_id, hoc_vien_id, diem, created_at, updated_at
) VALUES
('D1', 'LH1', 'HV1', 8.5, '2025-03-10 17:00:00', '2025-03-10 17:30:00'),
('D2', 'LH1', 'HV2', 7.8, '2025-03-10 17:10:00', '2025-03-10 17:30:00'),
('D3', 'LH3', 'HV3', NULL, '2025-02-20 09:00:00', '2025-02-20 09:00:00'),
('D4', 'LH4', 'HV4', NULL, '2025-03-10 09:00:00', '2025-03-10 09:00:00'),
('D5', 'LH5', 'HV5', NULL, '2025-02-19 10:00:00', '2025-02-19 10:00:00');