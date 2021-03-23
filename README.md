
# rtmp fallback proxy

Simple ffmpeg-based rtmp relay with text fallback

## Usage

`rtmpproxy.py <target_url> <widh> <height> <listen_url> <font_path> <ffmpeg_path> <disconnect_text> <idle_text>`

## Example
`python3 rtmpproxy.py rtmp://example.com/path/key 2048 1536 rtmp://0.0.0.0:1935/live/app font.ttf /path/to/ffmpeg Disconnected Idle`

