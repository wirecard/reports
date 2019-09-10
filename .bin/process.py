import os
from junitparser import JUnitXml
from datetime import datetime
from string import Template

REPORT_FILE_NAME = 'report.xml'
MASTER_BRANCH_NAME = 'master'
INDEX_TEMPLATE_FILE = os.path.join(os.getcwd(), 'docs', 'index_template.html')
INDEX_FILE = os.path.join(os.getcwd(), 'docs', 'index.html')
FULL_REPORT_LINK = "https://rawcdn.githack.com/" \
                   "wirecard/reports/master/" \
                   "$project/$gateway/$date/report.html"
FAILED_TEST = '<span style="color:red">FAIL</span>'
PASSED_TEST = '<span style="color:green">PASS</span>'
DATE_FOLDER_FORMAT = '%Y-%m-%d'
HTML_TABLE_HEADER_LINES = '<h2><b>Current status of acceptance tests</b><h2>\n'
HTML_TABLE_HEADER_CONTENT = '''<table class="blueTable">
<thead>
<tr>
<th>Project</th>
<th>Test Name</th>
<th>Status</th>
<th>Report link</th>
</tr></thead>'''

IGNORE_FOLDERS = [".bin", "docs", ".git", ".idea"]
REPORT_LINK_DATA = {}


def add_to_dict_array(input_dict, key,  value):
    try:
        results_arr = input_dict[key]
        if value not in results_arr:
            results_arr.append(value)
            input_dict[key] = results_arr
    except KeyError as e:
        results_arr = []
        if value not in results_arr:
            results_arr.append(value)
            input_dict[key] = results_arr
    return input_dict


def get_date_from_report_link_data(project_name, gateway):
    date_dict = filter(lambda gateway_dict: gateway_dict.get(gateway), REPORT_LINK_DATA[project_name])
    date = date_dict[0][gateway]
    return date


def find_latest_result_file(location, project, gateway)
    global REPORT_LINK_DATA
    dates = []
    if os.path.isdir(location):
        for sub_dirs in os.listdir(location):
            dates.append(datetime.strptime(sub_dirs, DATE_FOLDER_FORMAT))
        latest = max(d for d in dates)
        if os.path.isfile(os.path.join(location, latest.strftime(DATE_FOLDER_FORMAT), REPORT_FILE_NAME)):
            # Also keep the date for later link in the report
            REPORT_LINK_DATA = add_to_dict_array(REPORT_LINK_DATA, project, {gateway: latest.strftime(DATE_FOLDER_FORMAT)})
            return os.path.join(location, latest.strftime(DATE_FOLDER_FORMAT), REPORT_FILE_NAME)
        elif MASTER_BRANCH_NAME in os.listdir(os.path.join(location, latest.strftime(DATE_FOLDER_FORMAT))):
            REPORT_LINK_DATA = add_to_dict_array(REPORT_LINK_DATA, project, {gateway: latest.strftime(DATE_FOLDER_FORMAT)})
            return os.path.join(location, latest.strftime(DATE_FOLDER_FORMAT), MASTER_BRANCH_NAME, REPORT_FILE_NAME)
        else:
            return None
    else:
        return None


def process_results_file(gateway, result_file):
    gateway_res = {}
    features = {}
    # process
    xml = JUnitXml.fromfile(result_file)
    for suite in xml:
        # handle suites
        for case in suite:
            feature_name = case.name
            if feature_name not in features.keys():
                features[feature_name] = PASSED_TEST
            if case.result:
                features[feature_name] = FAILED_TEST
    gateway_res[gateway] = features
    return gateway_res


def process_results_files():
    test_results = {}
    root_dir = os.getcwd()
    for dir in os.listdir(root_dir):
        if dir not in IGNORE_FOLDERS and os.path.isdir(dir):
            print dir
            project = dir
            gateway_results = []
            for sub_dirs in os.listdir(os.path.join(root_dir, dir)):
                gateway = sub_dirs
                result_file = find_latest_result_file(os.path.join(root_dir, dir, sub_dirs), project, gateway)
                if result_file:
                    gateway_results.append(process_results_file(gateway, result_file))
            test_results[project] = gateway_results
    return reformat_dictionary(test_results)


def reformat_dictionary(dictionary):
    new_dict = {}
    # reformat test results dictionary
    # to have format that is easier to print
    for project, gateway in dictionary.items():
        for gateway_dict in gateway:
            for gateway_name, results in gateway_dict.items():
                new_dict = add_to_dict_array(new_dict, gateway_name, {project: results})
    return new_dict


def create_report_file():
    results = process_results_files()
    # create contents to put into html template
    html_table = HTML_TABLE_HEADER_LINES
    for gateway, project_results in sorted(results.items()):
        html_table += "<h3>{}<h3>\n".format(gateway)
        html_table += HTML_TABLE_HEADER_CONTENT
        for project in sorted(project_results):
            for project_name, test_results in sorted(project.items()):
                for test_name, test_result in sorted(test_results.items()):
                    date = get_date_from_report_link_data(project_name, gateway)
                    report_link = Template(FULL_REPORT_LINK).substitute({"project": project_name,
                                                                         "gateway": gateway,
                                                                         "date": date})
                    html_table += '<tr>'
                    for value in [project_name, test_name, test_result,
                                  '<a href="{}">Full report link</a></td>'.format(report_link)]:
                        html_table += '<td>{}</td>'.format(value)
                    html_table += '</tr>'
        html_table += '</table>'
    # put data into html template
    with open(INDEX_TEMPLATE_FILE, 'r') as template_file:
        src = Template(template_file.read())
        new_text = src.substitute({"table": html_table})
    with open(INDEX_FILE, 'w') as template_file:
        template_file.write(new_text)


def main():
    create_report_file()


if __name__ == "__main__":
    main()
