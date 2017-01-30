import config
import utils
import os
from glob import glob

def erase_keys_from_localizables(keys_to_remove):
	files_by_lang = utils.get_localizable_files()
	for lang, file in files_by_lang.iteritems():
		print ">> Autocorrecting : {}".format(file)
		lines = utils.get_file_lines(file)
		#Create a tmp file to write the correct version of the localizable.string
		with open("tmp","w+") as f:
			for line in lines:
				line = line.content
				localizable_key = utils.extract_localizable_key_definition(line)
				if localizable_key != None:
				 	if not is_localizable_key_to_remove(localizable_key, keys_to_remove):
						f.write(line)
				else:
				 	f.write(line) #write in file, because it s probably a commentary
		os.rename('tmp', file) #Replace old file	
	return 0

def is_localizable_key_to_remove(key, keys_to_erase):
	if len(key) == 0: #manage error
		return True
	if key in keys_to_erase:
		return True
	return False

	