# 配置文件，定义了程序中使用的文件路径和常量

# 拼音汉字表文件路径
PINYIN_WORD_TABLE = './data/拼音汉字表.txt'
ALL_WORDS = './data/一二级汉字表.txt'
SINA_NEWS = './corpus/sina_news_gbk/2016-%02d.txt'

# 处理后的数据文件路径
WORD_TABLE = './sets/word_table.json'  # 拼音-汉字表文件路径
PINYIN_TABLE = './sets/pinyin_table.json'  # 汉字-拼音表文件路径
PROCESSED_DATA = './sets/processed_data/month_%02d.json'  # 处理后的数据文件路径
UNI_WORD = './sets/1_word.json'  # 单字频率文件路径
BI_WORD = './sets/2_word.json'  # 双字频率文件路径
TRI_WORD = './sets/3_word.json'  # 三字频率文件路径

# 模型参数
ALPHA = 0.999999  # 平滑参数
LAMBDA = 0.999  # 平滑参数
TEST_NUM=501 #测试数据的数量