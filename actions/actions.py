from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


def get_weather(city: str):
    """Consulta a WeatherAPI e retorna os dados de clima da cidade."""
    try:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": "SUA_CHAVE_AQUI",  # <-- Substitua pela sua chave da WeatherAPI
            "q": city,
            "aqi": "no"
        }
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erro ao consultar a API: {e}")
        return None


class ActionInformaClima(Action):

    def name(self) -> Text:
        return "action_informa_clima"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Tenta pegar a entidade "city" extraída pelo Rasa
        city = next(tracker.get_latest_entity_values("city"), None)

        # Se não encontrou entidade, usa o texto bruto como fallback
        if not city:
            city = tracker.latest_message.get("text")

        print(f"[DEBUG] Cidade capturada: {city}")

        # Consulta a API de clima
        weather_data = get_weather(city)

        # Monta a resposta
        if weather_data and "current" in weather_data:
            temp_c = weather_data["current"]["temp_c"]
            location = weather_data["location"]["name"]
            country = weather_data["location"]["country"]
            condition = weather_data["current"]["condition"]["text"]
            message = (
                f"🌡️ O clima em {location}, {country}:\n"
                f"Temperatura: {temp_c}°C\n"
                f"Condição: {condition}"
            )
        else:
            message = (
                "Desculpe, não consegui obter informações do clima para essa cidade. "
                "Verifique o nome da cidade e tente novamente."
            )

        dispatcher.utter_message(text=message)
        return []