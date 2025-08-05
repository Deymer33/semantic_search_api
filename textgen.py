from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Cargar modelo y tokenizer solo una vez
model_name = "google/flan-t5-base"  # Puedes usar flan-t5-small si prefieres
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generar_respuesta(query, tools):
    top_tools = tools[:3]
    herramientas = "\n".join([f"- {t['tool']}" for t in top_tools])

    prompt = (
        f"Estas herramientas fueron seleccionadas por las siguientes razones:\n"
        f"{herramientas}\n\n"
        f"Estas herramientas son útiles porque"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_new_tokens=80)
    respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Formatear para que siempre termine en punto
    return respuesta.strip().rstrip('.') + '.'

