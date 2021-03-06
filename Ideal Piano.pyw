class Button:
    def __init__(self, img, x, y):
        self.img = pyglet.resource.image(img)
        self.img.width /= button_resize_num
        self.img.height /= button_resize_num
        self.x = x
        self.y = y

    def MakeButton(self):
        return pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self):
        range_x, range_y = self.get_range()
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]


screen_width, screen_height = screen_size
show_delay_time = int(show_delay_time * 1000)
pressed = keyboard.is_pressed
pygame.mixer.init(frequency, size, channel, buffer)
pyglet.resource.path = [abs_path]
for each in [
        'background_image', 'piano_image', 'notes_image', 'go_back_image',
        'self_play_image', 'self_midi_image', 'play_midi_image',
        'piano_background_image'
]:
    each_value = eval(each)
    each_path = os.path.dirname(each_value)
    if each_path:
        pyglet.resource.path.append(each_path.replace('/', '\\'))
        exec(f"{each} = '{os.path.basename(each_value)}'")
pyglet.resource.reindex()
icon = pyglet.resource.image('piano.ico')
background = pyglet.resource.image(background_image)
if not background_size:
    ratio_background = screen_width / background.width
    background.width = screen_width
    background.height *= ratio_background
else:
    background.width, background.height = background_size

batch = pyglet.graphics.Batch()
bottom_group = pyglet.graphics.OrderedGroup(0)
piano_bg = pyglet.graphics.OrderedGroup(1)
piano_key = pyglet.graphics.OrderedGroup(2)
play_highlight = pyglet.graphics.OrderedGroup(3)

if not draw_piano_keys:
    bar_offset_x = 9
    image = pyglet.resource.image(piano_image)
    if not piano_size:
        ratio = screen_width / image.width
        image.width = screen_width
        image.height *= ratio
    else:
        image.width, image.height = piano_size
    image_show = pyglet.sprite.Sprite(image,
                                      x=0,
                                      y=0,
                                      batch=batch,
                                      group=piano_bg)
playing = pyglet.resource.image(notes_image)
playing.width /= notes_resize_num
playing.height /= notes_resize_num

if note_mode == 'dots':
    if not draw_piano_keys:
        plays = [
            pyglet.sprite.Sprite(playing,
                                 x=j[0] + dots_offset_x,
                                 y=j[1],
                                 group=play_highlight) for j in note_place
        ]
    else:
        plays = [
            pyglet.sprite.Sprite(playing,
                                 x=j[0] + dots_offset_x,
                                 y=j[1],
                                 group=play_highlight) for j in note_place
        ]
else:
    plays = []

go_back = Button(go_back_image, *go_back_place)
button_go_back = go_back.MakeButton()
self_play = Button(self_play_image, *self_play_place)
button_play = self_play.MakeButton()
self_midi = Button(self_midi_image, *self_midi_place)
button_self_midi = self_midi.MakeButton()
play_midi = Button(play_midi_image, *play_midi_place)
button_play_midi = play_midi.MakeButton()
window = pyglet.window.Window(*screen_size, caption='Ideal Piano')
window.set_icon(icon)

label = pyglet.text.Label('',
                          font_name=fonts,
                          font_size=fonts_size,
                          bold=bold,
                          x=label1_place[0],
                          y=label1_place[1],
                          color=message_color,
                          anchor_x=label_anchor_x,
                          anchor_y=label_anchor_y)
label2 = pyglet.text.Label('',
                           font_name=fonts,
                           font_size=fonts_size,
                           bold=bold,
                           x=label2_place[0],
                           y=label2_place[1],
                           color=message_color,
                           anchor_x=label_anchor_x,
                           anchor_y=label_anchor_y)
label3 = pyglet.text.Label('',
                           font_name=fonts,
                           font_size=fonts_size,
                           bold=bold,
                           x=label3_place[0],
                           y=label3_place[1],
                           color=message_color,
                           anchor_x=label_anchor_x,
                           anchor_y=label_anchor_y)
