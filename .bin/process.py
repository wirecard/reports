# this to be run on each push to the repo
import os
import subprocess
from junitparser import JUnitXml
from datetime import datetime

REPORT_FILE_NAME = 'report.xml'
TEST_RESULT_FILE_NAME = 'RESULTS.md'
TEST_RESULT_FILE = os.path.join("docs", TEST_RESULT_FILE_NAME)

FAILED_TEST = '<span style="color:red">FAIL</span>'
PASSED_TEST = '<span style="color:green">PASS</span>'
DATE_FOLDER_FORMAT = '%Y-%m-%d'
HEADER_LINE = "# Current status of acceptance tests per instance \n"
TABLE_HEADER = '''| Project | Test name | Status |
| ---  | --- | --- |\n'''
PROJECTS = ["paymentSDK-php", "woocommerce-ee"]
TEST_RESULTS = {}


def find_latest_result_file(location):
    dates = []
    if os.path.isdir(location):
        for sub_dirs in os.listdir(location):
            dates.append(datetime.strptime(sub_dirs, DATE_FOLDER_FORMAT))
        latest = max(d for d in dates)
        return os.path.join(location, latest.strftime(DATE_FOLDER_FORMAT), REPORT_FILE_NAME)
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
            feature_name = case.name.split(" ")[0].strip(":")
            if feature_name not in features.keys():
                features[feature_name] = PASSED_TEST
            if case.result:
                features[feature_name] = FAILED_TEST
    gateway_res[gateway] = features
    return gateway_res


def process_results_files():
    test_results = {}
    os.chdir('..')
    root_dir = os.getcwd()
    for dirs in os.listdir(root_dir):
        if dirs in PROJECTS:
            project = dirs
            gateway_results = []
            for sub_dirs in os.listdir(os.path.join(root_dir, dirs)):
                gateway = sub_dirs
                result_file = find_latest_result_file(os.path.join(root_dir, dirs, sub_dirs))
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
                try:
                    results_arr = new_dict[gateway_name]
                    if {project: results} not in results_arr:
                        results_arr.append({project: results})
                    new_dict[gateway_name] = results_arr
                except KeyError as e:
                    results_arr = []
                    if {project: results} not in results_arr:
                        results_arr.append({project: results})
                    new_dict[gateway_name] = results_arr
    return new_dict


# update README.md with latest results
def create_report_file():
    results = process_results_files()
    with open(TEST_RESULT_FILE, "w") as result_file:
        result_file.writelines(HEADER_LINE)
        for gateway, project_results in results.items():
            result_file.writelines("## {} \n".format(gateway))
            result_file.writelines(TABLE_HEADER)
            for project in project_results:
                for project_name, test_results in project.items():
                    for test_name, test_result in test_results.items():
                        result_file.writelines("| {}  | {} | {} |\n".format(project_name, test_name, test_result))


# push updated README to the repository
def push_to_upstream():
    subprocess.call('git config --global user.name "Travis CI"')
    subprocess.call('git config --global user.email "wirecard@travis-ci.org"')
    subprocess.call('git add docs/*')
    subprocess.call('git commit -m "[skip ci] Update docs with latest test results"')
    subprocess.call('git push https://{}@github.com/{} HEAD:master'.format(os.environ["GITHUB_TOKEN"],
                                                                           os.environ["TRAVIS_REPO_SLUG"]))
    print("Updated docs/RESULTS.md")


def main():
    create_report_file()
    push_to_upstream()


if __name__ == "__main__":
    main()
