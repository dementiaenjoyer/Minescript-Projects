import TabUI.globals as essentials;

class Window:
    def __init__(self, position_x = 10, position_y = 10, parent = None):
        self.features = [ ];
        
        self.visible = True;
        self.c_tab = None;

        self.position = essentials.vector2(essentials.j_float(position_x), essentials.j_float(position_y));
        self.parent = parent;

        self.index = 0;
        
        self.colors = {
            "background": essentials.argb.color(255, 32, 38, 46),
            "border": essentials.argb.color(150, 21, 25, 31),
            "text": essentials.argb.color(255, 255, 255, 255),
            "toggled": essentials.argb.color(255, 98, 160, 110),
            "selected": essentials.argb.color(120, 57, 62, 69)
        };
        
        if (parent):
            self.colors = parent.colors;

    def render(self, draw_context):
        visible, active_tab = self.visible, self.c_tab;
        
        if (not visible):
            return;
    
        draw, font = essentials.DRAWING.new, essentials.FONT;

        width, e_height = self.get_width(), 15;
        height = (len(self.features) * e_height) + 2;

        position_x, position_y = self.position.x, self.position.y;
        colors, tab_index = self.colors, self.index;

        background, border, selected, toggled = colors["background"], colors["border"], colors["selected"], colors["toggled"];
        draw("filled_rect", draw_context, position_x, position_y, position_x + width, position_y + height, background);
        
        for index, feature in enumerate(self.features):
            bb = index * e_height;
            feature_y = position_y + 1 + bb;
            
            if (index == tab_index and not active_tab):                
                draw("filled_rect", draw_context, position_x + 1, feature_y, position_x + width - 1, feature_y + e_height, selected);
            
            draw("text", draw_context, feature["name"], position_x + 5, feature_y + (e_height - font.lineHeight) / 2, toggled if (feature["enabled"]) else colors["text"]);
        
        draw("rect", draw_context, position_x, position_y, position_x + width, position_y + height, border);
        
        if (active_tab):
            active_tab.render(draw_context);

    def down(self):
        visible, active_tab = self.visible, self.c_tab;
        
        if (not visible):
            return;
            
        if (active_tab):
            return active_tab.down();
            
        self.index = (self.index + 1) % len(self.features);

    def up(self):
        visible, active_tab = self.visible, self.c_tab;
        
        if (not visible):
            return;
            
        if (active_tab):
            return active_tab.up();
            
        self.index = (self.index - 1) % len(self.features);

    def right(self):
        visible, active_tab = self.visible, self.c_tab;
        
        if (not visible):
            return;
            
        if (active_tab):
            return active_tab.right();
            
        index, features = self.index, self.features;
        
        if (index < 0 or index >= len(features)):
            return;
            
        e_data = features[index];
        e_type, callback = e_data["type"], e_data["callback"];
        
        if (e_type == "toggle"):
            e_data["enabled"] = not e_data["enabled"];
            if (callback):
                callback(e_data["enabled"]);
        elif (e_type == "function"):
            if (callback):
                    callback();
        elif (e_type == "tab"):
            if ("tab" in e_data and len(e_data["tab"].features)):
                self.c_tab = e_data["tab"];

    def left(self):
        visible, active_tab, parent = self.visible, self.c_tab, self.parent;
        
        if (not visible):
            return;
            
        if (active_tab):
            if (active_tab.c_tab):
                active_tab.left();
            else:
                self.c_tab = None;
            
            return;
            
        if (parent):
            parent.c_tab = None;

    def toggle(self):
        active_tab = self.c_tab;
        self.visible = not self.visible;
        
        if (active_tab):
            active_tab.toggle();

    def add_element(self, element, name, default = False, callback = None):
        """
        Used to add an element to an existing menu.

        Args:
            element (Literal["tab", "toggle", "function", "info"]): Defines the object type.
                - "tab": Creates a submenu.
                - "toggle": Creates a toggle element. Pressing the right arrow toggles its value and triggers the callback (if provided).
                - "function": Creates a simple action element. Pressing the right arrow runs the callback (if provided).
                - "info": Creates a simple display-only element with no interaction.
            name (_type_): Text of the element.
            default (bool, optional): Default toggle value. Defaults to False.
            callback (_type_, optional): Callback function.
                - For "toggle", the callback receives the new toggle value.
                - For "function", the callback is executed every time the right arrow is pressed.
                - For any other element type, the callback is ignored.

        Returns:
            Optional[Window]: The newly created tab window when the element type is "tab".
        """

        data = {"name": name, "type": element, "enabled": default, "callback": callback};
        self.features.append(data);
        
        if (element == "tab"):
            new_tab = Window(self.position.x + self.get_width() + 2, self.position.y, self);
            data["tab"] = new_tab;

            return new_tab;

    def get_width(self):
        t_width = 0;
        
        for feature in self.features:
            t_width = max(t_width, essentials.FONT.width(feature["name"]));
        
        return t_width + 20;

    def get_flag(self, name):
        for feature in self.features:
            if (feature["name"] == name and feature["type"] != "tab"):
                return feature;
    
            result = feature["tab"].get_flag(name);
    
            if (result):
                return result;

    def set_color(self, color_type, color):
        if (color_type not in self.colors):
            return;
        
        active_tab = self.c_tab;
        self.colors[color_type] = color;
        
        if (active_tab):
            active_tab.set_color(color_type, color);