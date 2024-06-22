#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import importlib
import logging
from pprint import pprint

logger = logging.getLogger(__name__)

PUBLISHER_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(PUBLISHER_DIR, "ExternalModules")
sys.path.append(EXT_MODULES_PATHS)


class Publisher(object):

    def __init__(self, project_code, url, mail, password):
        url = url.strip("\\/") + "/api"

        self._gazu = importlib.import_module("gazu")
        self._gazu.client.set_host(url)
        self._gazu.log_in(mail, password)

        self._project = self._gazu.project.get_project_by_name(project_code)

    @property
    def gazu(self):
        return self._gazu

    def get_sequence(self, code):
        sequence = self._gazu.shot.get_sequence_by_name(self._project, code)
        return sequence

    def get_shot(self, code, sequence=None):
        if not sequence:
            raise ValueError("Need an Sequence")
        elif isinstance(sequence, str):
            sequence = self.get_sequence(sequence)
        shot = self._gazu.shot.get_shot_by_name(sequence, code)
        return shot

    def get_tasks(self, shot):
        return self._gazu.task.all_task_types_for_shot(shot)

    def get_task(self, task_name, shot_name):
        shot = self.get_shot(shot_name, shot_name.split("_")[0])
        tasks = self.get_tasks(shot)
        task_type = {}
        for i in tasks:
            if i.get("name") == task_name:
                task_type = self._gazu.task.get_task_by_entity(shot, i)
        return task_type

    def get_status(self, status_name):
        return self._gazu.task.get_task_status_by_short_name(status_name)

    def add_publish(self, task, status_name, comment="", file_path=None, preview_file=None):
        status = self.get_status(status_name)
        attachment = []
        if file_path:
            attachment = [file_path]
        kt_comment = self._gazu.task.add_comment(
            task, status, comment, attachments=attachment
        )
        if preview_file:
            self.add_preview_to_comment(task, kt_comment, preview_file)
        return kt_comment

    def get_comment(self, task, shot_name=None, last=False):
        if isinstance(task, str) and shot_name:
            task = self.get_task(task, shot_name)
        return self._gazu.task.get_last_comment_for_task(task)

    def get_comments(self, task, shot_name=None):
        if isinstance(task, str) and shot_name:
            task = self.get_task(task, shot_name)
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

    def test(self):
        task = self.get_task("Compositing", "test_sh_020")
        pprint(task)
        rev = self._gazu.files.new_working_file(
            task, name='main', mode='working',
            software=None, comment='', person=None,
            revision=0
        )
        pprint(rev)


if __name__ == '__main__':
    file_path = "D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Playblasts\\Animation\\v0015\\output.mp4"
    # file_path = "D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Playblasts\\Animation\\v0015\\vinc-vinc_sh_020_Animation_v0015.1001.jpg"
    publish = Publisher("Test Prod")
    seq = publish.get_sequence("vinc")

    # task = publish.get_task("Compositing", "test_sh_010")
    # pprint(task)
    # comment = publish.add_publish(task, "wip", "kjdlkqjzd")
    # pprint(comment)
    # pprint(comment)
    # publish.add_preview(task, comment, file_path)
    # for shot in publish.gazu.shot.all_shots_for_sequence(seq):
    # print(seq)
    shot = publish.get_shot("vinc_sh_020", seq)
    task = publish.get_task("Animation", shot.get("name"))
    # print("shot")
    # pprint(shot)
    # print("task")
    # pprint(task)
    # aa = publish.gazu.task.get_task_by_entity(shot, task)
    # pprint(aa)
    last_comment_revision = publish.get_comment(task)
    # comments = publish.get_comments(task)
    # print("comment")
    # i = 0
    # for comment in comments:
    #     if comment.get("revision") == last_comment_revision:
    #         pprint(comment)
    #         i+= 1
    # print(i)
    pprint(last_comment_revision)
    # pprint( publish.get_comment(task))
    # print("file_type")
    # file_type = publish.gazu.files.get_output_type_by_name("Quicktime")
    # pprint(file_type)
    # print("revision")

    # print("status")
    # status = publish.get_status("wip")
    # pprint(status)
    # print("revision")
    # revision = publish.gazu.task.add_revision(task, status["id"])
    # pprint(revision)
    # print("a")

    # working_file = publish.gazu.files.get_all_preview_files_for_task(
    #     task,
    # )
    # pprint(working_file)
    # print(len(working_file))

    # # comment = publish.gazu.task.add_comment(task, status, "Change status to work in progress")
    # preview_file = publish.gazu.task.add_preview(
    #     task, comment,
    #     preview_file_path=file_path
    # )
    # publish.gazu.task.set_main_preview(preview_file)  # Set preview as asset thumbnail
    #
    # pprint(comment)
    # pprint(preview_file)

    # with open(file_path, "rb") as file_data:
    #     print("file_data")
    #     pprint(file_data)
    #     a = publish.gazu.task.add_revision_preview(revision, file_data, file_path)
    # pprint(a)

    # revision = publish.gazu.files.new_entity_output_file(
    #     shot.get("id"), file_type, task.get("id"), "ocmentaire", working_file=file_path
    # )
    # # prev = publish.add_publish(task, "wip", "comment", file_path)
    # print()
    # pprint(revision)
    # print(len(comments))
    # pprint(publish.gazu.files.new_output_type("Quicktime", "mov"))
    # pprint(publish.gazu.files.get_output_type_by_name("Quicktime"))