if show_music_analysis:
    music_analysis_label = pyglet.text.Label(
        '',
        font_name=fonts,
        font_size=music_analysis_fonts_size,
        bold=bold,
        x=music_analysis_place[0],
        y=music_analysis_place[1],
        color=message_color,
        anchor_x=label_anchor_x,
        anchor_y=label_anchor_y,
        multiline=True,
        width=music_analysis_width)


def get_off_sort(a):
    each_chord = a.split('/')
    for i in range(len(each_chord)):
        current = each_chord[i]
        if 'sort as' in current:
            current = current[:current.index('sort as') - 1]
            if current[0] == '[':
                current += ']'
            each_chord[i] = current
    return '/'.join(each_chord)


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
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


mouse_pos = 0, 0
is_click = True
first_time = True
message_label = False
notedic = key_settings
is_click = False
mode_num = None
func = None
click_mode = None
midi_device_load = False
piano_height = white_key_y + white_key_height
piano_keys = []
initial_colors = []
if draw_piano_keys:
    piano_background = pyglet.resource.image(piano_background_image)
    if not piano_size:
        ratio = screen_width / piano_background.width
        piano_background.width = screen_width
        piano_background.height *= ratio
    else:
        piano_background.width, piano_background.height = piano_size
    piano_background_show = pyglet.sprite.Sprite(piano_background,
                                                 x=0,
                                                 y=0,
                                                 batch=batch,
                                                 group=piano_bg)
    for i in range(white_keys_number):
        current_piano_key = shapes.Rectangle(x=white_key_start_x +
                                             white_key_interval * i,
                                             y=white_key_y,
                                             width=white_key_width,
                                             height=white_key_height,
                                             color=white_key_color,
                                             batch=batch,
                                             group=piano_key)
        piano_keys.append(current_piano_key)
        initial_colors.append((current_piano_key.x, white_key_color))
    first_black_key = shapes.Rectangle(x=black_key_first_x,
                                       y=black_key_y,
                                       width=black_key_width,
                                       height=black_key_height,
                                       color=black_key_color,
                                       batch=batch,
                                       group=piano_key)
    piano_keys.append(first_black_key)
    initial_colors.append((first_black_key.x, black_key_color))
    current_start = black_key_start_x
    for j in range(black_keys_set_num):
        for k in black_keys_set:
            current_start += k
            piano_keys.append(
                shapes.Rectangle(x=current_start,
                                 y=black_key_y,
                                 width=black_key_width,
                                 height=black_key_height,
                                 color=black_key_color,
                                 batch=batch,
                                 group=piano_key))
            initial_colors.append((current_start, black_key_color))
        current_start += black_keys_set_interval
    piano_keys.sort(key=lambda s: s.x)
    initial_colors.sort(key=lambda s: s[0])
    initial_colors = [t[1] for t in initial_colors]
    note_place = [(each.x, each.y) for each in piano_keys]
    bar_offset_x = 0


def has_load():
    global midi_device_load
    midi_device_load = True


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos = x, y


