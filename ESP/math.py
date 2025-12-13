from ESP.globals import WINDOW, OPTIONS, JavaFloat, JavaMath, JavaVector2;

def get_fov(player): # semi accurate, mc's getfov method is protected/priv so you cant access it w/o java reflection (which i dont wanna use)
    base_value = OPTIONS.fov().get().intValue();

    return base_value + (player.getFieldOfViewModifier(True, JavaFloat(base_value)));

def world_to_screen(game_renderer, destination):
    p2s = game_renderer.projectPointToScreen(destination); # NDC
    
    if (p2s.z >= 1.0): # off screen
        return;

    # NDC --> PIXELS
    width, height = WINDOW.getGuiScaledWidth(), WINDOW.getGuiScaledHeight();

    x = (JavaFloat(p2s.x) + 1.0) * (0.5 * width);
    y = ((1.0 - JavaFloat(p2s.y))) * (0.5 * height);

    return JavaVector2(JavaFloat(int(x)), JavaFloat(int(y)));

def get_screen_scale(origin, destination, width, height, player):
    distance = origin.distanceTo(destination);

    if (distance < 1.0): 
        distance = 1.0;

    cap = 5.0; # minimum size to fix outline issues

    scale = 1.0 / JavaMath.tan(get_fov(player) / 57.295779513 / 2.0); 
    x, y = JavaFloat(int(((width * 360.0) / distance) * scale)), JavaFloat(int(((height * 300.0) / distance) * scale));

    return JavaVector2(JavaFloat(max(x, cap)), JavaFloat(max(y, cap)));