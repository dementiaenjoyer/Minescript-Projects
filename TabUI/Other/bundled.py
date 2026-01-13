from system.pyj.minescript import *;

# Imports
MinecraftClass = JavaClass("net.minecraft.client.Minecraft");
ARGB = JavaClass("net.minecraft.util.ARGB");

Vector3 = JavaClass("net.minecraft.world.phys.Vec3");
Vector2 = JavaClass("net.minecraft.world.phys.Vec2");

JavaFloat = JavaClass("java.lang.Float");
JavaDouble = JavaClass("java.lang.Double");
JavaInteger = JavaClass("java.lang.Integer");
JavaTime = JavaClass("java.time.Instant");
JavaMath = JavaClass("java.lang.Math");

GLFW = JavaClass("org.lwjgl.glfw.GLFW");

WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents");
HudRenderCallback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback");
WorldRenderLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last");

# Colors
WHITE = ARGB.color(255, 255, 255, 255);
RED = ARGB.color(255, 255, 0, 0);
OUTLINE = ARGB.color(255, 0, 0, 0);
PURPLE = ARGB.color(255, 115, 100, 148);

# Variables
MINECRAFT = MinecraftClass.getInstance();
WINDOW = MINECRAFT.getWindow();

OPTIONS = MINECRAFT.options;
FONT = MINECRAFT.font;

# Classes
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

    def Up(Self, Key, Callback):
        if (Key not in Self.Events):
            Self.Events[Key] = { };

        Self.Events[Key]["up"] = Callback;

    def Down(Self, Key, Callback):
        if (Key not in Self.Events):
            Self.Events[Key] = { };

        Self.Events[Key]["down"] = Callback;

class CLOCK_CLASS:
    @staticmethod
    def tick():
        return JavaTime.now().toEpochMilli();

class DRAWING_CLASS:
    def Text(Self, DrawContext, Text, X, Y, Color):
        DrawContext.drawString(FONT, Text, int(X), int(Y), Color);

    def FilledRectangle(Self, DrawContext, StartX, StartY, EndX, EndY, Color):
        StartX, StartY = int(StartX), int(StartY);
        EndX, EndY = int(EndX), int(EndY);
        
        DrawContext.fill(StartX, StartY, EndX, EndY, Color);

    def Rectangle(Self, DrawContext, StartX, StartY, EndX, EndY, Color):
        StartX, StartY = int(StartX), int(StartY);
        EndX, EndY = int(EndX), int(EndY);

        DrawContext.fill(StartX, StartY, EndX, StartY + 1, Color);
        DrawContext.fill(StartX, EndY - 1, EndX, EndY, Color);
        DrawContext.fill(StartX, StartY, StartX + 1, EndY, Color);
        DrawContext.fill(EndX - 1, StartY, EndX, EndY, Color);

    def new(Self, DrawType, *Arguments):
        Callbacks = Self.Callbacks;

        if (DrawType not in Callbacks): 
            return; 

        return Callbacks[DrawType](*Arguments);

    def __init__(Self):
        Self.Callbacks = { "text": Self.Text, "filled_rect": Self.FilledRectangle, "rect": Self.Rectangle };

