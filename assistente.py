import csv
from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base

    def _contem_dado_pessoal(self, texto):
        if "@" in texto:
            return True
        digitos = sum(1 for ch in texto if ch.isdigit())
        return digitos >= 8

    def _ler_sn(self, mensagem):
        while True:
            resp = input(mensagem).strip().lower()
            if resp in ("s", "n"):
                return resp
            print("Entrada inválida. Digite 's' para sim ou 'n' para não.")

    def perguntar(self):
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return

            if not pergunta:
                print("Digite uma dúvida válida ou 0 para voltar.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Pergunta recusada por conter possível dado pessoal (e-mail ou sequência numérica).")
                continue

            resultados = self.base.buscar(pergunta)
            melhor_pontos, melhor_ori = resultados[0] if resultados else (0, None)

            if melhor_ori is not None and melhor_pontos >= 3:
                confianca = "ALTA" if melhor_pontos >= 6 else "MÉDIA"
                print(f"\nConfiança: {confianca} (pontuação: {melhor_pontos})")
                melhor_ori.exibir()
                melhor_ori.registrar_acesso()
                self.base.salvar()

                ajudou = self._ler_sn("\nEssa orientação respondeu sua dúvida? (s/n): ")
                if ajudou == "s":
                    return

                quer_cat = self._ler_sn("Quer procurar pelas categorias? (s/n): ")
                if quer_cat == "s":
                    escolhida = self.navegar()
                    if escolhida is not None:
                        confirmou = self._ler_sn("Essa orientação respondeu sua dúvida? (s/n): ")
                        if confirmou == "s":
                            self.aprender(pergunta, escolhida)
                return

            print("\nNão encontrei uma orientação confiável para essa dúvida.")
            quer_cat = self._ler_sn("Quer procurar pelas categorias? (s/n): ")
            if quer_cat == "s":
                escolhida = self.navegar()
                if escolhida is not None:
                    confirmou = self._ler_sn("Essa orientação respondeu sua dúvida? (s/n): ")
                    if confirmou == "s":
                        self.aprender(pergunta, escolhida)
            return

    def navegar(self):
        categorias = []
        for ori in self.base.orientacoes:
            if ori.categoria not in categorias:
                categorias.append(ori.categoria)

        if not categorias:
            print("Nenhuma categoria disponível.")
            return None

        while True:
            print("\n" + " ".join(f"[{i + 1}] {cat}" for i, cat in enumerate(categorias)))
            escolha_cat = input("Escolha a categoria (0 para voltar): ").strip()
            if escolha_cat == "0":
                return None
            if not escolha_cat.isdigit():
                print("Entrada inválida. Digite o número da categoria ou 0.")
                continue

            idx_cat = int(escolha_cat) - 1
            if idx_cat < 0 or idx_cat >= len(categorias):
                print("Categoria inexistente.")
                continue

            cat_selecionada = categorias[idx_cat]
            orientacoes_cat = [ori for ori in self.base.orientacoes if ori.categoria == cat_selecionada]

            while True:
                print()
                for i, ori in enumerate(orientacoes_cat):
                    print(f"[{i + 1}] {ori.titulo}")
                escolha_ori = input("Escolha a orientação (0 para voltar): ").strip()
                if escolha_ori == "0":
                    break
                if not escolha_ori.isdigit():
                    print("Entrada inválida. Digite o número da orientação ou 0.")
                    continue

                idx_ori = int(escolha_ori) - 1
                if idx_ori < 0 or idx_ori >= len(orientacoes_cat):
                    print("Orientação inexistente.")
                    continue

                ori_escolhida = orientacoes_cat[idx_ori]
                ori_escolhida.exibir()
                ori_escolhida.registrar_acesso()
                self.base.salvar()
                return ori_escolhida

        return None

    def aprender(self, pergunta, orientacao):
        candidatas = self.base.palavras_novas(pergunta, orientacao)
        aprendidas = 0

        for palavra in candidatas:
            resp = self._ler_sn(f"Aprender '{palavra}' para '{orientacao.titulo}'? (s/n): ")
            if resp == "s":
                orientacao.adicionar_palavra_chave(palavra)
                aprendidas += 1

        if aprendidas > 0:
            self.base.salvar()

        print(f"{aprendidas} palavra(s)-chave aprendida(s).")

    def relatorio(self):
        ordenado = self.base.ranking()
        print("\n=== RELATÓRIO DE USO ===")

        print("\nTop 3 orientações mais acessadas:")
        for ori in ordenado[:3]:
            print(f"- {ori.titulo} [{ori.categoria}]: {ori.acessos} acesso(s)")

        nunca_acessadas = [ori for ori in self.base.orientacoes if ori.acessos == 0]
        print("\nOrientações nunca acessadas:")
        if not nunca_acessadas:
            print("- Nenhuma")
        else:
            for ori in nunca_acessadas:
                print(f"- {ori.titulo} [{ori.categoria}]")

        acessos_por_categoria = {}
        for ori in self.base.orientacoes:
            acessos_por_categoria[ori.categoria] = acessos_por_categoria.get(ori.categoria, 0) + ori.acessos

        print("\nTotal de acessos por categoria:")
        print(acessos_por_categoria)

    def exportar_csv(self, caminho_csv="data/relatorio.csv"):
        campos = ["id", "categoria", "titulo", "acessos", "total_palavras_chave"]
        with open(caminho_csv, "w", newline="", encoding="utf-8") as arq_csv:
            writer = csv.DictWriter(arq_csv, fieldnames=campos)
            writer.writeheader()
            for ori in self.base.orientacoes:
                writer.writerow(
                    {
                        "id": ori.id,
                        "categoria": ori.categoria,
                        "titulo": ori.titulo,
                        "acessos": ori.acessos,
                        "total_palavras_chave": len(ori.palavras_chave),
                    }
                )
        print(f"\nRelatório exportado para {caminho_csv}.")
