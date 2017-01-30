 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import config

class Console(object):
	def __init__(self):
		self.number_lines = {}
		self.potential_localized_keys = 0
		self.keys_in_code = {}
		self.keys = {}
		self.untranslated_keys_number = 0
		self.untranslated_errors_number = 0
		self.untranslated_errors = []
		self.untranslated_keys = {}
		self.unused_keys_number = 0
		self.unused_keys = []
		self.errors_number = 0


	def analyze_keys(self, all_defined_keys, all_defined_keys_by_lang):
		self.keys['all'] = len(all_defined_keys)
		for lang, trans_keys in all_defined_keys_by_lang.iteritems(): 	
			self.keys[lang.upper()] = len(trans_keys)

	def report_on_console(self):
		print ''
		print '  ___                  _                             _   '
		print ' / __|___ _ _  ___ ___| |___   _ _ ___ _ __  ___ _ _| |_ '
		print "| (__/ _ \ ' \(_-</ _ \ / -_) | '_/ -_) '_ \/ _ \ '_|  _|"
		print ' \___\___/_||_/__/\___/_\___| |_| \___| .__/\___/_|  \__|'
		print '                                      |_|                '
		print ''
		print '========================================================================='
		print 'Code analyzing '
		print '========================================================================='
		for pattern, number_of_lines in self.number_lines.iteritems():
			print "Analyzing {} lines in {}".format(number_of_lines, pattern)
		print "Found {} potential keys in {} (cf 'config.py')".format(self.potential_localized_keys, config.files_to_analyze)
		print "Found {} unique KEYS in .m and .swift, {} usages in total (usage searched in config.py : {} )".format(self.keys_in_code['unique'], 
					self.keys_in_code['usage'], 
					config.localized_string_in_code_regex)

		print ''
		print '========================================================================='
		print "Inspect the {} keys in .strings".format(self.keys['all'])
		print '========================================================================='
		for lang, keys_number in self.keys.iteritems():
			if lang != 'all':
				missing_key = ""
				missing_key_number = self.keys['all'] - keys_number
				if missing_key_number > 0:
					missing_key = "Missing : {} key(s)".format(missing_key_number)
				print "Found {} keys in .strings for {lang} {missing_key}".format(keys_number, lang = lang, missing_key = missing_key)

		print ''
		print '========================================================================='
		print "{} untranslated keys present on {} code line(s)".format(self.untranslated_keys_number, self.untranslated_errors_number)
		print '========================================================================='
		if self.untranslated_keys_number == 0:
			print ''
		else :
			print '-------------------------------------------------------------------------'
			print 'Untranslated keys'
			print '-------------------------------------------------------------------------'
			for lang, untranslated_keys_by_lang in self.untranslated_keys.iteritems():
					if len(untranslated_keys_by_lang) > 0:
						print "{}".format(lang)
						for untranslated_key_by_lang in untranslated_keys_by_lang:
							print "\t{}".format(untranslated_key_by_lang)
			print '-------------------------------------------------------------------------'
			print 'Keys used in code but not in .string'
			print '-------------------------------------------------------------------------'
			for error in self.untranslated_errors:
				print error

		print ''
		print '========================================================================='
		print "{} unused keys".format(len(self.unused_keys))
		print '========================================================================='
		for unused_key in self.unused_keys:
			print "Warning : unused '{}'".format(unused_key)

		print ''
		print ''
		print '========================================================================='
		if self.errors_number > 0:
			print ' ___ _   ___ _    '
			print '| __/_\ |_ _| |   '
			print '| _/ _ \ | || |__ '
			print '|_/_/ \_\___|____|'
			print ''
		else:
			print ' ___ _   _  ___ ___ ___ ___ ___  '
			print '/ __| | | |/ __/ __| __/ __/ __| '
			print '\__ \ |_| | (_| (__| _|\__ \__ \ '
			print "|___/\___/ \___\___|___|___/___/ "
			print ''
		print '========================================================================='

	def report_on_html_file(self, filepath):
		with open(filepath, "w+") as file:
			html = '<section name="testTraductions" fontcolor="#000000">\n'

			"""
			Code analyzing
			"""
			html +=		'<accordion name="Code analyzing">\n'
			html +=			'<field name="Files analyzing" titlecolor="black" value="" detailcolor="#000000"> <![CDATA[\n'
			for pattern, number_of_lines in self.number_lines.iteritems():
				html +=			"Analyzing {} lines in {}\n".format(number_of_lines, pattern)
			html +=			']]> </field>\n'
			html +=			'<field name="Keys analyzing" titlecolor="black" value="" detailcolor="#000000"> <![CDATA[\n'
			html +=				"Found {} potential keys in {} (cf 'config.py')\n".format(self.potential_localized_keys, 
				config.files_to_analyze)
			html +=				"Found {} unique KEYS in .m and .swift, {} usages in total (usage searched in config.py : {} )\n".format(self.keys_in_code['unique'], self.keys_in_code['usage'], 
				config.localized_string_in_code_regex)
			html +=			']]> </field>\n'
			html +=		'</accordion>\n'

			"""
			Inspect keys in .strings
			"""
			html +=		'<accordion name="Inspect keys in .strings">\n'
			html +=			'<field name="Found {} unique keys" titlecolor="black" value="" detailcolor="#000000"> <![CDATA[\n'.format(self.keys['all'])
			for lang, keys_number in self.keys.iteritems():
				if lang != 'all':
					missing_key = ""
					missing_key_number = self.keys['all'] - keys_number
					if missing_key_number > 0:
						missing_key = "<b style='color:red'>Missing : {} key(s)</b>".format(missing_key_number)
					html += 	"Found {} keys in .strings for {lang} {missing_key}\n".format(keys_number, lang = lang, missing_key = missing_key)
			html +=			']]> </field>\n'
			html +=		'</accordion>\n'

			"""
			Untranslated keys
			"""
			html +=		'<accordion name="{} untranslated keys present on {} code line(s)">\n'.format(self.untranslated_keys_number, self.untranslated_errors_number)
			if self.untranslated_keys_number == 0:
				html += 	'<field name="No error" titlecolor="green" value="Good job !" detailcolor="green"></field>\n'
			else:
				html +=		'<field name="Untranslated keys" titlecolor="black" value="" detailcolor="#000000"> <![CDATA[\n'
				for lang, untranslated_keys_by_lang in self.untranslated_keys.iteritems():
					if len(untranslated_keys_by_lang) > 0:
						html +=		"{}\n".format(lang)
						for untranslated_key_by_lang in untranslated_keys_by_lang:
							html +=	"\t<b style='color:red'>{}</b>\n".format(untranslated_key_by_lang)
				html +=			']]> </field>\n'
				html +=			'<field name="Keys used in code but not in .string" titlecolor="black" value="" detailcolor="#000000"> <![CDATA[\n'
				for error in self.untranslated_errors:
					html +=			"{}\n".format(error)
				html +=			']]> </field>\n'
			html +=		'</accordion>\n'

			"""
			Unused keys
			"""
			if len(self.unused_keys) > 0:
				html +=		'<accordion name="{} unused keys">\n'.format(len(self.unused_keys))
				html +=			'<field name="{} unused keys" titlecolor="orange" value="(use \'python main.py autocorrect\' to clean it)" detailcolor="black"> <![CDATA[\n'.format(len(self.unused_keys))
				for unused_key in self.unused_keys:
					html += "Warning : unused '<b style='color: orange'>{}</b>'".format(unused_key)
				html +=			']]> </field>\n'
				html +=		'</accordion>\n'
			else:
				html +=		'<field name="0 Unused keys" titlecolor="green" value="Good job !" detailcolor="green"></field>\n'

			html +=	'</section>\n'
			
			file.write(html)