import os
from groq import Groq
from groq.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam
)

_GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not _GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY env variable is not set")
client = Groq(api_key=_GROQ_API_KEY)

BASE_PROMPTS = {
    "tg": "Напиши структурированный пост для Telegram-канала на основе тезисов юзера. Разбей на короткие абзацы. В конце добавь призыв к действию.",
    "vk": "Напиши дружелюбный пост для группы ВКонтакте на основе тезисов юзера. Добавь в конец 3-5 хэштегов.",
    "seo_site": "Напиши информационную статью для сайта. Используй подзаголовки H2, H3 и маркированные списки. Упор на пользу."
}

REWRITE_PROMPT = """
Ты — гениальный, харизматичный редактор с отличным чувством юмора и легкой иронией. 
Твоя задача — полностью переписать предоставленный сухой текст, сделав его ЖИВЫМ, сочным и вовлекающим.

ПРАВИЛА ОЖИВЛЕНИЯ:
1. Выкинь нахрен канцелярские штампы, маркеры робота ('В современном мире...', 'Важно отметить...', 'Уникальное решение').
2. Пиши так, будто рассказываешь это хорошему другу в баре за стаканом сока. Простым, понятным, но экспертным языком.
3. Добавь динамики: сочные глаголы, короткие предложения, классные метафоры.
4. Сохрани исходную структуру (абзацы, списки, призывы), которую сделал первый робот, но перепиши сами слова.
5. Если текст для Telegram — аккуратно расставь редкие эмодзи как визуальные якоря (не чаще 1 на абзац).
"""


def generate_smm_content(platform_type: str, user_topic: str) -> str:
    if platform_type not in BASE_PROMPTS:
        return "Ошибка: Неверный тип платформы."

    try:
        # === ЭТАП 1: Базовая генерация ===
        messages_step1 = [
            ChatCompletionSystemMessageParam(role="system", content=BASE_PROMPTS[platform_type]),
            ChatCompletionUserMessageParam(role="user", content=user_topic)
        ]

        first_step = client.chat.completions.create(
            messages=messages_step1,
            model="qwen/qwen3-32b",
            temperature=0.4,
            max_tokens=1500
        )
        # ИСПРАВЛЕНО: Добавлен индекс [0] для извлечения первого choice из списка
        dry_text = first_step.choices[0].message.content

        # === ЭТАП 2: Сочный рерайт ===
        messages_step2 = [
            ChatCompletionSystemMessageParam(role="system", content=REWRITE_PROMPT),
            ChatCompletionUserMessageParam(role="user",
                                           content=f"Вот сухой текст, сделай его живым и сочным:\n\n{dry_text}")
        ]

        final_step = client.chat.completions.create(
            messages=messages_step2,
            model="qwen/qwen3-32b",
            temperature=0.85,
            max_tokens=2048
        )
        # ИСПРАВЛЕНО: Добавлен индекс [0] для извлечения первого choice из списка
        answer = final_step.choices[0].message.content
        if answer is None or len(answer.strip()) == 0:
            answer = "NO CONTENT"
        return answer

    except Exception as e:
        return f"Ошибка конвейера генерации Qwen3: {str(e)}"