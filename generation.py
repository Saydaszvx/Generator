# Минимальный генератор опросов на основе LLM

import os
import json
from openai import OpenAI  # pip install openai

client = OpenAI()

def generate_survey(user_journey: str, categories: list[str]) -> dict:
    prompt = f"""
Ты — генератор персонализированных опросов удовлетворённости сервисом.

На основе клиентского пути пользователя:
{user_journey}

Возможные категории опроса:
{json.dumps(categories, ensure_ascii=False)}

Задача:
1. Определи категорию опроса из списка выше.
2. Сгенерируй 3–5 релевантных вопросов для оценки удовлетворённости.
3. Верни результат строго в формате JSON:
   {{"category": "название_категории", "questions": ["вопрос1", "вопрос2", ...]}}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # или другая модель
        messages=[
            {"role": "system", "content": "Ты помощник для генерации опросов."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}  # для моделей с поддержкой JSON
    )

    result = json.loads(response.choices[0].message.content)
    return result

# Пример использования
if __name__ == "__main__":
    # Обезличенный клиентский путь (пример)
    user_journey_example = """
    Пользователь зашёл на сайт бизнес-портала, авторизовался, 
    посмотрел тарифы, перешёл в раздел поддержки, 
    задал вопрос через чат, получил ответ через 2 минуты, 
    открыл счёт для бизнеса, но не завершил открытие.
    """

    categories_example = [
        "Скорость работы сервиса",
        "Качество поддержки",
        "Простота открытия счёта",
        "Понятность тарифов",
        "Общая удовлетворённость"
    ]

    survey = generate_survey(user_journey_example, categories_example)
    print("Сгенерированный опрос:")
    print(json.dumps(survey, ensure_ascii=False, indent=2))
