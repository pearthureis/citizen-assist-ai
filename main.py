from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    base = BaseConhecimento()
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print(f"\n=== {assistente.nome} ===")
        print("[1] Fazer pergunta")
        print("[2] Navegar por categorias")
        print("[3] Ver relatório de uso")
        print("[4] Exportar CSV")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Encerrando...")
            break
        elif opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.relatorio()
        elif opcao == "4":
            assistente.exportar_csv()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
