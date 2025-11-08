from flask import jsonify, request
from flask_restful import Resource
from rapidfuzz import process

class Mateus(Resource):

    categorias = {
        "Sangue": [
            {"nome": "hemograma", "tempo": 10, "descricao": "Avalia os componentes do sangue, como glóbulos vermelhos, brancos e plaquetas."},
            {"nome": "colesterol", "tempo": 10, "descricao": "Mede os níveis de colesterol total e suas frações no sangue."},
            {"nome": "glicemia", "tempo": 5, "descricao": "Verifica a quantidade de glicose (açúcar) no sangue, essencial para diagnóstico de diabetes."},
            {"nome": "triglicerídeos", "tempo": 10, "descricao": "Avalia os níveis de gordura no sangue, importante para o risco cardiovascular."},
            {"nome": "hemoglobina glicada", "tempo": 15, "descricao": "Mede a média da glicose no sangue nos últimos três meses."}
        ],
        "Imagem": [
            {"nome": "raio-x", "tempo": 15, "descricao": "Produz imagens de estruturas internas do corpo usando radiação."},
            {"nome": "ressonância magnética", "tempo": 60, "descricao": "Usa campos magnéticos e ondas de rádio para gerar imagens detalhadas de órgãos e tecidos."},
            {"nome": "tomografia", "tempo": 30, "descricao": "Cria imagens em seções transversais do corpo com o uso de raios X e computador."},
            {"nome": "ultrassonografia", "tempo": 25, "descricao": "Usa ondas sonoras para criar imagens de órgãos e tecidos em tempo real."},
            {"nome": "mamografia", "tempo": 20, "descricao": "Exame de imagem das mamas para detectar nódulos e alterações precoces."},
            {"nome": "densitometria óssea", "tempo": 30, "descricao": "Avalia a densidade dos ossos, ajudando no diagnóstico de osteoporose."}
        ],
        "Cardiológicos": [
            {"nome": "eletrocardiograma", "tempo": 10, "descricao": "Registra a atividade elétrica do coração para detectar arritmias e outras alterações."},
            {"nome": "ecocardiograma", "tempo": 40, "descricao": "Avalia o funcionamento do coração por meio de ultrassom."},
            {"nome": "teste ergométrico", "tempo": 35, "descricao": "Avalia o desempenho cardíaco durante esforço físico controlado."}
        ],
        "Urina": [
            {"nome": "urocultura", "tempo": 5, "descricao": "Identifica a presença de bactérias na urina e orienta o tratamento de infecções urinárias."},
            {"nome": "exame de urina", "tempo": 5, "descricao": "Analisa substâncias presentes na urina para avaliação da função renal e infecções."}
        ],
        "Hormonais": [
            {"nome": "tsh", "tempo": 10, "descricao": "Avalia a função da tireoide medindo o hormônio estimulante da tireoide (TSH)."},
            {"nome": "t4 livre", "tempo": 10, "descricao": "Complementa o exame de TSH, medindo o hormônio tiroxina livre no sangue."},
            {"nome": "testosterona", "tempo": 10, "descricao": "Mede o nível do hormônio testosterona, importante para a saúde reprodutiva e metabólica."},
            {"nome": "estradiol", "tempo": 10, "descricao": "Avalia o hormônio estrogênio, essencial no ciclo menstrual e na fertilidade feminina."},
            {"nome": "cortisol", "tempo": 10, "descricao": "Mede o hormônio do estresse, importante na avaliação da função adrenal."},
            {"nome": "progesterona", "tempo": 10, "descricao": "Examina o hormônio relacionado ao ciclo menstrual e à gestação."}
        ],
        "Infecciosos": [
            {"nome": "hiv", "tempo": 15, "descricao": "Detecta a presença de anticorpos contra o vírus HIV."},
            {"nome": "hepatite b", "tempo": 15, "descricao": "Identifica a infecção pelo vírus da hepatite B e monitora a resposta ao tratamento."},
            {"nome": "hepatite c", "tempo": 15, "descricao": "Detecta a infecção pelo vírus da hepatite C através de anticorpos específicos."},
            {"nome": "sífilis", "tempo": 15, "descricao": "Detecta anticorpos contra a bactéria causadora da sífilis."}
        ],
        "Respiratórios": [
            {"nome": "espirometria", "tempo": 20, "descricao": "Avalia a capacidade pulmonar e ajuda no diagnóstico de doenças respiratórias."},
            {"nome": "gasometria arterial", "tempo": 10, "descricao": "Mede os níveis de oxigênio e dióxido de carbono no sangue arterial."}
        ]
    }

    LIMITAR_CONFIANCA = 100

    def get(self):
        nome = request.args.get("nome")

        nome = nome.lower().strip()
        melhor_cat = "Categoria não encontrada"
        melhor_exame = None
        melhor_score = 0

        for cat, exames in self.categorias.items():
            nomes_exames = [e["nome"] for e in exames]
            match, score, _ = process.extractOne(nome, nomes_exames)
            if score > melhor_score:
                melhor_score = score
                melhor_cat = cat
                melhor_exame = next(e for e in exames if e["nome"] == match)

        if melhor_score < self.LIMITAR_CONFIANCA:
            return jsonify({
                "categoria_sugerida": "Categoria não encontrada",
                "confianca": f"{melhor_score:.2f}%",
                "tempo_estimado": None,
                "descricao": None
            })

        return jsonify({
            "nome": melhor_exame["nome"],
            "categoria_sugerida": melhor_cat,
            "confianca": f"{melhor_score:.2f}%",
            "tempo_estimado": melhor_exame["tempo"],
            "descricao": melhor_exame["descricao"]
        })
