import os
os.system("clear")

i
from dataclasses import dataclass, asdict
# --- Classe Funcionario ---
class Funcionariomport csv:
    """
    Representa um funcionário da empresa DENDÊ TECH.
    """
    def __init__(self, nome, cargo, salario):
        """
        Inicializa um novo funcionário.

        Args:
            nome (str): Nome do funcionário.
            cargo (str): Cargo do funcionário.
            salario (float): Salário do funcionário.
        """
        self.nome = nome
        self.cargo = cargo
        self.salario = salario

    def __str__(self):
        """
        Retorna uma representação em string do funcionário.
        """
        return f"Nome: {self.nome}, Cargo: {self.cargo}, Salário: R${self.salario:.2f}"

    def to_dict(self):
        """
        Converte os dados do funcionário para um dicionário.
        Útil para salvar em CSV.
        """
        return {"nome": self.nome, "cargo": self.cargo, "salario": self.salario}

# --- Lista para armazenar os funcionários em memória ---
lista_funcionarios = []
NOME_ARQUIVO_CSV = "funcionarios.csv"

# --- Funções de Persistência de Dados (CSV) ---
def carregar_dados_csv(nome_arquivo=NOME_ARQUIVO_CSV):
    """
    Carrega os dados dos funcionários de um arquivo CSV para a lista em memória.
    """
    global lista_funcionarios
    lista_funcionarios = [] # Limpa a lista antes de carregar para evitar duplicatas
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8', newline='') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
                try:
                    # Trata casos onde 'salario', 'nome' ou 'cargo' podem estar faltando ou serem None
                    nome = linha.get("nome", "").strip()
                    cargo = linha.get("cargo", "").strip()
                    salario_str = linha.get("salario")

                    if not nome or not cargo or salario_str is None:
                        print(f"Aviso: Linha com dados incompletos ignorada: {linha}")
                        continue
                    
                    salario = float(salario_str)
                    if nome and cargo: # Garante que nome e cargo não são vazios após strip
                        funcionario = Funcionario(nome, cargo, salario)
                        lista_funcionarios.append(funcionario)
                    else:
                        print(f"Aviso: Nome ou cargo ausente na linha: {linha}. Funcionário não carregado.")

                except ValueError:
                    print(f"Erro ao converter salário para float na linha: {linha}. Funcionário não carregado.")
                except Exception as e:
                    print(f"Erro inesperado ao processar linha {linha}: {e}")
        print(f"Dados carregados de '{nome_arquivo}' com sucesso ({len(lista_funcionarios)} funcionários).")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado. Iniciando com lista de funcionários vazia.")
    except Exception as e:
        print(f"Erro ao carregar dados de '{nome_arquivo}': {e}")

def salvar_dados_csv(nome_arquivo=NOME_ARQUIVO_CSV):
    """
    Salva os dados da lista de funcionários em um arquivo CSV.
    """
    campos = ["nome", "cargo", "salario"] # Define os campos esperados no CSV
    try:
        with open(nome_arquivo, mode='w', encoding='utf-8', newline='') as arquivo_csv:
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
            escritor_csv.writeheader()
            for funcionario in lista_funcionarios:
                escritor_csv.writerow(funcionario.to_dict())
        print(f"Dados salvos em '{nome_arquivo}' com sucesso.")
    except IOError:
        print(f"Erro de E/S ao salvar dados em '{nome_arquivo}'.")
    except Exception as e:
        print(f"Erro inesperado ao salvar dados: {e}")

# --- Funções CRUD ---

