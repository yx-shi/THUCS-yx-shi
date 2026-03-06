import prepare
import settings
import count

def process():
    prepare.process_word_table()
    prepare.process_sina()
    count.count_frequency(settings.PROCESSED_DATA)