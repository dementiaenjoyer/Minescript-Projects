from system.pyj.minescript import *;

# MC
MinecraftClass = JavaClass("net.minecraft.client.Minecraft");

ARGB = JavaClass("net.minecraft.util.ARGB");

Vector3 = JavaClass("net.minecraft.world.phys.Vec3");
Vector2 = JavaClass("net.minecraft.world.phys.Vec2");

# JAVA
JavaFloat = JavaClass("java.lang.Float");
JavaDouble = JavaClass("java.lang.Double");
JavaInteger = JavaClass("java.lang.Integer");
JavaTime = JavaClass("java.time.Instant");
JavaMath = JavaClass("java.lang.Math");

# OPENGL
GLFW = JavaClass("org.lwjgl.glfw.GLFW");

# FABRIC
WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents");
HudRenderCallback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback");
WorldRenderLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last");