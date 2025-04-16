import os
import json
from openai import OpenAI


def get_user_input():
    print("환영합니다! 혁신적인 음료 및 디저트 레시피 생성기를 사용해 주셔서 감사합니다.")

    weather_options = ["맑음", "흐림", "비", "눈", "더움", "추움"]
    print("\n현재 날씨를 선택해 주세요:")
    for i, weather in enumerate(weather_options, 1):
        print(f"{i}. {weather}")
    weather_choice = int(input("옵션 번호를 입력해 주세요: "))
    weather = weather_options[weather_choice - 1]

    season_options = ["봄", "여름", "가을", "겨울"]
    print("\n현재 계절을 선택해 주세요:")
    for i, season in enumerate(season_options, 1):
        print(f"{i}. {season}")
    season_choice = int(input("옵션 번호를 입력해 주세요: "))
    season = season_options[season_choice - 1]

    type_options = ["밀크티", "과일 차", "케이크"]
    print("\n원하는 제품 유형을 선택해 주세요:")
    for i, type_option in enumerate(type_options, 1):
        print(f"{i}. {type_option}")
    type_choice = int(input("옵션 번호를 입력해 주세요: "))
    product_type = type_options[type_choice - 1]

    customization = {}
    if product_type in ["밀크티", "과일 차"]:
        print("\n당도를 선택해 주세요:")
        sweetness_options = ["무설탕", "반당", "보통당"]
        for i, sweet in enumerate(sweetness_options, 1):
            print(f"{i}. {sweet}")
        sweetness_choice = int(input("옵션 번호를 입력해 주세요: "))
        customization["sweetness"] = sweetness_options[sweetness_choice - 1]

        print("\n온도를 선택해 주세요:")
        temp_options = ["상온", "얼음 없음", "보통 얼음"]
        for i, temp in enumerate(temp_options, 1):
            print(f"{i}. {temp}")
        temp_choice = int(input("옵션 번호를 입력해 주세요: "))
        customization["temperature"] = temp_options[temp_choice - 1]

    special_requests = input("\n특별 요청 사항이 있으면 입력해 주세요 (없으면 엔터를 눌러 건너뛰기): ")

    return {
        "weather": weather,
        "season": season,
        "product_type": product_type,
        "customization": customization,
        "special_requests": special_requests
    }


# 혼원 API를 사용하여 혁신적인 레시피 생성
def generate_recipe(params):
    client = OpenAI(
        api_key=os.environ.get("HUNYUAN_API_KEY"),
        base_url="https://api.hunyuan.cloud.tencent.com/v1",
    )

    customization_str = ""
    if params['product_type'] in ["밀크티", "과일 차"]:
        customization_str = f"당도: {params['customization']['sweetness']}, 온도: {params['customization']['temperature']}"

    prompt = f"""
    다음 정보를 기반으로 혁신적인 {params['product_type']} 레시피를 생성하고, 아래 JSON 형식으로 출력해 주세요:

    입력 정보:
    - 날씨: {params['weather']}
    - 계절: {params['season']}
    - 제품 유형: {params['product_type']}
    - 맞춤 요구 사항: {customization_str}
    - 특별 요청: {params['special_requests'] if params['special_requests'] else '없음'}

    JSON 형식으로 반환해 주세요:
    {{
        "name": "제품 이름",
        "description": "제품 간단 설명 (50자 이내)",
        "ingredients": [
            {{"item": "재료 이름", "amount": "용량", "unit": "단위"}},
        ],
        "steps": [
            "단계1",
            "단계2",
            "단계3"
        ],
        "seasonal_reason": "현재 날씨와 계절에 적합한 이유 (50자 이내)",
        "selling_points": [
            "판매 포인트1",
            "판매 포인트2"
        ]
    }}

    유효한 JSON 형식으로 반환하고, 모든 한글은 UTF-8 인코딩을 사용해 주세요. 레시피는 실현 가능하고 상업적 제작에 적합해야 합니다.
    """

    completion = client.chat.completions.create(
        model="hunyuan-turbos-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        extra_body={
            "enable_enhancement": True,
        },
    )
    return completion.choices[0].message.content


# 생성된 레시피 JSON 데이터를 표준 레시피 형식으로 변환
def format_recipe_output(recipe_data):
    output = []

    output.append(f"【제품 이름】{recipe_data['name']}")
    output.append(f"【제품 설명】{recipe_data['description']}")
    output.append("")

    output.append("【재료 목록】")
    for ingredient in recipe_data['ingredients']:
        output.append(f"- {ingredient['item']}: {ingredient['amount']}{ingredient['unit']}")
    output.append("")

    output.append("【제작 단계】")
    for i, step in enumerate(recipe_data['steps'], 1):
        output.append(f"{i}. {step}")
    output.append("")

    output.append(f"【계절 적합성】{recipe_data['seasonal_reason']}")
    output.append("")

    output.append("【특징 및 장점】")
    for point in recipe_data['selling_points']:
        output.append(f"- {point}")
    output.append("")

    return "\n".join(output)


def main():
    os.environ['HUNYUAN_API_KEY'] = 'sk-CcsGmxDjyV8PTsFADBhXZyR5DLjJNLt60XaTJciQjbg0IQEM'

    params = get_user_input()
    print("\n혁신적인 레시피를 생성 중입니다. 잠시 기다려 주세요...")
    recipe = generate_recipe(params)

    print(recipe)

    recipe = recipe[7:-3]
    print(recipe)
    recipe = json.loads(recipe)

    recipe = format_recipe_output(recipe)
    print("\n===== 생성된 혁신 레시피 =====\n")
    print(recipe)


if __name__ == "__main__":
    main()