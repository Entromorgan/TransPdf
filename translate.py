import os
import sys
import argparse
import time
from googletrans import Translator


eos_punc_list = ['.', ';', '?', '!'] # punctuations that can mark the end of a sentence


def find_sub_index(mini_batch, eos_punc_list=eos_punc_list): # find the optimal seperation of subsentence
	
	sub_index_list = []
	for obj in eos_punc_list:
		sub_index_list.append(mini_batch.rfind(obj))

	return max(sub_index_list)


def preprocessing(filename, max_batch_size=4600, eos_punc_list=eos_punc_list): # parse input pdf file into mini batches whose sizes are smaller than max_batch_size bytes

	print("Extracting text from " + filename + " ...")
	os.system("pdf2txt.py " + filename + " -o " + filename.replace(".pdf", "_raw.txt"))  # extract text from pdf, save as filename_raw.txt
	print("Extraction success!")
	
	print("Replacing line breaks ...")
	with open(filename.replace(".pdf", "_raw.txt"), 'r', encoding='utf8') as rawfile:
		content = rawfile.read().replace("\n", " ")
		with open(filename.replace(".pdf", "_strip.txt"), 'w', encoding='utf8') as stripfile:
			content = ''.join([i for i in content if ord(i)<127]) # remove characters that have ascii value bigger than 126
			stripfile.write(content)
	print("Replacement success!")

	print("Spliting text into mini batches ...")
	batches = []
	mini_batch = ""
	sub_sentence = ""
	index = 0
	sub_index = 0
	loops = int(len(content) / max_batch_size)
	loop_num = 1;
	while loop_num <= loops:
		print("Processing mini batch [" + str(loop_num) + "/" + str(loops) + "]")
		mini_batch = content[index:index + max_batch_size]
		mini_batch = sub_sentence + mini_batch
		sub_sentence = ""
		if mini_batch[len(mini_batch)-1] not in eos_punc_list: # if the end of the mini batch is not a complete sentence
			sub_index = find_sub_index(mini_batch, eos_punc_list)
			sub_sentence = mini_batch[sub_index+1:]
			mini_batch = mini_batch.rstrip(sub_sentence)
		batches.append(chr(96+loop_num) + mini_batch) # label the number
		mini_batch = ""
		index += max_batch_size
		loop_num += 1
	print("Processing mini batch [" + str(loop_num) + "/" + str(loops+1) + "]")
	batches.append(chr(96+loop_num) + sub_sentence + content[index:])
	print("Split success!")

	return sorted(batches)


def translate(translator, origin_text, src='auto', dest='zh-CN'): # translate src language into dest language

	translated_text = translator.translate(origin_text, src=src, dest=dest).text

	return translated_text


def maketheparser(): # initialize the parser
    
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("-s", "--src", type=str, default='auto', help="Set src language.")
    parser.add_argument("-d", "--dest", type=str, default='zh-CN', help="Set dest language.")
    parser.add_argument("-p", "--path", type=str, default='./', help="Specify working path.")
    parser.add_argument("-b", "--batch_size", type=int, default=4600, help="Max batch size of a mini batch.")
    parser.add_argument("-l", "--language", default=False, action="store_true", help="List all supported src & dest languages.")
    parser.add_argument("-f", "--flush", default=False, action="store_true", help="Clear all temp files.")

    return parser


