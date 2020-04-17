import pygame, keyboard, os, time, sys, pyglet
from config import *
from musicpy.musicpy import *
import pygame.midi
pressed = keyboard.is_pressed
pygame.mixer.init(frequency, size, channel, buffer)
pyglet.resource.path = ['']
pyglet.resource.reindex()
image = pyglet.resource.image('piano1.png')
playing = pyglet.resource.image('playing.png')
playing.width /= 1.2
playing.height /= 1.2
plays = [pyglet.sprite.Sprite(playing, x=j[0], y=j[1]) for j in note_place]
window = pyglet.window.Window(int(image.width), int(image.height) - 150)
label = pyglet.text.Label('',
                          font_name='Comic Sans MS',
                          font_size=20,
                          x=650,
                          y=400,
                          color=(0, 0, 0, 255),
                          anchor_x='center',
                          anchor_y='center')
label2 = pyglet.text.Label('',
                           font_name='Comic Sans MS',
                           font_size=20,
                           x=650,
                           y=350,
                           color=(0, 0, 0, 255),
                           anchor_x='center',
                           anchor_y='center')
label3 = pyglet.text.Label('',
                           font_name='Comic Sans MS',
                           font_size=20,
                           x=650,
                           y=450,
                           color=(0, 0, 0, 255),
                           anchor_x='center',
                           anchor_y='center')
label_mode1 = pyglet.text.Label(
    'press Z to self playing on computer keyboard, X to self playing on a midi keyboard, C to play a midi file',
    font_name='Comic Sans MS',
    font_size=15,
    x=650,
    y=250,
    color=(0, 0, 0, 255),
    anchor_x='center',
    anchor_y='center')


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def configkey(q):
    return pressed(f'{config_key} + {q}')


def configshow(content):
    label.text = str(content)


def switchs(q, name):
    if configkey(q):
        globals()[name] = not globals()[name]
        configshow(f'{name} changes to {globals()[name]}')


first_time = True
message_label = False
notedic = key_settings

mode_num = None


@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)
    if first_time:

        global mode_num
        label_mode1.draw()
        if mode_num is None:
            if keyboard.is_pressed('Z'):
                mode_num = 0
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif keyboard.is_pressed('X'):
                mode_num = 1
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif keyboard.is_pressed('C'):
                mode_num = 2
                label.text = 'loading midi notes...please wait'
                label.draw()

        else:
            if mode_num == 0:
                init_self_pc()
                label.text = 'sounds loading finished'
                func = mode_self_pc
            elif mode_num == 1:
                init_self_midi()
                label.text = 'sounds loading finished'
                func = mode_self_midi
            elif mode_num == 2:
                init_show()
                func = mode_show
            not_first()
            pyglet.clock.schedule_interval(func, 1 / 120)
    else:
        label.draw()
        label2.draw()
        if message_label:
            label3.draw()
        if mode_num == 0:
            if label2.text != '':
                for i in currentchord.notes:
                    plays[i.degree - 21].draw()
        elif mode_num == 1:
            for i in current_play:
                plays[i.degree - 21].draw()
        else:
            for i in playnotes:
                plays[i.degree - 21].draw()


currentchord = chord([])
playnotes = []


def not_first():
    global first_time
    first_time = False


