from TabUI.imports import *;

WHITE = ARGB.color(255, 255, 255, 255);
RED = ARGB.color(255, 255, 0, 0);
OUTLINE = ARGB.color(255, 0, 0, 0);
PURPLE = ARGB.color(255, 115, 100, 148);

MINECRAFT = MinecraftClass.getInstance();
WINDOW = MINECRAFT.getWindow();

OPTIONS = MINECRAFT.options;
FONT = MINECRAFT.font;

class EVENT_MANAGER_CLASS:
    def __init__(Self):
        Self.Events = { };
        
    def Register(Self, Name, Callback):
        Self.Events[Name] = Callback;

class KEYBIND_CLASS: # i made this because add_event_listener causes INSANE amounts of fps drops. my 1k fps would get to as low as 250 fps from ONLY using add_event_listener on another project, dis works good though!
    def __init__(Self):
        Self.Previous = {};
        Self.Events = { };
        Self.Keys = {
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

        for key_code in Self.Keys.values():
            Self.Previous[key_code] = False;

    def OnUpdate(Self, Context):
        Release, Press = GLFW.GLFW_RELEASE, GLFW.GLFW_PRESS;

        Events, Previous = Self.Events, Self.Previous;
        Window = WINDOW.getWindow();

        for Name in Events:
            Code = Self.Keys.get(Name);
            
            if (not Code):
                continue;
            
            State = (("MB" in Name) and GLFW.glfwGetMouseButton(Window, Code)) or GLFW.glfwGetKey(Window, Code);
            Prev = Previous.get(Code, Release);

            if (State == Press and Prev != Press):
                if ( "down" in Events[Name] ):
                    Events[Name]["down"]( );

            if (State == Release and Prev != Release):
                if ( "up" in Events[Name] ):
                    Events[Name]["up"]( );

            Previous[Code] = State;

    def Up(Self, key, Callback):
        if (key not in Self.Events):
            Self.Events[key] = { };

        Self.Events[key]["up"] = Callback;

    def Down(Self, Key, Callback):
        if (Key not in Self.Events):
            Self.Events[Key] = { };

        Self.Events[Key]["down"] = Callback;

class CLOCK_CLASS:
    @staticmethod
    def tick():
        return JavaTime.now().toEpochMilli();

EVENT_MANAGER = EVENT_MANAGER_CLASS();
KEYBINDS = KEYBIND_CLASS();

import TabUI.drawing as DRAWING;
import TabUI.menu as MENU;

def HUD_RENDER(DrawContext, _):
    for Name, Callback in EVENT_MANAGER.Events.items():
        Callback(DrawContext);

HudRenderCallback.EVENT.register(HudRenderCallback(ManagedCallback(HUD_RENDER)));
WorldRenderEvents.LAST.register(WorldRenderLast(KEYBINDS.OnUpdate));