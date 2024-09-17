import TkEasyGUI as eg
import pyautogui as gui
import subprocess
import settings as settings
from main import main

WEB_SITE = "https://github.com/suya172/FingerCursor"
gui_w, gui_h = gui.size()
canvas_w, canvas_h = 75 * (gui_w/gui_h), 75
menu_def = [
    ["File", ["Exit"]],
    ["Help", ["About", "GitHub"]],
]
layout = [
    [eg.Menu(menu_def)],
    [
        eg.Column(
            [[eg.Text("X0"), eg.Input(settings.x0, key="-x0-", size=(8, 1), enable_events=True), eg.Text("Y0"), eg.Input(settings.y0, key="-y0-", size=(8, 1), enable_events=True)],
             [eg.Text("X1"), eg.Input(settings.x1, key="-x1-", size=(8, 1), enable_events=True), eg.Text("Y1"), eg.Input(settings.y1, key="-y1-", size=(8, 1), enable_events=True)],],
        ),
        eg.VSeparator(pad=2),
        eg.Column(
            [[eg.Canvas(size=(canvas_w, canvas_h),
                        key="-canvas-", background_color="grey")]]
        ),
    ],
    [eg.Text("Device"), eg.Input(settings.device, key="-device-", size=(5, 1), enable_events=True),
     eg.Text("Threshold"), eg.Input(settings.threshold, key="-threshold-", size=(8, 1), enable_events=True)],
    [eg.Text("Cursor Interval"), eg.Input(settings.cursor_interval,
                                          key="-cursor_interval-", size=(8, 1), enable_events=True)],
    [eg.Text("Scroll Interval"), eg.Input(settings.scroll_interval, key="-scroll_interval-", size=(8, 1), enable_events=True),
     eg.Text("Scroll Amount"), eg.Input(settings.scroll_amount, key="-scroll_amount-", size=(8, 1), enable_events=True)],
    [eg.Text("Width"), eg.Input(settings.width, key="-width-", size=(8, 1), enable_events=True),
     eg.Text("Height"), eg.Input(settings.height, key="-height-", size=(8, 1), enable_events=True)],
    [eg.Checkbox("Debug Mode", default=settings.debug,
                 key="-debug-", enable_events=True)],
    [eg.HSeparator()],
    [eg.Button("Run", key="-run-", size=(8, 1)), eg.Text("", key="-message-")],
]
validate_int: list[str] = ["-device-", "-threshold-",
                           "-scroll_amount-", "-width-", "-height-"]
validate_float: list[str] = ["-x0-", "-y0-", "-x1-",
                             "-y1-", "-cursor_interval-", "-scroll_interval-"]
validate_required: list[str] = ["-device-", "-threshold-", "-scroll_amount-", "-width-",
                                "-height-", "-x0-", "-y0-", "-x1-", "-y1-", "-cursor_interval-", "-scroll_interval-"]
validate_0_1: list[str] = ["-x0-", "-y0-", "-x1-", "-y1-"]
to_run: bool = False

with eg.Window("Finger Cursor", layout, keep_on_top=True, grab_anywhere=True) as window:
    canvas = window["-canvas-"]
    widget = canvas.Widget
    def draw(x0, y0, x1, y1): return widget.create_rectangle(x0 * canvas_w,
                                                             y0 * canvas_h, x1 * canvas_w, y1 * canvas_h, outline="LightGreen", width=2)

    def clear(): return canvas.delete("all")
    draw(settings.x0, settings.y0, settings.x1, settings.y1)
    for event, values in window.event_iter():
        if event in validate_required:
            clear()
            if values[event] == "":
                window["-message-"].update("Please fill in all fields.")
                window["-run-"].update(disabled=True)
                continue
            else:
                window["-message-"].update("")
                window["-run-"].update(disabled=False)
        if event in validate_int:
            try:
                int(values[event])
                window["-message-"].update("")
                window["-run-"].update(disabled=False)
            except ValueError:
                window["-message-"].update(
                    f'{event[1:-1]} must be an integer.')
                window["-run-"].update(disabled=True)
                continue
        if event in validate_float:
            try:
                float(values[event])
                window["-message-"].update("")
                window["-run-"].update(disabled=False)
            except ValueError:
                window["-message-"].update(f'{event[1:-1]} must be a float.')
                window["-run-"].update(disabled=True)
                continue
        if event in validate_0_1:
            if float(values[event]) < 0 or float(values[event]) > 1:
                window["-message-"].update(
                    f'{event[1:-1]} must be between 0 and 1.')
                window["-run-"].update(disabled=True)
                continue
            else:
                draw(float(values["-x0-"]), float(values["-y0-"]),
                     float(values["-x1-"]), float(values["-y1-"]))
                window["-message-"].update("")
                window["-run-"].update(disabled=False)
        if event == "-run-":
            settings.debug = values["-debug-"]
            settings.device = int(values["-device-"])
            settings.x0 = float(values["-x0-"])
            settings.y0 = float(values["-y0-"])
            settings.x1 = float(values["-x1-"])
            settings.y1 = float(values["-y1-"])
            settings.threshold = int(values["-threshold-"])
            settings.cursor_interval = float(values["-cursor_interval-"])
            settings.scroll_interval = float(values["-scroll_interval-"])
            settings.scroll_amount = int(values["-scroll_amount-"])
            settings.width = int(values["-width-"])
            settings.height = int(values["-height-"])

            to_run = True
            break
        if event == "About":
            eg.popup_ok("FingerCursor:v0.1.0 by @suya172", title="About")
        if event == "GitHub":
            if eg.is_mac():
                # Macの場合
                subprocess.call(f"open {WEB_SITE}", shell=True)
            else:
                # Windowsの場合
                subprocess.call(f"start {WEB_SITE}", shell=True)
        if event in ["Exit", eg.WIN_CLOSED]:
            break

if to_run:
    main()
