import inquirer

class Robo:
    def __init__(self):
        self.posicao = {"x": 0, "y": 0, "z": 0}
        self.ferramenta_ligada = False

    def home(self):
        self.posicao = {"x": 0, "y": 0, "z": 0}
        return "Robô retornou à posição inicial."

    def ligar_ferramenta(self):
        self.ferramenta_ligada = True
        return "Ferramenta ligada."

    def desligar_ferramenta(self):
        self.ferramenta_ligada = False
        return "Ferramenta desligada."

    def mover(self, eixo, distancia):
        if eixo.lower() in ["x", "y", "z"]:
            self.posicao[eixo.lower()] += distancia
            return f"Robô movido {distancia} unidades no eixo {eixo}."
        else:
            return "Eixo inválido. Use 'x', 'y' ou 'z'."

    def atual(self):
        return f"Posição atual do robô: {self.posicao}, Ferramenta ligada: {self.ferramenta_ligada}"


def execute_comando(robo, comando):
    if comando == "home":
        return robo.home()
    elif comando == "ligar_ferramenta":
        return robo.ligar_ferramenta()
    elif comando == "desligar_ferramenta":
        return robo.desligar_ferramenta()
    elif comando == "mover":
        eixo = inquirer.prompt([inquirer.List("eixo", message="Escolha o eixo", choices=["x", "y", "z"])])["eixo"]
        distancia = inquirer.prompt([inquirer.Text("distancia", message="Digite a distância")])["distancia"]
        return robo.mover(eixo, int(distancia))
    elif comando == "atual":
        return robo.atual()
    else:
        return "Comando inválido."


if __name__ == "__main__":
    robo = Robo()

    while True:
        perguntas = [
            inquirer.List("comando", message="Escolha um comando", choices=["home", "ligar_ferramenta", "desligar_ferramenta", "mover", "atual", "sair"])
        ]

        resposta = inquirer.prompt(perguntas)

        if resposta["comando"] == "sair":
            break

        resultado = execute_comando(robo, resposta["comando"])
        print(resultado)
