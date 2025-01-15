import json
import numpy as np


def handle_results(
        results,
        MBTI_file_path="MBTI.json",
        MMPI_file_path="MMPI.json",
        MBTILinks_file_path="MBTILinks.json",
        MMPILinks_file_path="MMPILinks.json"
):
    try:
        with (open(MBTI_file_path, "r", encoding="utf-8") as MBTI_json,
              open(MMPI_file_path, "r", encoding="utf-8") as MMPI_json,
              open(MBTILinks_file_path, "r", encoding="utf-8") as MBTILinks_json,
              open(MMPILinks_file_path, "r", encoding="utf-8") as MMPILinks_json):

            MBTI_dict = json.load(MBTI_json)
            MMPI_dict = json.load(MMPI_json)
            MBTILinks_dict = json.load(MBTILinks_json)
            MMPILinks_dict = json.load(MMPILinks_json)
            answer = []
            for result in results:
                MBTI = MBTI_dict.get(str(result[0]))
                MMPI = MMPI_dict.get(str(result[1]))
                MBTILink = MBTILinks_dict.get(MBTI)
                MMPILink = MMPILinks_dict.get(MMPI)
                answer.append((MBTI, MMPI, MBTILink, MMPILink, result[2]))
            return answer
    except FileNotFoundError:
        print("Файл не найден!")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON!")
        return []


if __name__ == "__main__":
    print(handle_results([[0, 10], [2, 9]]))