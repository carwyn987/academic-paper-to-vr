from moviepy.editor import *

# def stitch_pages(page_image_map: dict[int,str], page_audio_map: dict[int,list], output_file: str, fps: float):
#     clips = []
#     for page in page_image_map:
#         image = ImageClip(page_image_map[page])
#         audio = AudioFileClip(page_audio_map[page])
#         clip = CompositeVideoClip([image.set_duration(audio.duration)])
#         clip = clip.set_audio(audio)
#         clips.append(clip)
    
#     final_clip = concatenate_videoclips(clips)
#     final_clip.write_videofile(output_file, fps=fps)

def stitch_pages(page_image_map: dict[int,str], page_audio_map: dict[int,list], output_file: str, fps: float):
    clips = []
    for page in page_image_map:
        print("PAGE: ", page)
        print("page_image_map::: ", page_image_map)
        image = ImageClip(page_image_map[page])
        audio_files = page_audio_map[page]
        
        # If the audio is split into multiple files, concatenate them
        audio_clips = [AudioFileClip(file) for file in audio_files]
        audio = concatenate_audioclips(audio_clips)
        
        clip = CompositeVideoClip([image.set_duration(audio.duration)])
        clip = clip.set_audio(audio)
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, fps=fps)