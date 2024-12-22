import re


class StringsToolKit:
    @staticmethod
    def normalize_string(data: str) -> str:
        # print(f"Before normalize: {data}")
        data = data.lower()
        # Заменяем все символы, кроме букв, цифр и пробелов, на "-"
        normalized = re.sub(r"[^\w\s]", "-", data)
        # Заменяем пробелы на "-"
        normalized = re.sub(r"\s+", "-", normalized)

        # print(f"After normalize: {normalized}")
        # Приводим строку к нижнему регистру
        return normalized

