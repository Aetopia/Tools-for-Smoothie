from sys import argv
from os import path

def blur_settings():
    values = ()
    try:
        with open(argv[1], 'r') as file:
            options = file.read().splitlines()
    except IndexError:
        exit(1)           

    filters = (
        'blur:',
        'blur output fps:', 
        'blur amount:',
        'interpolate:',
        'interpolated fps:',
        'interpolation speed:',
        'interpolation tuning:',
        'interpolation algorithm:',
        'gpu:',
        'deduplicate:',
        'input timescale:',
        'output timescale:',
        'custom ffmpeg filters:',
    )    
    for filter in filters:
        for line in options:
            if filter in line and '#' not in line:
                values += line,
    return values       
    
def smoothie_settings():
    settings = blur_settings()
    values = ()
    for value in settings:
        values += value.split(':', 1)[1].strip(), 

    frame_blending = {'enabled':values[0], 
    'fps':values[1], 
    'intensity':values[2]
    }

    interpolation = {
        'enabled':values[3],
        'fps':values[4],
        'speed':values[5], 
        'tuning':values[6], 
        'algorithm':values[7], 
        'gpu':values[8],
        'deduplicate':values[9]
    }

    timescale = {
        'in':values[10],
        'out':values[11]
        }
    encoding_args = values[12]
    return (frame_blending, interpolation, timescale, encoding_args)     

def main():
    frame_blending, interpolation, timescale, encoding_args = smoothie_settings()
    if encoding_args == '':
        encoding_args = '-c:v libx265 -preset medium -crf 18'

    file = f"""[interpolation]
enabled={interpolation['enabled']}
fps={interpolation['fps']}
speed={interpolation['speed']}
tuning={interpolation['tuning']}
algorithm={interpolation['algorithm']}
gpu={interpolation['gpu']}

[frame blending]
enabled={frame_blending['enabled']}
fps={frame_blending['fps']}
intensity={frame_blending['intensity']}

[encoding]
process=ffmpeg
args={encoding_args}

[misc]
folder=
deduplication={interpolation['deduplicate']}
container=.mp4
flavors=fruits

[timescale] 
in={timescale['in']}
out={timescale['out']}    
"""
    with open(f'{path.abspath(path.splitext(path.split(argv[1])[1])[0])}.ini', 'w') as config:
        config.write(file)

if __name__ == '__main__':
    main()        