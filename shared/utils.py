import numpy as np
from .embed_model import embedding_base


def get_cosine_sim(q: str, d: list[str]) -> list[dict]:
    """
    Tính toán độ tương đồng cosine giữa một câu truy vấn và danh sách các câu văn bản.

    :param q: Câu truy vấn (query) cần so sánh.
    :type q: str
    :param d: Danh sách các câu văn bản để so sánh với truy vấn.
    :type d: list[str]
    :return: Danh sách dict chứa các trường:
    
        + content: nội dung văn bản trong d
        + score: điểm cosine similarity với truy vấn (giá trị từ -1 đến 1)
        + old_idx: chỉ số ban đầu của văn bản trong d
    
        Danh sách được sắp xếp giảm dần theo score.
    :rtype: list[dict]
    """
    qe = embedding_base.generate_query_embeddings(q)  # shape: (embedding_dim,)
    de = embedding_base.generate_doc_embeddings(d)  # shape: (len(d), embedding_dim)

    # Đảm bảo qe là vector 2D (1, embedding_dim)
    qe = np.array(qe)
    if qe.ndim == 1:
        qe = qe.reshape(1, -1)
    de = np.array(de)

    # Tính cosine similarity
    qe_norm = qe / np.linalg.norm(qe, axis=1, keepdims=True)
    de_norm = de / np.linalg.norm(de, axis=1, keepdims=True)
    scores = np.dot(de_norm, qe_norm.T).flatten() # Ma trận similarity: (len(d),)

    # Sắp xếp theo thứ tự giảm dần
    sorted_idx = np.argsort(-scores)
    result = []
    for idx in sorted_idx:
        result.append({
            'content': d[idx],
            'score': float(scores[idx]),
            'old_idx': int(idx)
        })
    return result
