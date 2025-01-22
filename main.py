import httpx
import re
import os

TOKEN = f"Bearer <TOKEN>"
tasks = [
    {"url": "https://network-toolbox.spsapps.net/rsx/v1/schema/7.7.9/Orders/fields/", "output_file": "output/orders.go", "struct_name": "Orders"},
    {"url": "https://network-toolbox.spsapps.net/rsx/v1/schema/7.7.9/OrderAcks/fields/", "output_file": "output/order_acks.go", "struct_name": "OrderAcks"},
    {"url": "https://network-toolbox.spsapps.net/rsx/v1/schema/7.7.9/Shipments/fields/", "output_file": "output/shipments.go", "struct_name": "Shipments"},
    {"url": "https://network-toolbox.spsapps.net/rsx/v1/schema/7.7.9/Invoices/fields/", "output_file": "output/invoices.go", "struct_name": "Invoices"}
]


def to_snake_case(camel_case):
    camel_case = re.sub(r'([a-z])([A-Z])', r'\1_\2', camel_case)
    camel_case = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', camel_case)
    camel_case = re.sub(r'([0-9])([a-zA-Z])', r'\1_\2', camel_case)
    return camel_case.lower()


def generate_go_struct(parsed_data, struct_name="GeneratedStruct"):
    field_type_mapping = {
        "xs:string": "string",
        "xs:decimal": "float64",
        "xs:int": "int64",
        "xs:boolean": "bool",
        "xs:date": "string",
        "xs:time": "string"
    }

    struct_lines = []

    struct_lines.append(f"type {struct_name} struct {{")
    for field in parsed_data:
        json_field = to_snake_case(field['name'])
        go_type = field_type_mapping.get(field["field_type"], "interface{}")
        struct_lines.append(f"    {field['name']} {go_type} `json:\"{json_field}\"`")

    struct_lines.append("}")

    return "\n".join(struct_lines)


async def fetch_and_parse(url):
    headers = {
        "User-Agent": "CustomAgent/1.0",
        "Accept": "application/json",
        "Authorization": TOKEN
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()  # 상태 코드 확인

        # JSON 파싱
        data = response.json()

        # 필요한 정보 추출
        parsed_data = []
        for field in data.get("fields", []):
            field_dict = {
                "name": field.get("name"),
                "field_type": field.get("field_type")
            }
            parsed_data.append(field_dict)

        return parsed_data


# 파일로 저장하는 함수
def save_to_file(content, filename):
    with open(filename, "w") as f:
        f.write(content)


# 비동기 실행을 위한 코드
if __name__ == "__main__":
    import asyncio

    # 출력 디렉토리 생성
    os.makedirs("output", exist_ok=True)


    async def process_tasks():
        for task in tasks:
            try:
                parsed_data = await fetch_and_parse(task["url"])
                go_struct = generate_go_struct(parsed_data, struct_name=task["struct_name"])

                save_to_file(go_struct, task["output_file"])
                print(f"Go struct saved to {task['output_file']}")
            except Exception as e:
                print(f"Failed to process URL {task['url']}: {e}")


    asyncio.run(process_tasks())
