import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import json
import solution
import count
from settings import *
import argparse  # 用于解析命令行参数
import process



if __name__ == "__main__":
    process.process()
    with open(UNI_WORD, 'r', encoding='utf-8') as f:
        uni_frequency=json.load(f)
    with open(BI_WORD, 'r', encoding='utf-8') as f:
        binary_frequency=json.load(f)
    with open(WORD_TABLE, 'r', encoding='utf-8') as f:
        word_table=json.load(f)

    my_uni_frequency = solution.get_uni_frequency(uni_frequency)
    my_binary_frequency = solution.get_binary_frequency(binary_frequency)

    sum_pinyin = 0
    for pinyin in uni_frequency:
        for i in range(len(uni_frequency[pinyin]["words"])):
            if uni_frequency[pinyin]["counts"][i] > 0:
                sum_pinyin += uni_frequency[pinyin]["counts"][i]
    para=sum_pinyin
    

    # 若使用二元模型，采用输入输出重定向，则使用该段代码
    input_lines = sys.stdin.readlines()
    for line in input_lines:
        sentence = line.strip()
        result = solution.Viterbi(sentence, my_uni_frequency, my_binary_frequency, word_table, para)
        sys.stdout.write(result + "\n")

    # # 若使用三元模型，则关闭标准输入输出，使用该段代码，即取消后文代码段注释
    # count.count_3gram_frequency(PROCESSED_DATA)
    # with open(TRI_WORD, 'r', encoding='utf-8') as f:
    #     tri_frequency=json.load(f)
    # my_tri_frequency = solution.get_tri_frequency(tri_frequency)
    # # 创建命令行参数解析器
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--input', '-i', default='./data/input.txt', help='The input file.')
    # parser.add_argument('--output', '-o', default='./data/output.txt', help='The output file.')
    # parser.add_argument('--answer', '-a', default='./data/answer.txt', help='The answer file.')
    # # 解析命令行参数
    # args = parser.parse_args()
    # # 获取输入文件、输出文件和答案文件的路径
    # input_file = args.input
    # output_file = args.output
    # val_file = args.answer
    # output=[]
    # with open(output_file, 'w', encoding='utf-8') as output_f:
    #     with open(input_file, 'r', encoding='utf-8') as input_f:
    #          lines = input_f.readlines()
    #      # 处理每一行的拼音序列
    #          for line in lines:
    #             sentence = line.strip()
    #             result = solution.Viterbi_3gram(sentence, my_uni_frequency, my_binary_frequency,my_tri_frequency, word_table,para)
    #             output_f.write(result + "\n")
    #             output.append(result)
                
    
    # #读取答案文件
    # with open(val_file, 'r', encoding='utf-8') as val_f:
    #     answer_lines = val_f.readlines()
    #     correct_sen_num=0
    #     correct_word_num=0
    #     word_num=0

    #     for i in range(len(answer_lines)):
    #         answer_line = answer_lines[i].strip()
    #         if answer_line == output[i]:
    #             correct_sen_num += 1
    #             word_num += len(answer_line)
    #             correct_word_num += len(output[i])
    #         else:
    #             for j in range(len(answer_line)):
    #                 if answer_line[j] == output[i][j]:
    #                     correct_word_num += 1
    #                 word_num += 1
            

    #  # 打印整句正确率
    # print('整句正确率：', str(int(correct_sen_num / len(output) * 10000) / 100) + '%')
    # # 打印逐字正确率
    # print('逐字正确率：', str(int(correct_word_num / word_num * 10000) / 100) + '%')    


                
          
