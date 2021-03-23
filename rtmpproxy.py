import subprocess
import select
import shutil
import sys

ffmpeg = sys.argv[6]
args_mts = ['-loglevel', 'error', '-timeout', '115', '-listen_timeout', '0', '-rw_timeout', '10000000', '-f', 'flv', '-listen', '1', '-i', sys.argv[4], '-c', 'copy', '-f', 'mpegts', '-']
args_flv = ['-loglevel', 'error', '-fflags', '+genpts', '-re', '-f', 'mpegts', '-i', '-', '-c:a', 'copy', '-bsf:a', 'aac_adtstoasc', '-c:v', 'copy', '-f', 'flv' ]
stream_url = sys.argv[1]
def main():
	flv = subprocess.Popen([ffmpeg]+args_flv+[stream_url],stdin=subprocess.PIPE)
	while True:
		mts = subprocess.Popen([ffmpeg]+args_mts,stdout=subprocess.PIPE)
		while True:
			r,w,e = select.select([mts.stdout],[],[],10)
			print((r,w,e))
			if len(r):
				shutil.copyfileobj(mts.stdout,flv.stdin)
				mts.wait()
				print('stream end')
				break
			else:
				f = open('idle.ts','rb')
				shutil.copyfileobj(f,flv.stdin)
				f.close()
				print('idle end')
		f = open('disconnect.ts','rb')
		shutil.copyfileobj(f,flv.stdin)
		f.close()
		print('restarting server')


def generate_text(duration,color,name,text,width,height,font):
	 subprocess.call([ffmpeg, '-i', '1.aac', '-y', '-filter_complex', "color=%s:s=%dx%d,loop=-1:size=2,drawtext='fontfile=%s:fontsize=60:text=%s:x=(w-text_w)/2:y=(h-text_h)/2'" % (color, width, height, font, text), '-t', str(duration), '-c:v', 'libx264', '-x264-params', 'keyint=60', '-bufsize', '500k', '-profile:v', 'main', '-preset:v','ultrafast', '-r', '15', '-g', '60', '-c:a', 'copy', '-f', 'mpegts', name])

width = int(sys.argv[2])
height = int(sys.argv[3])
generate_text(3,'red','disconnect.ts',sys.argv[7],width,height, sys.argv[5])
generate_text(5,'green','idle.ts',sys.argv[8],width,height, sys.argv[5])

main()