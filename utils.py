import os
import config
import re
from glob import glob

class CodeLine(object):
	def __init__(self, content, filepath, line_nb):
		self.content = content
		self.filepath = filepath
		self.line_nb = line_nb

def get_files_lines(path):
	files = [y for x in os.walk(config.project_path) for y in glob(os.path.join(x[0], path))]
	lines = []
	for file in files:
		excluded_regex = reduce(merge_regex, config.excluded_pathes)
		if not re.search(excluded_regex, file):
			lines += get_file_lines(file)
	return lines

def get_file_lines(filepath):
	lines = []
	with open(filepath) as f:
		line_nb = 1
		for line in f:
			if len(line) > 1: #Remove empty lines (but each line finish by '\n' character => 'len(line) > 1')
				lines.append(CodeLine(line, filepath, line_nb))
			line_nb += 1
	return lines

def extract_localizable_keys(code_line):
	localized_string_in_code_regex = reduce(merge_regex, config.localized_string_in_code_regex)
	localizable_keys = re.findall(localized_string_in_code_regex, code_line)
	filtered_localizable_keys = [] 
	for localizable_key in localizable_keys:
		valid_localizable_keys = extract_and_filter_localizable_keys(localizable_key)
		if valid_localizable_keys:
			filtered_localizable_keys += valid_localizable_keys

	return filtered_localizable_keys

"""
Extract localizable keys on .strings files
"""
def extract_localizable_key_definition(code_line):
	regex = r'{}\s*=\s*".+";'.format(construct_localizable_key_regex())
	valid_keys = re.match(regex, code_line)
	if valid_keys:
		return valid_keys.group('key')
	return None

def extract_potential_localized_key(code_line):
	if len(code_line) < 500: # escape too long line => performance
		return extract_and_filter_localizable_keys(code_line)
	return []
	
def get_localizable_files():
	files = {}
	for lang in config.languages:
		for file in config.localizable_string_files:
			path = "{folder_path}{lang}.lproj/{file_name}.strings".format(folder_path = config.localizable_string_folder_path, lang = lang, file_name = file)
			localizable_files = [y for x in os.walk(config.project_path) for y in glob(os.path.join(x[0], path))]
			if len(localizable_files) > 0:
				files[lang] = localizable_files[0] 
	return files


def extract_and_filter_localizable_keys(code_line):
	regex = construct_localizable_key_regex()
	valid_keys = re.findall(regex, code_line)
	if len(valid_keys):
		return valid_keys
	return []

def construct_localizable_key_regex():
	localizable_key_regex = reduce(merge_regex, config.localizable_key_regex)
	return r'"(?P<key>{}(?:{}){})"'.format(config.unwanted_localizable_key_prefix, localizable_key_regex, config.unwanted_localizable_key_suffix)

def merge_regex(regex_a, regex_b):
	return "{}|{}".format(regex_a, regex_b)

