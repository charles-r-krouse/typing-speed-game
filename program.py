import linecache
import os
import random
import datetime
import itertools


def main():
    book = get_random_book()
    print('Working from: {}'.format(os.path.basename(book).strip('.txt')))
    print('To exit at any time, type \"exit\" or \"x\"')
    valid_exit_codes = 'exit', ' x'
    line_num = get_starting_line_num(book)
    total_num_characters = 0
    total_num_errors = 0
    _ = input('Press <Enter> to continue... \n')
    start_time = datetime.datetime.now()
    while True:
        string, line_num = get_text(book, line_num)
        typed_string = input(string+'\n')
        total_num_characters = total_num_characters + len(typed_string.strip())
        total_num_errors = total_num_errors + compare_strings(string, typed_string)
        if typed_string.lower().endswith(valid_exit_codes):
            end_time = datetime.datetime.now()
            wpm = compute_wpm(start_time, end_time, total_num_characters)
            # subtract errors for typing the exit command
            total_num_errors = total_num_errors - 2
            # TODO: show/highlight errors
            accuracy = 100 - total_num_errors/total_num_characters*100
            print('\nCongratulations! Your current session details...')
            print('WPM = {}'.format(wpm))
            print('Errors = {}'.format(total_num_errors))
            print('Accuracy = {:.1f}%'.format(accuracy))
            break
        line_num += 1


def compute_wpm(t1, t2, num_chars:int):
    delta_time = (t2 - t1).total_seconds()
    wpm = (num_chars / 5) / (delta_time / 60)
    return int(wpm)


def get_starting_line_num(book):
    max_num_lines = get_num_lines(book)
    random_line = random.randint(1, max_num_lines)
    return random_line


def get_num_lines(file):
    with open(file, 'r', encoding='utf-8') as fin:
        count = 0
        for _ in fin:
            count += 1
        return count


def get_random_book():
    books_dir = os.path.join(os.getcwd(),'books')
    book_names = os.listdir(books_dir)
    random_book = random.choice(book_names)
    random_book_full_path = os.path.join(books_dir,random_book)
    return random_book_full_path


def get_text(book, line):
    passes = False
    text = None
    while passes is False:
        # print('Running WHILE loop...')
        text = linecache.getline(book, line)
        if text.strip() != '':
            passes = True
        else:
            line += 1
    return text.strip(), line


def compare_strings(str1, str2):
    count = 0
    for letter in itertools.zip_longest(str1, str2):
        if letter[0] != letter[1]:
            count += 1
    return count


if __name__ == '__main__':
    main()