def adicionar_funcionario():
    """
    Adiciona um novo funcionário à lista.
    """
    print("\n--- Cadastrar Novo Funcionário ---")
    nome = input("Nome do funcionário: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    cargo = input("Cargo do funcionário: ").strip()
    if not cargo:
        print("Cargo não pode ser vazio.")
        return
        
    while True:
        try:
            salario_str = input("Salário do funcionário: ").strip()
            salario = float(salario_str)
            if salario < 0:
                print("Salário não pode ser negativo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Salário inválido. Por favor, insira um número (ex: 5000.75).")

    # Verifica se funcionário com mesmo nome já existe (case-insensitive)
    _, func_existente = buscar_funcionario_pelo_nome(nome)
    if func_existente:
        print(f"Erro: Funcionário com nome '{nome}' já existe.")
        return

    novo_funcionario = Funcionario(nome, cargo, salario)
    lista_funcionarios.append(novo_funcionario)
    print(f"Funcionário '{nome}' cadastrado com sucesso!")

def buscar_funcionario_pelo_nome(nome_busca):
    """
    Busca um funcionário pelo nome na lista. Retorna o índice e o objeto Funcionario ou (None, None).
    A busca é case-insensitive.
    """
    for i, funcionario in enumerate(lista_funcionarios):
        if funcionario.nome.lower() == nome_busca.lower():
            return i, funcionario
    return None, None

def listar_funcionarios():
    """
    Exibe a lista de todos os funcionários cadastrados.
    """
    print("\n--- Lista de Funcionários DENDÊ TECH ---")
    if not lista_funcionarios:
        print("Nenhum funcionário cadastrado.")
        return

    for i, funcionario in enumerate(lista_funcionarios):
        print(f"{i+1}. {funcionario}")
    print("---------------------------------------")

def buscar_funcionario_especifico_interativo():
    """
    Permite ao usuário buscar um funcionário específico pelo nome e exibe seus detalhes.
    """
    print("\n--- Buscar Funcionário Específico ---")
    if not lista_funcionarios:
        print("Nenhum funcionário cadastrado para buscar.")
        return

    nome_busca = input("Digite o nome do funcionário que deseja buscar: ").strip()
    if not nome_busca:
        print("Nome para busca não pode ser vazio.")
        return
        
    _, funcionario = buscar_funcionario_pelo_nome(nome_busca)

    if funcionario:
        print("\n--- Funcionário Encontrado ---")
        print(funcionario)
        print("-----------------------------")
    else:
        print(f"Funcionário com nome '{nome_busca}' não encontrado.")


def atualizar_funcionario():
    """
    Modifica as informações de um funcionário existente na lista.
    """
    print("\n--- Atualizar Funcionário ---")
    if not lista_funcionarios:
        print("Nenhum funcionário cadastrado para atualizar.")
        return

    nome_antigo = input("Digite o nome do funcionário que deseja atualizar: ").strip()
    if not nome_antigo:
        print("Nome do funcionário para atualizar não pode ser vazio.")
        return

    indice, funcionario = buscar_funcionario_pelo_nome(nome_antigo)

    if funcionario:
        print(f"\nEditando funcionário: {funcionario}")
        print("Deixe o campo em branco e pressione Enter para manter o valor atual.")

        novo_nome = input(f"Novo nome (atual: {funcionario.nome}): ").strip()
        if novo_nome and novo_nome.lower() != funcionario.nome.lower():
            # Verifica se o novo nome já existe para outro funcionário
            idx_existente, func_existente = buscar_funcionario_pelo_nome(novo_nome)
            if func_existente and idx_existente != indice:
                print(f"Erro: Já existe outro funcionário com o nome '{novo_nome}'. O nome não será alterado.")
            else:
                funcionario.nome = novo_nome
        elif not novo_nome:
            print("Nome mantido.")


        novo_cargo = input(f"Novo cargo (atual: {funcionario.cargo}): ").strip()
        if novo_cargo:
            funcionario.cargo = novo_cargo
        else:
            print("Cargo mantido.")


        while True:
            novo_salario_str = input(f"Novo salário (atual: {funcionario.salario:.2f}): ").strip()
            if not novo_salario_str: # Se deixou em branco, mantém o atual
                print("Salário mantido.")
                break
            try:
                novo_salario = float(novo_salario_str)
                if novo_salario < 0:
                    print("Salário não pode ser negativo. Tente novamente.")
                    continue
                funcionario.salario = novo_salario
                break
            except ValueError:
                print("Salário inválido. Por favor, insira um número.")

        print(f"Funcionário '{funcionario.nome}' atualizado com sucesso!")
    else:
        print(f"Funcionário com nome '{nome_antigo}' não encontrado.")


def excluir_funcionario():
    """
    Remove um funcionário da lista.
    """
    print("\n--- Excluir Funcionário ---")
    if not lista_funcionarios:
        print("Nenhum funcionário cadastrado para excluir.")
        return

    nome_excluir = input("Digite o nome do funcionário que deseja excluir: ").strip()
    if not nome_excluir:
        print("Nome do funcionário para excluir não pode ser vazio.")
        return

    indice, funcionario = buscar_funcionario_pelo_nome(nome_excluir)

    if funcionario:
        print(f"\nFuncionário a ser excluído: {funcionario}")
        confirmacao = input(f"Tem certeza que deseja excluir '{funcionario.nome}'? (s/N): ").strip().lower()
        if confirmacao == 's':
            lista_funcionarios.pop(indice)
            print(f"Funcionário '{funcionario.nome}' excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
    else:
        print(f"Funcionário com nome '{nome_excluir}' não encontrado.")


# --- Menu Principal ---
def exibir_menu():
    """
    Exibe o menu interativo para o usuário.
    """
    print("\n╔═══════════════════════════════════╗")
    print("║   Sistema de Cadastro DENDÊ TECH  ║")
    print("╠═══════════════════════════════════╣")
    print("║ 1. Cadastrar Funcionário          ║")
    print("║ 2. Listar Todos os Funcionários   ║")
    print("║ 3. Buscar Funcionário Específico  ║")
    print("║ 4. Atualizar Funcionário          ║")
    print("║ 5. Excluir Funcionário            ║")
    print("║ 6. Salvar Dados em CSV            ║")
    print("║ 7. Carregar Dados de CSV          ║")
    print("║ 8. Sair                           ║")
    print("╚═══════════════════════════════════╝")

# --- Função Principal (main) ---
def main():
    """
    Função principal que executa o sistema.
    """
    print("Bem-vindo ao Sistema de Cadastro de Funcionários DENDÊ TECH!")
    carregar_dados_csv() # Carrega dados ao iniciar

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção (1-8): ").strip()

        if escolha == '1':
            adicionar_funcionario()
        elif escolha == '2':
            listar_funcionarios()
        elif escolha == '3':
            buscar_funcionario_especifico_interativo()
        elif escolha == '4':
            atualizar_funcionario()
        elif escolha == '5':
            excluir_funcionario()
        elif escolha == '6':
            salvar_dados_csv()
        elif escolha == '7':
            if lista_funcionarios: # Verifica se há dados em memória que podem ser perdidos
                confirm_load = input("Atenção: Carregar dados do CSV irá sobrescrever quaisquer alterações não salvas na memória. Deseja continuar? (s/N): ").strip().lower()
                if confirm_load != 's':
                    print("Carregamento cancelado.")
                    input("\nPressione Enter para continuar...")
                    continue # Volta ao menu
            carregar_dados_csv()
        elif escolha == '8':
            if lista_funcionarios: # Sugere salvar se houver dados
                 # Poderia adicionar uma verificação mais sofisticada de "dados alterados"
                salvar_ao_sair = input("Deseja salvar os dados antes de sair? (s/N): ").strip().lower()
                if salvar_ao_sair == 's':
                    salvar_dados_csv()
            print("Saindo do sistema DENDÊ TECH. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 8.")
        
        input("\nPressione Enter para continuar...") # Pausa para o usuário ler a saída
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela

# --- Execução do Programa ---
if __name__ == "__main__":
    main()