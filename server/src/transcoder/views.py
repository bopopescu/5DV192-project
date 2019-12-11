import re

@staticmethod
def valid_output(str):
    pattern = re.compile("^\S[0-9a-zA-Z]*$")
    return bool(pattern.match(str))

def convert_resolution(resolution):
    if resolution == "Unchanged":
        return None
    elif resolution == "240p":
        return "426x240"
    elif resolution == "480p":
        return "854x480"
    elif resolution == "720p":
        return "hd720"
    elif resolution == "1080p":
        return "hd1080"
    elif resolution == "2k":
        return "2560x1440"
    elif resolution == "4k":
        return "3840x2160"


def convert_compression(compression):
    if compression == "Unchanged":
        return "copy"
    elif compression == "low":
        return "libx264 -crf 51"
    elif compression == "medium":
        return "libx264 -crf 23"
    elif compression == "high":
        return "libx264 -crf 0"

@staticmethod
def build_ffmpeg_os_encode_str():
    json_input_name = "sample-Elysium-2160p.mkv"
    json_resolution = "1080p"
    json_compression = "medium"
    json_output_namn = "outputFile"
    json_format = "avi"

    if not valid_output(json_output_namn):
        return False


    input_name = json_input_name
    resolution = convert_resolution(json_resolution)
    compression = convert_compression(json_compression)
    output = json_output_namn
    format = json_format

    return build_ffmpeg_encode(input_name, resolution, compression, output, format)

def build_ffmpeg_encode(input_name, resolution, compression, output_namn, format):
    if resolution is None:
        return "ffmpeg -i " + input_name + " -c:v " + compression + " " + output_namn + "." + format
    else:
        return "ffmpeg -i " + input_name + " -c:v " + compression + " -s " + resolution + " " + output_namn + "." + format
