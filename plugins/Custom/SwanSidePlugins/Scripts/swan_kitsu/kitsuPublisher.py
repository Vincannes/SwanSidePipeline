#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import logging
import argparse
import importlib
from pprint import pprint

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

logger = logging.getLogger(__name__)

PUBLISHER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXT_MODULES_PATHS = os.path.join(PUBLISHER_DIR, "ExternalModules")
sys.path.append(EXT_MODULES_PATHS)


class Publisher(object):

    def __init__(self, project_code, kitsu):
        self._kitsu = kitsu
        self._gazu = self._kitsu.gazu
        self._project = self._gazu.project.get_project_by_name(project_code)

    @property
    def gazu(self):
        return self._gazu

    def get_all_assets(self):
        assts = self._gazu.asset.all_assets_for_project(self._project)
        return assts

    def get_all_shots(self):
        shots = self._gazu.shot.all_shots_for_project(self._project)
        return shots

    def get_sequence(self, code):
        sequence = self._gazu.shot.get_sequence_by_name(self._project, code)
        return sequence

    def get_shot(self, code, sequence=None):
        shot = None
        if not sequence:
            shots = self.get_all_shots()
            for kit_shot in shots:
                if kit_shot.get("name") == code:
                    shot = kit_shot
                    break
        elif isinstance(sequence, str):
            sequence = self.get_sequence(sequence)
            shot = self._gazu.shot.get_shot_by_name(sequence, code)
        return shot

    def get_asset(self, code):
        asset = self._gazu.asset.get_asset_by_name(self._project, code)
        return asset

    def get_tasks(self, shot_asset, entity="shot"):
        if entity == "shot":
            return self._gazu.task.all_task_types_for_shot(shot_asset)
        else:
            return self._gazu.task.all_task_types_for_asset(shot_asset)

    def get_task(self, task_name, shot_name, entity="shot"):
        if entity == "shot":
            shot_asset = self.get_shot(shot_name)
        else:
            shot_asset = self.get_asset(shot_name)
        tasks = self.get_tasks(shot_asset, entity)
        task_type = {}
        for i in tasks:
            if i.get("name") == task_name:
                task_type = self._gazu.task.get_task_by_entity(shot_asset, i)
        return task_type

    def get_status(self, status_name):
        return self._gazu.task.get_task_status_by_short_name(status_name)

    def add_publish(self, task, status_name, comment="", file_path=None, preview_file=None):
        attachment = []
        status = self.get_status(status_name)
        if file_path:
            attachment = [file_path]
        kt_comment = self._gazu.task.add_comment(
            task, status, comment, attachments=attachment
        )
        if preview_file:
            self.add_preview_to_comment(task, kt_comment, preview_file)
        return kt_comment

    def last_status_task(self, task, shot_name=None, is_asset=False):
        comment = self.get_comment(task, shot_name, is_asset)
        if not comment:
            return None
        status = comment.get("task_status", {"short_name": None}).get("short_name")
        return status

    def get_status_from_path(self, task, shot_name, path):
        basename = os.path.basename(path).split(".")[0]
        comments = self.get_comments(task, shot_name)
        for com in comments:
            com_text = com.get("text")
            if basename in com_text:
                return com

    def get_comment(self, task, shot_name=None, is_asset=False):
        if isinstance(task, str) and shot_name:
            task = self.get_task(task, shot_name, "shot" if not is_asset else "asset")
        return self._gazu.task.get_last_comment_for_task(task)

    def get_comments(self, task, shot_name=None, is_asset=False):
        if isinstance(task, str) and shot_name:
            task = self.get_task(task, shot_name, "shot" if not is_asset else "asset")
        return self._gazu.task.all_comments_for_task(task)

    def add_preview_to_comment(self, task, comment, file_path):
        preview_file = self._gazu.task.add_preview(
            task, comment,
            preview_file_path=file_path
        )
        self._gazu.task.set_main_preview(preview_file)  # Set preview as asset thumbnail
        return preview_file

    def add_comment(self, task, status, comment, file_path):
        return self._gazu.task.add_comment(
            task, status, comment, attachments=[file_path]
        )

    def attach_file_to_comment(self, task, comment, file_path):
        preview_file = self._gazu.task.add_attachment_files_to_comment(
            task, comment, [file_path]
        )
        return preview_file

    @err_catcher(name=__name__)
    def publish(self, shot, task, path, entity="shot", status="wfa", comment="", preview_file=None):
        task = self.get_task(task, shot, entity)

        result = self.add_publish(
            task=task,
            comment=comment,
            file_path=path,
            preview_file=preview_file,
            status_name=status,
        )

        return result


if __name__ == '__main__':

    pub = Publisher("jbuybn")
    preview_file = "D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_010\\Renders\\2dRender\\base\\v0001\\_thumbs\\vinc-vinc_sh_010_base_v0001.1001.jpg"
    path = "D:/Desk/python/Projects/jbuybn/03_Production/Assets/Character/haaaaaaanj/Renders/3dRender/Shading/v0004/beauty/haaaaaaanj_Shading_v0004_beauty.1001.exr"
    print(pub.publish("haaaaaaanj", "Shading", path, "asset", "wfa", "teteztetete", preview_file))
    quit()
    import json
    import tempfile
    import platform

    prism_json = ""
    user_dir = os.environ["userprofile"]
    if platform.system() == "Windows":
        prism_json = os.path.join(user_dir, "Documents", "Prism2", "Prism.json")

    url = json.load(open(prism_json)).get("kitsu").get("url")
    email = json.load(open(prism_json)).get("kitsu").get("email")
    password = json.load(open(prism_json)).get("kitsu").get("password")

    parser = argparse.ArgumentParser(prog='Publisher')

    parser.add_argument('prod')
    parser.add_argument('type')
    parser.add_argument('shot')
    parser.add_argument('task')
    parser.add_argument('filepath')

    args = parser.parse_args()
    print(f"Process {args.prod} {args.type} {args.shot} {args.task} {args.filepath}")
    logger.info(f"Process {args.prod} {args.type} {args.shot} {args.task} {args.filepath}")

    status = "wfa"
    prod = args.prod
    publisher = Publisher(project_code=prod, url=url, mail=email, password=password)

    task = publisher.get_task(args.task, args.shot)

    preview_file = None
    file_path = args.filepath
    comment = "Publisher from Command Line : \n{}".format(os.path.basename(file_path).split(".")[0])
    if any([file_path.endswith(i) for i in [".exr", ".png", ".jpg"]]):
        ext = os.path.basename(file_path).split(".")[-1]
        _, temp_name = tempfile.mkstemp(suffix="mov")
        preview_file = "{}.mov".format(temp_name)
        frame_in, frame_out = publisher.media.get_first_last_frames(args.filepath, ext)
        file_status = publisher.media.process_mov_from_nuke(
            path=file_path,
            output_path=preview_file,
            frame_in=frame_in,
            frame_out=frame_out,
        )
        file_path = None

    aa = publisher.add_publish(
        task=task,
        comment=comment,
        file_path=file_path,
        preview_file=preview_file,
        status_name=status,
    )
    # cls & python.exe C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\Scripts\kitsuPublisher.py "Test Prod"  Shot vinc_sh_010 Compositing D:\Desk\python\Projects\TestProd\03_Production\Shots\vinc\vinc_sh_020\Renders\2dRender\test\v0007\vinc-vinc_sh_020_test_v0007.%04d.exr
