Python version: `3.6.15`

##### Após criar ambiente virtual, instale as dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
``` 


##### Criar uma cópia do arquivo na pasta `intranet` e parametrizar suas variáveis locais:
`local_settings_example.py` para `local_settings.py`

##### Instalar redis-server
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis
```

##### Executar o Celery localmente
```bash
celery -A intranet worker -B -l info
```

##### Executar o backend
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 

##### Criar superusuário
```bash
python manage.py createsuperuser --username=SEU_USERNAME --email=SEU_EMAIL
# Aguardar e digitar a senha no terminal
```

##### Executar o frontend
`$ cd frontend`
```bash
npm install
npm run serve
``` 

##### Subir Container banco de dados
```bash
docker-compose up -d myintradb
```

##### Apps
###### Agendamento
- Gerenciamento de reservas de espaços

###### Atendimento
- Serviço de Fila de Atendimentos 
- Ambiente de atendimento do atendente
- Triagem/Emissõ de senha
- Painel - Chamada de Senhas

###### Cofre de senhas (Django admin)
- Registros de senhas (criptografadas)

###### Infraestrutura
- Monitoramento de resposta sobre a requisições web
- Circulação de materiais - controle de uso de equipamentos (entradas e saídas)

###### Local Notifications
- Notificação em tela inicial no formato de slides

###### Repositório de dados (embed URLs)
- Criação de Modais para exibição de hyperlinks embutidos

###### Users
- Gerenciamento de usuários, Perfis e Permissões

###### Wiki
- Documentações e Tutoriais em formatação HTML

##### Adds ambiente Linux
- Instalar locale pt_BR.utf8
- Comando ```locale``` pra listar o locale atual
- Comando ```locale -a``` pra listar os disponíveis
- Se não existir o locale pt_BR, instalar: ```locale-gen pt_BR.UTF-8```
- Reconfigurar após o pacote estar instalado:
```
dpkg-reconfigure locales
```
- Atualizar locale padrão:
```
update-locale LANG=pt_BR.UTF-8
```
- Consultar o valor definido em LANG:
```
cat /etc/default/locale
```
