"""
I usually only use PascalCase for classes, but i ended up writing this entire thing
in PascalCase just because there's nothing else to add really, and i wasn't sure whether to use snake_case or not

Feel free to change stuff such as the amount of iterations for the chunk sections, may drop a lot of fps currently.
"""

# Imports
from system.pyj.minescript import *;

# Game Classes
Blocks = JavaClass("net.minecraft.world.level.block.Blocks");
Minecraft = JavaClass("net.minecraft.client.Minecraft");
Predicate = JavaClass("java.util.function.Predicate");
Field = JavaClass("java.lang.reflect.Field");

# Python Classes
class Reflection:
    Cache = { };

    @staticmethod
    def GetField(Object, Mapping):
        Cache = Reflection.Cache;
        Class = Object.getClass();
        
        Field = Cache.setdefault(Mapping, Class.getDeclaredField(Mapping));
        
        if (not Field.canAccess(Object)):
            Field.setAccessible(True);
        
        return Field.get(Object);

class Getter:
    def __init__(self):
        self.Minecraft = Minecraft.getInstance();

    def GetBlocks(self, BlockType, MaxBlocks = 100):
        Locations = [ ];
        Collected = 0;

        Instance = self.Minecraft;
        Level = Instance.level;

        ChunkCache = Level.getChunkSource();

        Storage = Reflection.GetField(ChunkCache, "field_16246");
        Chunks = Reflection.GetField(Storage, "field_16251");

        for Index in range(Chunks.length()):
            Chunk = Chunks.get(Index);
        
            if (not Chunk):
                continue;
            
            Location = Chunk.getPos();
            ChunkX, ChunkZ = Location.x, Location.z;
        
            for Key, Section in enumerate(Chunk.getSections()):
                if (Section.hasOnlyAir()):
                    continue;
                
                States = Section.getStates();
        
                if (not States.maybeHas(Predicate(lambda BlockState: BlockState.getBlock() == BlockType))): # thank god minecraft has this, otherwise this would be running at 0.5 fps
                    continue;
                                
                Data = Reflection.GetField(States, "field_34560");
        
                BitStorage = Reflection.GetField(Data, "comp_118");
                Palette = Reflection.GetField(Data, "comp_119");
        
                BaseY = Key * 16 - 63;
        
                for Step in range(4096): # BitStorage.getSize() = (16 ^ 3)
                    if (Palette.valueFor(BitStorage.get(Step)).getBlock() != BlockType):
                        continue;
                                        
                    if (Collected >= MaxBlocks):
                        break;
                    
                    Collected += 1;

                    X = ChunkX * 16 + (Step % 16);
                    Y = BaseY + Step // 256;
                    Z = ChunkZ * 16 + ((Step % 256) // 16);
        
                    Locations.append((X, Y - 2, Z));

        return Locations;
