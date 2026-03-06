from modules.ml_module import treinar_ml
from modules.text_module import analisar_texto
from modules.video_module import video_score

pipeline = treinar_ml()

def calcular_risco(evento):
    # Dados estruturados
    import pandas as pd
    x = pd.DataFrame([evento])[['tempo','local_cameras','online_posts']]
    ml_score = pipeline.predict_proba(x)[0][1]

    # Texto
    texto_score = analisar_texto(evento.get('texto',''))

    # Vídeo
    global video_score
    vid_score = video_score

    # Score final
    score_final = (ml_score + texto_score + vid_score) / 3
    return score_final