class Window:
    def __init__(Self, PositionX = 10, PositionY = 10, Parent = None):
        Self.Features = [ ];
        Self.Notifications = [ ];
        
        Self.Visible = True;
        Self.CurrentTab = None;

        Self.Position = Vector2(JavaFloat(PositionX), JavaFloat(PositionY));
        Self.Parent = Parent;

        Self.Index = 0;
        Self.ElementHeight = 16;
        
        Self.Colors = {
            "background": ARGB.color(255, 32, 38, 46),
            "border": ARGB.color(150, 21, 25, 31),
            "text": ARGB.color(255, 255, 255, 255),
            "toggled": ARGB.color(255, 98, 160, 110),
            "selected": ARGB.color(120, 57, 62, 69)
        };
        
        if (Parent):
            Self.Colors = Parent.Colors;

    def Render(Self, DrawContext):
        Visible, ActiveTab = Self.Visible, Self.CurrentTab;
        Draw, Font = DRAWING.new, FONT;

        Width, ElementHeight = Self.GetWidth(), Self.ElementHeight;
        Height = (len(Self.Features) * ElementHeight) + 2;

        HeightOffset = (ElementHeight - Font.lineHeight) * 0.5; # in lua (which i mainly use) multiplication is faster than division , idk if this applies to java but its wahtever

        PositionX, PositionY = Self.Position.x, Self.Position.y;
        Colors, TabIndex = Self.Colors, Self.Index;

        Background, Border, Selected, Toggled, Text = Colors["background"], Colors["border"], Colors["selected"], Colors["toggled"], Colors["text"];
        
        if (Visible):
            Draw("filled_rect", DrawContext, PositionX, PositionY, PositionX + Width, PositionY + Height, Background);
        
            for Index, Feature in enumerate(Self.Features):
                FeatureY = PositionY + Self.GetPadding(Index);
                
                if (Index == TabIndex and not ActiveTab):
                    Draw("filled_rect", DrawContext, PositionX, FeatureY, PositionX + Width, FeatureY + (ElementHeight + 1), Selected);
                
                ElementType = Feature["type"];
                ElementColor, ElementText = ((ElementType == "button" or ElementType == "label") and Text) or (ElementType == "toggle" and Toggled if (Feature["enabled"]) else Text), (ElementType == "label" and Feature["text"]) or Feature["name"];
                
                Draw("text", DrawContext, ElementText, PositionX + 5, FeatureY + HeightOffset, ElementColor);
            
            Draw("rect", DrawContext, PositionX, PositionY, PositionX + Width, PositionY + Height, Border);
            
            if (ActiveTab):
                ActiveTab.Render(DrawContext);
    
        ScaledWidth = WINDOW.getGuiScaledWidth();
        Clock = CLOCK_CLASS.tick();

        OldNotifications = [ ];
        
        for Index, Value in enumerate(Self.Notifications):
            Running, Lifetime = Clock - Value["tick"], Value["lifetime"] * 1000;

            if (Lifetime <= Running):
                OldNotifications.append(Value);

                continue;

            BackgroundRed, BackgroundGreen, BackgroundBlue = ARGB.red(Background), ARGB.green(Background), ARGB.blue(Background);
            BorderRed, BorderGreen, BorderBlue = ARGB.red(Border), ARGB.green(Border), ARGB.blue(Border);
            TextRed, TextGreen, TextBlue = ARGB.red(Text), ARGB.green(Text), ARGB.blue(Text);

            Transparency, NotifText = int(255 * ((Running < 200) and (Running / 200) or ((Running > Lifetime - 200) and ((Lifetime - Running) / 200) or 1))), Value["text"];

            TextWidth, TextHeight = FONT.width(NotifText) + 20, 20;
            X, Y = ScaledWidth - TextWidth - 8, 8 + (Index * 25);

            HeightOffset = (15 - Font.lineHeight) * 0.5;

            Draw("filled_rect", DrawContext, X, Y, X + TextWidth, Y + TextHeight, ARGB.color(Transparency, BackgroundRed, BackgroundGreen, BackgroundBlue));
            Draw("rect", DrawContext, X, Y, X + TextWidth, Y + TextHeight, ARGB.color(Transparency, BorderRed, BorderGreen, BorderBlue));
            Draw("text", DrawContext, NotifText, X + 10, Y + (HeightOffset + 3), ARGB.color(Transparency, TextRed, TextGreen, TextBlue));
    
        for Value in OldNotifications: # removing the current index in the same for loop would throw 'ConcurrentModificationException', so i just did this instead
            Self.Notifications.remove(Value)

    def Down(Self):
        Visible, ActiveTab = Self.Visible, Self.CurrentTab;
        
        if (not Visible):
            return;
            
        if (ActiveTab):
            return ActiveTab.Down();
            
        Self.Index = (Self.Index + 1) % len(Self.Features);

    def Up(Self):
        Visible, ActiveTab = Self.Visible, Self.CurrentTab;
        
        if (not Visible):
            return;
            
        if (ActiveTab):
            return ActiveTab.Up();
            
        Self.Index = (Self.Index - 1) % len(Self.Features);

    def Right(Self):
        Visible, ActiveTab = Self.Visible, Self.CurrentTab;
        
        if (not Visible):
            return;
            
        if (ActiveTab):
            return ActiveTab.Right();
            
        Index, Features = Self.Index, Self.Features;
        
        if (Index < 0 or Index >= len(Features)):
            return;
            
        ElementData = Features[Index];
        ElementType, Callback = ElementData["type"], ElementData["callback"];
        
        if (ElementType == "toggle"):
            ElementData["enabled"] = not ElementData["enabled"];

            if (Callback):
                Callback(ElementData["enabled"]);
        elif (ElementType == "button" and Callback):
            Callback();
        elif (ElementType == "tab"):
            Self.CurrentTab = ElementData["tab"];

    def Left(Self):
        Visible, ActiveTab, Parent = Self.Visible, Self.CurrentTab, Self.Parent;
        
        if (not Visible):
            return;
            
        if (ActiveTab):
            if (ActiveTab.CurrentTab):
                ActiveTab.Left();
            else:
                Self.CurrentTab = None;
            
            return;
            
        if (Parent):
            Parent.CurrentTab = None;

    def Toggle(Self):
        ActiveTab = Self.CurrentTab;
        Self.Visible = not Self.Visible;
        
        if (ActiveTab):
            ActiveTab.Toggle();
    
    def UpdateTabs(Self):
        Width = Self.GetWidth();
        PositionX, PositionY = Self.Position.x, Self.Position.y;

        for Index, Feature in enumerate(Self.Features):
            if (Feature["type"] != "tab"):
                continue;

            TabWindow = Feature["tab"];
            
            TabWindow.Position = Vector2(JavaFloat(PositionX + Width + 2), JavaFloat(PositionY + Self.GetPadding(Index)));
            TabWindow.UpdateTabs();

    def AddElement(Self, Element, Name, Default = False, Callback = None, Flag = None):
        if (not Flag):
            Flag = Name;

        Data = { "name": Name, "type": Element, "enabled": Default, "callback": Callback, "flag": Flag };
        Self.Features.append(Data);
        
        if (Element == "label"):
            def UpdateText(txt):
                Data["text"] = txt;
            
            UpdateText(Name);
            Data["update"] = UpdateText;

            Self.UpdateTabs();

            return Data;
        
        if (Element == "tab"):
            NewTab = Window(Self.Position.x + (Self.GetWidth() + 2), Self.Position.y + Self.GetPadding(len(Self.Features) - 1), Self);
            Data["tab"] = NewTab;

            Self.UpdateTabs();

            return NewTab;

        Self.UpdateTabs();

    def GetWidth(Self):
        TextWidth, Font = 0, FONT;
        
        for Feature in Self.Features:
            TextWidth = max(TextWidth, (Feature["type"] == "label" and Font.width(Feature["text"])) or Font.width(Feature["name"]));
        
        return TextWidth + 20;

    def GetFlag(Self, name):
        for Feature in Self.Features:
            if (Feature["flag"] == name and Feature["type"] == "toggle"):
                return Feature;
    
            if (Feature["type"] != "tab"):
                continue;
    
            Result = Feature["tab"].GetFlag(name);
    
            if (Result):
                return Result;

    def GetPadding(Self, Index):
        return Index * Self.ElementHeight;

    def SetScale(Self, Height):
        if (Height <= 8):
            return;

        Self.ElementHeight = Height;

        for Index, Feature in enumerate(Self.Features):
            if (Feature["type"] != "tab"):
                continue;

            TabWindow = Feature["tab"];
            
            TabWindow.Position = Vector2(Self.Position.x + (Self.GetWidth() + 2), Self.Position.y + (Index * Height));
            TabWindow.SetScale(Height);

    def SetColor(Self, ColorType, Color):
        if (ColorType not in Self.Colors):
            return;
        
        ActiveTab = Self.CurrentTab;
        Self.Colors[ColorType] = Color;
        
        if (ActiveTab):
            ActiveTab.SetColor(ColorType, Color);

    def Notify(Self, Text, Lifetime = 4):
        Self.Notifications.append({ "text": Text, "lifetime": Lifetime, "tick": CLOCK_CLASS.tick() });

EVENT_MANAGER = EVENT_MANAGER_CLASS();
KEYBINDS = KEYBIND_CLASS();
DRAWING = DRAWING_CLASS();

def HUD_RENDER(DrawContext, _):
    for Name, Callback in EVENT_MANAGER.Events.items():
        Callback(DrawContext);

HudRenderCallback.EVENT.register(HudRenderCallback(ManagedCallback(HUD_RENDER)));
WorldRenderEvents.LAST.register(WorldRenderLast(KEYBINDS.OnUpdate));
