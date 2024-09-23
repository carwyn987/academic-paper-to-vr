# academic-paper-to-vr

 You retain more information when you learn via multi-modal media. The goal of
 this project is to merge a pdf and a generated audio translation of said pdf 
 into a video. The user can then consume the content at once, maximizing 
 retention. I plan to use this on the treadmill at the gym, with my xreal 
 air AR glasses. For ease of compatibility, I will upload these to youtube, and
 piggyback off of youtube support. Although, the ultimate vision would be to
 take concepts from the text, convert them to diagrams or 3d figures, and 
 present next to the paper.

 Specifically, this repo automates the process of taking a paper (pdf), converting
 it to audio (mp3) and image (jpg), mixing the two together, and creating a video (mp4).

 Average cost per page (assuming no bugs, which I do NOT guarantee) = $0.07
  - E.g. an average length research paper is expected to cost ~$1.10

# Repo Organization

All outputs are generated in bin/ with the following structure

```
bin/
    PDF_FILENAME_NO_EXTENSION/
        audio/
            PDF_FILENAME_NO_EXTENSION_0.mp3                     # audio file for page 0
            PDF_FILENAME_NO_EXTENSION_1.mp3                     # audio file for page 1
            ...
        images/
            PDF_FILENAME_NO_EXTENSION_0.jpg                     # iamge file for page 0
            PDF_FILENAME_NO_EXTENSION_1.jpg                     # image file for page 0
            ...
        PDF_FILENAME_NO_EXTENSION.mp4                           # Final output file
```

# Setup

Ensure the environment is setup. Mine is set up in a venv with the requirements.txt file, and python 3.10.12

Ensure OPENAI_API_KEY is set as an environment variable.
 - The openai api key is used to clean text to ensure smooth diction, create the audio file, and potentially parse any images on the screen.

Install prerequisites
```
# Ensure you have python (I used 3.10.12)
sudo apt-get install python3-venv # if on debian distro
```

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="<YOUR API KEY HERE>" # Alternatively, put this in your ~/.bashrc to share across all projects
```

## Example Use:

```
python gen.py papers/do_things_that_dont_scale.pdf
```

```
python gen.py papers
```

# Assumptions

 - Any single page must be less than the fuzzy upper limit of 8192 characters (not a hard limit due to sentence boundaries chosen to split for audio translation).

# Future to-do's

 - Automatic upload to youtube, including title, tags, timestamp sectioning, etc. generation.
   - "Give me a short summary of this paper to put in my youtube description (e.g. this paper is about _), that also includes many "tag"-like words and concepts to match search queries well:" (needs updating so it doesn't explain)
 - Automate to take url's and automatically download pdf
 - Support other document types