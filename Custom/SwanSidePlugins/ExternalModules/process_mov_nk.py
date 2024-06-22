#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import json
import nuke
import base64

this_dir = os.path.dirname(__file__)


def encode_dict(data_dict):
    # encode
    data_as_64 = json.dumps(data_dict, ensure_ascii=False)
    data_as_64 = six.ensure_binary(data_as_64)
    data_as_64 = base64.urlsafe_b64encode(data_as_64)
    data_as_64 = str(data_as_64)
    return data_as_64


def decode_dict(endode_dict):
    data = base64.urlsafe_b64decode(str(endode_dict))
    data_dict = json.loads(data)
    return data_dict


def run(path_in, path_out, frame_in, frame_out, from_blender=False):
    nuke.scriptOpen(os.path.join(this_dir, "to_mov.nk"))

    r = nuke.nodes.Read(file=path_in)
    w = nuke.toNode("OUT")
    s = nuke.toNode("Shuffle1")

    s.setInput(0, r)
    w.setInput(0, s)

    r['first'].setValue(frame_in)
    r['last'].setValue(frame_out)
    w["file"].setValue(path_out)
    s["disable"].setValue(0 if from_blender else 1)

    nuke.execute("OUT", frame_in, frame_out)


if __name__ == '__main__':
    from pprint import pprint
    f = open(str(sys.argv[1]))
    data_dict = json.load(f)

    pprint(data_dict)

    run(
        data_dict.get("input_path").replace("\\", "/"),
        data_dict.get("output_path").replace("\\", "/"),
        int(data_dict.get("frame_in")),
        int(data_dict.get("frame_out")),
        bool(data_dict.get("from_blender", False))
    )

# "C:\\Program Files\\Nuke13.0v1\\Nuke13.0.exe" -x C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\ExternalModules\process_mov_nk.py 'eyJpbnB1dF9wYXRoIjogIkQ6XFxEZXNrXFxweXRob25cXFByb2plY3RzXFxUZXN0UHJvZFxcMDNfUHJvZHVjdGlvblxcU2hvdHNcXHZpbmNcXHZpbmNfc2hfMDIwXFxSZW5kZXJzXFwzZFJlbmRlclxcQW5pbWF0aW9uXFx2MDAxNVxcYmVhdXR5XFx2aW5jLXZpbmNfc2hfMDIwX0FuaW1hdGlvbl92MDAxNV9iZWF1dHkuJTA0ZC5leHIiLCAib3V0cHV0X3BhdGgiOiAiRDpcXERlc2tcXHB5dGhvblxcUHJvamVjdHNcXFRlc3RQcm9kXFwwM19Qcm9kdWN0aW9uXFxTaG90c1xcdmluY1xcdmluY19zaF8wMjBcXFJlbmRlcnNcXDNkUmVuZGVyXFxBbmltYXRpb25cXHYwMDE1XFx0ZXN0Lm1vdiIsICJmcmFtZV9pbiI6IDEwMDEsICJmcmFtZV9vdXQiOiAxMDAyfQ=='