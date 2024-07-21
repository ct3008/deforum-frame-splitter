# deforum-frame-splitter

Intro: Basic python helper to output proper frames for transitions and scene changes in Deforum Stable Diffusion

To know:
- It's assumed that there are 15 frames per second
- Speed multipliers are hardcoded as {"vslow": 0.25, "slow": 0.5, "normal": 1, "fast": 2.5, "vfast": 6}
- Strengths are hardcoded as 
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

Instructions: 
1) Determine the timestamps at which you want your scenes to start at. The code will interpolate between 0 to the length of the song of interest (so **DO NOT** include 0 or the final timestamp in this range)
2) Determine the timestamps of desired motion transitions. Anytime you want a new motion to start in the scene or make a currently present motion have a different strength, mark it as a timestamp and input it when prompted
3) You will be shown each time range of interest when a motion will occur.
- You will be prompted to input the speed of the segment of video. This will change the number of frames for this segment by 0.25 for vslow, 0.5 for slow, 2.5 for fast and 6 for vfast (the assumed speed multipliers in video editing software)
- You will be prompted for a motion type (options differ based on if you chose 2d or 3d motion in the beginning)
- You will be prompted for the strength of the motion which will change the magnitude of the motion
- You will be prompted to continually add motions for the same time frame
4) The final output will be a final list of frame transitions broken up my motion type and placed in the proper format for Deforum and, at the very end, there is a short list in the form of "0: | [frame]: | [frame]: ...." based on the timestamps from step 1, which you can copy and paste your prompts directly into. Each of these you can copy and paste directly into deforum for ease of use.
