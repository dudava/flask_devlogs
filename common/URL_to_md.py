import requests
import base64


def download_md_file(github_uurl, key_api):
    owner, repo, md_filename = extract_github_info(github_uurl)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{md_filename}"
    headers = {'Authorization': f"token {key_api}"}
    response = requests.get(url, headers=headers)
    content = response.json()
    if 'content' not in content:
        print(f"Error Не удалось найти {md_filename} в репозитории.")
        return
    file_content = base64.b64decode(content['content']).decode('utf-8')
    return file_content
    # with open(md_filename, 'w', encoding='utf-8') as md_file:
    #     md_file.write(file_content)
    # print(f"Файл {md_filename} успешно скачан.")


def extract_github_info(github_urll):
    url_parts = github_urll.strip('/').split('/')
    owner = url_parts[-2]
    repo = url_parts[-1]
    md_filename = 'README.md'
    return owner, repo, md_filename


if __name__ == "__main__":
    github_url = input("Введите ссылку на GitHub проект: ")
    api_key = "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"
    download_md_file(github_url, api_key)
