from googletrans import Translator
import sys
import json


if __name__ == '__main__':
    translator = Translator()
    if len(sys.argv) < 2:
        print("missing argument")

    datafile = sys.argv[1]

    with open(datafile, 'r') as f:
        data = json.load(f)

    for k in data.keys():
        steps = data[k]['en'].split('\n\n')
        chinese = ""
        arab = ""
        for step in steps:
            chinese += translator.translate(step, src='en', dest='zh-cn').text 
            arab += translator.translate(step, src='en', dest='ar').text 
            chinese += '\n\n'
            arab += '\n\n'
        data[k]['zh'] = chinese
        data[k]['ar'] = arab

    with open("/tmp/result.json", 'w') as f:
        json.dump(data, f, indent=4)