@window.event
def on_mouse_press(x, y, button, modifiers):
    global is_click
    global click_mode
    if go_back.inside() & button & mouse.LEFT and not first_time:
        try:
            global playls
            if playls:
                pyglet.clock.unschedule(func)
                del playls
                for each in plays:
                    each.batch = None
        except:
            pass
        if mode_num in [0, 1, 2]:
            pyglet.clock.unschedule(func)
            for each in plays:
                each.batch = None
            if mode_num == 2:
                if play_midi_file:
                    pygame.mixer.music.stop()
                if show_music_analysis:
                    music_analysis_label.text = ''
        is_click = True
        click_mode = None
        if note_mode == 'bars' or note_mode == 'bars drop':
            plays.clear()
            still_hold.clear()
            if note_mode == 'bars drop':
                bars_drop_time.clear()
        if draw_piano_keys:
            for k in range(len(piano_keys)):
                piano_keys[k].color = initial_colors[k]
        label3.text = ''

    if self_play.inside() & button & mouse.LEFT and first_time:
        click_mode = 0
    if self_midi.inside() & button & mouse.LEFT and first_time:
        click_mode = 1
    if play_midi.inside() & button & mouse.LEFT and first_time:
        click_mode = 2


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    if not draw_piano_keys:
        image_show.draw()
    if batch:
        batch.draw()
    button_go_back.draw()
    if first_time:
        global is_click
        global mode_num
        global func
        button_play.draw()
        button_self_midi.draw()
        button_play_midi.draw()
        if mode_num is None:
            if click_mode == 0:
                mode_num = 0
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif click_mode == 1:
                mode_num = 1
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif click_mode == 2:
                mode_num = 2

        else:
            if mode_num == 0:
                init_self_pc()
                label.text = 'sounds loading finished'
                label.draw()
                func = mode_self_pc
                not_first()
                pyglet.clock.schedule_interval(func, 1 / fps)
            elif mode_num == 1:
                try:
                    init_self_midi()
                    if not device:
                        label.text = 'there is no midi input devices, please check'
                        mode_num = 3
                        reset_click_mode()
                        label.draw()
                    else:
                        label.text = 'sounds loading finished'
                        label.draw()
                        func = mode_self_midi
                        not_first()
                        pyglet.clock.schedule_interval(func, 1 / fps)
                except:
                    label.text = 'there is no midi input devices, please check'
                    mode_num = 3
                    reset_click_mode()
                    label.draw()

            elif mode_num == 2:
                init_result = init_show()
                if init_result == 'back':
                    mode_num = 4
                else:
                    func = mode_show
                    not_first()
                    pyglet.clock.schedule_interval(func, 1 / fps)

            elif mode_num == 3:
                time.sleep(1)
                label.text = ''
                mode_num = None
            elif mode_num == 4:
                label.text = ''
                mode_num = None
                reset_click_mode()

    else:

        if is_click:
            is_click = False
            not_first()
            label.text = ''
            label2.text = ''

            pyglet.clock.unschedule(func)
            mode_num = None
        label.draw()
        label2.draw()
        if message_label:
            label3.draw()
        if show_music_analysis:
            music_analysis_label.draw()


currentchord = chord([])
playnotes = []


def reset_click_mode():
    global click_mode
    click_mode = None


def not_first():
    global first_time
    first_time = not first_time


