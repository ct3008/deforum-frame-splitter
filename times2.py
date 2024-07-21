def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from {valid_options}.")

def get_motion_and_speed(time, motion_type):
    motion_options_2d = ["zoom_in", "zoom_out", "pan_right", "pan_left", "pan_up", "pan_down", "spin_cw", "spin_ccw", "none"]
    motion_options_3d = ["zoom_in", "zoom_out", "rotate_up", "rotate_down", "rotate_right", "rotate_left", "rotate_cw", "rotate_ccw", "none"]
    speed_options = ["vslow", "slow", "normal", "fast", "vfast"]
    strength_options = ["weak", "normal", "strong", "vstrong"]

    if motion_type == "2d":
        motion_options = motion_options_2d
    else:
        motion_options = motion_options_3d

    motions = []
    speed = get_valid_input(f"Enter the speed level for this range {time} (vslow, slow, normal, fast, vfast):\n", speed_options)
    while True:
        motion = get_valid_input(f"Enter a motion for range {time} ({', '.join(motion_options)}):\n", motion_options)
        strength = get_valid_input(f"Enter the strength of the motion {motion} in range {time} (weak, normal, strong, vstrong):\n", strength_options)
        motions.append((motion, speed, strength))
        more = get_valid_input("Do you want to add another motion for this time range? (yes/no):\n", ["yes", "no"])
        if more == "no":
            break
    return motions

