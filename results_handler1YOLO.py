import json
import numpy as np


def handle_results(
        results,
        metrics_file_path="metrics.json",
        MBTILinks_file_path="MBTILinks.json",
        MMPILinks_file_path="MMPILinks.json"
):
    try:
        with (open(metrics_file_path, 'r', encoding='utf-8') as metrics,
              open(MBTILinks_file_path, "r", encoding="utf-8") as MBTILinks_json,
              open(MMPILinks_file_path, "r", encoding="utf-8") as MMPILinks_json):
            metrics = json.load(metrics)
            MBTILinks_dict = json.load(MBTILinks_json)
            MMPILinks_dict = json.load(MMPILinks_json)
            answer = []
            for result in results:
                MBTI_MMPI = metrics.get(str(result[0] + 1)).split()
                MBTI, MMPI = f'{MBTI_MMPI[0]} {MBTI_MMPI[1]}', MBTI_MMPI[2]
                MBTILink = MBTILinks_dict.get(MBTI)
                MMPILink = MMPILinks_dict.get(MMPI)
                answer.append((MBTI, MMPI, MBTILink, MMPILink, result[1]))
            return answer
    except FileNotFoundError:
        print("Файл не найден!")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON!")
        return []


if __name__ == "__main__":
    print(handle_results([[0, 10], [2, 9]]))