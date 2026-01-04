from TabUI.globals import ( FONT );

def Text(DrawContext, Text, X, Y, Color):
    DrawContext.drawString(FONT, Text, int(X), int(Y), Color);

def FilledRectangle(DrawContext, StartX, StartY, EndX, EndY, Color):
    StartX, StartY = int(StartX), int(StartY);
    EndX, EndY = int(EndX), int(EndY);
    
    DrawContext.fill(StartX, StartY, EndX, EndY, Color);

def Rectangle(DrawContext, StartX, StartY, EndX, EndY, Color):
    StartX, StartY = int(StartX), int(StartY);
    EndX, EndY = int(EndX), int(EndY);

    DrawContext.fill(StartX, StartY, EndX, StartY + 1, Color);
    DrawContext.fill(StartX, EndY - 1, EndX, EndY, Color);
    DrawContext.fill(StartX, StartY, StartX + 1, EndY, Color);
    DrawContext.fill(EndX - 1, StartY, EndX, EndY, Color);

def new(DrawType, *Arguments):
    global Callbacks;

    if (DrawType not in Callbacks): 
        return; 

    return Callbacks[DrawType](*Arguments);

Callbacks = { "text": Text, "filled_rect": FilledRectangle, "rect": Rectangle };