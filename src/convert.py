# https://github.com/computervision-xray-testing/GDXray


import os
import supervisely as sly
from supervisely.io.fs import (
    get_file_name_with_ext,
    get_file_name,
    get_file_ext,
    dir_exists,
    file_exists,
)
from collections import defaultdict
import scipy.io
from dotenv import load_dotenv

import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "GDXray"
    dataset_path = "/home/grokhi/rawdata/gdxray"
    batch_size = 30
    ds_name = "ds"
    images_ext = ".png"
    bboxes_file_name = "BoundingBox.mat"

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        file_index = int(get_file_name(image_path).split("_")[-1])
        series_value = get_file_name(image_path).split("_")[0]

        data = idx_to_bboxes.get(file_index)
        if data is not None:
            for bboxes in data:
                left = int(bboxes[0])
                top = int(bboxes[2])
                right = int(bboxes[1])
                bottom = int(bboxes[3])
                if top > bottom:  # B0031 error
                    top = int(bboxes[3])
                    bottom = int(bboxes[2])
                rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                label = sly.Label(rect, obj_class)
                labels.append(label)

        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == subfolder.lower()]

        tags += [sly.Tag(tag_series, value=series_value)]
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("object of interest", sly.Rectangle)
    tag_names = ["baggages", "castings", "nature", "settings", "welds"]
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    tag_series = sly.TagMeta("series", sly.TagValueType.ANY_STRING)

    # subfolder_meta = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=tag_metas + [tag_series])
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for subfolder in os.listdir(dataset_path):
        curr_images_path = os.path.join(dataset_path, subfolder)
        if dir_exists(curr_images_path):
            for curr_subfolder in os.listdir(curr_images_path):
                curr_data_path = os.path.join(curr_images_path, curr_subfolder)
                if dir_exists(curr_data_path):
                    images_names = [
                        im_name
                        for im_name in os.listdir(curr_data_path)
                        if get_file_ext(im_name) == images_ext
                        and im_name[: len(curr_subfolder)] == curr_subfolder
                    ]

                    idx_to_bboxes = defaultdict(list)
                    bboxes_path = os.path.join(curr_data_path, bboxes_file_name)
                    if file_exists(bboxes_path):
                        mat = scipy.io.loadmat(bboxes_path)["bb"]
                        for curr_data in mat:
                            idx_to_bboxes[int(curr_data[0])].append(
                                [
                                    int(curr_data[1]),
                                    int(curr_data[2]),
                                    int(curr_data[3]),
                                    int(curr_data[4]),
                                ]
                            )

                    progress = sly.Progress(
                        "Create dataset {}, add {} data, {}".format(
                            ds_name, subfolder, curr_subfolder
                        ),
                        len(images_names),
                    )

                    for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                        images_pathes_batch = [
                            os.path.join(curr_data_path, im_name) for im_name in images_names_batch
                        ]

                        img_infos = api.image.upload_paths(
                            dataset.id, images_names_batch, images_pathes_batch
                        )
                        img_ids = [im_info.id for im_info in img_infos]

                        anns = [create_ann(image_path) for image_path in images_pathes_batch]
                        api.annotation.upload_anns(img_ids, anns)

                        progress.iters_done_report(len(images_names_batch))
    return project
