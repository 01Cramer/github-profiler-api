from flask import Flask, jsonify
import requests


app = Flask(__name__)


@app.route('/get-data/<username>', methods=['GET'])
def get_github_user_data(username):
    response_repos = requests.get('https://api.github.com/users/'+username+'/repos')
    repos_list = []

    if response_repos.status_code != requests.codes.ok:
        return jsonify(result="Something went wrong with repos request!"), 200
    else:
        repo_data = response_repos.json()
        for repo in repo_data:
            name = repo.get("name")

            language_url = repo.get("languages_url")
            language_info = requests.get(language_url).json()
            if not language_info:
                language_info = {"No languages found": 0}

            repos_info = {}
            repos_info.update({name:language_info})
            repos_list.append(repos_info)
    

    response_user = requests.get('https://api.github.com/users/'+username)

    user_info = {}

    if response_user.status_code != requests.codes.ok:
        return jsonify(result="Something went wrong with user data request!"), 200
    else:
        user_data = response_user.json()

        login = user_data.get("login")
        name = user_data.get("name")
        bio = user_data.get("bio")

        user_info["login"] = login
        user_info["name"] = name
        user_info["bio"] = bio
        user_info["repos"] = repos_list


    return jsonify(user_info), 200

@app.route('/')
def home():
    return jsonify(instructions = 'Change the url to: http://127.0.0.1:5000/get-data/<username> to get information about user with given username.')

if __name__ == "__main__":
    app.run(debug=True)