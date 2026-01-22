from langchain.embeddings import init_embeddings
import numpy as np
from .constants import EMBEDDING_MODEL_ID, EMBEDDING_MODEL_PROVIDER


class EmbeddingBase():
    def __init__(self, model: str, provider: str):
        self.model = model
        self.provider = provider
        self.embedding_model = init_embeddings(
            model=self.model,
            provider=self.provider
        )
    
    def generate_doc_embeddings(self, input: str|list[str]) -> np.ndarray:
        """
        Tạo embedding cho tài liệu.
        
        :param query: Tài liệu cần tạo embedding.
        :type query: str | list[str]
        :return: Array numpy kết quả embedding.
            
            Shape: (n, d) với n là số tài liệu và d là số chiều embedding.
        :rtype: numpy.ndarray
        """
        if isinstance(input, str):
            input = [input]
        
        output = self.embedding_model.embed_documents(input)
        output_np = np.array(output)
        
        return output_np
    
    def generate_query_embeddings(self, query: str|list[str]) -> np.ndarray:
        """
        Tạo embedding cho câu hỏi.
        
        :param query: Câu hỏi cần tạo embedding.
        :type query: str | list[str]
        :return: Array numpy kết quả embedding.
            
            Shape: (n, d) với n là số câu hỏi và d là số chiều embedding.
        :rtype: numpy.ndarray
        """
        if isinstance(query, str):
            output = self.embedding_model.embed_query(query)
        elif isinstance(query, list):
            output = [self.embedding_model.embed_query(i) for i in query]

        output_np = np.array(output)
        
        return output_np



# class OllamaEmbeddingBase():
#     def __init__(self, model_id: str = "bge-m3"):
#         self.model_id = model_id
#         self.model = OllamaEmbeddings(
#             model=self.model_id,
#             keep_alive=3,
#             base_url="http://localhost:11434"
#         )
    
#     def generate_doc_embeddings(self, input: str|list[str]) -> np.ndarray:
#         """
#         Tạo embedding cho tài liệu.
        
#         :param query: Tài liệu cần tạo embedding.
#         :type query: str | list[str]
#         :return: Array numpy kết quả embedding.
            
#             Shape: (n, d) với n là số tài liệu và d là số chiều embedding.
#         :rtype: numpy.ndarray
#         """
#         if isinstance(input, str):
#             input = [input]
        
#         output = self.model.embed_documents(input)
#         output_np = np.array(output)
        
#         return output_np
    
#     def generate_query_embeddings(self, query: str|list[str]) -> np.ndarray:
#         """
#         Tạo embedding cho câu hỏi.
        
#         :param query: Câu hỏi cần tạo embedding.
#         :type query: str | list[str]
#         :return: Array numpy kết quả embedding.
            
#             Shape: (n, d) với n là số câu hỏi và d là số chiều embedding.
#         :rtype: numpy.ndarray
#         """
#         if isinstance(query, str):
#             output = self.model.embed_query(query)
#         elif isinstance(query, list):
#             output = [self.model.embed_query(i) for i in query]
            
#         output_np = np.array(output)
        
#         return output_np


# ollama_embedding_base = OllamaEmbeddingBase()
embedding_base = EmbeddingBase(model=EMBEDDING_MODEL_ID, provider=EMBEDDING_MODEL_PROVIDER) 