from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "GDXray+"
PROJECT_NAME_FULL: str = "GDXray+: The GRIMA X-ray Database"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(
    source_url="https://domingomery.ing.puc.cl/material/gdxray/", redistributable=False
)
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Security()]
CATEGORY: Category = Category.Security()

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [CVTask.ObjectDetection()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2015

HOMEPAGE_URL: str = "https://domingomery.ing.puc.cl/material/gdxray/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 8854265
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/gdxray"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Castings (314MB)": "http://dmery.sitios.ing.uc.cl/images/GDXray/Castings.zip",
    "Welds* (209MB)": "http://dmery.sitios.ing.uc.cl/images/GDXray/Welds.zip",
    "Baggage (3.048GB)": "http://dmery.sitios.ing.uc.cl/images/GDXray/Baggages.zip",
    "Nature (192MB)": "http://dmery.sitios.ing.uc.cl/images/GDXray/Nature.zip",
    "Settings (73MB)": "http://dmery.sitios.ing.uc.cl/images/GDXray/Settings.zip",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[
    Union[str, List[str], Dict[str, str]]
] = "http://dmery.sitios.ing.uc.cl/Prints/ISI-Journals/2015-JNDE-GDXray.pdf"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {
    "GitHub": "https://github.com/computervision-xray-testing/GDXray"
}

CITATION_URL: Optional[str] = "https://domingomery.ing.puc.cl/material/gdxray/"
AUTHORS: Optional[List[str]] = [
    "Domingo Mery",
    "Vladimir Riffo",
    "Uwe Zscherpel",
    "German Mondrag'on",
    "Ivan Lillo",
    "Irene Zuccar",
    "Hans Lobel",
    "Miguel Carrasco",
]
AUTHORS_CONTACTS: Optional[List[str]] = [
    "http://dmery.ing.puc.cl/",
    "https://github.com/domingomery",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "Pontificia Universidad Catolica de Chile",
    "Universidad de Atacama, Chile",
    "BAM, Germany",
    "Universidad de Santiago de Chile",
    "Universidad Adolfo Ibanez",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.uc.cl/",
    "https://uda.cl/",
    "https://www.bam.de/Navigation/EN/Home/home.html",
    "https://www.usach.cl/",
    "https://www.uai.cl/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "groups": ["baggages", "castings", "nature", "settings", "welds"]
}
TAGS: Optional[List[str]] = ["synthetic"]


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