still_hold_pc = []


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
                if note_mode == 'bars' or note_mode == 'bars drop':
                    current_note = toNote(notedic[each])
                    places = note_place[current_note.degree - 21]
                    current_bar = shapes.Rectangle(
                        x=places[0] + bar_offset_x,
                        y=bar_y,
                        width=bar_width,
                        height=bar_height,
                        color=bar_color if color_mode == 'normal' else
                        (random.randint(0, 255), random.randint(0, 255),
                         random.randint(0, 255)),
                        batch=batch,
                        group=play_highlight)
                    current_bar.opacity = bar_opacity
                    still_hold_pc.append([each, current_bar])
                if draw_piano_keys:
                    current_note = toNote(notedic[each])
                    piano_keys[
                        current_note.degree -
                        21].color = bar_color if color_mode == 'normal' else (
                            random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255))
        else:
            if each not in last:
                changed = True
                wavdic[each].play()
                if note_mode == 'bars' or note_mode == 'bars drop':
                    current_note = toNote(notedic[each])
                    places = note_place[current_note.degree - 21]
                    current_bar = shapes.Rectangle(
                        x=places[0] + bar_offset_x,
                        y=bar_y,
                        width=bar_width,
                        height=bar_height,
                        color=bar_color if color_mode == 'normal' else
                        (random.randint(0, 255), random.randint(0, 255),
                         random.randint(0, 255)),
                        batch=batch,
                        group=play_highlight)
                    current_bar.opacity = bar_opacity
                    still_hold_pc.append([each, current_bar])
                if draw_piano_keys:
                    current_note = toNote(notedic[each])
                    piano_keys[
                        current_note.degree -
                        21].color = bar_color if color_mode == 'normal' else (
                            random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255))
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
    if note_mode == 'bars' or note_mode == 'bars drop':
        i = 0
        while i < len(plays):
            each = plays[i]
            each.y += bar_steps
            if each.y >= screen_height:
                each.batch = None
                del plays[i]
                continue
            i += 1
        for k in still_hold_pc:
            current_hold_note, current_bar = k
            if current_hold_note in truecurrent:
                current_bar.height += bar_hold_increase
            else:
                plays.append(current_bar)
                still_hold_pc.remove(k)
    if changed:
        changed = False
        if delay:
            if delay_only_read_current:
                notels = [notedic[t] for t in truecurrent]
            else:
                notels = [notedic[t] for t in stillplay_obj]
        else:
            notels = [notedic[t] for t in last]
        if note_mode == 'dots':
            if lastshow:
                for t in lastshow:
                    plays[t.degree - 21].batch = None
        if draw_piano_keys:
            if lastshow:
                for t in lastshow:
                    piano_keys[t.degree - 21].color = initial_colors[t.degree -
                                                                     21]
        if notels:
            currentchord = chord(notels)
            for k in currentchord:
                if note_mode == 'dots':
                    plays[k.degree - 21].batch = batch
                if draw_piano_keys:
                    piano_keys[
                        k.degree -
                        21].color = bar_color if color_mode == 'normal' else (
                            random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255))

        if notels:
            currentchord.notes.sort(key=lambda x: x.degree)
            if currentchord != lastshow:
                lastshow = currentchord
                label.text = str(currentchord.notes)
                if show_chord:
                    chordtype = detect(
                        currentchord, detect_mode, inv_num, rootpitch,
                        change_from_first, original_first, ignore_add_from,
                        same_note_special, whole_detect, return_fromchord,
                        two_show_interval, poly_chord_first,
                        root_position_return_first, alter_notes_show_degree)

                    label2.text = str(
                        chordtype) if not sort_invisible else get_off_sort(
                            str(chordtype))
        else:
            lastshow = notels
            label.text = str(notels)
            label2.text = ''
        if show_key:
            label.text = str(truecurrent)


still_hold = []


def piano_key_reset(dt, each):
    piano_keys[each.degree - 21].color = initial_colors[each.degree - 21]


