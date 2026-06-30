# URP in Unity 6

## Pipeline Version
- URP 17.x
- RenderGraph API: enabled by default
- ShaderGraph 17.x

## New Features (Compared to 2022.3)
- **GPU Resident Drawer**: Reduces CPU overhead by batching draw calls on GPU
- **Adaptive Probe Volumes**: Replaces Light Probe Groups with automatic placement and blending (GI)
- **Render Graph**: Default rendering framework, automatic resource management and barrier insertion
- **Improved Shader Stripping**: Better build size and compilation time
- **STP Upscaling**: Spatial-Temporal Post-processing for performance/quality trade-off
- **Foveated Rendering**: For XR applications

## Changed Behaviour
- Render Graph handles render textures lifecycle — don't manually create/release in Renderer Features
- Shader dependencies auto-resolved by Render Graph
- Some 2022.3 Renderer Features are incompatible with Render Graph (must use RenderGraph-based passes)

## Common Unity 6 Patterns
```csharp
// RenderGraph-based Renderer Feature (new API)
class BlitRenderPass : ScriptableRenderPass {
    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData) {
        // Use RenderGraph API instead of CommandBuffer
    }
}
```

## Upgrading from 2022.3
- Back up URP Asset before upgrading
- Custom Renderer Features: rewrite using RecordRenderGraph if they use CommandBuffer directly
- Adaptive Probe Volumes require scene re-baking
- Check all shaders for compatibility (ShaderGraph auto-upgrades, hand-written shaders may need updates)
- GPU Resident Drawer disabled by default — enable in URP Asset for CPU gains

## Still Unchanged from 2022.3
- Camera Stacking
- Forward/Forward+/Deferred paths
- 2D Renderer
- Post-processing Volume framework
- Decal system
- Reflection Probes
