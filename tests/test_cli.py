import subprocess


def test_invoke_list():
    """Test invoke --list"""
    return_code = subprocess.call("invoke --list", shell=True)

    assert return_code == 0


def test_requirements_txt():
    """Validate that requirements.txt and requirements-dev.txt
       are up2date with Pipefile"""
    temp_output_dir = "tests/temp_output"
    req_test_file_path = "{}/test-requirements.txt".format(temp_output_dir)
    req_dev_test_file_path = "{}/test-requirements-dev.txt".format(temp_output_dir)

    return_code_0 = subprocess.call("mkdir -p {}".format(temp_output_dir), shell=True)
    return_code_1 = subprocess.call(
        "pipenv lock -r \
                                    > {}".format(
            req_test_file_path
        ),
        shell=True,
    )

    return_code_2 = subprocess.call(
        "pipenv lock -r --dev \
                                    > {}".format(
            req_dev_test_file_path
        ),
        shell=True,
    )

    with open("requirements.txt") as file:
        req_file = file.read()

    with open("requirements-dev.txt") as file:
        req_dev_file = file.read()

    with open(req_test_file_path) as file:
        req_test_file = file.read()

    with open(req_dev_test_file_path) as file:
        req_dev_test_file = file.read()

    return_code_z = subprocess.call("rm -rf {}".format(temp_output_dir), shell=True)

    assert req_file == req_test_file

    assert req_dev_file == req_dev_test_file
