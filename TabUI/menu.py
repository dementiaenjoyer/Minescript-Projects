import TabUI.globals as essentials;

class Window:
    def __init__(self, position_x = 10, position_y = 10, parent = None):
        self.features = [ ];
        self.notifications = [ ];
        
        self.visible = True;
        self.c_tab = None;

        self.position = essentials.vector2(essentials.j_float(position_x), essentials.j_float(position_y));
        self.parent = parent;

        self.index = 0;
        self.e_height = 16;
        
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

        width, e_height = self.get_width(), self.e_height;
        height = (len(self.features) * e_height) + 2;

        l_height = font.lineHeight;
        h_offset = (e_height - l_height) * 0.5; # in lua (which i mainly use) multiplication is faster than division , idk if this applies to java but its wahtever

        position_x, position_y = self.position.x, self.position.y;
        colors, tab_index = self.colors, self.index;

        background, border, selected, toggled, text = colors["background"], colors["border"], colors["selected"], colors["toggled"], colors["text"];
        draw("filled_rect", draw_context, position_x, position_y, position_x + width, position_y + height, background);
        
        for index, feature in enumerate(self.features):
            feature_y = position_y + self.get_padding(index);
            
            if (index == tab_index and not active_tab):
                draw("filled_rect", draw_context, position_x, feature_y, position_x + width, feature_y + (e_height + 1), selected);
            
            e_type = feature["type"];
            e_color, e_text = ((e_type == "button" or e_type == "label") and text) or (e_type == "toggle" and toggled if (feature["enabled"]) else text), (e_type == "label" and feature["text"]) or feature["name"];
            
            draw("text", draw_context, e_text, position_x + 5, feature_y + h_offset, e_color);
        
        draw("rect", draw_context, position_x, position_y, position_x + width, position_y + height, border);
        
        if (active_tab):
            active_tab.render(draw_context);
    
        s_width = essentials.WINDOW.getGuiScaledWidth();
        clock = essentials.CLOCK_CLASS.tick();

        old = [ ];
        
        for index, value in enumerate(self.notifications):
            running, lifetime = clock - value["tick"], value["lifetime"] * 1000;

            if (lifetime <= running):
                old.append(value);

                continue;

            argb = essentials.argb;

            bg_red, bg_green, bg_blue = argb.red(background), argb.green(background), argb.blue(background);
            border_red, border_green, border_blue = argb.red(border), argb.green(border), argb.blue(border);
            txt_red, txt_green, txt_blue = argb.red(text), argb.green(text), argb.blue(text);

            n_trans, n_text = int(255 * ((running < 200) and (running / 200) or ((running > lifetime - 200) and ((lifetime - running) / 200) or 1))), value["text"];

            txt_width, h_height = essentials.FONT.width(n_text) + 20, 20;
            x, y = s_width - txt_width - 8, 8 + (index * 25);

            l_height = font.lineHeight;
            h_offset = (15 - l_height) * 0.5;

            draw("filled_rect", draw_context, x, y, x + txt_width, y + h_height, argb.color(n_trans, bg_red, bg_green, bg_blue));
            draw("rect", draw_context, x, y, x + txt_width, y + h_height, argb.color(n_trans, border_red, border_green, border_blue));
            draw("text", draw_context, n_text, x + 10, y + (h_offset + 3), argb.color(n_trans, txt_red, txt_green, txt_blue));
    
        for value in old: # removing the current index in the same for loop would throw 'ConcurrentModificationException', so i just did this instead
            self.notifications.remove(value)

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
        elif (e_type == "button" and callback):
            callback();
        elif (e_type == "tab"):
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
        data = {"name": name, "type": element, "enabled": default, "callback": callback};
        self.features.append(data);
        
        if (element == "label"):
            def update_text(txt):
                data["text"] = txt;
            
            update_text(name);
            data["update"] = update_text;

            return data;
        
        if (element == "tab"):
            new_tab = Window(self.position.x + (self.get_width() + 2), self.position.y + self.get_padding(len(self.features) - 1), self);
            data["tab"] = new_tab;

            return new_tab;

    def get_width(self):
        t_width, font = 0, essentials.FONT;
        
        for feature in self.features:
            t_width = max(t_width, (feature["type"] == "label" and font.width(feature["text"])) or font.width(feature["name"]));
        
        return t_width + 20;

    def get_flag(self, name):
        for feature in self.features:
            if (feature["name"] == name and feature["type"] == "toggle"):
                return feature;
    
            if (feature["type"] != "tab"):
                continue;
    
            result = feature["tab"].get_flag(name);
    
            if (result):
                return result;

    def get_padding(self, index):
        return index * self.e_height;

    def set_scale(self, height):
        if (height <= 8):
            return;

        self.e_height = height;

        for index, feature in enumerate(self.features):
            if (feature["type"] != "tab"):
                continue;

            tab_window = feature["tab"];
            
            tab_window.position = essentials.vector2(self.position.x + (self.get_width() + 2), self.position.y + (index * height));
            tab_window.set_scale(height);

    def set_color(self, color_type, color):
        if (color_type not in self.colors):
            return;
        
        active_tab = self.c_tab;
        self.colors[color_type] = color;
        
        if (active_tab):
            active_tab.set_color(color_type, color);

    def notify(self, text, lifetime = 4):
        self.notifications.append({
            "text": text,
            "lifetime": lifetime,
            "tick": essentials.CLOCK_CLASS.tick()
        });