from transformers import AutoTokenizer, AutoModelForCausalLM

class LLM_engine():
    def __init__(self):
        model_id = "shenzhi-wang/Llama3-8B-Chinese-Chat"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype="auto", device_map="auto"
        )


    def run(self):
        return