def mode_self_midi(dt):
    global last
    global current_play
    global stillplay
    global delay_only_read_current
    current_time = time.time()
    for each in stillplay:
        if each not in current_play:
            if current_time - each.count_time >= delay_time:
                if load_sound:
                    wavdic[str(each)].stop()
                stillplay.remove(each)
                if not delay_only_read_current:
                    if draw_piano_keys:
                        piano_keys[each.degree -
                                   21].color = initial_colors[each.degree - 21]
                    if stillplay:
                        currentchord = chord(stillplay)
                        currentchord.notes.sort(key=lambda x: x.degree)
                        label.text = str(currentchord.notes)
                        if show_chord:
                            chordtype = detect(
                                currentchord, detect_mode, inv_num, rootpitch,
                                change_from_first, original_first,
                                ignore_add_from, same_note_special,
                                whole_detect, return_fromchord,
                                two_show_interval, poly_chord_first,
                                root_position_return_first,
                                alter_notes_show_degree)
                            label2.text = str(
                                chordtype
                            ) if not sort_invisible else get_off_sort(
                                str(chordtype))
                    else:
                        label.text = '[]'
                        label2.text = ''

        else:
            each.count_time = current_time
    if last != current_play:
        if note_mode == 'dots':
            for k in last:
                plays[k.degree - 21].batch = None
        last = current_play.copy()
        if current_play:
            for each in current_play:
                if note_mode == 'dots':
                    plays[each.degree - 21].batch = batch

            currentchord = chord(
                current_play) if delay_only_read_current else chord(stillplay)
            currentchord.notes.sort(key=lambda x: x.degree)
            label.text = str(currentchord.notes)
            if show_chord:
                chordtype = detect(
                    currentchord, detect_mode, inv_num, rootpitch,
                    change_from_first, original_first, ignore_add_from,
                    same_note_special, whole_detect, return_fromchord,
                    two_show_interval, poly_chord_first,
                    root_position_return_first, alter_notes_show_degree)

                label2.text = str(
                    chordtype) if not sort_invisible else get_off_sort(
                        str(chordtype))
        else:
            if delay_only_read_current:
                label.text = '[]'
                label2.text = ''

    if device.poll():
        event = device.read(1)[0]
        data, timestamp = event
        status, note_number, velocity, note_off_velocity = data
        current_note = degree_to_note(note_number)
        if status == 128 or (status == 144 and velocity == 0):
            # 128 is the status code of note off in midi
            if note_mode == 'dots':
                plays[note_number - 21].batch = None
            if draw_piano_keys and delay_only_read_current:
                piano_keys[note_number -
                           21].color = initial_colors[note_number - 21]
            if current_note in current_play:
                current_play.remove(current_note)
        elif status == 144:
            # 144 is the status code of note on in midi
            if note_mode == 'bars' or note_mode == 'bars drop':
                places = note_place[current_note.degree - 21]
                current_bar = shapes.Rectangle(
                    x=places[0] + bar_offset_x,
                    y=bar_y,
                    width=bar_width,
                    height=bar_height,
                    color=bar_color if color_mode == 'normal' else
                    (random.randint(0, 255), random.randint(0, 255),
                     random.randint(0, 255)),
                    batch=batch,
                    group=play_highlight)
                current_bar.opacity = 255 * (
                    velocity /
                    127) if opacity_change_by_velocity else bar_opacity
                still_hold.append([current_note, current_bar])
            if draw_piano_keys:
                piano_keys[
                    current_note.degree -
                    21].color = bar_color if color_mode == 'normal' else (
                        random.randint(0, 255), random.randint(0, 255),
                        random.randint(0, 255))
            if current_note not in current_play:
                current_play.append(current_note)
                if current_note not in stillplay:
                    stillplay.append(current_note)
                current_note.count_time = current_time
                if load_sound:
                    current_sound = wavdic[str(current_note)]
                    current_sound.set_volume(velocity / 127)
                    current_sound.play()
        elif status == 176 and note_number == 64:
            if velocity >= 64:
                if delay_only_read_current:
                    if draw_piano_keys:
                        for each in stillplay:
                            piano_keys[each.degree -
                                       21].color = initial_colors[each.degree -
                                                                  21]
                delay_only_read_current = False
            else:
                if not delay_only_read_current:
                    if draw_piano_keys:
                        for each in stillplay:
                            pyglet.clock.schedule_once(
                                piano_key_reset,
                                delay_time - (current_time - each.count_time),
                                each)
                delay_only_read_current = True

    if note_mode == 'bars' or note_mode == 'bars drop':
        i = 0
        while i < len(plays):
            each = plays[i]
            each.y += bar_steps
            if each.y >= screen_height:
                each.batch = None
                del plays[i]
                continue
            i += 1
        for k in still_hold:
            current_hold_note, current_bar = k
            if current_hold_note in current_play:
                current_bar.height += bar_hold_increase
            else:
                plays.append(current_bar)
                still_hold.remove(k)


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
    global show_music_analysis_list
    if not paused:
        currentime = time.time() - startplay
        if note_mode == 'bars drop':
            if bars_drop_time:
                j = 0
                while j < len(bars_drop_time):
                    next_bar_drop = bars_drop_time[j]
                    if currentime >= next_bar_drop[0]:
                        current_note = next_bar_drop[1]
                        places = note_place[current_note.degree - 21]
                        current_bar = shapes.Rectangle(
                            x=places[0] + bar_offset_x,
                            y=screen_height,
                            width=bar_width,
                            height=bar_unit * current_note.duration,
                            color=bar_color if color_mode == 'normal' else
                            (random.randint(0, 255), random.randint(0, 255),
                             random.randint(0, 255)),
                            batch=batch,
                            group=bottom_group)
                        current_bar.opacity = 255 * (
                            current_note.volume /
                            127) if opacity_change_by_velocity else bar_opacity
                        current_bar.num = current_note.degree - 21
                        current_bar.hit_key = False
                        plays.append(current_bar)
                        del bars_drop_time[j]
                        continue
                    j += 1
        for k in range(sheetlen):
            nownote = playls[k]
            current_sound, start_time, stop_time, situation, number, current_note = nownote
            if situation != 2:
                if situation == 0:
                    if currentime >= start_time:
                        if not play_midi_file:
                            current_sound.play()
                        nownote[3] = 1
                        if show_music_analysis:
                            if show_music_analysis_list:
                                current_music_analysis = show_music_analysis_list[
                                    0]
                                if k == current_music_analysis[0]:
                                    music_analysis_label.text = current_music_analysis[
                                        1]
                                    del show_music_analysis_list[0]
                        if note_mode == 'bars':
                            places = note_place[current_note.degree - 21]
                            current_bar = shapes.Rectangle(
                                x=places[0] + bar_offset_x,
                                y=bar_y,
                                width=bar_width,
                                height=bar_unit * current_note.duration,
                                color=bar_color if color_mode == 'normal' else
                                (random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)),
                                batch=batch,
                                group=play_highlight)
                            current_bar.opacity = 255 * (
                                current_note.volume / 127
                            ) if opacity_change_by_velocity else bar_opacity
                            plays.append(current_bar)
                elif situation == 1:
                    if currentime >= stop_time:
                        if not play_midi_file:
                            current_sound.fadeout(show_delay_time)
                        nownote[3] = 2
                        if k == sheetlen - 1:
                            finished = True

        playnotes = [wholenotes[x[4]] for x in playls if x[3] == 1]
        if playnotes:
            playnotes.sort(key=lambda x: x.degree)
            if playnotes != lastshow:
                if note_mode == 'dots':
                    if lastshow:
                        for each in lastshow:
                            plays[each.degree - 21].batch = None
                    for i in playnotes:
                        plays[i.degree - 21].batch = batch
                elif draw_piano_keys and note_mode != 'bars drop':
                    if lastshow:
                        for each in lastshow:
                            piano_keys[each.degree -
                                       21].color = initial_colors[each.degree -
                                                                  21]
                    for i in playnotes:
                        piano_keys[
                            i.degree -
                            21].color = bar_color if color_mode == 'normal' else (
                                random.randint(0, 255), random.randint(0, 255),
                                random.randint(0, 255))

                lastshow = playnotes
                label.text = str(playnotes)
                if show_chord:
                    chordtype = detect(
                        playnotes, detect_mode, inv_num, rootpitch,
                        change_from_first, original_first, ignore_add_from,
                        same_note_special, whole_detect, return_fromchord,
                        two_show_interval, poly_chord_first,
                        root_position_return_first, alter_notes_show_degree)
                    label2.text = str(
                        chordtype) if not sort_invisible else get_off_sort(
                            str(chordtype))

        if keyboard.is_pressed(pause_key):
            paused = True
            pause_start = time.time()
            message_label = True
            label3.text = f'paused, press {unpause_key} to unpause'
        if note_mode == 'bars':
            i = 0
            while i < len(plays):
                each = plays[i]
                each.y += bar_steps
                if each.y >= screen_height:
                    each.batch = None
                    del plays[i]
                    continue
                i += 1
        elif note_mode == 'bars drop':
            i = 0
            while i < len(plays):
                each = plays[i]
                each.y -= bar_steps
                if not each.hit_key and each.y <= bars_drop_place:
                    each.hit_key = True
                    if draw_piano_keys:
                        piano_keys[each.num].color = each.color
                if each.height + each.y <= piano_height:
                    each.batch = None
                    if draw_piano_keys:
                        piano_keys[each.num].color = initial_colors[each.num]
                    del plays[i]
                    continue
                i += 1

    else:
        if keyboard.is_pressed(unpause_key):
            paused = False
            message_label = False
            pause_stop = time.time()
            pause_time = pause_stop - pause_start
            startplay += pause_time
    if finished:
        label2.text = ''
        for each in plays:
            each.batch = None
        if show_music_analysis:
            music_analysis_label.text = ''
            show_music_analysis_list = copy(default_show_music_analysis_list)
        label.text = f'music playing finished, press {repeat_key} to listen again, or press {exit_key} to exit'
        if keyboard.is_pressed(repeat_key):
            label.text = 'reloading, please wait...'
            if note_mode == 'bars' or note_mode == 'bars drop':
                plays.clear()
                if note_mode == 'bars drop':
                    bars_drop_time.clear()
            if draw_piano_keys:
                for k in range(len(piano_keys)):
                    piano_keys[k].color = initial_colors[k]
            del playls
            playls = initialize(musicsheet, unit_time, musicsheet.start_time)
            startplay = time.time()
            lastshow = None
            playnotes.clear()
            finished = False
        if keyboard.is_pressed(exit_key):
            sys.exit(0)


