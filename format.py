#!/usr/bin/env python3
import json
import sys
import requests

BASE_URL = (
    lambda s: f"https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/{s}/info.json"
)


def getKeymap(file_path: str) -> dict:
    with open(file_path) as f:
        return json.load(f)


def getInfo(keyboard_name: str) -> dict:
    response = requests.get(BASE_URL(keyboard_name))
    info_file = response.content.decode()
    return json.loads(info_file)


def longestKeycode(layers: list[list[str]]) -> int:
    longest_length = 0
    for layer in layers:
        for keycode in layer:
            l = len(keycode)
            if l > longest_length:
                longest_length = l
    return longest_length


def formatKeymap(keymap: dict, layout: list[dict]):
    output = keymap.copy()
    layers: list[list[str]] = output.pop("layers", [[""]])
    output = dict(sorted(output.items()))
    max_len = longestKeycode(layers) + 2
    print(max_len)
    output["layers"] = []
    for layer in layers:
        prev_row = 0
        layer_lst = []
        layer_str = ""
        keycodes = iter(layer)
        for key in layout:
            row, _ = key["matrix"]
            if row == prev_row + 1:
                layer_lst.append(layer_str)
                layer_str = ""
                prev_row += 1
            keycode = f'"{next(keycodes)}"'
            width = float(key.get("w", "1"))
            layer_str += keycode.center(round(max_len * width + (width - 1))) + ","
        output["layers"].append(layer_lst)
    for line in output["layers"][0]:
        print(line)


if __name__ == "__main__":
    num_args = len(sys.argv)
    file_path = sys.argv[1]
    keymap_file = getKeymap(file_path)
    info = getInfo(keymap_file["keyboard"])
    layout = info["layouts"][keymap_file["layout"]]["layout"]
    formatKeymap(keymap_file, layout)

    pass