def mode_self_pc(dt):
    global stillplay
    global last
    global changed
    global lastshow
    global currentchord
    global global_volume
    if config_enable:
        if configkey(volume_up):
            global_volume += volume_change_unit
            [wavdic[j].set_volume(global_volume) for j in wavdic]
            configshow(f'volume up to {int(global_volume*100)}%')
        if configkey(volume_down):
            global_volume -= volume_change_unit
            [wavdic[j].set_volume(global_volume) for j in wavdic]
            configshow(f'volume down to {int(global_volume*100)}%')
        switchs(change_delay, 'delay')
        switchs(change_read_current, 'delay_only_read_current')
        switchs(change_pause_key_clear_notes, 'pause_key_clear_notes')
    if keyboard.is_pressed(pause_key):
        [wavdic[x].stop() for x in last]
        if pause_key_clear_notes:
            if delay:
                stillplay = []
    current = keyboard.get_hotkey_name().split('+')
    current = [i for i in current if i in wavdic]
    if delay:
        stillplay_obj = [x[0] for x in stillplay]
        if delay_only_read_current or show_key:
            truecurrent = current.copy()
    for each in current:
        if delay:
            if each in stillplay_obj:
                inds = stillplay_obj.index(each)
                if not stillplay[inds][2] and time.time(
                ) - stillplay[inds][1] > touch_interval:
                    wavdic[each].stop()
                    stillplay.pop(inds)
                    stillplay_obj.pop(inds)
            else:
                changed = True
                wavdic[each].play()
                stillplay.append([each, time.time(), True])
                stillplay_obj.append(each)
        else:
            if each not in last:
                changed = True
                wavdic[each].play()
    for j in last:
        if j not in current:

            if delay:
                if j in stillplay_obj:
                    ind = stillplay_obj.index(j)
                    stillobj = stillplay[ind]
                    if time.time() - stillobj[1] > delay_time:
                        changed = True
                        wavdic[j].stop()
                        stillplay.pop(ind)
                        stillplay_obj.pop(ind)
                    else:
                        stillplay[ind][2] = False
                        current.append(j)
                else:
                    changed = True
                    wavdic[j].stop()
            else:
                changed = True
                wavdic[j].stop()
    last = current
    if changed:
        changed = False

        if delay:
            if delay_only_read_current:
                notels = [notedic[t] for t in truecurrent]
            else:
                notels = [notedic[t] for t in stillplay_obj]
        else:
            notels = [notedic[t] for t in last]
        if show_chord:
            if len(notels) != 0:
                currentchord = chord(notels)
                currentchord.notes.sort(key=lambda x: x.degree)
                if currentchord != lastshow:
                    lastshow = currentchord
                    label.text = str(currentchord.notes)
                    chordtype = detect(currentchord,
                                       ignore_sort_from=ignore_sort_from,
                                       change_from_first=change_from_first,
                                       original_first=original_first,
                                       ignore_add_from=ignore_add_from,
                                       same_note_special=same_note_special,
                                       two_show_interval=two_show_interval)
                    if 'cannot' in chordtype:
                        label.text = f'note {", ".join([str(x) for x in currentchord])}'
                    else:
                        label2.text = str(chordtype)
            else:
                lastshow = notels
                label.text = str(notels)
                label2.text = ''
        else:
            lastshow = notels
            label.text = str(notels)
        if show_key:
            label.text = str(truecurrent)


def mode_self_midi(dt):
    global last
    global current_play
    if last != current_play:
        last = current_play.copy()
        if current_play:
            currentchord = chord(current_play)
            currentchord.notes.sort(key=lambda x: x.degree)
            label.text = str(currentchord.notes)
            chordtype = detect(currentchord,
                               ignore_sort_from=ignore_sort_from,
                               change_from_first=change_from_first,
                               original_first=original_first,
                               ignore_add_from=ignore_add_from,
                               same_note_special=same_note_special,
                               two_show_interval=two_show_interval)
            if 'cannot' in chordtype:
                label2.text = f'note {", ".join([str(x) for x in currentchord])}'
            else:
                label2.text = str(chordtype)
        else:
            label.text = '[]'
            label2.text = ''

    if device.poll():
        event = device.read(1)[0]
        data = event[0]
        timestamp = event[1]
        note_number = data[1]
        velocity = data[2]
        current_note = degree_to_note(note_number)
        if velocity == 0:
            if current_note in current_play:
                current_play.remove(current_note)
                #wavdic[str(current_note)].stop()
        else:
            if current_note not in current_play:
                current_play.append(current_note)
                current_sound = wavdic[str(current_note)]
                current_sound.set_volume(velocity / 127)
                current_sound.play(maxtime=delay_time)


paused = False
pause_start = 0


