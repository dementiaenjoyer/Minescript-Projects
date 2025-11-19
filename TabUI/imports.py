from system.pyj.minescript import *;

# MC
minecraft_class = JavaClass("net.minecraft.client.Minecraft");

argb = JavaClass("net.minecraft.util.ARGB");
gui_graphics = JavaClass("net.minecraft.client.gui.GuiGraphics");

vector3 = JavaClass("net.minecraft.world.phys.Vec3");
vector2 = JavaClass("net.minecraft.world.phys.Vec2");

# JOML
matrix4f = JavaClass("org.joml.Matrix4f");

# JAVA
j_float = JavaClass("java.lang.Float");
j_double = JavaClass("java.lang.Double");
j_integer = JavaClass("java.lang.Integer");
j_time = JavaClass("java.time.Instant");
j_math = JavaClass("java.lang.Math");

# OPENGL
glfw = JavaClass("org.lwjgl.glfw.GLFW");

# FABRIC
world_render_events = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents");
hud_render_callback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback");
world_render_last = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last");