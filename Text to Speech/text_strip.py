def check_for_template(context):
    _scene = context.scene
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor
    for strip in seq.sequences_all:
        if strip.name == "Template_strip":
            return strip
    return False

def text_strip(context, text, start_frame, end_frame, strip_channel, template_strip):
    _scene = context.scene
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor
    new_strip = seq.sequences.new_effect(
        name=text,
        type='TEXT',
        frame_start=start_frame,
        frame_end=end_frame,
        channel=strip_channel)

    new_strip.text = text

    if template_strip:
        new_strip.location = template_strip.location
        new_strip.align_x = template_strip.align_x
        new_strip.align_y = template_strip.align_y
        new_strip.alpha_mode = template_strip.alpha_mode
        new_strip.blend_alpha = template_strip.blend_alpha
        new_strip.blend_type = template_strip.blend_type
        new_strip.use_box = template_strip.use_box
        new_strip.box_color = template_strip.box_color
        new_strip.box_margin = template_strip.box_margin
        new_strip.color = template_strip.color
        new_strip.color_multiply = template_strip.color_multiply
        new_strip.color_saturation = template_strip.color_saturation
        new_strip.color_tag = template_strip.color_tag
        new_strip.effect_fader = template_strip.effect_fader
        new_strip.font = template_strip.font
        new_strip.font_size = template_strip.font_size
        new_strip.shadow_color = template_strip.shadow_color
        new_strip.use_bold = template_strip.use_bold
        new_strip.use_cache_composite = template_strip.use_cache_composite
        new_strip.use_cache_preprocessed = template_strip.use_cache_preprocessed
        new_strip.use_cache_raw = template_strip.use_cache_raw
        new_strip.use_default_fade = template_strip.use_default_fade
        new_strip.use_deinterlace = template_strip.use_deinterlace
        new_strip.use_flip_x = template_strip.use_flip_x
        new_strip.use_flip_y = template_strip.use_flip_y
        new_strip.use_float = template_strip.use_float
        new_strip.use_italic = template_strip.use_italic
        new_strip.use_linear_modifiers = template_strip.use_linear_modifiers
        new_strip.use_proxy = template_strip.use_proxy
        new_strip.use_reverse_frames = template_strip.use_reverse_frames
        new_strip.use_shadow = template_strip.use_shadow
        new_strip.wrap_width = template_strip.wrap_width

    return new_strip