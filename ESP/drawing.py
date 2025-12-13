from ESP.globals import OUTLINE, FONT;

def text(draw_context, text, x, y, color):
    draw_context.drawString(FONT, text, int(x), int(y), color);

def outline_text(draw_context, tstr, x, y, color):
    text(draw_context, tstr, x - 1, y, OUTLINE);
    text(draw_context, tstr, x + 1, y, OUTLINE);
    text(draw_context, tstr, x, y - 1, OUTLINE);
    text(draw_context, tstr, x, y + 1, OUTLINE);
    
    text(draw_context, tstr, x, y, color);

def filled_rect(draw_context, start_x, start_y, end_x, end_y, color):    
    start_x, start_y = int(start_x), int(start_y);
    end_x, end_y = int(end_x), int(end_y);
    
    draw_context.fill(start_x, start_y, end_x, end_y, color);

def filled_gradient(draw_context, start_x, start_y, end_x, end_y, upper, lower):
    start_x, start_y = int(start_x), int(start_y);
    end_x, end_y = int(end_x), int(end_y);

    draw_context.fillGradient(start_x, start_y, end_x, end_y, upper, lower);

def rect(draw_context, start_x, start_y, end_x, end_y, color):
    filled_rect(draw_context, start_x, start_y, end_x, start_y + 1, color);
    filled_rect(draw_context, start_x, end_y - 1, end_x, end_y, color);
    filled_rect(draw_context, start_x, start_y, start_x + 1, end_y, color);
    filled_rect(draw_context, end_x - 1, start_y, end_x, end_y, color);

def new(draw_type, *args):
    global callbacks;

    if (draw_type not in callbacks): 
        return; 

    return callbacks[draw_type](*args);

callbacks = {"outline_text": outline_text, "text": text, "filled_rect": filled_rect, "filled_gradient": filled_gradient, "rect": rect};