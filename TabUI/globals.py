import TabUI.drawing as DRAWING;
import TabUI.menu as MENU;

from TabUI.imports import *;

WHITE = argb.color(255, 255, 255, 255);
RED = argb.color(255, 255, 0, 0);
OUTLINE = argb.color(255, 0, 0, 0);
PURPLE = argb.color(255, 115, 100, 148);

MINECRAFT = minecraft_class.getInstance();
WINDOW = MINECRAFT.getWindow();

OPTIONS = MINECRAFT.options;
FONT = MINECRAFT.font;

class EVENT_MANAGER_CLASS:
    def __init__(self):
        self.events = { };
        
    def register(self, name, callback):
        self.events[name] = callback;

class KEYBIND_CLASS: # i made this because add_event_listener causes INSANE amounts of fps drops. my 1k fps would get to as low as 250 fps from ONLY using add_event_listener on another project, dis works good though!
    def __init__(self):
        self.previous = {};
        self.events = { };
        self.keys = {
            "MB1": 0,
            "MB2": 1,
            "A": 65,
            "B": 66,
            "C": 67,
            "D": 68,
            "E": 69,
            "F": 70,
            "G": 71,
            "H": 72,
            "I": 73,
            "J": 74,
            "K": 75,
            "L": 76,
            "M": 77,
            "N": 78,
            "O": 79,
            "P": 80,
            "Q": 81,
            "R": 82,
            "S": 83,
            "T": 84,
            "U": 85,
            "V": 86,
            "W": 87,
            "X": 88,
            "Y": 89,
            "Z": 90,
            "0": 48,
            "1": 49,
            "2": 50,
            "3": 51,
            "4": 52,
            "5": 53,
            "6": 54,
            "7": 55,
            "8": 56,
            "9": 57,
            "SPACE": 32,
            "APOSTROPHE": 39,
            "COMMA": 44,
            "MINUS": 45,
            "PERIOD": 46,
            "SLASH": 47,
            "SEMICOLON": 59,
            "EQUAL": 61,
            "LEFT_BRACKET": 91,
            "BACKSLASH": 92,
            "RIGHT_BRACKET": 93,
            "GRAVE_ACCENT": 96,
            "ESCAPE": 256,
            "ENTER": 257,
            "TAB": 258,
            "BACKSPACE": 259,
            "INSERT": 260,
            "DELETE": 261,
            "RIGHT": 262,
            "LEFT": 263,
            "DOWN": 264,
            "UP": 265,
            "PAGE_UP": 266,
            "PAGE_DOWN": 267,
            "HOME": 268,
            "END": 269,
            "CAPS_LOCK": 280,
            "SCROLL_LOCK": 281,
            "NUM_LOCK": 282,
            "PRINT_SCREEN": 283,
            "PAUSE": 284,
            "F1": 290,
            "F2": 291,
            "F3": 292,
            "F4": 293,
            "F5": 294,
            "F6": 295,
            "F7": 296,
            "F8": 297,
            "F9": 298,
            "F10": 299,
            "F11": 300,
            "F12": 301,
            "LEFT_SHIFT": 340,
            "LEFT_CONTROL": 341,
            "LEFT_ALT": 342,
            "LEFT_SUPER": 343,
            "RIGHT_SHIFT": 344,
            "RIGHT_CONTROL": 345,
            "RIGHT_ALT": 346,
            "RIGHT_SUPER": 347,
            "MENU": 348
        };

        for key_code in self.keys.values():
            self.previous[key_code] = False;

    def on_update(self, context):
        release, press = glfw.GLFW_RELEASE, glfw.GLFW_PRESS;

        events, previous = self.events, self.previous;
        window = WINDOW.getWindow();

        for name in events:
            code = self.keys.get(name);
            
            if (str(screen_name()) == "Chat screen"):
                continue;
            
            if (not code):
                continue;
            
            state = (("MB" in name) and glfw.glfwGetMouseButton(window, code)) or glfw.glfwGetKey(window, code);
            prev = previous.get(code, release);

            if (state == press and prev != press):
                if ("down" in events[name]):
                    events[name]["down"]( );

            if (state == release and prev != release):
                if ("up" in events[name]):
                    events[name]["up"]( );

            previous[code] = state;

    def up(self, key, callback):
        if (key not in self.events):
            self.events[key] = { };

        self.events[key]["up"] = callback;

    def down(self, key, callback):
        if (key not in self.events):
            self.events[key] = { };

        self.events[key]["down"] = callback;

class CLOCK_CLASS:
    @staticmethod
    def tick():
        return j_time.now().toEpochMilli();

EVENT_MANAGER = EVENT_MANAGER_CLASS();
KEYBINDS = KEYBIND_CLASS();

def HUD_RENDER(draw_context, _):
    for name, callback in EVENT_MANAGER.events.items():
        callback(draw_context);

hud_render_callback.EVENT.register(hud_render_callback(ManagedCallback(HUD_RENDER)));
world_render_events.LAST.register(world_render_last(KEYBINDS.on_update));

# Tracks whether we *think* the inventory is open because of an input field
INPUT_INVENTORY_OPEN = False;      # just for info, if you care
INPUT_INVENTORY_LOCKED = False;    # when True, we won't auto-open inventory for the current input selection
LAST_SCREEN_NAME = None;


def open_inventory_gui():
    """
    Open the player's inventory screen.

    You must implement this using the Minecraft Java class.
    Example in Java (1.19+ style):
        Minecraft mc = Minecraft.getInstance();
        mc.setScreen(new InventoryScreen(mc.player));
    """
    press_key_bind("key.inventory", True)
    press_key_bind("key.inventory", False)
    pass;

def _get_active_window(menu):
    """
    Go down into the currently active tab chain to get the deepest window.
    """
    win = menu;
    while win.c_tab:
        win = win.c_tab;
    return win;

def is_input_selected(menu):
    """
    Returns True if, in the active window, the selected feature is of type "input".
    """
    win = _get_active_window(menu);
    feature = win._get_selected_feature();
    return (feature is not None) and (feature["type"] == "input");