def mode_show(dt):
    global startplay
    global lastshow
    global finished
    global playls
    global paused
    global pause_start
    global message_label
    global playnotes
    if not paused:
        currentime = time.time() - startplay
        for k in range(sheetlen):

            nownote = playls[k]
            situation = nownote[3]
            if situation != 2:
                if situation == 0:
                    if currentime >= nownote[1]:
                        nownote[0].play()
                        playls[k][3] = 1
                elif situation == 1:
                    if currentime >= nownote[2]:
                        nownote[0].fadeout(show_delay_time)
                        playls[k][3] = 2
                        if k == sheetlen - 1:
                            finished = True
        time.sleep(delay_each_loop)
        if show_chord:
            playnotes = [wholenotes[x[4]] for x in playls if x[3] == 1]
            if len(playnotes) != 0:
                playnotes.sort(key=lambda x: x.degree)
                if playnotes != lastshow:
                    lastshow = playnotes
                    label.text = str(playnotes)
                    chordtype = detect(playnotes,
                                       ignore_sort_from=ignore_sort_from,
                                       change_from_first=change_from_first,
                                       original_first=original_first,
                                       ignore_add_from=ignore_add_from,
                                       same_note_special=same_note_special,
                                       two_show_interval=two_show_interval)
                    if 'cannot' not in chordtype:
                        label2.text = str(chordtype)
        if keyboard.is_pressed(pause_key):
            paused = True
            pause_start = time.time()
            message_label = True
            label3.text = f'paused, press {unpause_key} to unpause'
    else:
        if keyboard.is_pressed(unpause_key):
            paused = False
            message_label = False
            pause_stop = time.time()
            pause_time = pause_stop - pause_start
            startplay += pause_time
    if finished:
        if show_chord:
            label2.text = ''
        label.text = str(
            f'music playing finished, press {repeat_key} to listen again, or press {exit_key} to exit'
        )
        if keyboard.is_pressed(repeat_key):
            label.text = str('loading...please wait')
            playls = initialize()
            startplay = time.time()
            lastshow = None
            finished = False
        if keyboard.is_pressed(exit_key):
            sys.exit(0)


def initialize(musicsheet, unit_time):
    playls = []
    start = 0
    for i in range(sheetlen):
        currentnote = musicsheet.notes[i]
        currentwav = pygame.mixer.Sound(
            f'{sound_path}{currentnote}.{sound_format}')
        duration = unit_time * currentnote.duration
        interval = unit_time * musicsheet.interval[i]
        currentstart = start
        currentstop = start + duration
        note_volume = currentnote.volume / 127
        note_volume *= global_volume
        currentwav.set_volume(note_volume)
        playls.append([currentwav, currentstart, currentstop, 0, i])
        start += interval
    return playls


def init_self_pc():
    global wavdic
    global last
    global changed
    if delay:
        global stillplay
    global lastshow
    pygame.mixer.set_num_channels(maxinum_channels)
    wavdic = load(notedic, sound_path, sound_format, global_volume)
    last = []
    changed = False
    if delay:
        stillplay = []
    lastshow = None


def init_self_midi():
    global current_play
    global delay_time
    global wavdic
    global device
    global last
    pygame.mixer.set_num_channels(maxinum_channels)
    notenames = os.listdir(sound_path)
    notenames = [x[:x.index('.')] for x in notenames]
    wavdic = load({i: i
                   for i in notenames}, sound_path, sound_format,
                  global_volume)

    pygame.midi.init()
    device = pygame.midi.Input(midi_device_id)
    current_play = []
    last = current_play.copy()
    delay_time = int(delay_time * 1000)
    func = mode_self_midi


def init_show():
    global playls
    global startplay
    global lastshow
    global finished
    global show_delay_time
    global sheetlen
    global wholenotes
    if path is not None:
        if '.mid' in path:
            path2 = path.replace('.mid', '')
        bpm2, musicsheet = read(path2, track_ind, track)
        if bpm is None:
            bpm_to_use = bpm2
        else:
            bpm_to_use = bpm
    else:
        musicsheet = eval(musicsheet)
    sheetlen = len(musicsheet)
    if play_interval is not None:
        play_start, play_stop = int(sheetlen *
                                    (play_interval[0] / 100)) + 1, int(
                                        sheetlen * (play_interval[1] / 100))
        musicsheet = musicsheet[play_start:play_stop]
        sheetlen = len(musicsheet)
    if show_change_pitch != None:
        musicsheet = musicsheet.up(show_change_pitch)
    if show_modulation != None:
        musicsheet = modulation(musicsheet, eval(show_modulation[0]),
                                eval(show_modulation[1]))

    if sheetlen == 0:
        label.text = 'this track has no music notes'
    pygame.mixer.set_num_channels(sheetlen)
    wholenotes = musicsheet.notes
    unit_time = 60 / bpm_to_use
    show_delay_time = int(show_delay_time * 1000)

    # every object in playls has a situation flag at the index of 3,
    # 0 means has not been played yet, 1 means it has started playing,
    # 2 means it has stopped playing
    playls = initialize(musicsheet, unit_time)
    startplay = time.time()
    lastshow = None
    finished = False
    func = mode_show


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()