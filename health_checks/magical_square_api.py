import http.client

def main():
    exit_code = 0
    domain = "api-magical-square.chesspomme.com"
    paths = ["/get_moves/1", "/get_path/0"]
    expectations = [
        "[3, 30]",
        "[0, 3, 6, 9, 39, 36, 33, 30, 60, 63, 66, 69, 99, 96, 93, 90, 72, 75, 78, 48, 18, 15, 12, 42, 45, 67, 97, 94, 91, 61, 64, 34, 37, 7, 4, 1, 31, 53, 56, 86, 89, 59, 29, 26, 23, 20, 50, 80, 83, 65, 68, 98, 95, 92, 62, 32, 2, 5, 8, 38, 35, 17, 14, 11, 41, 71, 74, 77, 47, 44, 22, 25, 28, 58, 88, 85, 82, 52, 55, 73, 70, 40, 10, 13, 16, 19, 49, 79, 76, 46, 43, 21, 24, 27, 57, 54, 51, 81, 84, 87]"
    ]
    conn = http.client.HTTPSConnection(domain)
    print("-- domain:", domain)
    for i, path in enumerate(paths):
        print("path:", path)
        conn.request("GET", path)
        res = conn.getresponse()
        content = res.read().decode(encoding="utf-8")
        if res.status != 200:
            print(f"status not 200 but {res.status}")
            print(f"output: {content}")
            exit_code = 1
        elif content != expectations[i]:
            print(f"status 200 but wrong content")
            print(f"expected: {expectations[i]}")
            print(f"but got: {content}")
            exit_code = 1
        else:
            print(f"status 200")
            print(f"output: {content}")
        print()
    conn.close()
    exit(exit_code)

main()
