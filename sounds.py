from machine import Pin, PWM
import time, math

# 定義音符頻率映射，基於 A4 = 440 Hz
def note_to_freq(note):
    """計算音符頻率，基於 A4 = 440 Hz"""
    A4_FREQ = 440.0
    pitch_map = {
        'C': -9, 'C#': -8, 'Db': -8, 'D': -7, 'D#': -6, 'Eb': -6,
        'E': -5, 'F': -4, 'F#': -3, 'Gb': -3, 'G': -2, 'G#': -1,
        'Ab': -1, 'A': 0, 'A#': 1, 'Bb': 1, 'B': 2
    }
    
    if not isinstance(note, str) or len(note) < 2:
        print(f"音符格式錯誤: {note}")
        return None
    if note[-2] in '#b':
        pitch_name, octave = note[:-1], note[-1]
    else:
        pitch_name, octave = note[0], note[1:]
    
    if pitch_name not in pitch_map:
        print(f"無效音符名稱: {pitch_name}")
        return None
    
    try:
        octave = int(octave)
    except ValueError:
        print(f"無效八度: {octave}")
        return None
    
    semitones_from_A4 = pitch_map[pitch_name] + (octave - 4) * 12
    freq = int(round(A4_FREQ * (2 ** (semitones_from_A4 / 12))))
    
    # 檢查頻率是否在可播放範圍內（通常 PWM 支援 100 Hz 至 20 kHz）
    if freq < 100 or freq > 20000:
        print(f"頻率 {freq} Hz 超出可播放範圍 (100-20000 Hz)")
        return None
    print(f"音符 {note} 頻率: {freq} Hz")  # 診斷日誌
    return freq

# 靜音單個揚聲器
def mute_speaker(speaker):
    """將 PWM 占空比設為 0，靜音揚聲器"""
    speaker.duty(0)

# 初始化多個揚聲器
def speaker_init(pins=[6, 7, 8]):
    """初始化 PWM 揚聲器，預設使用 3 個引腳"""
    speakers = []
    for pin in pins:
        speaker = PWM(Pin(pin, Pin.OUT))
        speaker.freq(1000)  # 預設頻率
        mute_speaker(speaker)  # 初始靜音
        speakers.append(speaker)
    print(f"初始化 {len(speakers)} 個揚聲器，引腳: {pins}")  # 診斷日誌
    return speakers

# 釋放所有揚聲器資源
def speaker_deinit(speakers):
    """釋放所有 PWM 揚聲器資源"""
    for speaker in speakers:
        speaker.deinit()
    print("揚聲器資源已釋放")  # 診斷日誌

# 播放單音或和弦
def play_chord(speakers, index, chords, volume=0.5):
    """
    播放單音或和弦（最多3音）或休止符
    參數:
        speakers: PWM 揚聲器列表
        chord: 音符字串，如 'E3', 'C#5', 'E3 C#5', 'r'
        volume: 音量 (0.0-1.0)
    """
    # 若當前音符為 'r'，則靜音揚聲器
    if chords[index] == 'r':
        for speaker in speakers:
            mute_speaker(speaker)
        return
    
    # 判斷是單音還是和弦
    notes = chords[index].split()
    num_notes = len(notes)
    
    if num_notes < 1 or num_notes > len(speakers):
        print(f"錯誤：無效音符數量: {num_notes}")
        return
    
    # 計算每個音的頻率
    frequencies = []
    for note in notes:
        freq = note_to_freq(note)
        if freq is not None:
            frequencies.append(freq)
        else:
            print(f"跳過無效和弦: {chords[index]}")
            return
    
    # 設置揚聲器
#     print(f"播放和弦: {chords[index]}, 音符數: {num_notes}, 頻率: {frequencies}")  # 診斷日誌
    for i in range(len(speakers)):
        if i < num_notes:
            speakers[i].freq(frequencies[i])
            speakers[i].duty(int(volume * 1023 / num_notes))
        else:
            speakers[i].duty(0)  # 未使用的揚聲器靜音


