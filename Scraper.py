import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as soup

class Scraper():
    
    def __init__(self, path=None, filtered='no'):
        self.keys = ['font-size:36px;', 'font-size:24px;', 'font-size:18px']
        self.path = path
        self.filtered = filtered

    def get_headers(self):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            # 'content-length': '752',
            # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'origin': 'https://mediakit.iportal.ru',
            # 'referer': 'https://mediakit.iportal.ru/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Linux',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
        return headers

    def scrap(self):
                
        headers = self.get_headers()
        response = requests.get('https://mediakit.iportal.ru/our-team', headers=headers).text
        
        s = soup(response, 'lxml')
        parsed_data = pd.DataFrame(columns=['Город', 'Имя', 'email', 'Должность'])
        df_ind = 0
        
        rows = s.find_all('div', {'data-record-type':'396'})
        for row in rows:
            type_record = row.get('data-record-type')
        
            style = row.find('style', )
            try:
                style = style.text
            except Exception as ex:
                print('style is N\A')
                
            if style != 'N\A':
                medias = re.findall(r'(@media?.*?\}\})', style)
                
                without_medias = re.sub(r'(@media?.*?\}\})', '', style)
                records = re.findall(r'(\#rec.*?\})', without_medias)
                
                elements = [[],[],[]]
                for key_index in range(len(self.keys)):
                    for record in records:
                        if self.keys[key_index] in record:
                            if 'opacity:0;' not in record:
                                elements[key_index].append(re.findall(r'data-elem-id="(.*?)"\]', record)[0])
                
                for i in range(len(elements)):
                    if len(elements[i]) > 2:
                        delete_list = []
                        for j in range(len(elements[i])):
                            if len(row.find('div', {'data-elem-id':f'{elements[i][j]}'}).text.strip()) == 0:
                                delete_list.append(elements[i][j])
                        for d in delete_list:
                            elements[i].remove(d)
                
                left, right = [], []
                for el in elements:
                    
                    if len(el) == 2:
                        for record in records:
                            if (el[0] in record) and ('left' in record):
                                px1 = int(re.findall(r'left: calc\(.*?px.*?...(\d+)', record)[0])
                                
                            if (el[1] in record) and ('left' in record):
                                px2 = int(re.findall(r'left: calc\(.*?px.*?...(\d+)', record)[0])
                        
                        if px1 < px2:
                            left.append(el[0]), right.append(el[1])
                        else:
                            left.append(el[1]), right.append(el[0])
                    
                    elif len(el) == 1:
                        for record in records:
                            if (el[0] in record) and ('left' in record):
                                px1 = int(re.findall(r'left: calc\(.*?px.*?...(\d+)', record)[0])
                        if px1 < 500:
                            left.append(el[0]), right.append('N/A')
                        else:
                            right.append(el[0]), left.append('N/A')
                    
                    left_info, right_info = [], []
                    for ind in range(len(left)):
                        
                        # if ind == 0:
                        #     if left[ind] != 'N/A':
                        #         if row.find('div', {'data-elem-id':f'{left[ind]}'}).find('a') == None:
                        #             left_info.append(row.find('div', {'data-elem-id':f'{left[ind]}'}).text.strip())
                        #         else:
                        #             left_info.append('N/A')
                        #     else:
                        #         left_info.append('N/A')
                                
                        #     if right[ind] != 'N/A':
                        #         if row.find('div', {'data-elem-id':f'{right[ind]}'}).find('a') == None:
                        #             right_info.append(row.find('div', {'data-elem-id':f'{right[ind]}'}).text.strip())
                        #         else:
                        #             right_info.append('N/A')
                        #     else:
                        #         right_info.append('N/A')
                            
                        if ind == 2:
                            if left[ind] != 'N/A':
                                subrow = row.find('div', {'data-elem-id':f'{left[ind]}'})
                                left_info.append(subrow.a.text.strip())
                                subrow.select_one('a').decompose()
                                left_info.append(subrow.text.split('8')[0].strip())
                            else:
                                left_info.append('N/A'), left_info.append('N/A')
                                
                            if right[ind] != 'N/A':
                                subrow = row.find('div', {'data-elem-id':f'{right[ind]}'})
                                right_info.append(subrow.a.text.strip())
                                subrow.select_one('a').decompose()
                                right_info.append(subrow.text.split('8')[0].strip())
                            else:
                                right_info.append('N/A'), right_info.append('N/A')
                        
                        else:
                            if left[ind] != 'N/A':
                                left_info.append(row.find('div', {'data-elem-id':f'{left[ind]}'}).text.strip())
                            else:
                                left_info.append('N/A')
                                
                            if right[ind] != 'N/A':
                                right_info.append(row.find('div', {'data-elem-id':f'{right[ind]}'}).text.strip())
                            else:
                                right_info.append('N/A')
                
                try:
                    parsed_data.loc[df_ind] = left_info
                    parsed_data.loc[df_ind+1] = right_info
                    df_ind += 2
                except Exception:
                    pass
            
        rows = s.find_all('div', {'data-record-type':'527'})
        for row in rows:
            type_record = row.get('data-record-type')
            
            if type_record == '527':
                subrows = row.find_all('div', {'class':'t527__col t-col t-col_6 t-align_left t527__col-mobstyle'})
                for subrow in subrows:
                    name = subrow.find('div', {'class':'t527__persname t-name t-name_lg t527__bottommargin_sm'}).text.strip()
                    func = subrow.find('div', {'class':'t527__persdescr t-descr t-descr_xxs t527__bottommargin_lg'}).text.strip()
                    
                    parsed_data.loc[df_ind] = ['N/A', name, 'N/A', func]
                    df_ind += 1
            
        rows = s.find_all('div', {'data-record-type':'544'})
        for row in rows:
            name = row.find('div', {'field':'title'}).text.strip()
            func = row.find('div', {'field':'descr'}).text.strip()
            
            text_block = row.find('div', {'field':'text'})
            mail = row.find('div', {'field':'text'}).a.text
            parsed_data.loc[df_ind] = ['N/A', name, mail, func]
            df_ind += 1
        
        parsed_data = parsed_data.reindex(columns=['Город', 'Имя', 'Должность', 'email'])
        parsed_data = parsed_data[parsed_data['Имя'] != 'N/A']
        
        return parsed_data

    def apply_filter(self, data):
        
        df = data.copy()
        df['Фамилия'] = df['Имя'].str.split().str[1].str.strip()
        df['Имя'] = df['Имя'].str.split().str[0].str.strip()
        
        df = df.drop_duplicates(subset=['Имя', 'Должность', 'email'])
        df = df.drop_duplicates(subset=['Имя', 'Фамилия', 'email'])
        df = df.drop_duplicates(subset=['Имя', 'Фамилия', 'Должность'])
        
        return df
        
    def count_letters(self, data):
        
        df = data.copy()
        
        df['1lt'] = df['Фамилия'].str[0].str.lower()
        group = df.groupby(['1lt'])['1lt'].count()
        group.sort_values(ascending=False, inplace=True)
        
        for i in group.index:
            print(i, '-', group[i])

    def main(self):
        
        data = self.scrap()
        filtered_data = self.apply_filter(data)
        
        self.count_letters(filtered_data)
        
        if self.filtered == 'yes':
            if self.path != None:
                filtered_data.to_csv(self.path)
            return filtered_data
        
        else:
            if self.path != None:
                data.to_csv(self.path)
            return data

if __name__ == '__main__':
    
    ### Сохранение: ведите путь к директории и название для файла
    path = '/home/ivan/BrandPol/data.csv'
    
    ### Для получения отфильтрованных данных введите filtered = 'yes'
    filtered = 'no'
    ### Примечание: при изменении будет произведено сохранение отфильтрованного файла
    
    data = Scraper(path, filtered).main()
    