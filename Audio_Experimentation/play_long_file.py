# import soundfile as sf
# import sounddevice as sd
# import argparse
#
# def int_or_str(text):
#   try:
#     return int(text)
#   except ValueError:
#     return text
#
#
# parser = argparse.ArgumentParser(add_help=False)
# parser.add_argument('-l', '--list-device', action='store_true', help='show list of audio devices and exit')
# args, remaining = parser.parse_known_args()
# if args.list_devices:
#   print(sd.query_devices())
#   parser.exit(0)
# parser.add_argument(descrption=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[parser])
# parser.add_argument('filename', metavar='FILENAME', help='audio file to be playedback')
# parser.add_argument('-d', '--device', type=int_or_str, help='output device (numeric ID or substring)')
# args = parser.parse_args(remaining)
#
# try:
#   data, fs = sf.read(args.filename, dtype='float32')
#   sd.play(data, fs, device=args.device)
#   status = sd.wait()
# except KeyboardInterrupt:
#   parser.exit('\nInterrupted by user')
# except Exception as e:
#   parser.exit(type(e).__name__ + ': ' + str(e))
# if status:
#   parser.exit('Error during playback: ' + str(status))


import argparse

import sounddevice as sd
import soundfile as sf


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', metavar='FILENAME',
    help='audio file to be played back')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
args = parser.parse_args(remaining)

try:
    data, fs = sf.read(args.filename, dtype='float32')
    sd.play(data, fs, device=args.device)
    status = sd.wait()
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
if status:
    parser.exit('Error during playback: ' + str(status))