def language_helper(): # list all the languages supported (Ref: https://cloud.google.com/translate/docs/languages)

	print("	南非荷兰语				af \
			阿尔巴尼亚语				sq \
			阿姆哈拉语				am \
			阿拉伯语	    			ar \
			亚美尼亚语				hy \
			阿塞拜疆语				az \
			巴斯克语	    			eu \
			白俄罗斯语				be \
			孟加拉语	    			bn \
			波斯尼亚语				bs \
			保加利亚语				bg \
			加泰罗尼亚语				ca \
			宿务语	    			ceb (ISO-639-2) \
			中文（简体）				zh-CN (BCP-47) \
			中文（繁体）				zh-TW (BCP-47) \
			科西嘉语	    			co \
			克罗地亚语				hr \
			捷克语	    			cs \
			丹麦语	    			da \
			荷兰语	    			nl \
			英语	        			en \
			世界语	    			eo \
			爱沙尼亚语				et \
			芬兰语	    			fi \
			法语	        			fr \
			弗里斯兰语				fy \
			加利西亚语				gl \
			格鲁吉亚语				ka \
			德语	        			de \
			希腊语	    			el \
			古吉拉特语				gu \
			海地克里奥尔语			ht \
			豪萨语			 		ha \
			夏威夷语					haw (ISO-639-2) \
			希伯来语					iw \
			印地语					hi \
			苗语						hmn (ISO-639-2) \
			匈牙利语					hu \
			冰岛语					is \
			伊博语					ig \
			印度尼西亚语				id \
			爱尔兰语					ga \
			意大利语					it \
			日语						ja \
			爪哇语					jw \
			卡纳达语					kn \
			哈萨克语					kk \
			高棉语					km \
			韩语						ko \
			库尔德语					ku \
			吉尔吉斯语				ky \
			老挝语					lo \
			拉丁语					la \
			拉脱维亚语				lv \
			立陶宛语					lt \
			卢森堡语					lb \
			马其顿语					mk \
			马尔加什语				mg \
			马来语					ms \
			马拉雅拉姆语				ml \
			马耳他语					mt \
			毛利语					mi \
			马拉地语					mr \
			蒙古语					mn \
			缅甸语					my \
			尼泊尔语					ne \
			挪威语					no \
			尼杨扎语（齐切瓦语）		ny \
			普什图语					ps \
			波斯语					fa \
			波兰语					pl \
			葡萄牙语（葡萄牙、巴西）	pt \
			旁遮普语					pa \
			罗马尼亚语				ro \
			俄语						ru \
			萨摩亚语					sm \
			苏格兰盖尔语				gd \
			塞尔维亚语				sr \
			塞索托语					st \
			修纳语					sn \
			信德语					sd \
			僧伽罗语					si \
			斯洛伐克语				sk \
			斯洛文尼亚语				sl \
			索马里语					so \
			西班牙语					es \
			巽他语					su \
			斯瓦希里语				sw \
			瑞典语					sv \
			塔加路语（菲律宾语）		tl \
			塔吉克语					tg \
			泰米尔语					ta \
			泰卢固语					te \
			泰语						th \
			土耳其语					tr \
			乌克兰语					uk \
			乌尔都语					ur \
			乌兹别克语				uz \
			越南语					vi \
			威尔士语					cy \
			班图语					xh \
			意第绪语					yi \
			约鲁巴语					yo \
			祖鲁语					zu")


def list_pdf(path): # list all pdf files under designated path

	whole_list = os.listdir(path)
	pdf_list = []
	for obj in whole_list:
		path_file = os.path.join(path,obj) # obtain absolute file path 
		if os.path.isfile(path_file):  # if current obj is a file
			if '.pdf' in obj: # is a pdf file
				pdf_list.append(obj)

	return pdf_list


def main(args=None):

	P = maketheparser()
	A = P.parse_args(args=args)

	if A.language:
		language_helper()
		sys.exit(0)

	translator = Translator(service_urls=['translate.google.cn']) # initialize translator

	translated_text = "" # initizalize output string

	pdf_list = list_pdf(A.path)
	for pdf_file in pdf_list:
		print("Translating " + pdf_file + " ...")
		batches = preprocessing(os.path.join(A.path, pdf_file), A.batch_size)
		index = 1
		for mini_batch in batches:
			print("Translating mini batch [" + str(index) + "/" + str(len(batches)) + "]")
			translated_text += translate(translator, mini_batch[1:], A.src, A.dest) # remove mini batch number label before translation
			index += 1
		with open(pdf_file.replace(".pdf", "_trans.txt"), 'w', encoding='utf8') as transfile:
			transfile.write(translated_text)
			translated_text=""

	if A.flush:
		for pdf_file in pdf_list:
			os.remove(os.path.join(A.path, pdf_file.replace(".pdf", "_raw.txt")))
			os.remove(os.path.join(A.path, pdf_file.replace(".pdf", "_strip.txt")))

	return 0


if __name__ == '__main__': sys.exit(main())