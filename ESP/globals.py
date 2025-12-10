from ESP.imports import *;

PURPLE = argb.color(255, 115, 100, 148);
WHITE = argb.color(255, 255, 255, 255);
RED = argb.color(255, 255, 0, 0);
OUTLINE = argb.color(255, 0, 0, 0);
FLAGS = style.EMPTY.withShadowColor(0xFFFFFF);

"""
@Nullable TextColor textColor,
@Nullable Integer integer,
@Nullable Boolean boolean_,
@Nullable Boolean boolean2,
@Nullable Boolean boolean3,
@Nullable Boolean boolean4,
@Nullable Boolean boolean5,
@Nullable ClickEvent clickEvent,
@Nullable HoverEvent hoverEvent,
@Nullable String string,
@Nullable FontDescription fontDescription
"""

MINECRAFT = minecraft_class.getInstance();
WINDOW = MINECRAFT.getWindow();

GAME_RENDERER = MINECRAFT.gameRenderer;
LEVEL = MINECRAFT.level;

OPTIONS = MINECRAFT.options;
FONT = MINECRAFT.font;

FONT_MANAGER = MINECRAFT.getClass().getDeclaredField("field_1708");
FONT_MANAGER.setAccessible(True);

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

hud_render_callback.EVENT.register(hud_render_callback(ManagedCallback(HUD_RENDER)));
