import os

def upload_thumbnail(self, video_id, file_path):
        print('Uploading thumbnail...')
        request = self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=file_path
        )
        response = request.execute()
        print(response)

def upload_video(self, file_path, video_content):
    body = dict(
        snippet=dict(
            title=video_content.title,
            description=video_content.description,
            tags=video_content.tags,
            categoryId=video_content.category_id
        ),

        status=dict(
            privacyStatus=video_content.privacy_status
        )
    )

    insert_request = self.youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body= MediaFileUpload(
            file_path, chunksize=-1, resumable=True)
    )

    video_id = self.resumable_upload(insert_request)
    self.upload_thumbnail(video_id, 'files/youtube/thumbnail.png')

def upload(bin_dir: str, image_dir: str, filename: str):
    # Try and find thumbnail.png or thumbnail.jpg. If they don't exist, use the first image from the paper
    if os.path.exists(os.path.join(bin_dir, "thumbnail.png")):
        thumbnail = os.path.join(bin_dir, "thumbnail.png")
    elif os.path.exists(os.path.join(bin_dir, "thumbnail.jpg")):
        thumbnail = os.path.join(bin_dir, "thumbnail.jpg")
    elif os.path.exists(os.path.join(image_dir, f"{filename}_{0}.png")):
        thumbnail = os.path.join(image_dir, f"{filename}_{0}.png")
    else:
        assert False, "No thumbnail available"
         
    # Use cleaned content and get a video title, video description (including github link), and tags
    

    # Upload