#!/usr/bin/env python3

"""
This script writes in the README.md file the list of public repositories from a GitHub user.
It doesnt include the repositories coming from a fork.
For each repository, this script includes some details like the repository name, the topics, the language ...
"""

import json
import requests

def get_details_about_a_repository(repo):
    name = repo['name']
    description = repo['description']
    if not description:
        description = ''
    topics = str(repo['topics'])
    if not topics:
        topics = ''
    stars = str(repo['stargazers_count'])
    url = repo['html_url']
    repository_details = '**Name**: ' + name + '  \n' + '**Description**: ' + description + '  \n' + '**Topics**: ' + topics + '  \n' + '**Stars**: ' + stars + '  \n' + '**URL**: ' + url + '  \n' + '*'*70 + '  \n'
    return (repository_details)

def main():
    # each github page has a maximum of 30 repositories. 
    # lets start to get all repositories from the first page
    with open("README.md", 'w') as outfile:
        outfile.write("This repository uses a python script and a GitHub action to update periodically this README.md file with the list of public repositories from my GitHub account. It doesnt include my repositories coming from a fork. For each repository, this script includes some details like the name, the description, the topics,  ...  \n" + '*'*70 + '  \n')
    page = 1
    user = 'ksator'
    URL = 'https://api.github.com/users/' + user + '/repos?page=' + str(page)
    response = requests.request("GET", URL)
    for repo in response.json():
        if repo['fork'] == False:
            repo_to_add = get_details_about_a_repository(repo)
            with open("README.md", 'a') as outfile:
                outfile.write(repo_to_add)

    # lets check if this is the last page. if not, lets get the repository from the next page. 
    while 'rel="last"' in response.headers['link']:
        page = page + 1
        URL = 'https://api.github.com/users/' + user + '/repos?page=' + str(page)
        response = requests.request("GET", URL)
        for repo in response.json():
            if repo['fork'] == False:
                repo_to_add = get_details_about_a_repository(repo)
                with open("README.md", 'a') as outfile:
                    outfile.write(repo_to_add)

if __name__ == '__main__':
    main()
