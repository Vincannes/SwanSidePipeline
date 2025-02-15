#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re
import sys
import logging
import tempfile
import subprocess

from PrismUtils.Decorators import err_catcher

PUBLISHER_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(PUBLISHER_DIR, "ExternalModules")

logger = logging.getLogger(__name__)


class Media(object):

    def __init__(self, core):
        self.core = core
        self._core_media = self.core.media

    def get_first_last_frames(self, inputpathdir, inputExt):
        # self.core.paths.getFrameFromFilename()
        endNum = None
        startNum = None
        pattern = r'\.(\d+)\.[^.]+$'
        inputpathdir = os.path.normpath(inputpathdir)
        if not os.path.isdir(inputpathdir):
            inputpathdir = os.path.dirname(inputpathdir)
        if any([inputExt in ext for ext in [".exr", ".jpg", ".png", ".dpx"]]):
            frames = []
            for filename in os.listdir(inputpathdir):
                match = re.search(pattern, filename)
                if match:
                    frames.append(int(match.group(1)))
            startNum = sorted(frames)[0] or 1001
            endNum = sorted(frames)[-1] or 1001
        return startNum, endNum

    @err_catcher(name=__name__)
    def process_mov_file_from_sequence(self, path):
        _, file_extension = os.path.splitext(path)

        # generate tmp file
        filename = self.generate_tmp_file()
        tmp_mov = os.path.join(
            os.path.dirname(filename), os.path.basename(filename) + ".mov"
        )
        tmp_mov = tmp_mov.replace("\\", "/")
        concat_file = self._generate_concat_file(
            os.path.dirname(path), file_extension
        )

        argList = [
            "-f", "concat", "-safe", "0",
            "-r", "24", "-i",  f"{concat_file}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "18",
            f"{tmp_mov}"
        ]

        self.process_custom_ffmpeg(argList, useShell=False)
        return tmp_mov

    def _old_process_mov_file_from_exr(self, path):
        _, file_extension = os.path.splitext(path)
        first_frame, last_frame = self.get_first_last_frames(
            os.path.dirname(path), file_extension
        )

        # generate tmp file
        filename = self.generate_tmp_file()
        tmp_mov = os.path.join(
            os.path.dirname(filename), os.path.basename(filename) + ".mov"
        )
        tmp_mov = tmp_mov.replace("\\", "/")
        result = self._core_media.convertMedia(path, first_frame, tmp_mov)

        if "Conversion failed" in result[1]:
            msg = "{}\n\nMissing Channel RGB for file {}.\nPlease check your file, rerender with right RGB channels " \
                  "and republish\n".format("\n".join(result), path)
            raise ValueError(msg)

        return tmp_mov

    @err_catcher(name=__name__)
    def process_custom_ffmpeg(self, argList, useShell=True):
        ffmpeg_path = '{}'.format(self._core_media.getFFmpeg(validate=True))

        argList.insert(0, ffmpeg_path)
        argList = [arg.replace("\\", "/") for arg in argList]

        try:
            nProc = subprocess.Popen(
                argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            # nProc.wait()
            stdout, stderr = nProc.communicate()

            try:
                stdout_decoded = stdout.decode("utf-8", errors="ignore")
                stderr_decoded = stderr.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                stdout_decoded = stdout.decode("latin1", errors="ignore")
                stderr_decoded = stderr.decode("latin1", errors="ignore")

            if nProc.returncode != 0:
                raise RuntimeError(
                    f"FFmpeg failed with code {nProc.returncode}\n"
                    f"Command: {' '.join(argList)}\n"
                    f"Error: {stderr_decoded}"
                )
            return stdout_decoded, stderr_decoded
        except Exception as e:
            raise RuntimeError(f"Error running FFmpeg command: {str(e)}")

    def _process_custom_ffmpeg(self, argList):
        ffmpeg_path = self._core_media.getFFmpeg(validate=True)
        argList.insert(0, ffmpeg_path)
        nProc = subprocess.Popen(
            argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        nProc.wait()
        result = nProc.communicate()

        if sys.version[0] == "3":
            result = [x.decode("utf-8", "ignore") for x in result]
        return result

    def generate_tmp_file(self):
        _, filename = tempfile.mkstemp(prefix="mov")
        return filename

    def _generate_concat_file(self, folder, extension):
        tmp_filename = self.generate_tmp_file()
        filename = os.path.basename(tmp_filename)
        output_txt = os.path.join(
            os.path.dirname(tmp_filename),
            "{}_List.txt".format(filename)
        )

        files = sorted([f for f in os.listdir(folder) if f.endswith(extension)])
        with open(output_txt, "w") as f:
            for file in files:
                file_path = os.path.join(folder, file).replace("\\", "/")
                f.write(f"file '{file_path}'\n")

        return output_txt
