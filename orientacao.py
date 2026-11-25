class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, fonte, acessos=0):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = list(palavras_chave)
        self.resposta = resposta
        self.fonte = fonte
        self.acessos = int(acessos)

    def exibir(self):
        print(f"\n>> {self.titulo}")
        print(f"[{self.categoria}]")
        print(self.resposta)
        print(f"Fonte: {self.fonte}")
        print("Aviso: este assistente NÃO é um canal oficial.")

    def registrar_acesso(self):
        self.acessos += 1

    def adicionar_palavra_chave(self, palavra):
        palavra_limpa = palavra.strip().lower()
        if palavra_limpa and palavra_limpa not in self.palavras_chave:
            self.palavras_chave.append(palavra_limpa)

    def para_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "palavras_chave": list(self.palavras_chave),
            "resposta": self.resposta,
            "fonte": self.fonte,
            "acessos": self.acessos,
        }
