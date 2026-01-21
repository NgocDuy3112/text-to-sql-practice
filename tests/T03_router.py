"""
Tester cho phần thực hành 03 - Router phân định luồng xử lý.
Chạy tester:
  + Tại thư mục dự án.
  + Chạy lệnh `python -m tests.T03_router`.
"""

# from implements import route_question
from implements.P03_router import route_question
from tests.test_data import ROUTER_DATA


def main():
    false_outputs = []

    for data in ROUTER_DATA:
        output = route_question(data["question"])
        if output != data["expected"]:
            false_outputs.append(
                {
                    "question": data["question"],
                    "expected": data["expected"],
                    "got": output
                }
            )

    n_total = len(ROUTER_DATA)
    n_correct = n_total - len(false_outputs)
    n_prop = n_correct / n_total * 100

    print(f"Kết quả đúng mong đợi: {n_correct}/{n_total} ({n_prop:.2f}%)")

    if false_outputs:
        print("\n>>> Các câu phân loại sai <<<")
        for e in false_outputs:
            print(f"\n> Câu hỏi: {e['question']}")
            print(f"  Mong đợi: {e['expected']}")
            print(f"  Kết quả thật: {e['got']}")


if __name__ == "__main__":
    main()