import json

objeto = open("data/settings.json")
datos = json.load(objeto)
print(datos["target_ip"])
