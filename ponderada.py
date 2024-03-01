from serial.tools import list_ports
import inquirer
import pydobot  
from yaspin import yaspin

# Traz o spinner para apresentar uma animação enquanto o robô está se movendo
spinner = yaspin(text="Processando...", color="blue")

# Listas as portas seriais disponíveis
available_ports = list_ports.comports()
porta_escolhida = inquirer.prompt([
    inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])
])["porta"]
# Cria uma instância do robô
device = pydobot.Dobot(port=porta_escolhida, verbose=False)

device.speed(100, 100)

choices = ["home", "mover", "posicao_atual", "sair"]
coords = device.pose()
    

def execute_comando(comando):
    match comando:
        case "home":
            spinner.start()
            device.move_to_J(240.53, 0, 150.23, 0, wait=True)
            spinner.stop()
            return "Robô retornou à posição inicial."
        case "ligar_ferramenta":
                device.suck(True)
                choices.remove("ligar_ferramenta")
                choices.insert(1, "desligar_ferramenta")
                return "Ferramenta ligada."
        case "desligar_ferramenta":
                device.suck(False)
                choices.remove("desligar_ferramenta")
                choices.insert(1, "ligar_ferramenta")
                return "Ferramenta desligada."
        case "mover":
            distancia_x = inquirer.prompt([inquirer.Text("distancia_x", message="Distância no eixo X")])["distancia_x"]
            distancia_y = inquirer.prompt([inquirer.Text("distancia_y", message="Distância no eixo Y")])["distancia_y"]
            distancia_z = inquirer.prompt([inquirer.Text("distancia_z", message="Distância no eixo Z")])["distancia_z"]
            
            nova_posicao_x = coords[0] + float(distancia_x)
            nova_posicao_y = coords[1] + float(distancia_y)
            nova_posicao_z = coords[2] + float(distancia_z)

            spinner.start()
            device.move_to(nova_posicao_x, nova_posicao_y, nova_posicao_z, 0, wait=True)
            spinner.stop()
            return f"Robô movido para a posição {device.pose()}."
         
        case "posicao_atual":
            return f"Posição atual do robô: {device.pose()}"
        case _:
            return "Comando inválido."


if __name__ == "__main__":
    choices.insert(1, "ligar_ferramenta")

    questions = [
        inquirer.List('action',
                      message="Escolha a ação",
                      choices=choices,
                      ),
    ]
    while True:
        perguntas = [
        inquirer.List("comando", message="Escolha um comando", choices=choices)
    ]
        resposta = inquirer.prompt(perguntas)
        if resposta["comando"] == "sair":
            break

        resultado = execute_comando(resposta["comando"])
        print(resultado)
        
