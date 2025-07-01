from sounds import *
import json

speakers = speaker_init(pins=[6, 7, 8])

# 定義旋律和持續時間列表（使用前述馬力歐主題曲數據）
chords = [
    'E4', 'E4', 'r', 'E4', 'r', 'C4', 'E4', 'r', 'G4', 'r', 'G3', 'r',  # 前奏部分
    'C4', 'r', 'G3', 'r', 'E3', 'r', 'A3', 'B3', 'r', 'A#3', 'A3', 'r',  # 主旋律開始
    'G3 E4', 'G4', 'A4', 'r', 'F4', 'G4', 'r', 'E4', 'r', 'C4', 'D4', 'B3', 'r',  # 第一段發展
    'C4', 'r', 'G3', 'r', 'E3', 'r', 'A3', 'B3', 'r', 'A#3', 'A3', 'r',  # 重複部分
    'G3 E4', 'G4', 'A4', 'r', 'F4', 'G4', 'r', 'E4', 'r', 'C4', 'D4', 'B3', 'r'  # 結尾
]
durations = [
    0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.3, 0.15, 0.3, 0.15, 0.3, 0.15,  # 前奏部分
    0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.15, 0.15, 0.3, 0.15,  # 主旋律開始
    0.2, 0.2, 0.3, 0.15, 0.15, 0.15, 0.15, 0.3, 0.15, 0.15, 0.15, 0.3, 0.15,  # 第一段發展
    0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.15, 0.15, 0.3, 0.15,  # 重複部分
    0.2, 0.2, 0.3, 0.15, 0.15, 0.15, 0.15, 0.3, 0.15, 0.15, 0.15, 0.3, 0.15  # 結尾
]

if len(chords) != len(durations):
    length = min(len(chords), len(durations))
    chords = chords[:length]
    durations = durations[:length]

# # 建立字典來儲存數據
# melody = {
#     "chords": chords,
#     "durations": durations
# }
# 
# # 將數據寫入 JSON 檔案
# with open('melody.json', 'w') as json_file:
#     json.dump(melody, json_file)
# 
# print("JSON 檔案已成功儲存為 'melody.json'")
# 
# with open('melody.json', 'r') as json_file:
#     melody = json.load(json_file)
#     chords = melody['chords']
#     durations = melody['durations']
# 
# play_melody(speakers, chords, durations, volume=0.3)
index = 0
chord_start = time.time()
while True:
    # 每  秒播放一個音符
    if index == 0 or (time.time()-chord_start) >= durations[index-1]:
        if index >= len(chords):
            for speaker in speakers:
                mute_speaker(speaker)
            break
        play_chord(speakers, index, chords=chords, volume=0.3)
        index += 1  # 遞增音符索引，準備播放下一個音符
        chord_start = time.time()  # 更新計時器的起始時間為當前時間