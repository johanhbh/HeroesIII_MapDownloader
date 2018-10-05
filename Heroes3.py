#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:05:44 2018

@author: johanhaslebuch-hansen
"""
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re,os,math

class Heroes3Maps():
    """ Heroes of Might and Magic III (HMM3)
    
    
    to download HMM3 maps from the http://www.maps4heroes.com webpage
    
    It uses webscraping to go through all pages containing maps and reads
    the maps' types and specs, such as Can be Human, Teams etc. Then the API 
    can save maps that fulfills specifications made by the user, to facilitate
    eager HMM3 gamers' search for specific games.
    
    Lastly the script donwloads the maps found from the scraping using urllib's
    request.urlretrieve to donwload them the directory specified with it's 
    path by the user. 
    
    Parameters
    ----------
    no_maps : int or float
        Number of maps to be downloaded.
        if no_maps is not set default is:
            no_maps = float("inf")
        meaning that it will download all maps on the site that fulfills 
        the conditions
        
    mods : list of int
        The integers in the list determines which Heroes 3 moderations and 
        expansion packs are eligible for download. The expansion packs and
        moderations are represented with the following int:
            {
             '1' : 'Heroes 3 The Shadow of Death',
             '2' : "Heroes 3 Armageddon's Blade",
             '3' : 'Heroes 3 The Restoration of Eratia', 
             '4' : 'Heroes 3 Horn of the Abyss',
             '5' : 'Heroes 3 In the Wake of Gods', 
             '6' : 'Heroes 3 In the Wake of Gods + Era'
             }
        Default is all maps:
            mods = [1,2,3,4,5,6]
        
    no_teams : int
        The minimum number of teams in a map.
        Default is 0, i.e. no restrictions:
            no_teams = 0
    
    no_humans : int
    The minimum number players that can be human in a map.
        Default is 0, i.e. no restrictions:
            no_humans = 0
    
    sizes : str, or list of str
        The map sizes the user accepts as downloads. Options are:
            {
            'S':'Small'
            'M':"Medium"
            'L' : 'Large' 
            'XL' : 'Extra Large'
            'H' : 'Huge' 
            'EH' : 'Extra Huge'
            'G':'Giant'
            }
        If more than one size is acceptable specify, which ones in a list of
        stings, e.g. sizes = ['L','XL'] if user only want Large or Extra Large
        maps. Default is that all sizes are excepted:
            sizes = ['S','M','L','XL','H','EH','G']
    
    no_players : int
        Minimum number of players in the map. 
        Default is 0, i.e. no restrictions:
            no_players = 0
    
    Attributes
    ----------
    .conditions()[1] : list
        List of the names of the maps eligible for download.
        
    
    If the downloader downloads a map zipped in a WinRar Archive, which macs
    can't open per default, you can use:
        https://online.b1.org/online

    Examples
    --------        
    >>> from Heroes3 import Heroes3Maps
    >>> initializer = Heroes3Maps(no_maps=1,mods=[1,2,3],no_teams=1,no_humans=1)
    >>> initializer.downloader('/Users/downloads/')

    This example will download 1 map (the first map the parser finds that 
    fulfills the conditions) from either Heroes 3 The Shadow of Death,
    Heroes 3 Armageddon's Blade or Heroes 3 The Restoration of Eratia.
    """

    
    def __init__(self, no_maps=float("inf"),mods=[x for x in range(1,7)],
                 no_teams=0,no_humans=0,sizes=['S','M','L','XL','H','EH','G'],
                 no_players = 0):
        self.no_maps = math.ceil(no_maps)
        self.mods = mods
        self.no_teams = math.ceil(no_teams)
        self.no_humans = math.ceil(no_humans)
        self.sizes = sizes
        self.no_players = no_players
        self.numbers = re.compile(r'\b(?:[0-9])\b')
    
    def parser(self,pg):
        """ 
        Parses the website one page with 10 maps on each page at the time
        """
        base = 'http://www.maps4heroes.com/heroes3/maps.php?&limit='    
        page = str(pg)
        domain = urlopen(base + page)
        soup = BeautifulSoup(domain, 'html.parser')
        return soup
    
        
    def conditions(self):
        """
        Takes parsed webpages from parser(self,pg) as input and scrapes each page of maps 
        to save maps that fulfills the specified conditions from __init__() until it either
        reaches the last page or until it has found the number of maps specified in self.no_maps
        that are eligible for download.
        """
        dwnl = [[],[]]
         
        moderations = {'1':'Heroes 3 The Shadow of Death','2':"Heroes 3 Armageddon's Blade",
                     '3' : 'Heroes 3 The Restoration of Eratia', '4' : 'Heroes 3 Horn of the Abyss',
                     '5' : 'Heroes 3 In the Wake of Gods', '6' : 'Heroes 3 In the Wake of Gods + Era'}
        
        size = {'S':'Small','M':"Medium",'L' : 'Large', 'XL' : 'Extra Large',
                   'H' : 'Huge', 'EH' : 'Extra Huge', 'G':'Giant'}
        try:
            if self.sizes is not None:
                size = [size[x] for x in list(self.sizes)]
            playables = []
            for i in list(self.mods):
                playables.append(moderations[str(i)])
        except:
            print('{0}: Not valid option in map type or size'.format(TypeError))
            
        for x in range(157):
            soup = self.parser(x)
    
            if len(dwnl[0]) >= self.no_maps:
                break
    
            for j in range(len(soup.find_all('tr'))):
                teams,cbh = 0,0
                try:
                    maps = soup.find_all('tr')[j].find_all('td')[0].find_all('b')[1].contents
                    map_name = soup.find_all('tr')[j].find_all('td')[0].find_all('b')[0].contents
                    if maps[0] in playables:
                        print(maps)
                        for i in soup.find_all('tr')[j].find_all('td')[3].contents:
                            if 'Size' in i:
                                sz = i[8:]
                                print("Size {0}".format(sz))
                            if 'Can be Human' in i:
                                cbh = int(self.numbers.findall(i)[0])
                                print("Can be Human {0}".format(cbh))
                            if 'Team' in i:
                                teams = int(self.numbers.findall(i)[0])
                                print("Teams {0}".format(teams))
                            if 'Players' in i:
                                players = int(self.numbers.findall(i)[0])
                                print("Players {0}".format(players))
                    if teams >= self.no_teams and cbh >= self.no_humans and \
                            sz in size and players >= self.no_players :
                        dwnl_no = str(soup.find_all('tr')[j].find_all('td')[0].find('a'))
                        dwnl_no = dwnl_no[dwnl_no.index('(')+1:dwnl_no.index(')')]
                        dwnl[0].append(dwnl_no)
                        dwnl[1].append(map_name)
                        if len(dwnl[0]) >= self.no_maps:
                            break
                        print("---- {0}".format(dwnl))
                except IndexError:
                    continue
        self.maps_ = dwnl[1]
        return dwnl
    
    def downloader(self,dwnl_dir):
        if os.path.exists(dwnl_dir) == False:
            raise FileNotFoundError("Can't find such directory : {0}, try '/' instead of '\\' as seperators".format(dwnl_dir))
        eligibles = self.conditions()
        eligibles,maps,downloaded = eligibles[0],eligibles[1],[]
        dwnl_domain = 'http://www.maps4heroes.com/heroes3/rating.php?testcookie=&id='
        for j,i in enumerate(eligibles):
            print('Now downloading "{0}"...'.format(maps[j][0]))
            downloaded.append(maps[j][0])
            domai = urlopen(dwnl_domain + i)
            sou = BeautifulSoup(domai, 'html.parser')
            url = sou.find('a')['href']
            file_name = url.split('/')[-1]
            if dwnl_dir.endswith('/'):
                urlretrieve(url, dwnl_dir+file_name)
            else:
                urlretrieve(url, dwnl_dir+'/'+file_name)
        return downloaded
