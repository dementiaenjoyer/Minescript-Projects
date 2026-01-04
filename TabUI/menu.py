from TabUI.globals import ( JavaFloat, Vector2, CLOCK_CLASS, WINDOW, FONT, DRAWING, ARGB, FONT );

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

    def AddElement(self, Element, Name, Default = False, Callback = None):
        Data = { "name": Name, "type": Element, "enabled": Default, "callback": Callback };
        self.Features.append(Data);
        
        if (Element == "label"):
            def UpdateText(txt):
                Data["text"] = txt;
            
            UpdateText(Name);
            Data["update"] = UpdateText;

            return Data;
        
        if (Element == "tab"):
            NewTab = Window(self.Position.x + (self.GetWidth() + 2), self.Position.y + self.GetPadding(len(self.Features) - 1), self);
            Data["tab"] = NewTab;

            return NewTab;

    def GetWidth(self):
        TextWidth, Font = 0, FONT;
        
        for Feature in self.Features:
            TextWidth = max(TextWidth, (Feature["type"] == "label" and Font.width(Feature["text"])) or Font.width(Feature["name"]));
        
        return TextWidth + 20;

    def GetFlag(self, name):
        for Feature in self.Features:
            if (Feature["name"] == name and Feature["type"] == "toggle"):
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

    def Notify(self, Text, Lifetime = 4):
        self.Notifications.append({ "text": Text, "lifetime": Lifetime, "tick": CLOCK_CLASS.tick() });