from ESP.imports import *; 

PURPLE = ARGB.color(255, 115, 100, 148);
WHITE = ARGB.color(255, 255, 255, 255);
RED = ARGB.color(255, 255, 0, 0);
OUTLINE = ARGB.color(255, 0, 0, 0);
FLAGS = Style.EMPTY.withShadowColor(0xFFFFFF);

MINECRAFT = Minecraft.getInstance();
WINDOW = MINECRAFT.getWindow();

GAME_RENDERER = MINECRAFT.gameRenderer;
LEVEL = MINECRAFT.level;

OPTIONS = MINECRAFT.options;
FONT = MINECRAFT.font;

import ESP.drawing as DRAWING;
import ESP.math as MATH;

class EVENT_MANAGER_CLASS:
    def __init__(self):
        self.events = { };
        
    def register(self, name, callback):
        self.events[name] = callback;

EVENT_MANAGER = EVENT_MANAGER_CLASS();

def HUD_RENDER(draw_context, _):
    for name, callback in EVENT_MANAGER.events.items():
        callback(draw_context);

HudRenderCallback.EVENT.register(HudRenderCallback(ManagedCallback(HUD_RENDER)));