def calculate_frames(scene_change_times, time_intervals, motion_data):
    frame_data = {
        "zoom": [],
        "translation_x": [],
        "translation_y": [],
        "angle": [],
        "rotation_3d_x": [],
        "rotation_3d_y": [],
        "rotation_3d_z": []
    }
    tmp_times = scene_change_times.copy()

    speed_multiplier = {"vslow": 0.25, "slow": 0.5, "normal": 1, "fast": 2.5, "vfast": 6}
    frame_rate = 15

    current_frame = 0
    animation_prompts = []
    

    for interval, motions in zip(time_intervals, motion_data):
        _, speed, _ = motions[0]
        start_time, end_time = map(int, interval.split('-'))
        if tmp_times:
            print(int(tmp_times[0]))
        if tmp_times != [] and int(tmp_times[0]) <= end_time and int(tmp_times[0]) >= start_time:
            new_frame = round(current_frame + (int(tmp_times[0]) - start_time) * 15 * speed_multiplier[speed])
            print("----------------END FRAME:---------------", new_frame)
            if new_frame not in final_anim_frames:
				
                final_anim_frames.append(new_frame)
            tmp_times.pop(0)
        duration = (end_time - start_time) * frame_rate
        adjusted_duration = round(duration * speed_multiplier[speed])
        end_frame = current_frame + adjusted_duration
        for motion, speed, strength in motions:
            animation_prompts.append((start_time, end_time, current_frame, end_frame))
            
            if motion == "zoom_in":
                frame_data["zoom"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "zoom_out":
                frame_data["zoom"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "pan_right":
                frame_data["translation_x"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "pan_left":
                frame_data["translation_x"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "pan_up":
                frame_data["translation_y"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "pan_down":
                frame_data["translation_y"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "spin_cw":
                frame_data["angle"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "spin_ccw":
                frame_data["angle"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_up":
                frame_data["rotation_3d_x"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_down":
                frame_data["rotation_3d_x"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_right":
                frame_data["rotation_3d_y"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_left":
                frame_data["rotation_3d_y"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_cw":
                frame_data["rotation_3d_z"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))
            elif motion == "rotate_ccw":
                frame_data["rotation_3d_z"].append((current_frame, end_frame, adjusted_duration, motion_magnitudes[motion][strength]))


        current_frame = end_frame

        if str(end_time) == str(total_song_len) and end_frame not in final_anim_frames and (end_frame - 1) not in final_anim_frames:
            final_anim_frames.append(end_frame)
        

    return frame_data, animation_prompts

def build_transition_strings(frame_data):
    #defaults = none
    motion_defaults = {
        "zoom": 1.0,
        "translation_x": 0,
        "translation_y": 0,
        "angle": 0,
        "rotation_3d_x": 0,
        "rotation_3d_y": 0,
        "rotation_3d_z": 0
    }
    

    motion_strings = {motion: [] for motion in frame_data}

    for motion, frames in frame_data.items():
        previous_end_frame = None
        for (start_frame, end_frame, duration, value) in frames:
            
            pre_frame = start_frame - 1
            post_frame = end_frame + 1
            print("pre frame: ", pre_frame)
            print("post frame: ", post_frame)

            if previous_end_frame is not None and previous_end_frame == start_frame:
                start_frame = start_frame + 2
                # if motion_strings[motion][-1].startswith(f"{start_frame + 1}:"):
                #     motion_strings[motion].pop()
                #     if motion_strings[motion][-1].startswith(f"{start_frame}:"):
                #         motion_strings[motion].pop()
            else:
                if pre_frame >= 0:
                    motion_strings[motion].append(f"{pre_frame}:({motion_defaults[motion]})")
                    
            motion_strings[motion].append(f"{start_frame}:({value})")
            motion_strings[motion].append(f"{end_frame}:({value})")
            
            if post_frame >= 0:
                motion_strings[motion].append(f"{post_frame}:({motion_defaults[motion]})")
                
            previous_end_frame = end_frame
            
		
    for motion in motion_strings:
        if not any(s.startswith('0:') for s in motion_strings[motion]):
            motion_strings[motion].insert(0, f"0:({motion_defaults[motion]})")


    return motion_strings

# Main program
motion_magnitudes = {
	"zoom_in": {"none": 1.00, "weak": 1.02, "normal": 1.04, "strong": 3, "vstrong": 6},
	"zoom_out": {"none": 1.00, "weak": 0.98, "normal": 0.96, "strong": 0.4, "vstrong": 0.1},
	"rotate_up": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"rotate_down": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6},
	"rotate_right": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"rotate_left": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6},
	"rotate_cw": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"rotate_ccw": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6},
    "pan_up": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"pan_down": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6},
	"pan_right": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"pan_left": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6},
	"spin_cw": {"none": 0, "weak": 0.5, "normal": 1, "strong": 3, "vstrong": 6},
	"spin_ccw": {"none": 0, "weak": -0.5, "normal": -1, "strong": -3, "vstrong": -6}
}
motion_type = get_valid_input("Do you want 2D or 3D motion? (2d/3d):\n", ["2d", "3d"])
total_song_len = int(input("How long is the song (in seconds)?\n"))
scene_change_times = input("Enter the times (in seconds) for scene changes, separated by spaces:\n").split()
if str(total_song_len) not in scene_change_times:
    scene_change_times.append(str(total_song_len))
final_anim_frames = []
final_anim_frames.append(0)

time_intervals = input("Enter the times (in seconds) when transitions or new motions should take place, separated by spaces:\n").split()
time_intervals = [f"{0}-{time_intervals[0]}"] + [f"{start}-{end}" for start, end in zip(time_intervals[:-1], time_intervals[1:])]

# Add final interval from the last specified time to the end of the song
if time_intervals:
    last_time = time_intervals[-1].split('-')[1]
    time_intervals.append(f"{last_time}-{total_song_len}")

motion_data = [get_motion_and_speed(time, motion_type) for time in time_intervals]

frame_data, animation_prompts = calculate_frames(scene_change_times, time_intervals, motion_data)

motion_strings = build_transition_strings(frame_data)

# Print the final list of frame transitions for each motion type
print("\nFinal List of Frame Transitions for Each Motion Type:")
for motion, transitions in motion_strings.items():
    print(f"{motion}: {', '.join(transitions)}")

final_scene_times = scene_change_times
final_scene_times.insert(0, '0')
print(final_anim_frames)
print(final_scene_times)
# Print the animation prompts
print("\nAnimation Prompts:")
animation_prompts = ""

for i in range(len(final_anim_frames) - 1):
    animation_prompts += f"{final_anim_frames[i]}: | "
    print(f"Start Time: {final_scene_times[i]}, End Time: {final_scene_times[i+1]}, Start Frame: {final_anim_frames[i]}, End Frame: {final_anim_frames[i+1]}")
# animation_prompts += f"{final_anim_frames[-1]}: "
# animation_prompts += f"{final_anim_frames[-1]}:"
animation_prompts = animation_prompts[:-2]
print(animation_prompts)