from system.pyj.minescript import *;

Blocks = JavaClass("net.minecraft.world.level.block.Blocks");
Minecraft = JavaClass("net.minecraft.client.Minecraft");
Predicate = JavaClass("java.util.function.Predicate");
Field = JavaClass("java.lang.reflect.Field");

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

    def GetBlocks(self, BlockType, MaxBlocks = 100, ExitIfExists = False):
        Locations = [ ];
        CachedChunks = [ ];

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
        
                if (not States.maybeHas(Predicate(lambda BlockState: BlockState.getBlock() == BlockType))):
                    continue;

                if (ExitIfExists):
                    Position = (ChunkX, ChunkZ);

                    if (Position in CachedChunks): # so we dont store the same chunk multiple times
                        continue;

                    CachedChunks.append(Position);
                    Locations.append((ChunkX * 16 + 8, 120, ChunkZ * 16 + 8));

                    continue;
                                
                Data = Reflection.GetField(States, "field_34560");
        
                BitStorage = Reflection.GetField(Data, "comp_118");
                Palette = Reflection.GetField(Data, "comp_119");
        
                BaseY = Key * 16 - 63;
        
                for Step in range(4096): # BitStorage.getSize() or (16 ^ 3)
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
