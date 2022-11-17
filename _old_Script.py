import os, sys, json

def GetShellOut(Command):
    Running_Shell = os.popen(Command)
    os.wait()
    Out = Running_Shell.read()
    Running_Shell.close()
    return Out.rstrip()

def Download(url, DirFile):
    DownloadArgs = 'axel -n 16 -o "' + DirFile + '" "' + url + '"'
    print('下载命令: ' + DownloadArgs)
    Code = os.system(DownloadArgs)
    return Code

# 下载视频
def Methed_Run1(url):
    Title = GetShellOut('yt-dlp --get-title ' + url).replace(" - ","-").replace(" ","_")
    if len(Title) == 0:
        print('出现未知错误，无法获取视频标题，请检查网络连接和输入链接')
        exit(1)
    
    print('视频标题:',Title)
    
    os.system('mkdir -p Video/' + Title + '/tmp/{Video,Music}')
    
    print('正在获取下载信息...')
    DataJSON = GetShellOut('yt-dlp --dump-json ' + url)
    DownloadVideoUrl = GetShellOut('yt-dlp -f "bv" --get-url ' + url)
    DownloadMusicUrl = GetShellOut('yt-dlp -f "ba" --get-url ' + url)
    DownloadVideoFileName = GetShellOut('yt-dlp -f "bv" --get-filename ' + url)
    DownloadMusicFileName = GetShellOut('yt-dlp -f "ba" --get-filename ' + url)
    DownloadIconUrl = GetShellOut('yt-dlp -f "ba" --get-thumbnail ' + url)
    
    print('视频下载链接:' + DownloadVideoUrl)
    print('音频下载链接:' + DownloadMusicUrl)
    print('封面下载链接:' + DownloadIconUrl)
    print('视频文件名:' + DownloadVideoFileName)
    print('音频文件名:' + DownloadMusicFileName)
    
    if len(DownloadVideoUrl) == 0 or len(DownloadMusicUrl) == 0 or len(DownloadVideoFileName) == 0 or len(DownloadMusicFileName) == 0 or len(DownloadIconUrl) == 0 or len(DataJSON) == 0:
        print('出现未知错误，请检查网络连接和输入链接')
        exit(1)
    
    # 初始化JSON
    DataJSONDef = json.loads(DataJSON)

    Code = Download(DownloadVideoUrl, 'Video/' + Title + '/tmp/Video/' + DownloadVideoFileName)
    if  Code != 0:
        print("下载错误，退出代码:", Code >> 8)
        exit(1)
    del Code
    
    Code = Download(DownloadMusicUrl, 'Video/' + Title + '/tmp/Music/' + DownloadMusicFileName)
    if  Code != 0:
        print("下载错误，退出代码:", Code >> 8)
        exit(1)
    del Code
    
    Code = Download(DownloadIconUrl, 'Video/' + Title + '/tmp/Icon.webp')
    if  Code != 0:
        print("下载错误，退出代码:", Code >> 8)
        exit(1)
    del Code
    
    #格式转换
    Code = os.system('ffmpeg -y -i Video/"' + Title + '/tmp/Video/' + DownloadVideoFileName + '" "Video/' + Title + '/tmp/Video.mp4"')
    if  Code != 0:
        print("转换错误，退出代码:", Code >> 8)
        exit(2)
    del Code
    Code = os.system('ffmpeg -y -i Video/"' + Title + '/tmp/Music/' + DownloadMusicFileName + '" "Video/' + Title + '/' + Title + '.wav"')
    if  Code != 0:
        print("转换错误，退出代码:", Code >> 8)
        exit(2)
    Code = os.system('ffmpeg -y -i Video/"' + Title + '/tmp/icon.webp' + '" "Video/' + Title + 'icon.png"')
    if  Code != 0:
        print("转换错误，退出代码:", Code >> 8)
        exit(2)
    Code = os.system('ffmpeg -y -i Video/"' + Title + '/tmp/Video.mp4" -i "Video/' + Title + '/Music.wav" -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 "/Video' + Title + '/' + Title + '.mp4"')
    if  Code != 0:
        print("转换错误，退出代码:", Code >> 8)
        exit(2)
    
    print("下载和转换完成!")
    os.exit(0)

# 下载播放列表
def Methed_Run2(url):
    print ('开发中')

print('传入', len(sys.argv) - 1, '个参数')
print('传入参数:', sys.argv[1:])

if sys.argv[1].isdigit() == False:
    print('参数', sys.argv[1] ,'不是数字，无法判断操作')
    exit(4)

if os.path.exists('Video') == False:
    os.mkdir('Video')

if sys.argv[1] == '1':
    Methed_Run1(sys.argv[2])
elif sys.argv[1] == '2':
    Methed_Run2(sys.argv[2])
else:
    print('无效参数:', sys.argv[1])
    exit(3)
