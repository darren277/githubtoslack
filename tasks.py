""""""
from celery import Celery
import json
import requests
import openai
from settings import LLM_API_KEY
from llm.tools.op import search_wiki_tool, search_wiki
from llm.tools.op import create_work_package_tool, create_work_package
from llm.tools.op import provide_work_package_output, WorkPackageOutput
from pydantic import ValidationError

celery = Celery("app", broker="amqp://guest@localhost//")

def my_llm_call(prompt: str):
    import openai
    import asyncio

    client = openai.OpenAI(api_key=LLM_API_KEY)

    model = 'gpt-4o-mini'

    messages = [
        {"role": "system", "content": "You are a helpful expert project management assistant."},
        {"role": "user", "content": prompt},
    ]

    result = client.chat.completions.create(model=model, messages=messages, tools=[search_wiki_tool, create_work_package_tool, provide_work_package_output], tool_choice='auto')

    print('result:', result)

    if not result:
        return jsonify({"response_type": "ephemeral", "text": "Error calling LLM endpoint"}), 500

    #response = result.choices[0].message.content
    choices = result.choices
    top_choice = choices[0]
    tool_calls = top_choice.message.tool_calls

    if not tool_calls:
        return top_choice.message.content

    loop = asyncio.get_event_loop()

    for tool_call in tool_calls:
        print('tool_call:', tool_call)
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == 'search_wiki':
            if loop.is_running(): tool_result = asyncio.ensure_future(search_wiki(**arguments))
            else: tool_result = loop.run_until_complete(search_wiki(**arguments))
            content = json.dumps(tool_result)
        elif function_name == 'create_work_package':
            if loop.is_running(): tool_result = asyncio.ensure_future(create_work_package(**arguments))
            else: tool_result = loop.run_until_complete(create_work_package(**arguments))
            content = json.dumps(tool_result)
        elif function_name == 'provide_work_package_output':
            try:
                structured_data = WorkPackageOutput.parse_obj(arguments)
                print("Parsed structured data:", structured_data)
                content = "Successfully parsed output. Now saving to OpenProject...\n"
                if loop.is_running(): tool_result = asyncio.ensure_future(create_work_package(**structured_data))
                else: tool_result = loop.run_until_complete(create_work_package(**structured_data))
                content += json.dumps(tool_result)
            except ValidationError as ve:
                raise Exception(f"LLM output validation failed: {ve}")
        else:
            raise Exception(f'Unknown function name: {function_name}')

        messages.append({"role": "function", "name": function_name, "content": content})

    print("ABOUT TO CALL SECOND TIME")
    result = client.chat.completions.create(model=model, messages=messages, tools=[search_wiki_tool, create_work_package_tool, provide_work_package_output], tool_choice='auto')

    print('result:', result)

    print("ABOUT TO RETURN")

    return result.choices[0].message.content


@celery.task
def process_llm(prompt, response_url):
    # 1) Call LLM (this might take a while)
    # (Placeholder code. Adjust to your own LLM library.)
    result_text = my_llm_call(prompt)

    # 2) Use the Slack response_url to POST the final answer
    payload = {
        "response_type": "in_channel",  # or "ephemeral"
        "text": result_text
    }
    requests.post(response_url, json=payload)
