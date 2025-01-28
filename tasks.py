""""""
from celery import Celery
import requests
import openai

celery = Celery("my_app", broker="amqp://guest@localhost//")  # or redis

def my_llm_call(prompt: str):
    import openai

    client = openai.OpenAI(api_key=LLM_API_KEY)

    model = 'gpt-4o-mini'

    messages = [
        {"role": "system", "content": "You are a helpful expert project management assistant."},
        {"role": "user", "content": prompt},
    ]

    result = client.chat.completions.create(model=model, messages=messages)

    print('result:', result)

    if not result:
        return jsonify({"response_type": "ephemeral", "text": "Error calling LLM endpoint"}), 500

    response = result.choices[0].message.content

    if not response:
        return "No response from LLM"

    return response


@celery.task
def process_llm(prompt, response_url):
    # 1) Call LLM (this might take a while)
    # (Placeholder code. Adjust to your own LLM library.)
    result_text = my_llm_call(prompt)

    # 2) Use the Slack response_url to POST the final answer
    payload = {
        "response_type": "ephemeral",  # or "in_channel"
        "text": result_text
    }
    requests.post(response_url, json=payload)