if note_mode == 'bars drop':
    bars_drop_time = []
    distances = screen_height - piano_height
    bar_steps = (distances / bars_drop_interval) / adjust_ratio
else:
    bars_drop_interval = 0


def midi_file_play(dt):
    pygame.mixer.music.play()


def initialize(musicsheet, unit_time, start_time):
    global play_midi_file
    play_midi_file = False
    playls = []
    start = start_time * unit_time + bars_drop_interval
    if play_as_midi:
        play_midi_file = True
        if not if_merge:
            import musicpy.musicpy
            musicpy.musicpy.write('temp.mid',
                                  musicsheet,
                                  60 / (unit_time / 4),
                                  time1=musicsheet.start_time)
            pygame.mixer.music.load('temp.mid')
            os.remove('temp.mid')
            os.chdir(abs_path)
        else:
            pygame.mixer.music.load(path)
        pyglet.clock.schedule_once(midi_file_play, bars_drop_interval)
        for i in range(sheetlen):
            currentnote = musicsheet.notes[i]
            duration = unit_time * currentnote.duration
            interval = unit_time * musicsheet.interval[i]
            currentstart = start
            currentstop = start + duration
            playls.append([0, currentstart, currentstop, 0, i, currentnote])
            if note_mode == 'bars drop':
                bars_drop_time.append(
                    (currentstart - bars_drop_interval, currentnote))
            start += interval
    else:
        try:
            for i in range(sheetlen):
                currentnote = musicsheet.notes[i]
                currentwav = pygame.mixer.Sound(
                    f'{sound_path}/{currentnote}.{sound_format}')
                duration = unit_time * currentnote.duration
                interval = unit_time * musicsheet.interval[i]
                currentstart = start
                currentstop = start + duration
                note_volume = currentnote.volume / 127
                note_volume *= global_volume
                currentwav.set_volume(note_volume)
                playls.append(
                    [currentwav, currentstart, currentstop, 0, i, currentnote])
                if note_mode == 'bars drop':
                    bars_drop_time.append(
                        (currentstart - bars_drop_interval, currentnote))
                start += interval
        except:
            pygame.mixer.music.load(path)
            play_midi_file = True
            playls.clear()
            if note_mode == 'bars drop':
                bars_drop_time.clear()
            start = start_time * unit_time + bars_drop_interval
            for i in range(sheetlen):
                currentnote = musicsheet.notes[i]
                duration = unit_time * currentnote.duration
                interval = unit_time * musicsheet.interval[i]
                currentstart = start
                currentstop = start + duration
                playls.append(
                    [0, currentstart, currentstop, 0, i, currentnote])
                if note_mode == 'bars drop':
                    bars_drop_time.append(
                        (currentstart - bars_drop_interval, currentnote))
                start += interval
            pyglet.clock.schedule_once(midi_file_play, bars_drop_interval)
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
    global stillplay
    global current_play
    global wavdic
    global device
    global last
    if not midi_device_load:
        device = None
        has_load()
        pygame.mixer.set_num_channels(maxinum_channels)
        pygame.midi.init()
        device = pygame.midi.Input(midi_device_id)
    else:
        if device:
            device.close()
            device = pygame.midi.Input(midi_device_id)
    notenames = os.listdir(sound_path)
    notenames = [x[:x.index('.')] for x in notenames]
    if load_sound:
        wavdic = load({i: i
                       for i in notenames}, sound_path, sound_format,
                      global_volume)
    current_play = []
    stillplay = []
    last = current_play.copy()


