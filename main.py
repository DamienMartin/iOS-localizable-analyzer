import config
import autocorrect
import console
import utils
import sys
from console import Console

autocorrect_active = False
console = Console()

if len(sys.argv) == 2 and sys.argv[1] == 'autocorrect':
	autocorrect_active = True

print '> Analyzing the code'
#Get all code lines
all_lines = []
for pattern in config.files_to_analyze:
	lines = utils.get_files_lines(pattern)
	all_lines += lines
	console.number_lines[pattern] = len(lines)

#Filter translation uses, and stock all regular strings to faster test2
lines = []
potential_localized_keys = []
for line in all_lines:
	translations_made = utils.extract_localizable_keys(line.content)
	for translation_made in translations_made:
		lines.append(utils.CodeLine(translation_made, line.filepath, line.line_nb))
	potential_localized_keys += utils.extract_potential_localized_key(line.content)
console.potential_localized_keys = len(potential_localized_keys)

#Clean doubles
used_key_list = {}
for line in lines:
	keyStr = line.content
	if keyStr in used_key_list:
		used_key_list[keyStr].append(line)
	else:
		used_key_list[keyStr] = [line]

total_keys_found = len(used_key_list)
console.keys_in_code = {'unique':total_keys_found, 'usage':len(lines)}

print '> Inspecting keys in .strings'
# Loop throught all localizable files (the .strings)
all_defined_keys = {}
all_defined_keys_by_lang = {}
error_key_double = 0
files_by_lang = utils.get_localizable_files()
for lang, file in files_by_lang.iteritems():
	lines = []
	defined_localizable_keys = []
	lines += utils.get_file_lines(file)
	for line in lines:
		localizable_key = utils.extract_localizable_key_definition(line.content)
		if localizable_key:
			if localizable_key in defined_localizable_keys:
				error_key_double += 1
			else:
				defined_localizable_keys.append(localizable_key)
				all_defined_keys[localizable_key] = True
	all_defined_keys_by_lang[lang] = list(set(defined_localizable_keys)) #set and remove all duplicates

console.analyze_keys(all_defined_keys, all_defined_keys_by_lang)

print '> Inspecting UNTRANSLATED Keys'
print '\t> Finding keys used in code but not in .string'
#Verify all Keys used in code have definition in all languages.string
error = 0
unfound_key_count = 0
for key, lines in used_key_list.iteritems():
	missing_lang = []
	for lang, trans_keys in all_defined_keys_by_lang.iteritems():
		found = 0
		if key not in trans_keys:
			missing_lang.append(lang.upper())
	if len(missing_lang):
		error += len(lines)
		unfound_key_count += 1
		console.untranslated_errors.append("Error: Untranslated {} for {}".format(key, missing_lang))
		for line in lines:
			console.untranslated_errors.append("\t {}, l:{}".format(line.filepath, line.line_nb))

print '\t> Finding keys not translated'
for lang, lang_keys in all_defined_keys_by_lang.iteritems():
	lang = lang.upper()
	for key, unused_var in all_defined_keys.iteritems():
		key_found = False
		if key not in lang_keys:
			unfound_key_count += 1
			if lang in console.untranslated_keys:
				console.untranslated_keys[lang].append(key)
			else:
				console.untranslated_keys[lang] = [key]
			
console.untranslated_keys_number = unfound_key_count
console.untranslated_errors_number = error

print '> Inspecting UNUSED keys'
keys_found_in_code = {}
keys_missing_in_code = {}
for key, unused_param in all_defined_keys.iteritems(): 
	#Search for key (as regular Str, ex: "plop") in all code line
	if key in potential_localized_keys:
		if key in keys_found_in_code: 
			keys_found_in_code[key].append(lang.upper())
		else:
			keys_found_in_code[key] = [lang.upper()]
	else:
		if key in keys_missing_in_code:
			keys_missing_in_code[key].append(lang.upper())
		else:
			keys_missing_in_code[key]= [lang.upper()]

for key, langs in keys_missing_in_code.iteritems():
	console.unused_keys.append(key)

if autocorrect_active:
	print '> Autocorrect launching'
	if len(console.unused_keys) == 0:
		print '\t> Nothing to be fixed'
	else:
		res = autocorrect.erase_keys_from_localizables(keys_missing_in_code)
		error += res

console.errors_number = error + error_key_double
if 	console.errors_number > 0:
	print "> Terminated with {} errors".format(console.errors_number)
else:
	print '> Successfully terminated'

print "> Reporting : HTML={}, Console={}".format(config.report_output_html, config.report_output_console)
if config.report_output_html:
	print '\t> Generating HTML Report : {}'.format(config.report_output_html_filepath)
	console.report_on_html_file(config.report_output_html_filepath)

if config.report_output_console:
	print '\t> Generating console report'
	console.report_on_console()

exit(console.errors_number)
