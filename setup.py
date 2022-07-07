from setuptools import setup
from typing import List

#Declaring variables for setup functions
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Nishit Hirpara"
DESCRIPTION="This is a first FSDS Machine Learning Projet"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"


def get_requirements_list()->List[str]:
    """
    Description: This function going to return list of requirement
    mentino in requirements.txt file

    return this functino is going to return a list which contain name 
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines()


setup(
name= PROJECT_NAME,
version= VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=PACKAGES,
install_requires=get_requirements_list()

)
 