def browse_reset():
    global file_path
    global track_ind_get
    global read_result
    global set_bpm
    global off_melody
    global appears
    file_path, track_ind_get, read_result, set_bpm, off_melody, appears = None, None, None, None, 0, False


melody_notes = []

if show_music_analysis:
    with open(music_analysis_file, encoding='utf-8-sig') as f:
        data = f.read()
        lines = [i for i in data.split('\n') if i]
        keys_list = [i for i in lines if i[:3] == 'key']
        keys = [j.split('key: ')[1] for j in keys_list]
        keys_list_ind = [i for i in range(len(lines)) if lines[i][:3] == 'key']
        music_analysis_list = [i.split(' ') for i in lines]
        if keys_list_ind:
            keys_num = len(keys_list_ind)
            for i in range(keys_num):
                current_key_ind = keys_list_ind[i]
                current_key = keys[i]
                if i != keys_num - 1:
                    next_key_ind = keys_list_ind[i + 1]
                else:
                    next_key_ind = len(music_analysis_list)
                for j in range(current_key_ind + 1, next_key_ind):
                    music_analysis_list[j][
                        1] = f'{key_header}{current_key}\n' + music_analysis_list[
                            j][1]
        music_analysis_list = [[k[0], ' '.join(k[1:])]
                               for k in music_analysis_list]
        music_analysis_list = [[float(j[0]) - 1, j[1]]
                               for j in music_analysis_list
                               if len(j) == 2 and j[0] != 'key:']


