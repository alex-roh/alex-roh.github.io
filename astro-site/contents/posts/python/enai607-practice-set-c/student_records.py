"""문제 7: 중첩 자료구조, 얕은 복사, 튜플 키와 기본 정렬."""


def create_students():
    students = [
        {"name": "Jodie", "grades": ["A", "A-", "B"]},
        {"name": "Paul", "grades": ["C", "B", "B"]},
        {"name": "Krissie", "grades": ["A-", "A", "B", "A+", "A"]},
        {"name": "Peter", "grades": ["D", "XF"]},
    ]
    # [P7.1-A] 리스트 -> 딕셔너리 -> 성적 리스트 순서로 찾아간다.
    students[2]["grades"].append("A")
    # [P7.1-B] 오른쪽 두 값을 먼저 구한 뒤 왼쪽 두 자리에 교환한다.
    grades = students[1]["grades"]
    grades[0], grades[1] = grades[1], grades[0]
    # [P7.1-C] 삽입 전 Krissie의 인덱스는 2다. 삽입 후에는 3이 된다.
    students.insert(2, {"name": "Joel", "grades": ["A", "C", "B", "B"]})
    return students


def demonstrate_copies(students):
    # [P7.2-A] 바깥 리스트만 새로 만든다. 내부 딕셔너리는 공유한다.
    backup = students.copy()
    backup[0]["grades"][0] = "B+"
    print("Original first grade after nested edit:", students[0]["grades"][0])
    # 공유 딕셔너리 안의 공유 성적 리스트를 수정했으므로 원본에도 보인다.
    old_name = students[0]["name"]
    # [P7.2-B] 이번에는 backup의 0번 칸이 가리키는 대상을 바꾼다.
    backup[0] = {"name": "Replacement", "grades": ["C"]}
    print("Original name changed:", students[0]["name"] != old_name)
    # [P7.2-C] 매번 새 딕셔너리와 새 성적 리스트를 만들어 공유를 끊는다.
    independent = [
        {"name": record["name"], "grades": record["grades"].copy()}
        for record in students
    ]
    independent[0]["grades"][0] = "A+"
    print("Independent first grade:", independent[0]["grades"][0])
    print("Original first grade:", students[0]["grades"][0])
    print("students is backup:", students is backup)
    # is는 같은 객체인지, ==는 값이 같은지를 비교한다.
    return backup, independent


def create_accounts():
    accounts = {
        ("joe", 786): 123456,
        ("jill", 545): 444567,
        ("ted", 346): 578345,
        ("gwen", 172): 771988,
    }
    # [P7.3] 키는 문자열 두 개가 아니라 (문자열, 정수) 튜플 하나다.
    print("Jill account:", accounts[("jill", 545)])
    print("(joe, 172) present:", ("joe", 172) in accounts)
    accounts[("ted", 346)] = 576644
    accounts[("sasha", 988)] = 111111
    del accounts[("gwen", 172)]
    print("Remaining accounts:", len(accounts))
    return accounts


def sort_products():
    products = [("widget", 5.28), ("gadget", 10.44),
                ("widget", 5.55), ("cool stuff", 6.87)]
    # [P7.4] 첫 원소(이름)부터 비교하고, 같으면 다음 원소(가격)를 비교한다.
    products.sort()
    return products


def main():
    students = create_students()
    print("Student count:", len(students))
    third = students[2]  # 세 번째 학생은 인덱스 2: 원문의 Joel 예시와 일치한다.
    print("Third student:", third["name"], "grade count:", len(third["grades"]))
    print("Paul grades:", students[1]["grades"])
    print("Krissie grades:", students[3]["grades"])
    demonstrate_copies(students)
    create_accounts()
    print("Sorted products:", sort_products())


if __name__ == "__main__":
    main()
