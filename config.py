"""
Relative path of the project 
ie : project_path = '../'
"""
project_path = '../'

"""
Pathes where file doesn't be analyze
ie : excluded_pathes = ['Pods/']
"""
excluded_pathes = ['Pods/']

"""
Patterns of the files to analyze in code
ie : files_to_analyze = ['*.swift', '*.m']
"""
files_to_analyze = ['*.swift', '*.m', '*.h']

"""
All languages to test
ie : languages = ["fr","en","es"]
"""
languages = ['de','en','es','fr','it','ru','tr','zh','pl']

"""
Folder path of the localizable files
ie : localizable_string_folder_path = 'Ressources/strings/'
"""
localizable_string_folder_path = 'Ressources/strings/'

"""
Names of the localizable file to test
ie : localizable_string_files = ["Localizable"]
"""
localizable_string_files = ['Localizable']

"""
Regex to find localized keys
ie = localized_string_in_code_regex = [r'["]\w+["][.]localized']
"""
localized_string_in_code_regex = [r'["]\w+["][.]localized', r'NSLocalizedString[(]@["]\w+["], nil[)]']

"""
White list regex of localizable keys
ie : localizable_key_regex = [r'[A-Z0-9_]+']
"""
localizable_key_regex = [r'[A-Z0-9_]+', r'iMSG_[A-Z0-9_]+', r'[A-Z0-9_]+_[a-zA-Z0-9_]+']

"""
Regex to define the unwanted prefix/suffix keys
ie : 
unwanted_localizable_key_prefix = r'(?!UNWANTED_PREFIX)'
unwanted_localizable_key_suffix = r'(?<!UNWANTED_SUFFIX)'
"""
unwanted_localizable_key_prefix = r'(?!RUGBYRAMA_)'
unwanted_localizable_key_suffix = r'(?<!_RUGBYRAMA)'

"""
Outputs of the report
"""
report_output_console = True
report_output_html = True

"""
Path to generate the report in HTML format
Can be used with a Jenkins to display the report after each test
Jenkins Plugin : https://wiki.jenkins-ci.org/display/JENKINS/Summary+Display+Plugin
ie : html_output_file = "./translate_reports.html"
"""
report_output_html_filepath = './translate_reports.html'

