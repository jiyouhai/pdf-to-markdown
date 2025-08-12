## TURING

![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-01.jpg?height=1557&width=1812&top_left_y=688&top_left_x=113)

## TURING

## Adding Hanwha Cameras to Turing Vision:

## Checklist, Installation Guide, and Video Tutorials

- Hanwha Camera Installation Steps
- 1. Access Camera's Web UI
- 2. Initialize Camera
- 3. Verify/Modify Camera Encoding Settings
- 4. Enable Motion Detection
- 5. Connect \& Add Camera(s) to Turing NVR
- Installation Video
- Hanwha Camera FAQs


## Hanwha Camera Installation Steps

For Steps 1-4, please connect your camera directly to LAN, as shown below
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-03.jpg?height=481&width=1142&top_left_y=556&top_left_x=437)

- Access Camera's Web UI
- Locate your camera's IP Address
(i) TIP: On Turing Smart NVR, use Auto Search under Settings > Camera > Camera to find your camera's IP address
- Enter your camera's IP address into browser search bar


## TURING

- Initialize Camera
- On a factory-defaulted camera, the web UI will prompt you to create a new password for your camera
- Click Apply to initialize camera(s)
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-04.jpg?height=365&width=1048&top_left_y=915&top_left_x=804)

TIP: If installing multiple, use Wisenet's Device Manager to initialize and modify network settings

## TURING

- Verify/Modify Camera Encoding Settings
- Go to Basic > Video Profile
- Modify the encoding settings to the Turing recommended settings
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-05.jpg?height=801&width=1499&top_left_y=564&top_left_x=310)
(i) MJPEG profile is not used by the NVR.

On the Turing NVR, "H.264" profile is considered Main Stream, and "H.265" profile is considered Sub Stream.

|  | Main Stream | Sub Stream |
| :--- | :--- | :--- |
| Video Compression | H. 264 | H. 264 |
| Resolution | Less than 3MP (2MP is recommended) | 1280 x 720 (720P) |
| Frame Rate | 15 | 15 |
| Frame Interval | 30 | 30 |
| Bitrate Type | CBR | CBR |
| Bit Rate | Less than or equal to 2048 | Less than or equal to 768 |

## TURING

- Enable Motion Detection
- Go to Analytics > Motion Detection
- Click the Enable motion detection checkbox
- Edit the detection area, level of detection, sensitivity and minimum duration as desired
- Click Apply to save all settings
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-06.jpg?height=882&width=1644&top_left_y=825&top_left_x=246)


## TURING

- Connect \& Add Camera(s) to Turing NVR
i If desired, you can now connect your Hanwha camera directly to one of the POE ports on the back of the Turing Smart NVR, as shown below
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=422&width=1053&top_left_y=613&top_left_x=544)
- Access your Turing NVR web UI by entering its IP address into a web browser
- Login and go to Setup > Camera > Camera
- Select the channel and click Modify
- Edit the username and password fields
- Click Save

