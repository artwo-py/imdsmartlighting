import requests
import time
import random

UPDATE_URL = "http://iot-agent:7896/iot/json"
API_KEY = "imdlightingmonitoring2026"
ENTITIES_URL = "http://orion:1026/v2/entities"

def get_lamps():
    params = {
        "type": "Lamp",
        "options": "keyValues"
    }

    headers = {
        "fiware-service": "imdlampservice",
        "fiware-servicepath": "/"
    }

    try:
        res = requests.get(ENTITIES_URL, params=params, headers=headers)
        data = res.json()
        #só envia dados as lamps que estão ativas
        return [
            entity["id"]
            for entity in data
            if entity.get("active", True) is True
        ]
    except Exception as e:
        print("Erro ao buscar lâmpadas:", e)
        return []
    
def simulate():
    print("Iniciando simulador...")

    while True:
        lamp_ids = get_lamps()

        for entity_id in lamp_ids:
            device_id = device_id = entity_id.lower()
            # 0-400 = noite | 401 - 800 = dia
            ambient_light = random.randint(0, 800) 
            motion = random.choice([True, False])
            active = True
            payload = {
                "al": ambient_light,
                "md": motion,
                "act": active
            }
            url = f"{UPDATE_URL}?i={device_id}&k={API_KEY}"
            try:
                requests.post(url, json=payload)
                print(f"{device_id} → ambient={ambient_light}, motion={motion}, active={active}")
            except Exception as e:
                print("Erro:", e)

        print("---- aguardando próxima rodada ----\n")
        time.sleep(15)

if __name__ == "__main__":
    simulate()