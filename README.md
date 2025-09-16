# acadêmicos
Lucayan Felioe Teixeira da Silva    
Theo Theodoro Novais

# 1. Criar a máquina virtual

Baixe uma ISO de Ubuntu Desktop (ou outra distro Linux de sua escolha).
No VirtualBox, crie uma nova VM:
Tipo: Linux
Versão: Other linux (64-bit)
Memória RAM: pelo menos 2GB
Disco: 20GB dinâmico
Monte a ISO no Optical Drive da VM e inicie a instalação.
Instale o sistema normalmente.

# 2. Atualizar o sistema

Após logar no linux, abra o terminal:
sudo apt update && sudo apt upgrade -y

# 3. Instalar dependências básicas

Você vai precisar de Python, pip, Tkinter e compiladores básicos, use os comandos no cli:   
sudo apt install -y python3 python3-     venv python3-tk python3-dev build-essential

# 4. Criar a pasta do projeto

coloque o programa zipcracker.py na mesma raiz do arquivo zip que deseja quebrar

# 5. Criar e ativar o ambiente virtual (venv)

python3 -m venv venv    
source venv/bin/activate

Agora o terminal vai mostrar algo tipo (venv) no começo → significa que você está dentro do ambiente virtual.

# 6. Instalar dependências no venv

Dentro do venv instale:
pip install --upgrade pip   
pip install pyzipper

# 7. criar um zip com senha para testar

baixe o p7zip para zipar:   
sudo apt install p7zip-full

no terminal compacte o arquivo usando:  
7z a -tzip -mem=AES256 -pSENHAAQUI archive.zip file1.txt  
-p : adicione sua senha
archive.zip: nome do zip
file1.txt: o arquivo que vc deseja compactar (tem que estar no diretório atual)

# 8. Rodar o programa

Dentro do venv rode o programa:   
python3 zipcracker.py

# 9. Usando o programa

Clique em Selecionar ZIP → escolha o arquivo .zip protegido por senha.
Clique em Adicionar Dicionário → selecione um arquivo .txt contendo as senhas (uma por linha).
Pode adicionar vários dicionários.
Clique em Iniciar Ataque.
A barra de progresso vai atualizar e você vai ver a senha testada em tempo real.
Se encontrar, aparece a mensagem:
👉 "Hackeado com sucesso meu patrão, senha do arquivo: {senha}"

# 10. executar na Maquina virtual

Lembre-se de executar via VENV toda vez que precisar executar:     
python3 -m venv venv      
source venv/bin/activate   