| TURING |  | Live View |  |  | Playback | 1 | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=18&width=20&top_left_y=1649&top_left_x=695) | Setup |  | do Smart |  |  |  |  |  |  | admin <br> Logout |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Client |  | Camera |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| System |  | $\square$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Auto Swritch to H. 265 - Off |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=49&width=161&top_left_y=1742&top_left_x=275) |  | Auto Switch to Smart Encoding Off Note: Effective when first connected |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| OSD |  | $\square$ <br> Refresh |  | Modify <br> Delete |  |  | Auto Search Search Segment |  |  |  |  | Batch Edit Pass... |  |  |  |  |  |  |  |  |  |
| Image |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=19&width=22&top_left_y=1829&top_left_x=476) | No. |  | Camera ID |  | Address |  |  |  |  | Port | Remote Camera ID |  | Protocol | Status | Vendor |  | Configure | Access |  |
| Schedule |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=16&width=20&top_left_y=1851&top_left_x=476) | 1 |  | D1 (Camera 01) |  | 172.16.0.105 |  |  |  |  | 80 |  | 1 | ONVIF | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=16&width=24&top_left_y=1851&top_left_x=1224) | ONVIF |  | VX-4V-OD-RI | Access |  |
|  |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=22&width=20&top_left_y=1867&top_left_x=482) |  | D2 (IP Camera 02) |  |  |  |  |  |  | 80 |  | 1 | ONVIF | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=17&width=22&top_left_y=1873&top_left_x=1224) | Avigilon |  | 2.0C-H4A-DP1 | Access |  |
| Video Loss |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=20&width=20&top_left_y=1888&top_left_x=482) |  | D3 (IP Camera 03) |  |  | 172.16.0.106 |  |  |  | 80 |  | 1 | ONVIF | $\square$ | Pelco |  |  | Access |  |
|  |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=21&width=20&top_left_y=1909&top_left_x=482) |  | D4 (IP Camera 04) |  |  | 172.16.0.108 |  |  |  | 80 |  | 1 | onvif | - | Axis |  | M2026-LE-MkII | Access |  |
| Tampering |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=20&width=20&top_left_y=1931&top_left_x=482) |  | D5 (IP Camera 05) |  |  | 172.16.0.109 |  |  |  | 80 |  | 1 | ONVIF | 떠 | Samsung Techwin |  | QNV-7010R | Access |  |
| Privacy Mask |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=20&width=20&top_left_y=1953&top_left_x=482) |  | D6 (IP Camera 06) |  |  | 172.15.0.7 |  |  |  | 80 |  | 1 | ONVIF | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=14&width=25&top_left_y=1959&top_left_x=1224) |  |  |  | Access |  |
| Snapshot |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=20&width=20&top_left_y=1975&top_left_x=482) |  | D8 (IP Camera 08) |  |  | 172.16.0.B |  |  |  | 80 |  | 1 | ONVIF | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=17&width=23&top_left_y=1980&top_left_x=1226) |  |  |  | Access |  |
| Audio Detection |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-07.jpg?height=21&width=20&top_left_y=1996&top_left_x=482) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Human Body Detection |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Hard Disk <br> $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Alarm | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Alert | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Network | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Platform | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| User |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Maintenance | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## TURING

![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-08.jpg?height=39&width=44&top_left_y=268&top_left_x=249)

3h http://10.2.11.37/cgi-bin/main-cgi

| W Wisenet WEBVIEWER | 2 | TR-MRP082T |  |  |  | x | $\square$ |  |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TURING |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-08.jpg?height=22&width=24&top_left_y=344&top_left_x=472) |  | Live View |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-08.jpg?height=22&width=27&top_left_y=345&top_left_x=606) |  |  | Playback | Setup |  | \% Smart |  |
| Client |  | Camera |  |  |  |  |  |  | Advanced |  |  |  |  |
| System |  |  | Add Mode <br> Plug-and-Play |  |  |  |  |  |  |  |  |  |  |
| $\wedge$ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Camera |  |  |  |  |  | $\square$ <br> Protocol |  |  | Private |  |  |  |  |
| Encoding |  |  | IP Address |  |  |  |  |  |  |  |  |  |  |
| OSD |  | Port |  |  |  |  |  |  | 80 |  |  |  |  |
| Image |  | Username |  |  |  |  |  |  | admin |  |  |  |  |
| Schedule |  | Password |  |  |  |  |  |  | ![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-08.jpg?height=23&width=57&top_left_y=591&top_left_x=685) |  |  |  |  |
| Video Loss |  |  |  | Remote Camera ID |  |  | 1 |  |  |  |  |  |  |
| Tampering |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Snapshot |  |  | Search | $\square$ |  | $\square$ <br> Save |  |  | $\square$ | Cancel |  |  |  |
| Audio Detection |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Human Body Detection |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Hard Disk | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |
| Alarm | $\vee$ |  |  |  |  |  |  |  |  |  |  |  |  |
| Alert | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |
| Network | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |
| Platform | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |
| User | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |
| Maintenance | $\checkmark$ |  |  |  |  |  |  |  |  |  |  |  |  |

## Installation Video

Click Here to Watch the Installation Video
![](https://cdn.mathpix.com/cropped/2025_08_04_fa7220547e4dcc903cd6g-08.jpg?height=993&width=1630&top_left_y=1412&top_left_x=253)

# TURING 

## Hanwha Camera FAQs

Q: Does the Turing Vision platform support Smart VCA Events from Hanwha camera?

At the moment, Turing Smart NVR and Turing Vision only support Motion events.

## TURING

## INTEGRATION GUIDE FOR HANWHA CAMERAS

Contact Us:

877-730-8222
sales@turingvideo.com

