import os
import yaml
from langchain.chat_models import init_chat_model, BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from pydantic import BaseModel
from messages import MESSAGE_TYPE, ChatbotMessage
from constants import IDENTITY_PROMPT


class LLMChatBase():
    def __init__(self, model_id: str = "qwen3:1.7b", model_provider: str = "ollama"):
        self.model_id = model_id
        self.model: BaseChatModel = init_chat_model(
            model=model_id, 
            model_provider=model_provider,
            configurable_fields={
                "temperature": 0.1,
                "keep_alive": 3,
                "num_predict": 10
            }
        )

    def _to_langchain_msg(self, message: ChatbotMessage) -> BaseMessage:
        assert "type" in message.keys() and "content" in message.keys(), "Đối tượng message mong đợi khóa type và content."
        
        match message['type']:
            case MESSAGE_TYPE.USER:
                return HumanMessage(message['content'])
            case MESSAGE_TYPE.ASSISTANT:
                return AIMessage(message['content'])
            case _:
                return HumanMessage(message['content'])

    def _to_langchain_prompt(self, prompt: str | list[str] | ChatbotMessage | list[ChatbotMessage] | BaseMessage | list[BaseMessage]) -> list[BaseMessage]:
        # If caller already supplies LangChain messages, respect them.
        if isinstance(prompt, BaseMessage):
            return [SystemMessage(IDENTITY_PROMPT), prompt]
        if isinstance(prompt, list) and prompt and isinstance(prompt[0], BaseMessage):
            return prompt

        msg = [SystemMessage(IDENTITY_PROMPT)]
        
        if isinstance(prompt, str):
            msg.extend([HumanMessage(prompt)])
        elif isinstance(prompt, dict):
            msg.extend([self._to_langchain_msg(prompt)])
        elif isinstance(prompt, list):
            if isinstance(prompt[0], str):
                msg.extend([HumanMessage(p) for p in prompt])
            elif isinstance(prompt[0], dict):
                msg.extend([self._to_langchain_msg(p) for p in prompt])
        
        # ==== Uncomment để log toàn bộ prompt gửi đến LLM ====
        
        # prompt_str = '\n'.join([f">>> {p.type} <<<\n{p.content}\n" for p in msg])
        # print("*"*25 +" LLM Trigger Prompt "+"*"*25)
        # print(prompt_str)
        # print("*"*70)
        
        # ==== Uncomment để log toàn bộ prompt gửi đến LLM ====
        
        return msg

    def generate(self, prompt: str|list[str]|ChatbotMessage|list[ChatbotMessage]) -> str:
        """
        Gọi tạo sinh LLM với prompt đầu vào.
        
        :param prompt: Prompt ngữ cảnh đầu vào.
        :type prompt: str | list[str] | ChatbotMessage | list[ChatbotMessage]
        :return: Chuỗi kết quả tạo sinh.
        :rtype: str
        """
        msg = self._to_langchain_prompt(prompt)
        
        output = self.model.invoke(msg)
        content = output.content.strip()
        
        # ==== Uncomment để log toàn bộ kết quả LLM trả về ====
        
        # print("*"*25 +" LLM Generation "+"*"*25)
        # print(content)
        # print("*"*70)
        
        # ==== Uncomment để log toàn bộ kết quả LLM trả về ====
        
        return content

    def generate_structured(
        self, prompt: str|list[str]|ChatbotMessage|list[ChatbotMessage],
        base_model_cls: BaseModel
    ) -> dict:
        """
        Gọi tạo sinh LLM có ràng buộc cấu trúc.
        
        :param prompt: Prompt ngữ cảnh đầu vào.
        :type prompt: str | list[str] | ChatbotMessage | list[ChatbotMessage]
        :param base_model_cls: Lớp python kế thừa pydantic BaseModel định nghĩa cấu trúc tạo sinh.
        :type base_model_cls: BaseModel
        :return: Đối tượng dict trả về theo cấu trúc BaseModel.
        :rtype: dict
        """
        # LangChain expects either a Pydantic model class or a schema.
        # Passing the Pydantic class ensures `parsed` is an instance with attribute access.
        structured_model = self.model.with_structured_output(base_model_cls, include_raw=True)
        
        msg = self._to_langchain_prompt(prompt)
        
        output = structured_model.invoke(msg)
        parsed = output["parsed"]
        return parsed


llm_chat_base = LLMChatBase(model_id="qwen3:4b", model_provider="ollama") 