from enum import StrEnum
from langchain_core.prompts import ChatPromptTemplate
from shared.chat_model import llm_chat_base
from shared.embed_model import embedding_base
from shared.constants import IDENTITY_PROMPT, NON_QUERY_SAMPLES, QUERY_SAMPLES
from shared.utils import get_cosine_sim

from pydantic import BaseModel


class ROUTER_QUESTION(StrEnum):
    NON_QUERY = "non_query"
    QUERY = "query"


class RouteSchema(BaseModel):
    route: ROUTER_QUESTION


def route_question(question: str) -> ROUTER_QUESTION:
    """
    Hàm router phân định luồng Truy vấn / Không truy vấn.
    
    Nhận đầu vào là yêu cầu người dùng, phân định xem
    có cần thực hiện truy vấn để trả lời hay không.
    
    :param question: Chuỗi câu hỏi đầu vào
    
    :type question: str
    
    :return: Enum phân định luồng:
        
        - NON_QUERY(`non_query`) - Không truy vấn,
        - QUERY(`query`) - Có truy vấn.
    
    :rtype: ROUTER_QUESTION
    """

    # ====== TODO: Thực hiện cài đặt dưới đây ======
    # Hàm hỗ trợ gọi tạo sinh LLM: llm_chat_base.generate()
    # Hàm hỗ trợ gọi tạo sinh LLM có ràng buộc cấu trúc: llm_chat_base.generate_structured()
    # Hàm hỗ trợ tạo embed câu hỏi: embedding_base.generate_query_embeddings()
    # Hàm hỗ trợ tạo embed tài liệu: embedding_base.generate_doc_embeddings()
    # Hàm hỗ trợ tính điểm cosine tương đồng: get_cosine_sim()
    
    ## Routing using cosine similarity with sample questions
    # print("Sử dụng phương pháp cosine similarity để phân định luồng...")
    # cos_sim_tables = get_cosine_sim(question, NON_QUERY_SAMPLES + QUERY_SAMPLES)
    # similar_content = cos_sim_tables[0]['content']
    # if similar_content in NON_QUERY_SAMPLES:
    #     response = RouteSchema(route=ROUTER_QUESTION.NON_QUERY)
    # else:
    #     response = RouteSchema(route=ROUTER_QUESTION.QUERY)

    ## Routing using LLM classification
    print("Sử dụng LLM để phân định luồng...")
    prompt_template = ChatPromptTemplate(
        [
            ("system", IDENTITY_PROMPT),
            ("system", f"""
                Bạn là một người điều phối luồng xử lý cho hệ thống chatbot hỗ trợ truy vấn dữ liệu. Dựa vào yêu cầu dưới đây từ người dùng, hãy phân định luồng xử lý tương ứng:
                + {ROUTER_QUESTION.NON_QUERY} - Trả lời trực tiếp mà không truy vấn.
                + {ROUTER_QUESTION.QUERY} - Truy vấn dữ liệu rồi trả lời.
                
                Chỉ dẫn phân định luồng:
                - Sử dụng luồng {ROUTER_QUESTION.NON_QUERY} cho các dạng yêu cầu:
                    + Chào hỏi xã giao.
                    + Giao tiếp cơ bản.
                    + Các câu hỏi không thuộc phạm vi chức năng hệ thống.
                    + Các câu hỏi không yêu cầu truy xuất dữ liệu từ CSDL.
                - Sử dụng luồng {ROUTER_QUESTION.QUERY} cho các câu hỏi cần truy vấn dữ liệu từ CSDL.

                Chỉ dẫn kết quả trả về:
                - Kết quả trả về của bạn chỉ trả về một trong: [{ROUTER_QUESTION.NON_QUERY}, {ROUTER_QUESTION.QUERY}].
                - Không trả về kèm theo bất kỳ văn bản nào khác.
            """),
            ("human", "{question}"),
        ],
        input_variables=["question"]
    )
    
    response = llm_chat_base.generate_structured(
        prompt=prompt_template.format_messages(question=question),
        base_model_cls=RouteSchema
    )

    # ====== Hết phần cài đặt ======

    assert isinstance(response.route, ROUTER_QUESTION), "Kết quả trả về phải là ROUTER_QUESTION"
    
    return response.route