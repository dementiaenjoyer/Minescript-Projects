import essentials.globals as main;

def text(draw_context, text, x, y, color):
    draw_context.drawString(main.FONT, text, int(x), int(y), color);

def filled_rect(draw_context, start_x, start_y, end_x, end_y, color):
    start_x, start_y = int(start_x), int(start_y);
    end_x, end_y = int(end_x), int(end_y);
    
    draw_context.fill(start_x, start_y, end_x, end_y, color);

def rect(draw_context, start_x, start_y, end_x, end_y, color):
    start_x, start_y = int(start_x), int(start_y);
    end_x, end_y = int(end_x), int(end_y);

    draw_context.fill(start_x, start_y, end_x, start_y + 1, color);
    draw_context.fill(start_x, end_y - 1, end_x, end_y, color);
    draw_context.fill(start_x, start_y, start_x + 1, end_y, color);
    draw_context.fill(end_x - 1, start_y, end_x, end_y, color);

def new(draw_type, *args):
    global callbacks;

    if (draw_type not in callbacks): 
        return; 

    return callbacks[draw_type](*args);

callbacks = {"text": text, "filled_rect": filled_rect, "rect": rect};