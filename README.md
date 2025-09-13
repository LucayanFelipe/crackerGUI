# 1. Criar a máquina virtual

Baixe uma ISO de Ubuntu Desktop (ou outra distro Linux de sua escolha).
No VirtualBox, crie uma nova VM:
Tipo: Linux
Versão: Ubuntu (64-bit)
Memória RAM: pelo menos 2GB
Disco: 20GB dinâmico
Monte a ISO no Optical Drive da VM e inicie a instalação.
Instale o sistema normalmente.

# 2. Atualizar o sistema

Após logar no Ubuntu, abra o terminal:
sudo apt update && sudo apt upgrade -y

# 3. Instalar dependências básicas

Você vai precisar de Python, pip, Tkinter e compiladores básicos:
sudo apt install -y python3 python3-venv python3-tk python3-dev build-essential

# 4. Criar a pasta do projeto

mkdir ~/zipcracker
cd ~/zipcracker
coloque aqui o programa zipcracker.py

# 5. Criar e ativar o ambiente virtual (venv)

python3 -m venv venv
Ative:
source venv/bin/activate
Agora o terminal vai mostrar algo tipo (venv) no começo → significa que você está dentro do ambiente virtual.

# 6. Instalar dependências no venv

Dentro do venv instale:
pip install --upgrade pip
pip install pyzipper

# 7. Rodar o programa

Dentro do venv rode o programa:
python3 zipcracker.py

# 8. Usando o programa

Clique em Selecionar ZIP → escolha o arquivo .zip protegido por senha.
Clique em Adicionar Dicionário → selecione um arquivo .txt contendo as senhas (uma por linha).
Pode adicionar vários dicionários.
Clique em Iniciar Ataque.
A barra de progresso vai atualizar e você vai ver a senha testada em tempo real.
Se encontrar, aparece a mensagem:
👉 "Hackeado com sucesso meu patrão, senha do arquivo: {senha}"
