import requests
import base64
import sys

# Введите ваш персональный токен доступа сюда
TOKEN = "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"


def get_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Authorization": f"token {TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
    # if True:
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return content
    else:
        print("Error")
        sys.exit(1)


def main():
    github_url = input()
    owner, repo = github_url.rstrip("/").split("/")[-2:]

    readme = get_readme(owner, repo)

    with open("Readme.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print()


if __name__ == "__main__":
    main()
