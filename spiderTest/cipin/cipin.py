# -*- coding: UTF-8 -*-
import os, re, datetime

class Dealtxt():
    def get_txt(self):
        all_files = os.listdir(os.getcwd())
        for i in all_files:
            if i.find('txt') > 0:
                if i.find('message.txt') > 0:
                    os.remove(os.getcwd() + os.sep +i)
                else:
                    path = os.getcwd() + os.sep +i
        return path

    def get_name(self, text):
        year = datetime.datetime.now().year
        names = []
        for line in text:
            if line.startswith(str(year)):
                name = line.split(' ')[-1]
                if name in names:
                    pass
                else:
                    names.append(name)
        return names

    def get_text(self, path):
        with open(path, 'r') as fl:
            content = fl.readlines()
        fl.close()
        content = content[8:]
        deal_content = []
        for message in content:
            message = re.sub('\n', '', message)
            deal_content.append(message)
        return deal_content

    def get_message(self, text, names):
        results = {}
        for i in names:
            i = i
            results[i] = []
        index = 0
        while True:
            try:
                if text[index].startswith('2016'):
                    name = text[index].split(' ')[-1]
                    if name in names:
                        while True:
                            index += 1
                            if not text[index].startswith('2016') and text[index]:
                                results[name].append(text[index])
                            elif text[index] == '':
                                pass
                            else:
                                break
            except IndexError:
                for result in results:
                    self.write_txt(result, results[result])
                return None

    def write_txt(self, save_name, result):
        save_path = os.getcwd() + os.sep + '%s_message.txt' % save_name.decode('utf-8').encode('gbk')
        with open(save_path, 'w') as fl:
            for message in result:
                fl.write(message + '|')
        fl.close()
    def main(self):
        path = self.get_txt()
        text = self.get_text(path)
        names = self.get_name(text)
        self.get_message(text, names)

class Analysis():
    def get_message_txt(self):
        fils = os.listdir(os.getcwd())
        txts = []
        for i in fils:
            if i.endswith('message.txt'):
                txts.append(os.getcwd() + os.sep + i)
        return txts

    def get_all_char(self, path):
        txt = open(path, 'r').read()
        txt = txt.replace('，','')
        r = re.compile('[\x80-\xff]+')
        all_char = r.findall(txt)
        return all_char

    def parse(self, all_char):
        dict = {}
        z1 = re.compile('[\x80-\xff]{2}')
        z2 = re.compile('[\x80-\xff]{4}')
        z3 = re.compile('[\x80-\xff]{6}')
        z4 = re.compile('[\x80-\xff]{8}')
        for zx in [z2,z3,z4]:
            for double_char in all_char:
                x = double_char.decode('utf-8').encode('gb18030')
                i = zx.findall(x)
                for j in i:
                    if (j in dict):
                        dict[j] += 1
                    else:
                        dict[j] = 1
        return dict

    def write_result(self, whos,dict):
        whos = whos.split('.')[0]
        wfile = open(os.getcwd() + os.sep +'%s_analysis.txt' % whos,'w')
        dict = sorted(dict.items(), key=lambda d:d[1])
        for a, b in dict:
            if b > 2:
                wfile.write(a.decode('gbk').encode('utf-8') + '---' + str(b) + '\n')
        wfile.close()
    def main(self):
        txts = self.get_message_txt()
        for path in txts:
            all_char = self.get_all_char(path)
            dict = self.parse(all_char)
            whos = (path.split(os.sep))[-1]
            self.write_result(whos, dict)

if __name__ == '__main__':
    deal = Dealtxt()
    deal.main()
    analysis = Analysis()
    analysis.main()
