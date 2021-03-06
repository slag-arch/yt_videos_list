import os
import sys
import shutil
import hashlib

from yt_videos_list                       import ListCreator
from yt_videos_list.download.user_os_info import determine_user_os


def determine_path_slash():
    if determine_user_os() == 'windows': return '\\'
    else:                                return '/'


def create_test_cases(browsers):
    return [
        ListCreator(driver=browser, reverse_chronological=is_reverse_chronological)
        for browser in browsers
        for is_reverse_chronological in [True, False]
    ]


def run_test_case(list_creator):
    path_slash = determine_path_slash()
    schafer5_url = 'youtube.com/user/schafer5'
    delete_all_schafer5_files()
    list_creator.create_list_for(schafer5_url)
    if getattr(list_creator, 'reverse_chronological'): verify_update(list_creator, schafer5_url, f'tests{path_slash}partial_schafer5_reverse_chronological', f'tests{path_slash}full_schafer5_reverse_chronological')
    else:                                              verify_update(list_creator, schafer5_url, f'tests{path_slash}partial_schafer5_chronological',         f'tests{path_slash}full_schafer5_chronological')


def delete_all_schafer5_files():
    for suffix in ['reverse_chronological', 'chronological']:
        schafer5 = f'CoreySchafer_videos_list_{suffix}'
        delete_file(schafer5, 'txt')
        delete_file(schafer5, 'csv')
        delete_file(schafer5, 'md' )


def delete_file(filepath, extension):
    if os.path.exists(f'{filepath}.{extension}'):
        os.remove(f'{filepath}.{extension}')

def verify_update(driver, schafer5_url, test_file, full_file):
    variations = [use_partial_csv_only, use_partial_txt_only, use_partial_md_only, use_partial_csv_txt_and_md]
    for create_file in variations:
        print(f'\nTESTING list_creator with list_creator.reverse_chronological set to {vars(driver)["reverse_chronological"]}')
        suffix    = 'reverse_chronological' if vars(driver)["reverse_chronological"] else 'chronological'
        create_file(test_file, suffix) # the file this function creates should be the SAME as the returned string to the file_name variable in the next line
        file_name = driver.create_list_for(schafer5_url)
        # verify calling the create_list_for() method updates the partial file properly
        compare_test_files_to_reference_files(full_file, file_name)


def use_partial_txt_only(test_file, suffix):
    print('TESTING with a pre-existing txt file only (no pre-existing csv or md file)....')
    delete_all_schafer5_files()
    create_partial_file(test_file, suffix, 'txt')

def use_partial_csv_only(test_file, suffix):
    print('TESTING with a pre-existing csv file only (no pre-existing txt or md file)....')
    delete_all_schafer5_files()
    create_partial_file(test_file, suffix, 'csv')

def use_partial_md_only(test_file, suffix):
    print('TESTING with a pre-existing md file only (no pre-existing txt or csv file)....')
    delete_all_schafer5_files()
    create_partial_file(test_file, suffix, 'md')

def use_partial_csv_txt_and_md(test_file, suffix):
    print('TESTING with pre-existing txt, csv, and md files....')
    create_partial_file(test_file, suffix, 'txt')
    create_partial_file(test_file, suffix, 'csv')
    create_partial_file(test_file, suffix, 'md' )

def create_partial_file(test_file, suffix, extension):
    shutil.copy(f'{test_file}.{extension}', f'CoreySchafer_videos_list_{suffix}.{extension}')


def compare_test_files_to_reference_files(full_file, file_name):
    with open(f'{file_name}.txt', 'r', encoding='utf-8') as test_txt, open(f'{file_name}.csv', 'r', encoding='utf-8') as test_csv, open(f'{file_name}.md', 'r', encoding='utf-8') as test_md:
        current_txt = hashlib.sha256(test_txt.read().encode('utf-8')).hexdigest()
        current_csv = hashlib.sha256(test_csv.read().encode('utf-8')).hexdigest()
        current_md  = hashlib.sha256(test_md.read().encode ('utf-8')).hexdigest()
    with open(f'{full_file}.txt', 'r', encoding='utf-8') as full_txt, open(f'{full_file}.csv', 'r', encoding='utf-8') as full_csv, open(f'{full_file}.md', 'r', encoding='utf-8') as full_md:
        verified_txt = hashlib.sha256(full_txt.read().encode('utf-8')).hexdigest()
        verified_csv = hashlib.sha256(full_csv.read().encode('utf-8')).hexdigest()
        verified_md  = hashlib.sha256(full_md.read().encode ('utf-8')).hexdigest()
    failed = False
    if current_txt != verified_txt: print(f'❌ ERROR! The updated txt file does NOT match the {full_file}.txt file!'); failed = True
    else:                           print(f'✅ The updated txt file matches the {full_file}.txt file :)')
    if current_csv != verified_csv: print(f'❌ ERROR! The updated csv file does NOT match the {full_file}.csv file!'); failed = True
    else:                           print(f'✅ The updated csv file matches the {full_file}.csv file :)')
    if current_md  != verified_md:  print(f'❌ ERROR! The updated md  file does NOT match the {full_file}.md  file!'); failed = True
    else:                           print(f'✅ The updated md  file matches the {full_file}.md  file :)')
    if failed:
        print('\n' * 5)
        sys.exit()
