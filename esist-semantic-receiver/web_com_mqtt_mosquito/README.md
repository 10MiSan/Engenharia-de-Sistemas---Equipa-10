# Python MQTT Webapp

Uma aplicação web simples em Python que permite a comunicação entre dois usuários via MQTT broker Mosquitto.

## Estrutura

- `app.py` - servidor Flask local
- `templates/index.html` - escolha de role
- `templates/room.html` - interface de transmitter / receiver
- `mosquitto.conf` - configuração local para WebSocket

## Requisitos

- Python 3.9+
- pip
- Mosquitto broker

## Instalação

1. Crie e ative um ambiente virtual local:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências Python:

```bash
python -m pip install -r requirements.txt
```

3. Instale Mosquitto no seu sistema se ainda não tiver:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

3. Inicie o broker usando a configuração local:

```bash
mosquitto -c mosquitto.conf
```

> O navegador só consegue conectar se o broker Mosquitto estiver rodando e aceitando WebSocket em `ws://localhost:9001`.

## Uso

1. Inicie o servidor Flask:

```bash
python3 app.py
```

2. Abra dois navegadores ou duas abas diferentes:

- `http://localhost:5000`

3. Em cada aba, escolha um role:

- `Transmitter` → `http://localhost:5000/transmitter`
- `Receiver` → `http://localhost:5000/receiver`

4. O transmitter envia mensagens ao broker e o receiver as recebe.

5. O receiver responde automaticamente com a mensagem `Mensagem Recibada`.

## Observações

- O broker Mosquitto é configurado para WebSocket em `ws://localhost:9001`.
- Se precisar usar MQTT puro, adapte o `mosquitto.conf` e o cliente MQTT do navegador.
