import base64
import os
from groq import Groq
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

class VisionInspector:
    """
    Visual Inspection Layer: Analyzes mechanical imagery using Llama-3.2-Vision.
    Provides context-aware audits of physical hardware health.
    """
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Prioritized Multimodal Model Stack
        self.model_candidates = [
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-3.2-11b-vision-preview",
            "llama-3.2-11b-vision-preview"
        ]

    def _encode_image(self, image_bytes):
        """
        Optimizes and encodes image data for LLM transmission.
        """
        img = Image.open(io.BytesIO(image_bytes))
        
        # Optimize for transmission (max 1024 width maintaining aspect ratio)
        max_size = (1024, 1024)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def audit_hardware(self, image_bytes, device_context="Mechanical Component"):
        """
        Performs a technical visual audit using a resilient failover bridge.
        """
        base64_image = self._encode_image(image_bytes)
        
        prompt = f"""
        Role: Senior Industrial Diagnostic Engineer (Vision Specialist).
        Context: Analyzing a {device_context} for potential mechanical failure or wear.
        
        Instructions:
        1. Identify visible anomalies: Corrosion, fluid leaks, structural cracks, thermal discoloration.
        2. Assess component integrity: Surface wear patterns and connection stability.
        3. Provide a technical summary of visual findings.
        4. Tone: Professional, precise, minimalist.
        """

        errors = []
        for model_id in self.model_candidates:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model=model_id,
                    temperature=0.1,
                    max_tokens=300
                )
                if chat_completion and hasattr(chat_completion, 'choices') and len(chat_completion.choices) > 0:
                    return chat_completion.choices[0].message.content
                else:
                    errors.append(f"{model_id}: Empty choices array returned.")
            except Exception as e:
                errors.append(f"{model_id}: {str(e)}")
                continue
        
        # All models failed: Return a detailed technical diagnostic error
        return f"Visual Audit Offline (Resilient Failover Exhausted). Trace: {'; '.join(errors)}"
