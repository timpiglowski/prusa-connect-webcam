# prusa-connect-webcam
[![status: experimental](https://github.com/GIScience/badges/raw/master/status/experimental.svg)](https://github.com/GIScience/badges#experimental)

A Python-based service that captures images from a USB camera and uploads them to Prusa Connect. Designed to run on a Raspberry Pi using Docker.

## Notes
A few words about the project. This is a very experimental project. I did no testing with other camers than my Logitech C270, or on other hardware. It *should* work fine, but that's about as confident as it gets. I'd love to hear from anyone who has it running or which errors ocurr. Furthermore, this is my first ever docker repository, so I'm sure there's a lot of room for improvement. I'm always happy to get feedback!

Furthermore, I want to say thank you to @cannikin, who wrote a bash script to use the Camera Module for Prusa Connect. This project is greatly inspired by [cannikin's script](https://gist.github.com/cannikin/4954d050b72ff61ef0719c42922464e5) and would not exist without it.

## Installation
1. Make sure your Camera is connected and recognized by the Raspberry Pi. You can use
  ```bash
  ls /dev/video*
  ```
  to list all video devices. You should see somethin like `/dev/video0`.

2. Get your camera token. Login to Prusa Connect, go to the camera tab and hit "Add New other camera". Give it a descriptive name and copy the token.

3. Deploy the service with docker compose and set up your token. You need a docker-compose.yml file with the following content:
```yaml
services:
    camera:
        image: timpiglowski/prusa-connect-webcam:0.1.1
        volumes:
            - /opt/prusa-connect-webcam/camera_images:/app/camera_images
            - /dev/video0:/dev/video0
        environment:
            - HTTP_URL=https://connect.prusa3d.com/c/snapshot
            - DELAY_SECONDS=10
            - LONG_DELAY_SECONDS=60
            - FINGERPRINT=123456789012345678
            # Put your camera token here
            - CAMERA_TOKEN=YOURTOKEN
        restart: unless-stopped
        devices:
            - "/dev/video0:/dev/video0"
```

4. Run the container with `docker-compose up-d`. You should see the camera streaming in Prusa Connect.

## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