# # 播放單音或和弦
# def play_chord(speakers, chord, duration, volume=0.5):
#     """
#     播放單音或和弦（最多3音）或休止符
#     參數:
#         speakers: PWM 揚聲器列表
#         chord: 音符字串，如 'E3', 'C#5', 'E3 C#5', 'r'
#         duration: 持續時間 (秒)
#         volume: 音量 (0.0-1.0)
#     """
#     if chord == 'r':  # 休止符
#         for speaker in speakers:
#             mute_speaker(speaker)
#         time.sleep(duration)
#         return
#     
#     notes = chord.split()  # 以空白分割，可能為單音或和弦
#     num_notes = len(notes)
#     
#     if num_notes > 3 or num_notes < 1:
#         print(f"無效音符數量: {chord}，僅支持1-3音")
#         return
#     
#     # 計算每個音的頻率
#     frequencies = []
#     for note in notes:
#         freq = note_to_freq(note)
#         if freq:
#             frequencies.append(freq)
#         else:
#             print(f"無效音符: {note}")
#             return
#     
#     # 設置揚聲器
#     for i in range(3):  # 最多3個音
#         if i < num_notes:
#             speakers[i].freq(frequencies[i])
#             speakers[i].duty(int(volume * 1023 / num_notes))
#         else:
#             speakers[i].duty(0)  # 未使用的揚聲器靜音
#     
#     time.sleep(duration)
#     for speaker in speakers:
#         mute_speaker(speaker)

# 播放旋律
def play_melody(speakers, chords, durations, volume=0.5):
    """
    播放旋律，支持單音、和弦（最多3音）及休止符
    參數:
        speakers: PWM 揚聲器列表
        chords: 音符列表，如 ['E3', 'C#5', 'E3 C#5', 'r']
        durations: 持續時間列表 (秒)，與 chords 等長
        volume: 音量 (0.0-1.0)
    """
    if len(chords) != len(durations):
        raise ValueError("chords 和 durations 長度必須相等")
    
    for chord, duration in zip(chords, durations):
        play_chord(speakers, chord, duration, volume)
        

if __name__ == "__main__":
    speakers = speaker_init(pins=[6, 7, 8])
    try:
        # 測試旋律
        CHORDS = ['C4', 'r', 'D#4', 'E4', 'r', 'F4 D4', 'G4', 'Ab4', 'B4', 'C#5']
        DURATIONS = [0.5, 0.3, 0.5, 1.0, 0.5, 0.5, 0.3, 0.5, 1.0, 0.5]
        index = 0
        chord_start = time.time()
        while True:
            # 每  秒播放一個音符
            if index == 0 or (time.time()-chord_start) >= DURATIONS[index-1]:
                if index >= len(CHORDS):
                    for speaker in speakers:
                        mute_speaker(speaker)
                    print("旋律播放完畢")  # 診斷日誌
                    break
                play_chord(speakers, index, chords=CHORDS, volume=0.3)
                index += 1  # 遞增音符索引，準備播放下一個音符
                chord_start = time.time()  # 更新計時器的起始時間為當前時間
        
        time.sleep(1)
        
        # 和弦旋律
        CHORDS = [
            'C4 E4 G4',   # C 大三和弦
            'B3 D4 G4',   # G/B (G 大三和弦，B 在低音)
            'A3 C4 E4',   # Am 小三和弦
            'G3 C4 E4',   # C/G (C 大三和弦，G 在低音)
            'F3 A3 C4',   # F 大三和弦
            'E3 G3 C4',   # C/E (C 大三和弦，E 在低音)
            'D3 F3 A3',   # Dm 小三和弦
            'G3 B3 D4'    # G 大三和弦
        ]
        DURATIONS = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        index = 0
        chord_start = time.time()
        while True:
            # 每  秒播放一個音符
            if index == 0 or (time.time()-chord_start) >= DURATIONS[index-1]:
                if index >= len(CHORDS):
                    for speaker in speakers:
                        mute_speaker(speaker)
                    print("旋律播放完畢")  # 診斷日誌
                    break
                play_chord(speakers, index, chords=CHORDS, volume=0.3)
                index += 1  # 遞增音符索引，準備播放下一個音符
                chord_start = time.time()  # 更新計時器的起始時間為當前時間
    
    finally:
        speaker_deinit(speakers)  # 釋放資源