def init_show():
    global playls
    global startplay
    global lastshow
    global finished
    global sheetlen
    global wholenotes
    global musicsheet
    global unit_time
    global get_off_melody
    global melody_notes
    global action
    global path
    setup()
    path = file_path
    if action == 1:
        action = 0
        browse_reset()
        return 'back'
    if path and read_result:
        global interval
        play_interval = interval
        if read_result != 'error':
            bpm2, musicsheet, start_time = read_result
            if set_bpm:
                bpm2 = float(set_bpm)

        else:
            browse_reset()
            return 'back'

        if bpm is None:
            bpm_to_use = bpm2
        else:
            bpm_to_use = bpm
    else:
        browse_reset()
        return 'back'

    get_off_melody = off_melody
    if get_off_melody:
        musicsheet = split_chord(musicsheet, 'hold', melody_tol, chord_tol,
                                 get_off_overlap_notes, average_degree_length,
                                 melody_degree_tol)
        sheetlen = len(musicsheet)

    browse_reset()
    if play_interval is not None:
        interval = None

        play_start, play_stop = int(sheetlen * (play_interval[0] / 100)), int(
            sheetlen * (play_interval[1] / 100))
        if play_start == 0:
            play_start = 1
        musicsheet = musicsheet[play_start:play_stop + 1]
        sheetlen = play_stop + 1 - play_start
    if show_change_pitch != None:
        musicsheet = musicsheet.up(show_change_pitch)
    if show_modulation != None:
        musicsheet = modulation(musicsheet, eval(show_modulation[0]),
                                eval(show_modulation[1]))

    if sheetlen == 0:
        return 'back'
    pygame.mixer.set_num_channels(sheetlen)
    wholenotes = musicsheet.notes
    unit_time = 4 * 60 / bpm_to_use

    # every object in playls has a situation flag at the index of 3,
    # 0 means has not been played yet, 1 means it has started playing,
    # 2 means it has stopped playing
    musicsheet.start_time = start_time
    playls = initialize(musicsheet, unit_time, start_time)
    if show_music_analysis:
        global show_music_analysis_list
        show_music_analysis_list = [[
            add_to_last_index(musicsheet.interval, each[0]), each[1]
        ] for each in music_analysis_list]
        global default_show_music_analysis_list
        default_show_music_analysis_list = copy(show_music_analysis_list)
    startplay = time.time()
    lastshow = None
    finished = False
    func = mode_show


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / fps)
pyglet.app.run()
