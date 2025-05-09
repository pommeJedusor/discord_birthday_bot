import http.client

def main():
    exit_code = 0
    domain = "magical-square.chesspomme.com"
    paths = ["/en"]
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
        else:
            print(f"status 200")
            print(f"output: {content}")
        print()
    conn.close()
    exit(exit_code)

main()
