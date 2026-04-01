import json
from PySide6.QtCore import QObject, Signal


class GeminiWorker(QObject):
    done = Signal(list)
    error = Signal(str)
    status = Signal(str)

    def __init__(self, api_key, model, existing, count):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.existing = existing
        self.count = count

    def run(self):
        try:
            try:
                from google import genai
                from google.genai import types

                sdk_version = "new"
            except ImportError:
                import google.genai as genai_old

                sdk_version = "old"
        except ImportError:
            self.error.emit("Aviso: Instale o SDK executando: pip install google-genai")
            return
        try:
            prompt = f"""Gere {self.count} questões NOVAS de legislação de trânsito brasileira. Retorne APENAS uma lista JSON com objetos contendo as chaves exatas: "id", "categoria", "dificuldade" (facil|media|dificil), "pergunta", "opcoes" (lista 4 str), "correta" (int 0-3), "explicacao", "pegadinha"."""
            self.status.emit("Handshake com Gemini API...")
            if sdk_version == "new":
                client = genai.Client(api_key=self.api_key)
                resp = client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    ),
                )
            else:
                genai_old.configure(api_key=self.api_key)
                resp = genai_old.GenerativeModel(
                    model_name=self.model,
                    generation_config={"response_mime_type": "application/json"},
                ).generate_content(prompt)
            self.status.emit("Processando payload JSON...")
            valid = [
                q
                for q in json.loads(resp.text)
                if all(k in q for k in ["pergunta", "opcoes", "correta", "explicacao"])
            ]
            if not valid:
                raise ValueError("Nenhum item válido processado")
            self.done.emit(valid)
        except Exception as e:
            self.error.emit(str(e))
