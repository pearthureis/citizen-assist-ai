import json
from orientacao import Orientacao

ACENTOS = {
    "á": "a",
    "à": "a",
    "ã": "a",
    "â": "a",
    "é": "e",
    "ê": "e",
    "í": "i",
    "ó": "o",
    "õ": "o",
    "ô": "o",
    "ú": "u",
    "ç": "c",
}

PALAVRAS_IGNORADAS = (
    "como",
    "onde",
    "quero",
    "preciso",
    "para",
    "qual",
    "quais",
    "fazer",
    "tirar",
    "meu",
    "minha",
    "meus",
    "minhas",
    "com",
    "sem",
    "por",
    "que",
    "uma",
    "uns",
    "umas",
    "dos",
    "das",
    "nos",
    "nas",
    "pelo",
    "pela",
    "sobre",
    "tem",
    "tenho",
    "pode",
    "posso",
    "quando",
    "quem",
    "isso",
    "essa",
    "esse",
)


def normalizar(texto):
    texto = str(texto).lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()\"'-/":
        texto = texto.replace(sinal, " ")
    return " ".join(texto.split())


class BaseConhecimento:
    def __init__(self, caminho_orientacoes="data/base_conhecimento.json", caminho_sinonimos="data/sinonimos.json"):
        self.caminho_orientacoes = caminho_orientacoes
        self.caminho_sinonimos = caminho_sinonimos
        self.orientacoes = []
        self.sinonimos = {}

    def carregar(self):
        with open(self.caminho_orientacoes, "r", encoding="utf-8") as arq_ori:
            dados_ori = json.load(arq_ori)
        self.orientacoes = [
            Orientacao(
                id=item["id"],
                categoria=item["categoria"],
                titulo=item["titulo"],
                palavras_chave=item.get("palavras_chave", []),
                resposta=item["resposta"],
                fonte=item["fonte"],
                acessos=item.get("acessos", 0),
            )
            for item in dados_ori
        ]

        with open(self.caminho_sinonimos, "r", encoding="utf-8") as arq_sin:
            dados_sin = json.load(arq_sin)
        self.sinonimos = {
            normalizar(chave): [normalizar(v) for v in valores]
            for chave, valores in dados_sin.items()
        }

    def salvar(self):
        dados = [ori.para_dict() for ori in self.orientacoes]
        with open(self.caminho_orientacoes, "w", encoding="utf-8") as arq_ori:
            json.dump(dados, arq_ori, ensure_ascii=False, indent=2)

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        if not pergunta_norm:
            return 0

        palavras = pergunta_norm.split()
        titulo_norm = normalizar(orientacao.titulo)
        palavras_titulo = titulo_norm.split()
        keywords_norm = [normalizar(kw) for kw in orientacao.palavras_chave]

        pontos = 0

        for kw in keywords_norm:
            if kw and f" {kw} " in f" {pergunta_norm} ":
                pontos += 3

        for palavra in palavras:
            sinonimos_palavra = self.sinonimos.get(palavra, [])
            for sin in sinonimos_palavra:
                if sin in keywords_norm:
                    pontos += 2

        for palavra in palavras:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for ori in self.orientacoes:
            pts = self.pontuar(pergunta, ori)
            resultados.append((pts, ori))
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados

    def palavras_novas(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        keywords_norm = {normalizar(kw) for kw in orientacao.palavras_chave}
        ignoradas_norm = {normalizar(p) for p in PALAVRAS_IGNORADAS}

        candidatas = []
        for palavra in pergunta_norm.split():
            if len(palavra) < 4:
                continue
            if palavra in keywords_norm:
                continue
            if palavra in ignoradas_norm:
                continue
            if palavra not in candidatas:
                candidatas.append(palavra)
            if len(candidatas) == 3:
                break

        return candidatas

    def ranking(self):
        return sorted(self.orientacoes, key=lambda ori: ori.acessos, reverse=True)
