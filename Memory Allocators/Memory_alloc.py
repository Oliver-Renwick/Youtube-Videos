from manim import *
import random


def mark_blocks_as_wasted(self, blocks):
    animations = [block.animate.set_fill(GREY, opacity=0.5) for block in blocks]
    self.play(*animations, run_time=0.6)


def allocate_memory_from_subsystems_no_animation(self, selected_subsystems, memory_rect):
    memory_blocks = []
    memory_height = memory_rect.height
    memory_width = memory_rect.width
    memory_left = memory_rect.get_left()

    print(len(selected_subsystems))

    offset = 0.0

    for i, subsystem in enumerate(selected_subsystems):
        color = subsystem["color"]
        name = subsystem["name"]
        top_pos = subsystem["top"]

        #make rectangle
        rand = random.uniform(0.01, 0.03)
        frag_off = random.uniform(0.05, 0.09)
        block_width = memory_width * rand
        memory_block = Rectangle(width=block_width,height=memory_height, fill_color=color, fill_opacity=0.8, stroke_width=0)
        memory_block.move_to(memory_left + RIGHT * (offset + block_width / 2) + RIGHT * frag_off)
        print(name)

        # Arrow from subsystem to memory

        memory_blocks.append({
            "name": name,
            "color": color,
            "width": block_width,
            "block": memory_block,
            "start_offset": offset
        })

        offset += block_width + frag_off

    return memory_blocks
    

def allocate_memory_from_subsystems(self, selected_subsystems, memory_rect):
    memory_blocks = []
    memory_height = memory_rect.height
    memory_width = memory_rect.width
    memory_left = memory_rect.get_left()

    print(len(selected_subsystems))

    offset = 0.0

    for i, subsystem in enumerate(selected_subsystems):
        color = subsystem["color"]
        name = subsystem["name"]
        top_pos = subsystem["top"]

        #make rectangle
        rand = random.uniform(0.01, 0.03)
        frag_off = random.uniform(0.05, 0.09)
        block_width = memory_width * rand
        memory_block = Rectangle(width=block_width,height=memory_height, fill_color=color, fill_opacity=0.8, stroke_width=0)
        memory_block.move_to(memory_left + RIGHT * (offset + block_width / 2) + RIGHT * frag_off)
        print(name)

        # Arrow from subsystem to memory
        arrow = Arrow(start=top_pos, end=memory_rect.get_bottom(), buff=0.1, color=color, stroke_width=3)
        self.play(GrowArrow(arrow), run_time=0.1)
        self.play(FadeIn(memory_block), run_time=.1)
        self.remove(arrow)

        memory_blocks.append({
            "name": name,
            "color": color,
            "width": block_width,
            "block": memory_block,
            "start_offset": offset
        })

        offset += block_width + frag_off

    return memory_blocks


def fade_out_all_except_five(self, block_list, num):
    if len(block_list) > num:
        keep_blocks = random.sample(block_list, num)
        fade_blocks = [block for block in block_list if block not in keep_blocks]
    else:
        return block_list

    animations = [FadeOut(block) for block in fade_blocks]
    self.play(*animations, run_time=0.6)

    return keep_blocks

class GhostEngineIntro(Scene):
    def construct(self):
        # Load and position image
        ghost_logo = ImageMobject("channels4_profile.jpg")
        ghost_logo.scale(0.75)
        ghost_logo.to_edge(LEFT)
        ghost_logo.shift(LEFT * 4)  # Start offscreen

        # Create the text
        ghost_text = Text(
            "Ghost Engine",
            font="Times New Roman",
            color=RED,
            font_size=72
        )
        #ghost_text.next_to(ghost_logo, RIGHT, buff=1)
        ghost_text.shift(RIGHT)
        # Animate both image sliding in and text being written
        self.play(
            ghost_logo.animate.shift(RIGHT * 6),
            run_time=1,
            rate_func=smooth
        )
        self.play(
             Write(ghost_text),
            run_time=1.5,
            rate_func=smooth
        )

        self.wait(1)

        self.play(
            FadeOut(ghost_logo),
            FadeOut(ghost_text),
            run_time=0.8
        )


def create_glow(rect, color=YELLOW, layers=10, spread=0.02, opacity=0.2):
        glow_group = VGroup()
        for i in range(1, layers + 1):
            glow_layer = rect.copy()
            glow_layer.set_fill(color, opacity / i)
            glow_layer.set_stroke(width=0)
            glow_layer.scale(1 + spread * i)
            glow_group.add(glow_layer)
        return glow_group
        
        


class WhyCustomAllocator(Scene):
    
    def construct(self):
               # Heading for next section
        heading = Text(
            "Why we need custom allocators",
            font="Times New Roman",
            color=RED,
            font_size=80
        )
        heading.move_to(ORIGIN)

        # Fade in the heading
        self.play(Write(heading), run_time=1.5)
        self.wait(1)

        self.play(heading.animate.shift(UP * 3).scale(0.6), run_time = 0.5)
        
        line = Line(
            heading.get_left() + DOWN * 0.4,
            heading.get_right() + DOWN * 0.4,
            color = WHITE,
            stroke_width = 4.0
        )

        self.play(Create(line), run_time = 0.5 )
        self.wait(0.5)


        # Memory BOX

        malloc_tex = Text("malloc()", font="Times New Roman", font_size= 45, color=WHITE)
        self.play(FadeIn(malloc_tex), run_time=1.7)
        self.play(FadeOut(malloc_tex), run_time=1.0)

        rectangle = Rectangle(width = 2, height = 4, color = BLUE)
        rectangle.shift(DOWN * 0.5)

        mem_label = Text("Memory", font= "Times New Roman", color= WHITE, font_size=20)
        mem_label.next_to(rectangle, DOWN, buff=0.2)

        #creation
        alloc1b = Rectangle(width= 2, height = 0.1, fill_color= GREEN, fill_opacity = 0.7, stroke_width=1 )
        alloc2mb = Rectangle(width= 2, height = 0.6, fill_color= YELLOW, fill_opacity = 0.7, stroke_width=1 )
        alloc4gb = Rectangle(width= 2, height = 1.2, fill_color= RED, fill_opacity = 0.7, stroke_width=1 )

        #move
        alloc1b.move_to(rectangle.get_bottom() + UP * 0.5)
        alloc2mb.move_to(rectangle.get_bottom() + UP * 1.5)
        alloc4gb.move_to(rectangle.get_bottom() + UP * 3.0)

        #arrow
        arrow1     = Arrow(start = alloc1b.get_left(), end= alloc1b.get_left() + LEFT * 1.5, buff=0.1, color = GREEN)
        arrowlabel1 = Text("1 B", font= "Times New Roman", font_size=24, color=WHITE, ).next_to(arrow1, LEFT)

        arrow2     = Arrow(start = alloc2mb.get_left(), end= alloc2mb.get_left() + LEFT * 1.5, buff=0.1, color = YELLOW)
        arrowlabel2 = Text("2 MB", font= "Times New Roman", font_size=24, color=WHITE, ).next_to(arrow2, LEFT)

        arrow3     = Arrow(start = alloc4gb.get_left(), end= alloc4gb.get_left() + LEFT * 1.5, buff=0.1, color = RED)
        arrowlabel3 = Text("4 GB", font= "Times New Roman", font_size=24, color=WHITE, ).next_to(arrow3, LEFT)

        #draw
        self.play(FadeIn(rectangle), runtime = 1.0)
        self.play(Write(mem_label), run_time=0.8)

        self.play(FadeIn(alloc1b),  run_time= 1.0)
        self.play(FadeIn(alloc2mb), run_time= 1.0)
        self.play(FadeIn(alloc4gb), run_time= 1.0)

        self.play(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3) , run_time = 0.5)
        self.play(Write(arrowlabel1), Write(arrowlabel2), Write(arrowlabel3), run_time = 0.5)

        self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3) , FadeOut(arrowlabel1), FadeOut(arrowlabel2), FadeOut(arrowlabel3),  run_time = 1.5)

        self.wait(3)

        #glowing BOX
        alloc1b_glow  = create_glow(alloc1b,  color=GREEN)
        alloc2mb_glow = create_glow(alloc2mb, color=YELLOW)
        alloc4gb_glow = create_glow(alloc4gb, color=RED)


        self.bring_to_back(alloc2mb_glow)
        self.bring_to_back(alloc1b_glow)
        self.bring_to_back(alloc4gb_glow)
        self.play(FadeIn(alloc2mb_glow),FadeIn(alloc1b_glow), FadeIn(alloc4gb_glow) , run_time=1.0)

        self.play(FadeOut(alloc2mb_glow),FadeOut(alloc1b_glow), FadeOut(alloc4gb_glow) , run_time=1.0)

        #Fragmentation Showcase
        frag_arrow1 = Arrow(end = alloc1b.get_right() + DOWN * 0.3, start= alloc1b.get_right() + RIGHT * 1.5 + DOWN * 0.3, buff=0.1, color = WHITE)
        frag_arrow2 = Arrow(end = alloc1b.get_left() + UP * 0.3,    start= alloc1b.get_left() + LEFT * 1.5 + UP * 0.3, buff=0.1, color = WHITE)
        frag_arrow3 = Arrow(end = alloc1b.get_right() + UP * 1.5,   start= alloc1b.get_right() + RIGHT * 1.5 + UP * 1.5, buff=0.1, color = WHITE)
        frag_arrow4 = Arrow(end = alloc1b.get_left() + UP * 3.3,    start= alloc1b.get_left() + LEFT * 1.5 + UP * 3.3, buff=0.1, color = WHITE)

        free_label1 = Text("Fragmented", font = "TIMES NEW ROMAN", font_size=20, color=WHITE).next_to(frag_arrow1,RIGHT)
        free_label2 = Text("Fragmented", font = "TIMES NEW ROMAN", font_size=20, color=WHITE).next_to(frag_arrow2,LEFT)
        free_label3 = Text("Fragmented", font = "TIMES NEW ROMAN", font_size=20, color=WHITE).next_to(frag_arrow3,RIGHT)
        free_label4 = Text("Fragmented", font = "TIMES NEW ROMAN", font_size=20, color=WHITE).next_to(frag_arrow4,LEFT)

        self.play(GrowArrow(frag_arrow1),GrowArrow(frag_arrow2), GrowArrow(frag_arrow3), GrowArrow(frag_arrow4), run_time=0.5)
        self.play(Write(free_label1), Write(free_label2), Write(free_label3), Write(free_label4),run_time=1.0)
        self.play(FadeOut(frag_arrow1),FadeOut(frag_arrow2), FadeOut(frag_arrow3), FadeOut(frag_arrow4), FadeOut(free_label1), FadeOut(free_label2), FadeOut(free_label3), FadeOut(free_label4),run_time=0.5)


        #overlaps
        alloc_bad = Rectangle(width= 2, height = 1.0, fill_color= BLUE, fill_opacity = 0.7, stroke_width=1 )
        alloc_bad.move_to(alloc2mb.get_bottom() + UP * 0.5 )
        self.play(FadeIn(alloc_bad), run_time = 1.0)  # Briefly show overlapping
        cross = Cross(alloc_bad)
        self.play(Write(cross), run_time = 1.0) 
        self.play(FadeOut(alloc_bad), FadeOut(cross), run_time = 1.0)

        self.play(FadeOut(mem_label), FadeOut(alloc1b), FadeOut(alloc2mb), FadeOut(alloc4gb), FadeOut(rectangle), FadeOut(line), FadeOut(heading), run_time=1.0)

        self.wait(1)

    

class ProblemOfDynamicAllocation(Scene):
     def construct(self):
          
          rendering = Square(color=BLUE)
          physics   = Square(color=RED)
          ai        = Square(color= LIGHT_BROWN)
          audio     = Square(color=PINK)

          rendering_label   = Text("Rendering", font="Times New Roman", font_size=24)
          physics_label     = Text("Physics", font="Times New Roman", font_size=24)
          ai_label          = Text("AI", font="Times New Roman", font_size=24)
          audio_label       = Text("Audio", font="Times New Roman", font_size=24)

          rendering.shift(LEFT * 4.5)
          physics.move_to(rendering.get_right() + RIGHT * 2)
          ai.shift(rendering.get_right() + RIGHT * 5)
          audio.shift(rendering.get_right() + RIGHT * 8)

          rendering_label.move_to(rendering.get_center())
          physics_label.move_to(physics.get_center())
          ai_label.move_to(ai.get_center())
          audio_label.move_to(audio.get_center())

          self.play(FadeIn(rendering), Write(rendering_label), run_time= 1.0)
          self.play(FadeIn(physics), Write(physics_label), run_time= 1.0)
          self.play(FadeIn(ai),Write(ai_label), run_time= 1.0)
          self.play(FadeIn(audio), Write(audio_label), run_time= 1.0)

          self.wait(1)

          self.play(rendering.animate.shift(DOWN * 2), physics.animate.shift(DOWN * 2), ai.animate.shift(DOWN * 2), audio.animate.shift(DOWN * 2),
                    rendering_label.animate.shift(DOWN * 2), physics_label.animate.shift(DOWN * 2), ai_label.animate.shift(DOWN * 2), audio_label.animate.shift(DOWN * 2),
                      run_time=1.0 )
          

          memory = Rectangle(width=8, height= 2, color= BLUE)
          memory.shift(UP*1.5)

          memory_label = Text("Memory", font="Times New Roman", color=WHITE, font_size=20)
          memory_label.next_to(memory, UP, buff=0.2)

          self.play(Create(memory), Write(memory_label), run_time=1.0)

          #memory Creation

          system = [
               {"name": "Rendering", "color": BLUE,        "top": rendering.get_top()},
               {"name": "Physics",   "color": RED,         "top": physics.get_top()},
               {"name": "AI",        "color": LIGHT_BROWN, "top": ai.get_top()},
               {"name": "Audio",     "color": PINK,        "top": audio.get_top()}
          ]

          weights = [5, 3, 2, 3]
          selected_subsystems = random.choices(system, weights=weights, k=30)

          memory_blocks = allocate_memory_from_subsystems(self, selected_subsystems, memory)
          self.wait(1)

          renderer_block = [block_info["block"] for block_info in memory_blocks if block_info["color"] in [BLUE]]
          physics_block  = [block_info["block"] for block_info in memory_blocks if block_info["color"] in [RED]]
          ai_block       = [block_info["block"] for block_info in memory_blocks if block_info["color"] in [LIGHT_BROWN]]
          audio_block    = [block_info["block"] for block_info in memory_blocks if block_info["color"] in [PINK]]

          remaining_block = []

          arrow_1 = Arrow(start=rendering.get_top(), end=memory.get_bottom(), buff=0.1, color=WHITE, stroke_width=3)
          free_label = Text("Free", font_size=20, color=WHITE)
          free_label.move_to(arrow_1.get_center() + UP * 0.3) 
          self.play(GrowArrow(arrow_1), FadeIn(free_label), run_time=0.7)
          renderer_kept = fade_out_all_except_five(self, renderer_block, 5)
          self.play(FadeOut(arrow_1), FadeOut(free_label), run_time=0.2)

          arrow_2 = Arrow(start=physics.get_top(), end=memory.get_bottom(), buff=0.1, color=WHITE, stroke_width=3)
          free_label.move_to(arrow_2.get_center() + UP * 0.3 + LEFT * 0.3)
          self.play(GrowArrow(arrow_2), FadeIn(free_label) ,run_time=0.7)
          physics_kept = fade_out_all_except_five(self, physics_block, 3)
          self.play(FadeOut(arrow_2), FadeOut(free_label), run_time=0.2)

          arrow_3 = Arrow(start=ai.get_top(), end=memory.get_bottom(), buff=0.1, color=WHITE, stroke_width=3)
          free_label.move_to(arrow_3.get_center() + UP * 0.3 + RIGHT * 0.3)
          self.play(GrowArrow(arrow_3), FadeIn(free_label), run_time=0.7)
          ai_kept = fade_out_all_except_five(self, ai_block, 1)
          self.play(FadeOut(arrow_3), FadeOut(free_label), run_time=0.2)

          arrow_4 = Arrow(start=audio.get_top(), end=memory.get_bottom(), buff=0.1, color=WHITE, stroke_width=3)
          free_label.move_to(arrow_4.get_center() + UP * 0.3)
          self.play(GrowArrow(arrow_4), FadeIn(free_label), run_time=0.7)
          audio_kept = fade_out_all_except_five(self, audio_block, 2)
          self.play(FadeOut(arrow_4), FadeOut(free_label), run_time=0.2)
          
          self.wait(1)

          remaining_block.extend(renderer_kept)
          remaining_block.extend(physics_kept)
          remaining_block.extend(ai_kept)
          remaining_block.extend(audio_kept)

          self.play(FadeOut(rendering), FadeOut(physics), FadeOut(audio), FadeOut(ai),
                    FadeOut(rendering_label), FadeOut(physics_label), FadeOut(audio_label), FadeOut(ai_label), run_time= 1.0)
          
          mark_blocks_as_wasted(self, remaining_block)

          self.wait(1)

          wasted_memory = Text("Wasted Memory", font= "Times New Roman", font_size=50, color=WHITE)
          wasted_memory.shift(memory.get_bottom() + DOWN)
          self.play(Write(wasted_memory), run_time= 1.0)
          
          
          self.wait(1)

          self.play(FadeOut(memory),FadeOut(memory_label),FadeOut(wasted_memory), *[FadeOut(block) for block in remaining_block], run_time =1.0)

          
class MemoryArena(Scene):
    def construct(self):
        memoryarena_label = Text("Memory Arena", font= "Times New Roman", font_size=80, color=ORANGE)

        self.play(Write(memoryarena_label), run_time=1.0)

        self.wait(1)

        self.play(FadeOut(memoryarena_label), run_time = 1.0)

        self.wait(1)

        memory = Rectangle(width=8, height= 2, color= BLUE)
        memory.shift(UP*1.5)

        memory_label = Text("Memory", font="Times New Roman", color=WHITE, font_size=20)
        memory_label.next_to(memory, UP, buff=0.2)

        #self.play(Create(memory), Write(memory_label), run_time=1.0) 


        rendering = Square(color=BLUE)
        physics   = Square(color=RED)
        ai        = Square(color= LIGHT_BROWN)
        audio     = Square(color=PINK)
        rendering_label   = Text("Rendering", font="Times New Roman", font_size=24)
        physics_label     = Text("Physics", font="Times New Roman", font_size=24)
        ai_label          = Text("AI", font="Times New Roman", font_size=24)
        audio_label       = Text("Audio", font="Times New Roman", font_size=24)
        rendering.shift(LEFT * 4.5 + DOWN * 2)
        physics.move_to(rendering.get_right() + RIGHT * 2 )
        ai.shift(rendering.get_right() + RIGHT * 5 )
        audio.shift(rendering.get_right() + RIGHT * 8 )
        rendering_label.move_to(rendering.get_center() )
        physics_label.move_to(physics.get_center() )
        ai_label.move_to(ai.get_center() )
        audio_label.move_to(audio.get_center() )

        self.play(Create(memory), Write(memory_label), FadeIn(rendering), Write(rendering_label), FadeIn(physics), Write(physics_label), 
                  FadeIn(ai),Write(ai_label), FadeIn(audio), Write(audio_label),  run_time= 1.0)
        self.wait(1)

        system = [
               {"name": "Rendering", "color": BLUE,        "top": rendering.get_top()},
               {"name": "Physics",   "color": RED,         "top": physics.get_top()},
               {"name": "AI",        "color": LIGHT_BROWN, "top": ai.get_top()},
               {"name": "Audio",     "color": PINK,        "top": audio.get_top()}
          ]

        weights = [5, 3, 2, 3]
        selected_subsystems = random.choices(system, weights=weights, k=30)

        memory_blocks = allocate_memory_from_subsystems_no_animation(self, selected_subsystems, memory)

        blocks = [block_info["block"] for block_info in memory_blocks]


        # Play the fade-in animation on all of them together
        self.play(*[FadeIn(block) for block in blocks], run_time=1.0)

        # note to say i huge code base the individual allocations would be 100 - 1000
        alloc_label = Text("In real projects, these would be 100s or 1000s of allocations.", font="Times New Roman", font_size=24, color=WHITE)
        alloc_label.move_to(memory.get_bottom() + DOWN * 0.5)

        self.play(FadeIn(alloc_label), run_time=1.0)

        self.wait(1)
        self.play(*[FadeOut(block) for block in blocks], FadeOut(alloc_label), run_time=1.0)

        self.wait(1)

        neutral_fill = Rectangle(
        width=memory.width,
        height=memory.height,
        fill_color=GREEN,
        fill_opacity=0.8,
        stroke_width=0
        ).move_to(memory.get_center())

        #alloc text
        alloc_call_text = Text('arena->alloc(SIZE);', font="Courier New", font_size=28, color=WHITE)
        alloc_call_text.move_to(memory.get_bottom() + DOWN * 0.6)

        self.play(Write(alloc_call_text, rate_func=linear), run_time=1.0)

        self.play(FadeIn(neutral_fill), run_time = 1.0)
        
        self.wait(1)
        
        self.play(FadeOut(alloc_call_text), run_time=1.0)

        #alocating memory 
        rendering_memory = Rectangle(height = memory.height, width= memory.width * 0.4, fill_color=BLUE, fill_opacity=0.8)
        physics_memory = Rectangle(height=memory.height, width=memory.width * 0.3, fill_color=RED, fill_opacity=0.8)
        ai_memory = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=LIGHT_BROWN, fill_opacity=0.8)
        audio_memory = Rectangle(height=memory.height, width = memory.width * 0.2, fill_color=PINK, fill_opacity=0.8)

        rendering_memory.move_to(memory.get_left() + RIGHT * (rendering_memory.width / 2.0))
        physics_memory.move_to(rendering_memory.get_right() + RIGHT * (physics_memory.width / 2.0))
        ai_memory.move_to(physics_memory.get_right() + RIGHT * (ai_memory.width/2.0))
        audio_memory.move_to(ai_memory.get_right() + RIGHT * (audio_memory.width / 2.0))

        #arrows

        arrow1 = Arrow(start = rendering_memory.get_bottom(), end=rendering.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow2 = Arrow(start = physics_memory.get_bottom(),   end=physics.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow3 = Arrow(start = ai_memory.get_bottom(), end=ai.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow4 = Arrow(start = audio_memory.get_bottom(), end=audio.get_top(), buff=0.1, color=WHITE, stroke_width=3) 

        self.play(FadeIn(rendering_memory), GrowArrow(arrow1), run_time=1.0)
        self.play(FadeIn(physics_memory), GrowArrow(arrow2), run_time = 1.0)
        self.play(FadeIn(ai_memory), GrowArrow(arrow3), run_time = 1.0)
        self.play(FadeIn(audio_memory), GrowArrow(arrow4), run_time = 1.0)

        self.play(FadeOut(rendering), FadeOut(rendering_label),
                  FadeOut(physics), FadeOut(physics_label),
                  FadeOut(ai), FadeOut(ai_label),
                  FadeOut(audio), FadeOut(audio_label),FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(arrow4),
                  run_time = 1.0)
        
        
        self.play(memory.animate.shift(DOWN*1.5),
                  rendering_memory.animate.shift(DOWN * 1.5),
                  physics_memory.animate.shift(DOWN * 1.5),
                  ai_memory.animate.shift(DOWN * 1.5), 
                  audio_memory.animate.shift(DOWN * 1.5),
                  neutral_fill.animate.shift(DOWN * 1.5),
                  memory_label.animate.shift(DOWN * 1.5), 
                  run_time = 1.0)

        #Free Label
        free_label = Text("alloc->free()", font= "Courier New", font_size=32, color=WHITE)
        free_label.move_to(memory.get_bottom() + DOWN * 0.6)
        self.play(Write(free_label, rate_func=linear), run_time=1.0) 

        self.wait(1)

        self.play(FadeOut(rendering_memory), FadeOut(physics_memory), FadeOut(ai_memory), FadeOut(audio_memory), FadeOut(neutral_fill), run_time=1.0)
        self.wait(1)



        final_text = VGroup(
        Text('// Just one malloc() for the arena...', font="Courier New", font_size=28),
        Text('// And one free() when we’re done.', font="Courier New", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)

        self.play(Write(final_text), run_time=1.5)

        self.wait(2)

        self.play(FadeOut(final_text),FadeOut(free_label), FadeOut(memory), FadeOut(memory_label), run_time=1.0)



class MemoryAllocators(Scene):
    def construct(self):

        memory_allocators = Text("Memory Allocators", font= "Times New Roman", font_size=80, color=BLUE)
        self.play(Write(memory_allocators), runtime=0.5)
        self.play(memory_allocators.animate.shift(UP * 3).scale(0.6), run_time = 0.5)

        line = Line(
            memory_allocators.get_left() + DOWN * 0.4,
            memory_allocators.get_right() + DOWN * 0.4,
            color = WHITE,
            stroke_width = 4.0
        )

        self.play(Create(line), run_time = 0.5 )
        self.wait(0.5)

        # Allocator bullet points
        linear_allocator = Text("Linear Allocator", font="Times New Roman", font_size=30, color=WHITE)
        stack_allocator = Text("Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        double_stack_allocator = Text("Double Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        pool_allocator = Text("Pool Allocator", font="Times New Roman", font_size=30, color=WHITE)

        # Position them
        linear_allocator.next_to(line, DOWN, buff=0.6)
        stack_allocator.next_to(linear_allocator, DOWN * 2.5, aligned_edge=LEFT, buff=0.4)
        double_stack_allocator.next_to(stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)
        pool_allocator.next_to(double_stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)

        self.play(FadeIn(linear_allocator), FadeIn(stack_allocator), FadeIn(pool_allocator), FadeIn(double_stack_allocator), run_time=0.4)

        self.wait(1)

        self.play(FadeOut(line), FadeOut(memory_allocators), FadeOut(stack_allocator), FadeOut(double_stack_allocator), FadeOut(pool_allocator), run_time=0.7)
        self.play(linear_allocator.animate.move_to(ORIGIN).scale(2), run_time=0.3)

        self.wait(1)

        self.play(FadeOut(linear_allocator), run_time=1.0)
        
        self.wait(1)
        


class LinearAllocator(Scene):
    def construct(self):

        memory = Rectangle(width=8, height= 2, color= BLUE)
        memory.shift(UP*1.5)

        memory_label = Text("Linear Allocator", font="Times New Roman", color=WHITE, font_size=20)
        memory_label.next_to(memory, UP * 2, buff=0.2)

        self.play(Create(memory), Write(memory_label), run_time=1.0)
        self.wait(1)
        
        init = Text("void init(size_t size)", font="Courier New", font_size=28)

        self.play(Write(init), run_time=1.0)
        self.wait(1)

        linear_memory  = Rectangle(height=memory.height, width=memory.width, fill_color=GREEN, fill_opacity=0.8)
        linear_memory.move_to(memory.get_center())

        self.play(FadeIn(linear_memory), run_time=1.0)
        self.wait(1)
        memory_pointer = Text("uint8_t* memory", font="Courier New", font_size=28) 
        memory_pointer.move_to(init.get_center())
        
        self.play(Transform(init, memory_pointer))
        self.wait(1.0)
        self.play(FadeOut(memory_pointer), FadeOut(init), run_time = 1.0)
        self.wait(1)

        alloc = Text("void* allocate(size_t size, size_t alignment) ", font="Courier New", font_size=28)
        alloc.shift(DOWN * 1.5)

        self.play(Write(alloc), run_time=1.0)
        self.wait(1)


        #allocating memory
        first_alloc = Rectangle(height=memory.height, width=memory.width * 0.3, fill_color=BLUE, fill_opacity=0.8)
        first_alloc.move_to(memory.get_left() + RIGHT * (first_alloc.width * 0.5))

        arrow1 = Arrow(start = first_alloc.get_corner(DL), end = first_alloc.get_corner(DL) + DOWN ,  buff=0.1, color=BLUE, stroke_width=3)
        first_alloc_memory = Text("*ptr1", font="Times New Roman", font_size=20, color=BLUE)
        first_alloc_memory.move_to(arrow1.end)

        self.play(FadeIn(first_alloc), run_time=1.0)
        self.wait(1)
        self.play(GrowArrow(arrow1), run_time=1.0)
        self.wait(1)
        self.play(Write(first_alloc_memory), run_time=1.0)
        self.wait(1)

        #second alloc

        alloc_2 = Text("void* allocate(size_t new_size, size_t new_alignment) ", font="Courier New", font_size=28)
        alloc_2.shift(DOWN * 2.0)

        self.play(Write(alloc_2), run_time=1.0)
        self.wait(1)

        second_alloc = Rectangle(height=memory.height, width=memory.width * 0.4, fill_color=RED, fill_opacity=0.8)
        second_alloc.move_to(first_alloc.get_right() + RIGHT * (second_alloc.width * 0.5))

        arrow2 = Arrow(start = second_alloc.get_corner(DL), end = second_alloc.get_corner(DL) + DOWN ,  buff=0.1, color=RED, stroke_width=3)
        second_alloc_memory = Text("*ptr2", font="Times New Roman", font_size=20, color=RED)
        second_alloc_memory.move_to(arrow2.end)

        self.play(FadeIn(second_alloc), run_time=1.0)
        self.wait(1)
        self.play(GrowArrow(arrow2), run_time=1.0)
        self.wait(1)
        self.play(Write(second_alloc_memory), run_time=1.0)
        self.wait(1)

        self.play(FadeOut(second_alloc_memory),FadeOut(first_alloc_memory), FadeOut(arrow1), FadeOut(arrow2), FadeOut(alloc), FadeOut(alloc_2), run_time=1.0)
        self.wait(1)

        self.play(memory.animate.move_to(ORIGIN), 
                  memory_label.animate.move_to(ORIGIN +  UP * 1.5),
                  first_alloc.animate.move_to(memory.get_left() + RIGHT * (first_alloc.width * 0.5) + DOWN*1.5),
                  second_alloc.animate.move_to(first_alloc.get_right() + RIGHT * (second_alloc.width * 0.5) + DOWN*1.5),
                  linear_memory.animate.move_to(ORIGIN),
                  run_time=1.0
                  )
        self.wait(1)
        
        shutdown_text = Text("void shutdown()", font="Courier New", font_size=28)
        shutdown_text.move_to(DOWN*1.5)

        self.play(Write(shutdown_text), run_time=1.0)
        self.wait(1)
        self.play(FadeOut(first_alloc),FadeOut(linear_memory), FadeOut(second_alloc), run_time=1.0)
        self.wait(1)


class StackAllocator_INTRO(Scene):
    def construct(self):
        
        memory_allocators = Text("Memory Allocators", font= "Times New Roman", font_size=80, color=BLUE)
        memory_allocators.shift(UP * 3).scale(0.6)


        line = Line(
            memory_allocators.get_left() + DOWN * 0.4,
            memory_allocators.get_right() + DOWN * 0.4,
            color = WHITE,
            stroke_width = 4.0
        )


        linear_allocator = Text("Linear Allocator", font="Times New Roman", font_size=30, color=WHITE)
        stack_allocator = Text("Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        double_stack_allocator = Text("Double Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        pool_allocator = Text("Pool Allocator", font="Times New Roman", font_size=30, color=WHITE)

        # Position them
        linear_allocator.next_to(line, DOWN, buff=0.6)
        stack_allocator.next_to(linear_allocator, DOWN * 2.5, aligned_edge=LEFT, buff=0.4)
        double_stack_allocator.next_to(stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)
        pool_allocator.next_to(double_stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)

        self.play( Write(memory_allocators),Create(line), FadeIn(linear_allocator), FadeIn(stack_allocator), FadeIn(pool_allocator), FadeIn(double_stack_allocator), run_time=1.0)

        self.wait(1)

        self.play(FadeOut(line), FadeOut(memory_allocators), FadeOut(linear_allocator), FadeOut(double_stack_allocator), FadeOut(pool_allocator), run_time=0.7)
        self.play(stack_allocator.animate.move_to(ORIGIN).scale(2), run_time=0.3)

        self.wait(1)

        self.play(FadeOut(stack_allocator), run_time=1.0)
        self.wait(1)



class StackAllocator(Scene):
    def construct(self):
            memory = Rectangle(width=8, height= 2, color= BLUE)
            memory.shift(UP)
            self.play(Create(memory), run_time=1.0)

            init_label = Text("void init(size_t size)", font="Courier New", font_size=28).shift(memory.get_bottom() + DOWN * 0.5)
            init_memory = Rectangle(height=memory.height, width=memory.width, fill_color=GREEN, fill_opacity=0.8).shift(memory.get_center())

            self.play(Write(init_label), run_time=1.0)
            self.play(FadeIn(init_memory), run_time=1.0)
            self.play(FadeOut(init_label), run_time=1.0)

            #alloc 1
            alloc1_label = Text("void* allocate(size_t size, size_t alignment)", font="Courier New", font_size=28)
            alloc1_label.move_to(memory.get_bottom() + DOWN)
            alloc_1 = Rectangle(height= memory.height, width= memory.width * 0.2, fill_color=RED, fill_opacity=0.8)
            alloc_1.move_to(memory.get_left() + RIGHT * alloc_1.width * 0.5)

            self.play(Write(alloc1_label), run_time=1.0)
            self.wait(1)
            self.play(FadeIn(alloc_1), run_time=1.0)
            self.wait(1)
            self.play(FadeOut(alloc1_label), run_time=1.0)

            #arrow for ptr1
            arrow1 = Arrow(start=alloc_1.get_corner(DL), end=alloc_1.get_corner(DL) + DOWN,  buff=0.1, color=RED, stroke_width=3)
            first_alloc_ptr = Text("*ptr1", font="Times New Roman", font_size=20,color=RED)
            first_alloc_ptr.move_to(arrow1.end)

            #arrow for current marker
            arrow2 = Arrow(start=alloc_1.get_corner(UR), end=alloc_1.get_corner(UR) + UP ,  buff=0.1, color=YELLOW, stroke_width=3)
            curr_marker = Text("curr", font="Times New Roman", font_size=22, color=YELLOW)
            curr_marker.move_to(arrow2.end)


            #ptr1 play
            self.play(GrowArrow(arrow1), run_time=1.0)
            self.play(Write(first_alloc_ptr), run_time=1.0)

            #curr_marker play
            self.play(GrowArrow(arrow2),run_time=1.0)
            self.play(Write(curr_marker), run_time=1.0)

            self.play(FadeOut(first_alloc_ptr), FadeOut(arrow1), run_time=1.0)


            #allocate new block
            temp_alloc_1 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
            temp_alloc_1.move_to(alloc_1.get_right() + RIGHT * (temp_alloc_1.width * 0.5))


            temp_alloc_2 = Rectangle(height=memory.height, width=memory.width * 0.2, fill_color=PINK, fill_opacity=0.8)
            temp_alloc_2.move_to(temp_alloc_1.get_right() + RIGHT * (temp_alloc_2.width * 0.5))


            temp_alloc_3 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=PURPLE, fill_opacity=0.8)
            temp_alloc_3.move_to(temp_alloc_2.get_right() + RIGHT * (temp_alloc_3.width * 0.5))


            temp_alloc_4 = Rectangle(height=memory.height, width=memory.width * 0.2, fill_color=DARK_BROWN, fill_opacity=0.8)
            temp_alloc_4.move_to(temp_alloc_3.get_right() + RIGHT * (temp_alloc_4.width * 0.5))


            temp_alloc_5 = Rectangle(height=memory.height, width=memory.width * 0.2, fill_color=MAROON, fill_opacity=0.8)
            temp_alloc_5.move_to(temp_alloc_4.get_right() + RIGHT * (temp_alloc_5.width * 0.5))




            # Move the current marker to new allocation's right corner
            self.play(FadeIn(temp_alloc_1), run_time=1.0) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_1.width), curr_marker.animate.shift(RIGHT * temp_alloc_1.width), run_time=1.0)
    
            self.play(FadeIn(temp_alloc_2), run_time=1.0) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_2.width), curr_marker.animate.shift(RIGHT * temp_alloc_2.width), run_time=1.0)

            self.play(FadeIn(temp_alloc_3), run_time=1.0) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_3.width), curr_marker.animate.shift(RIGHT * temp_alloc_3.width), run_time=1.0)
    
            self.play(FadeIn(temp_alloc_4), run_time=1.0) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_4.width), curr_marker.animate.shift(RIGHT * temp_alloc_4.width), run_time=1.0)

            self.play(FadeIn(temp_alloc_5), run_time=1.0) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_5.width), curr_marker.animate.shift(RIGHT * temp_alloc_5.width), run_time=1.0)


            #marker Position
            saved_marker_text = Text("size_t marker = stack->get_marker();", font="Courier New", font_size=28)
            deallocate_marker_text = Text("deallocate(marker);", font="Courier New", font_size=28)


            saved_marker_text.move_to(memory.get_bottom() + DOWN * 2)
            deallocate_marker_text.move_to(saved_marker_text.get_bottom()+ DOWN * 0.5)


            arrow3 = Arrow(start=alloc_1.get_corner(DR), end=alloc_1.get_corner(DR) + DOWN ,  buff=0.1, color=BLUE_B, stroke_width=3)
            saved_marker = Text("Marker", font="Times New Roman", font_size=22, color=BLUE_B)
            saved_marker.move_to(arrow3.end)

            self.play(Write(saved_marker_text), run_time=1.0)
            self.play(GrowArrow(arrow3), run_time=1.0)
            self.play(Write(saved_marker), run_time=1.0)


            self.play(Write(deallocate_marker_text), run_time=1.0)

            self.play(FadeOut(temp_alloc_1),FadeOut(temp_alloc_2),FadeOut(temp_alloc_3),FadeOut(temp_alloc_4),FadeOut(temp_alloc_5), run_time=1.0)


            self.play(arrow2.animate.shift(LEFT * memory.width * 0.8), curr_marker.animate.shift(LEFT * memory.width * 0.8), run_time=1.0)


            self.wait(1)

            # Move the current marker to new allocation's right corner
            self.play(FadeIn(temp_alloc_1), run_time=0.5) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_1.width), curr_marker.animate.shift(RIGHT * temp_alloc_1.width), run_time=0.5)
    
            self.play(FadeIn(temp_alloc_2), run_time=0.5) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_2.width), curr_marker.animate.shift(RIGHT * temp_alloc_2.width), run_time=0.5)

            self.play(FadeIn(temp_alloc_3), run_time=0.5) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_3.width), curr_marker.animate.shift(RIGHT * temp_alloc_3.width), run_time=0.5)
    
            self.play(FadeIn(temp_alloc_4), run_time=0.5) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_4.width), curr_marker.animate.shift(RIGHT * temp_alloc_4.width), run_time=0.5)

            self.play(FadeIn(temp_alloc_5), run_time=0.5) 
            self.play(arrow2.animate.shift(RIGHT * temp_alloc_5.width), curr_marker.animate.shift(RIGHT * temp_alloc_5.width), run_time=0.5)


            arrow4 = Arrow(start=temp_alloc_2.get_corner(DR), end=temp_alloc_2.get_corner(DR) + DOWN ,  buff=0.1, color=temp_alloc_2.color, stroke_width=3)
            saved_marker2 = Text("marker_2", font="Times New Roman", font_size=22, color=temp_alloc_2.color)
            saved_marker2.move_to(arrow4.end)


            #text for second animation
            saved_marker_text2 = Text("size_t marker_2 = stack->get_marker();", font="Courier New", font_size=28)
            deallocate_marker_text2 = Text("deallocate(marker_2);", font="Courier New", font_size=28)

            saved_marker_text2.move_to(saved_marker_text)
            deallocate_marker_text2.move_to(deallocate_marker_text)



            self.play(Transform(saved_marker_text, saved_marker_text2), run_time=0.5)

            self.play(GrowArrow(arrow4), Write(saved_marker2), run_time=1.0)


            self.play(Transform(deallocate_marker_text, deallocate_marker_text2), run_time=1.0)

            self.play(FadeOut(temp_alloc_3),FadeOut(temp_alloc_4),FadeOut(temp_alloc_5), run_time=0.5)

            self.play(arrow2.animate.shift(LEFT * memory.width * 0.5), curr_marker.animate.shift(LEFT * memory.width * 0.5), run_time=0.5)

            self.wait(1)


class DoubleStackAllocatorIntro(Scene):
    def construct(self):
        memory_allocators = Text("Memory Allocators", font= "Times New Roman", font_size=80, color=BLUE)
        memory_allocators.shift(UP * 3).scale(0.6)


        line = Line(
            memory_allocators.get_left() + DOWN * 0.4,
            memory_allocators.get_right() + DOWN * 0.4,
            color = WHITE,
            stroke_width = 4.0
        )


        linear_allocator = Text("Linear Allocator", font="Times New Roman", font_size=30, color=WHITE)
        stack_allocator = Text("Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        double_stack_allocator = Text("Double Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        pool_allocator = Text("Pool Allocator", font="Times New Roman", font_size=30, color=WHITE)

        # Position them
        linear_allocator.next_to(line, DOWN, buff=0.6)
        stack_allocator.next_to(linear_allocator, DOWN * 2.5, aligned_edge=LEFT, buff=0.4)
        double_stack_allocator.next_to(stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)
        pool_allocator.next_to(double_stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)

        self.play( Write(memory_allocators),Create(line), FadeIn(linear_allocator), FadeIn(stack_allocator), FadeIn(pool_allocator), FadeIn(double_stack_allocator), run_time=1.0)

        self.wait(1)

        self.play(FadeOut(line), FadeOut(memory_allocators), FadeOut(linear_allocator), FadeOut(stack_allocator), FadeOut(pool_allocator), run_time=0.7)
        self.play(double_stack_allocator.animate.move_to(ORIGIN).scale(2), run_time=0.3)

        self.wait(1)

        self.play(FadeOut(double_stack_allocator), run_time=1.0)
        self.wait(1)



class DoubleStackAllocator(Scene):
    def construct(self):
         memory = Rectangle(width=8, height= 2, color= BLUE)
         memory.shift(UP)
         self.play(Create(memory), run_time=1.0) 
         init_label = Text("void init(size_t size)", font="Courier New", font_size=28).shift(memory.get_bottom() + DOWN * 0.5)
         init_memory = Rectangle(height=memory.height, width=memory.width, fill_color=GREEN, fill_opacity=0.8).shift(memory.get_center()) 
         self.play(Write(init_label), run_time=1.0)
         self.play(FadeIn(init_memory), run_time=1.0)
         self.play(FadeOut(init_label), run_time=1.0)

         alloc1_label = Text("void* allocate_bottom(size_t size, size_t alignment)", font="Courier New", font_size=28)
         alloc1_label.move_to(memory.get_bottom() + DOWN)
         alloc_1 = Rectangle(height= memory.height, width= memory.width * 0.2, fill_color=RED, fill_opacity=0.8)
         alloc_1.move_to(memory.get_left() + RIGHT * alloc_1.width * 0.5) 
         self.play(Write(alloc1_label), run_time=1.0)
         self.wait(1)
         self.play(FadeIn(alloc_1), run_time=1.0)
         self.wait(1)

         alloc2_label = Text("void* allocate_top(size_t size, size_t alignment)", font="Courier New", font_size=28)
         alloc2_label.move_to(alloc1_label.get_bottom() + DOWN * 0.5)
         alloc_2 = Rectangle(height= memory.height, width= memory.width * 0.2, fill_color=BLUE, fill_opacity=0.8)
         alloc_2.move_to(memory.get_right() + LEFT * alloc_2.width * 0.5) 
         self.play(Write(alloc2_label), run_time=1.0)
         self.wait(1)
         self.play(FadeIn(alloc_2), run_time=1.0)
         self.wait(1)

         arrow1 = Arrow(start=alloc_1.get_corner(UR), end=alloc_1.get_corner(UR) + UP ,  buff=0.1, color=RED, stroke_width=3)
         bottom_marker = Text("bottom", font="Times New Roman", font_size=22, color=RED)
         bottom_marker.move_to(arrow1.end)

         arrow2 = Arrow(start=alloc_2.get_corner(UL), end=alloc_2.get_corner(UL) + UP ,  buff=0.1, color=BLUE, stroke_width=3)
         top_marker = Text("top", font="Times New Roman", font_size=22, color=BLUE)
         top_marker.move_to(arrow2.end)

         self.play(GrowArrow(arrow1), Write(top_marker), GrowArrow(arrow2), Write(bottom_marker), run_time=1.0)


         self.play(FadeOut(alloc1_label), FadeOut(alloc2_label), run_time=1.0)

         self.wait(1)


         temp_bottom_alloc_1 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=RED, fill_opacity=0.8)
         temp_bottom_alloc_1.move_to(alloc_1.get_right() + RIGHT * (temp_bottom_alloc_1.width * 0.5))

         temp_bottom_alloc_2 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=RED, fill_opacity=0.8)
         temp_bottom_alloc_2.move_to(temp_bottom_alloc_1.get_right() + RIGHT * (temp_bottom_alloc_2.width * 0.5))

         temp_bottom_alloc_3 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=RED, fill_opacity=0.8)
         temp_bottom_alloc_3.move_to(temp_bottom_alloc_2.get_right() + RIGHT * (temp_bottom_alloc_3.width * 0.5))


         temp_top_alloc_1 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
         temp_top_alloc_1.move_to(alloc_2.get_left() + LEFT * (temp_top_alloc_1.width * 0.5))

         temp_top_alloc_2 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
         temp_top_alloc_2.move_to(temp_top_alloc_1.get_left() + LEFT * (temp_top_alloc_2.width * 0.5))

         temp_top_alloc_3 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
         temp_top_alloc_3.move_to(temp_top_alloc_2.get_left() + LEFT * (temp_top_alloc_3.width * 0.5))

         temp_top_alloc_4 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
         temp_top_alloc_4.move_to(temp_top_alloc_3.get_left() + LEFT * (temp_top_alloc_4.width * 0.5))

         temp_top_alloc_5 = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=BLUE, fill_opacity=0.8)
         temp_top_alloc_5.move_to(temp_top_alloc_4.get_left() + LEFT * (temp_top_alloc_5.width * 0.5))


         self.play(FadeIn(temp_bottom_alloc_1), run_time=0.5) 
         self.play(arrow1.animate.shift(RIGHT * temp_bottom_alloc_1.width), bottom_marker.animate.shift(RIGHT * temp_bottom_alloc_1.width), run_time=0.5)
         self.play(FadeIn(temp_top_alloc_1), run_time=0.5) 
         self.play(arrow2.animate.shift(LEFT * temp_top_alloc_1.width), top_marker.animate.shift(LEFT * temp_top_alloc_1.width), run_time=0.5)
         
         self.play(FadeIn(temp_bottom_alloc_2), run_time=0.5) 
         self.play(arrow1.animate.shift(RIGHT * temp_bottom_alloc_2.width), bottom_marker.animate.shift(RIGHT * temp_bottom_alloc_2.width), run_time=0.5)
         self.play(FadeIn(temp_top_alloc_2), run_time=0.5) 
         self.play(arrow2.animate.shift(LEFT * temp_top_alloc_2.width), top_marker.animate.shift(LEFT * temp_top_alloc_2.width), run_time=0.5)
         
         self.play(FadeIn(temp_bottom_alloc_3), run_time=0.5) 
         self.play(arrow1.animate.shift(RIGHT * temp_bottom_alloc_3.width), bottom_marker.animate.shift(RIGHT * temp_bottom_alloc_3.width), run_time=0.5)

         self.wait(1)


         self.play(FadeOut(temp_bottom_alloc_1),
                    FadeOut(temp_bottom_alloc_2), 
                    FadeOut(temp_bottom_alloc_3),
                    arrow1.animate.shift(LEFT * memory.width * 0.3),
                    bottom_marker.animate.shift(LEFT * memory.width * 0.3), run_time=1.0)

         self.play(arrow2.animate.shift(LEFT * memory.width * 0.3), top_marker.animate.shift(LEFT * memory.width * 0.3),
                   FadeIn(temp_top_alloc_3), FadeIn(temp_top_alloc_4), FadeIn(temp_top_alloc_5), run_time=0.5) 
         

         #size_t get_topmarker(); size_t get_bottommarker(); void deallocate_top(size_t marker); void deallocate_bottom(size_t marker);

         get_bottom        = Text("bottom_marker = doublestack->get_bottommarker()", font= "Courier New", font_size=28)
         get_top           = Text("top_marker = doublestack->get_topmarker()", font="Courier New", font_size=28)
         deallocate_bottom = Text("void deallocate_bottom(bottom_marker)", font="Courier New", font_size=28)
         deallocate_top    = Text("void deallocate_top(top_marker)", font="Courier New", font_size=28)



         get_bottom.move_to(memory.get_bottom() + DOWN * 2.0)
         get_top.move_to(get_bottom.get_bottom() + DOWN * 0.5)
         deallocate_bottom.move_to(get_bottom)
         deallocate_top.move_to(get_top)

         
         arrow3 = Arrow(start=memory.get_corner(DL), end = memory.get_corner(DL) + DOWN, buff=0.1, color=PINK, stroke_width=3 )
         bot_mar = Text("bottom_marker", font="Times New Roman", font_size=20, color=PINK)
         bot_mar.move_to(arrow3.end)
         arrow4 = Arrow(start=temp_top_alloc_2.get_corner(DL), end = temp_top_alloc_2.get_corner(DL) + DOWN, buff=0.1, color=PINK, stroke_width=3 )
         top_mar = Text("top_marker", font="Times New Roman", font_size=20, color=PINK)
         top_mar.move_to(arrow4.end)



         self.play(Write(get_bottom), Write(get_top), run_time=1.0)
         self.play(GrowArrow(arrow3), GrowArrow(arrow4), run_time=1.0)
         self.play(Write(bot_mar), Write(top_mar), run_time = 1.0)

        
         self.wait(1)


         self.play(Transform(get_bottom, deallocate_bottom), Transform(get_top, deallocate_top), run_time=1.0)
         self.play(FadeOut(alloc_1), FadeOut(temp_top_alloc_3), FadeOut(temp_top_alloc_4), FadeOut(temp_top_alloc_5), 
                   arrow1.animate.shift(LEFT * memory.width *  0.2) , 
                   bottom_marker.animate.shift(LEFT * memory.width * 0.2 ),
                   arrow2.animate.shift(RIGHT * memory.width * 0.3),
                   top_marker.animate.shift(RIGHT * memory.width * 0.3),
                   run_time=1.0)
         

         self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)

         self.wait(1)


class PoolAllocatorIntro(Scene):
    def construct(self):
        memory_allocators = Text("Memory Allocators", font= "Times New Roman", font_size=80, color=BLUE)
        memory_allocators.shift(UP * 3).scale(0.6)


        line = Line(
            memory_allocators.get_left() + DOWN * 0.4,
            memory_allocators.get_right() + DOWN * 0.4,
            color = WHITE,
            stroke_width = 4.0
        )


        linear_allocator = Text("Linear Allocator", font="Times New Roman", font_size=30, color=WHITE)
        stack_allocator = Text("Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        double_stack_allocator = Text("Double Stack Allocator", font="Times New Roman", font_size=30, color=WHITE)
        pool_allocator = Text("Pool Allocator", font="Times New Roman", font_size=30, color=WHITE)

        # Position them
        linear_allocator.next_to(line, DOWN, buff=0.6)
        stack_allocator.next_to(linear_allocator, DOWN * 2.5, aligned_edge=LEFT, buff=0.4)
        double_stack_allocator.next_to(stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)
        pool_allocator.next_to(double_stack_allocator, DOWN* 2.5, aligned_edge=LEFT, buff=0.4)

        self.play( Write(memory_allocators),Create(line), FadeIn(linear_allocator), FadeIn(stack_allocator), FadeIn(pool_allocator), FadeIn(double_stack_allocator), run_time=1.0)

        self.wait(1)

        self.play(FadeOut(line), FadeOut(memory_allocators), FadeOut(linear_allocator), FadeOut(stack_allocator), FadeOut(double_stack_allocator), run_time=0.7)
        self.play(pool_allocator.animate.move_to(ORIGIN).scale(2), run_time=0.3)

        self.wait(1)

        self.play(FadeOut(pool_allocator), run_time=1.0)
        self.wait(1)


class PoolAllocator(Scene):
    def construct(self):

            pool_note1 = Text("Most suitable for game entities", font="Times New Roman", font_size=40, color="BLUE").shift(UP)
            pool_note2 = Text("that usually share the same memory size", font="Times New Roman", font_size=40, color="BLUE")
            self.play(Write(pool_note1), Write(pool_note2), run_time = 1.0)
            self.wait(1)
            self.play(Uncreate(pool_note1), Uncreate(pool_note2), run_time=1.0)
            self.wait(1)


            memory = Rectangle(width=8, height= 2, color= BLUE)
            memory.shift(UP)

            self.play(Create(memory), run_time=1.0)
            self.wait(1)

            init = Text("void init(void* buffer, size_t chunk_size, size_t chunk_alignment)",font="Courier New", font_size=24)
            init.move_to(memory.get_bottom() + DOWN )
            self.play(Write(init), run_time=1.0)
            self.wait(1)

            chunk_note = Text("lets say chunk size is 64 bytes", font="Times New Roman", font_size=24)
            chunk_note.move_to(init)




            backing_buffer = Rectangle(width=memory.width, height=memory.height, fill_color=GREEN, fill_opacity=1.0)
            backing_buffer.move_to(memory.get_center())

            self.play(FadeIn(backing_buffer), run_time=1.0)
            self.wait(1)
            #chunks
            num_chunks = 4

            chunk_width = memory.width / num_chunks

            chunks = VGroup(
                *[
                    Rectangle(width=chunk_width, height=memory.height, fill_color=GREEN, fill_opacity=1.0, stroke_width=1.0)
                    for _ in range(num_chunks)
                ])
            
            chunks.arrange(RIGHT, buff=0).move_to(memory.get_center())
            self.play(
            *[FadeIn(chunk) for chunk in chunks],
            run_time=1.0
        )
            self.wait(1)
            
            
            self.play(FadeOut(memory), FadeOut(backing_buffer),FadeOut(init), run_time=1.0)
            self.wait(1)
            self.play(
                       chunks.animate.arrange(RIGHT, buff=0.8).move_to(memory.get_center()),
                       run_time = 1.0
                     )
            self.wait(1)
            math_expr = MathTex("64 \\times 4 = 256", font_size=36)
           # math_expr.next_to(chunk_note, DOWN, buff=0.4)
            text_expr = Text("total bytes",font="Times New Roman", font_size=24)
            free_list_label = Text("Free List", font="Times New Roman", font_size=34, color=WHITE)
            free_list_label.move_to(chunk_note)

            group = VGroup(math_expr, text_expr).arrange(RIGHT, buff=0.3)
            group.move_to(chunk_note.get_bottom() + DOWN * 0.5)             

            self.play(Write(chunk_note),Write(group), run_time=1.0)
            self.wait(1)
            fills = VGroup()
            labels = VGroup()
            arrows = VGroup()

            for chunk in chunks:
                chunk_width = chunk.width

                fill_width = chunk.width * 0.2

                fill = Rectangle(
                    width = fill_width,
                    height= chunk.height,
                    fill_color= BLUE,
                    fill_opacity=1.0,
                    stroke_width=1.0
                    )


                fill.move_to(chunk.get_right() + LEFT * fill_width * 0.5)

                fills.add(fill)

                label = Text("next", font="Courier New", font_size=20, color=BLACK)
                label.rotate(PI / 2)  # Rotate 90 degrees counter-clockwise
                label.move_to(fill)   # Center label on the fill block
                labels.add(label)


            for i in range(1, len(chunks)):
                    arrow =Arrow( 
                        start= chunks[i - 1].get_right() + RIGHT * 0.05,
                        end=chunks[i].get_left() + LEFT * 0.05,
                        color = YELLOW,
                        stroke_width=2.5,
                        buff=0.0
                        )
                    
                    arrows.add(arrow)
            

            head = Text("head", font="Times New Roman", font_size=20, color=YELLOW_E)
            head.next_to(chunks[0], UP, buff=0.3)


            self.play(*[FadeIn(f) for f in fills], *[Write(l) for l in labels],  run_time=1.0)
            self.wait(1)
            self.play(*[Create(arrow) for arrow in arrows], run_time=1.0)
            self.wait(1)
            self.play(FadeOut(chunk_note), FadeOut(group), Write(head), run_time=1.0)
            self.wait(1)
            self.play(Write(free_list_label), run_time = 1.0)
            self.wait(1)

            alloc_label = Text("void* pool_alloc(Pool* p)", font = "Courier New", font_size=34, color=WHITE)
            alloc_label.move_to(free_list_label)

            self.play(Transform(free_list_label,alloc_label), run_time=1.0)
            self.wait(1)

            alloc_1 = Rectangle(width=chunks[0].width, height=chunks[0].height, fill_color=RED, fill_opacity=1.0)
            alloc_1.move_to(chunks[0])
            alloc_2 = Rectangle(width=chunks[1].width, height=chunks[1].height, fill_color=RED, fill_opacity=1.0)
            alloc_2.move_to(chunks[1])
            

            self.play(FadeIn(alloc_1), run_time=1.0)
            self.wait(1)
            self.play(head.animate.next_to(chunks[1], UP, buff=0.3), FadeOut(arrows[0]), run_time=1.0)
            self.wait(1)

            self.play(FadeIn(alloc_2), run_time=1.0)
            self.wait(1)

            self.play(head.animate.next_to(chunks[2], UP, buff=0.3), FadeOut(arrows[1]), run_time=1.0)
            self.wait(1)

            #pool free
            free_label = Text("void pool_free(Pool* p, void* ptr)", font = "Courier New", font_size=34, color=WHITE)
            check      = Text("start <= ptr && ptr < end", font= "Courier New", font_size=34, color=WHITE)
            free_label.move_to(alloc_label)
            check.move_to(free_label.get_bottom() + DOWN )

            self.play(Transform(alloc_label, free_label), FadeOut(free_list_label), run_time=1.0)
            self.wait(1)

            self.play(Write(check), run_time=1.0)
            self.wait(1)
            
            self.play(FadeOut(alloc_1), run_time=1.0)
            self.wait(1) 
            self.play(FadeOut(free_label), FadeOut(alloc_label) ,FadeOut(check), run_time=1.0)
            self.wait(1)
            #arrow
            arrow13 = Arrow(
                            start=chunks[1].get_right() + RIGHT * 0.05, 
                            end  =chunks[2].get_left() + LEFT * 0.05,
                            color = YELLOW,
                            stroke_width=2.5,
                            buff=0.0
                              )
            chunk2_pos = chunks[1].get_center()
            fill2_pos = fills[1].get_center()
            label2_pos = labels[1].get_center()
            
            chunk1_pos = chunks[0].get_center()
            fill1_pos = fills[0].get_center()
            label1_pos = labels[0].get_center()

            


            shift = 3
            self.play(chunks[1].animate.shift(DOWN * shift),
                      fills[1].animate.shift(DOWN * shift),
                      labels[1].animate.shift(DOWN * shift),
                      alloc_2.animate.shift(DOWN * shift) , 
                      chunks[0].animate.move_to(chunk2_pos ),
                      fills[0].animate.move_to(fill2_pos),
                      labels[0].animate.move_to(label2_pos),
                      run_time=1.0)
            self.wait(1)
            self.play(GrowArrow(arrows[1]), head.animate.next_to(chunks[0], UP, buff=0.3), run_time=1.0)
            self.wait(1)
            self.play(chunks[1].animate.move_to(chunk1_pos),
                      fills[1].animate.move_to(fill1_pos),
                      labels[1].animate.move_to(label1_pos),
                      alloc_2.animate.move_to(chunk1_pos),
                      run_time=1.0
                      )
            self.wait(1)
            self.play(FadeIn(free_label), run_time=1.0)
            self.wait(1)
            self.play(FadeOut(alloc_2), run_time=0.5)
            self.wait(1)
            self.play(GrowArrow(arrows[0]), head.animate.next_to(chunks[1], UP, buff=0.3), run_time=1.0)
            self.wait(1)      


class LinkInTheDescription(Scene):
     def construct(self):
          
          text = Text("LINK IN THE DESCRIPTION", font="Times New Roman", font_size=50, color=RED)
          text.shift(DOWN*1.0)

          arrow1 = Arrow(start=text.get_center() + DOWN * 0.3, end=text.get_center() + DOWN * 2.0, color = RED,
                        stroke_width=2.5,
                        buff=0.5)
          

          self.play(Write(text), GrowArrow(arrow1), run_time=1.0)

          self.wait(1)
          self.play(FadeOut(text), FadeOut(arrow1), run_time=1.0)


class Outro(Scene):
     def construct(self):
          
        main_cloud = Ellipse(width=5, height=3, color=RED)
        main_cloud.set_stroke(width=2)

        second_cloud = Ellipse(width=1.25, height=0.75, color=RED)
        second_cloud.set_stroke(width=2)

        third_cloud = Ellipse(width=1.25, height=0.75, color=RED)
        third_cloud.set_stroke(width=2)

        fourth_cloud = Ellipse(width=0.63, height=0.37, color=RED)
        fourth_cloud.set_stroke(width=2)

        ghost_logo = ImageMobject("channels4_profile.jpg")
        ghost_logo.scale(0.75)
        ghost_logo.to_edge(LEFT)
        ghost_logo.shift(LEFT * 4 + DOWN * 2.5)

        main_cloud.shift(RIGHT*4 + UP*2)
        second_cloud.next_to(main_cloud, DOWN*0.1 + LEFT*0.1, buff=0.001)
        third_cloud.next_to(second_cloud,DOWN*0.1 + LEFT*0.1, buff=0.001)
        fourth_cloud.next_to(third_cloud, DOWN*0.1 + LEFT*0.1, buff=0.005)

        main_cloud.shift(LEFT)
        fourth_cloud.shift(LEFT)
        third_cloud.shift(LEFT)
        second_cloud.shift(LEFT)

        self.play(
            ghost_logo.animate.shift(RIGHT * 6),
            run_time=1,
            rate_func=smooth
        )
        self.play(Create(fourth_cloud), run_time=0.4)
        self.play(Create(third_cloud), run_time=0.4)
        self.play(Create(second_cloud), run_time=0.4)
        self.play(Create(main_cloud), run_time=0.4)


        text = Text("Your Thoughts?", font="Times New Roman", font_size=30, color=WHITE)
        text.move_to(main_cloud)
        self.play(Write(text), run_time=1.0)
        self.wait(1)
        text2 = Text("See You Next Time!", font="Times New Roman", font_size=30, color=WHITE)
        text2.move_to(text)
        self.play(Transform(text, text2), run_time=1.0)
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


        
class Thumbnail_left(Scene):
     def construct(self):
        memoryarena_label = Text("Memory Arena", font= "Times New Roman", font_size=80, color=ORANGE)





        memory = Rectangle(width=8, height= 2, color= BLUE)
        memory.shift(UP*1.5)

        memory_label = Text("Memory", font="Times New Roman", color=WHITE, font_size=20)
        memory_label.next_to(memory, UP, buff=0.2)

        #self.play(Create(memory), Write(memory_label), run_time=1.0) 


        rendering = Square(color=BLUE)
        physics   = Square(color=RED)
        ai        = Square(color= LIGHT_BROWN)
        audio     = Square(color=PINK)
        rendering_label   = Text("Rendering", font="Times New Roman", font_size=24)
        physics_label     = Text("Physics", font="Times New Roman", font_size=24)
        ai_label          = Text("AI", font="Times New Roman", font_size=24)
        audio_label       = Text("Audio", font="Times New Roman", font_size=24)
        rendering.shift(LEFT * 4.5 + DOWN * 2)
        physics.move_to(rendering.get_right() + RIGHT * 2 )
        ai.shift(rendering.get_right() + RIGHT * 5 )
        audio.shift(rendering.get_right() + RIGHT * 8 )
        rendering_label.move_to(rendering.get_center() )
        physics_label.move_to(physics.get_center() )
        ai_label.move_to(ai.get_center() )
        audio_label.move_to(audio.get_center() )

        self.play(Create(memory), Write(memory_label), FadeIn(rendering), Write(rendering_label), FadeIn(physics), Write(physics_label), 
                  FadeIn(ai),Write(ai_label), FadeIn(audio), Write(audio_label),  run_time= 1.0)
        self.wait(1)

        system = [
               {"name": "Rendering", "color": BLUE,        "top": rendering.get_top()},
               {"name": "Physics",   "color": RED,         "top": physics.get_top()},
               {"name": "AI",        "color": LIGHT_BROWN, "top": ai.get_top()},
               {"name": "Audio",     "color": PINK,        "top": audio.get_top()}
          ]

        weights = [5, 3, 2, 3]
        selected_subsystems = random.choices(system, weights=weights, k=30)

        memory_blocks = allocate_memory_from_subsystems_no_animation(self, selected_subsystems, memory)

        blocks = [block_info["block"] for block_info in memory_blocks]


        # Play the fade-in animation on all of them together
        self.play(*[FadeIn(block) for block in blocks], run_time=1.0)
        self.wait(2)


class Thumbnail_right(Scene):
     def construct(self):
        memoryarena_label = Text("Memory Arena", font= "Times New Roman", font_size=80, color=ORANGE)

        memory = Rectangle(width=8, height= 2, color= BLUE)
        memory.shift(UP*1.5)

        memory_label = Text("Memory", font="Times New Roman", color=WHITE, font_size=20)
        memory_label.next_to(memory, UP, buff=0.2)

        #self.play(Create(memory), Write(memory_label), run_time=1.0) 


        rendering = Square(color=BLUE)
        physics   = Square(color=RED)
        ai        = Square(color= LIGHT_BROWN)
        audio     = Square(color=PINK)
        rendering_label   = Text("Rendering", font="Times New Roman", font_size=24)
        physics_label     = Text("Physics", font="Times New Roman", font_size=24)
        ai_label          = Text("AI", font="Times New Roman", font_size=24)
        audio_label       = Text("Audio", font="Times New Roman", font_size=24)
        rendering.shift(LEFT * 4.5 + DOWN * 2)
        physics.move_to(rendering.get_right() + RIGHT * 2 )
        ai.shift(rendering.get_right() + RIGHT * 5 )
        audio.shift(rendering.get_right() + RIGHT * 8 )
        rendering_label.move_to(rendering.get_center() )
        physics_label.move_to(physics.get_center() )
        ai_label.move_to(ai.get_center() )
        audio_label.move_to(audio.get_center() )

        self.play(Create(memory), Write(memory_label), FadeIn(rendering), Write(rendering_label), FadeIn(physics), Write(physics_label), 
                  FadeIn(ai),Write(ai_label), FadeIn(audio), Write(audio_label),  run_time= 1.0)
        self.wait(1)

        system = [
               {"name": "Rendering", "color": BLUE,        "top": rendering.get_top()},
               {"name": "Physics",   "color": RED,         "top": physics.get_top()},
               {"name": "AI",        "color": LIGHT_BROWN, "top": ai.get_top()},
               {"name": "Audio",     "color": PINK,        "top": audio.get_top()}
          ]

        weights = [5, 3, 2, 3]
        selected_subsystems = random.choices(system, weights=weights, k=30)

        memory_blocks = allocate_memory_from_subsystems_no_animation(self, selected_subsystems, memory)

        blocks = [block_info["block"] for block_info in memory_blocks]


        # Play the fade-in animation on all of them together

        # note to say i huge code base the individual allocations would be 100 - 1000
        alloc_label = Text("In real projects, these would be 100s or 1000s of allocations.", font="Times New Roman", font_size=24, color=WHITE)
        alloc_label.move_to(memory.get_bottom() + DOWN * 0.5)



        neutral_fill = Rectangle(
        width=memory.width,
        height=memory.height,
        fill_color=GREEN,
        fill_opacity=0.8,
        stroke_width=0
        ).move_to(memory.get_center())

        #alloc text
        alloc_call_text = Text('arena->alloc(SIZE);', font="Courier New", font_size=28, color=WHITE)
        alloc_call_text.move_to(memory.get_bottom() + DOWN * 0.6)

        self.play(Write(alloc_call_text, rate_func=linear), run_time=1.0)

        self.play(FadeIn(neutral_fill), run_time = 1.0)
        
        self.wait(1)
        
        self.play(FadeOut(alloc_call_text), run_time=1.0)

        #alocating memory 
        rendering_memory = Rectangle(height = memory.height, width= memory.width * 0.4, fill_color=BLUE, fill_opacity=0.8)
        physics_memory = Rectangle(height=memory.height, width=memory.width * 0.3, fill_color=RED, fill_opacity=0.8)
        ai_memory = Rectangle(height=memory.height, width=memory.width * 0.1, fill_color=LIGHT_BROWN, fill_opacity=0.8)
        audio_memory = Rectangle(height=memory.height, width = memory.width * 0.2, fill_color=PINK, fill_opacity=0.8)

        rendering_memory.move_to(memory.get_left() + RIGHT * (rendering_memory.width / 2.0))
        physics_memory.move_to(rendering_memory.get_right() + RIGHT * (physics_memory.width / 2.0))
        ai_memory.move_to(physics_memory.get_right() + RIGHT * (ai_memory.width/2.0))
        audio_memory.move_to(ai_memory.get_right() + RIGHT * (audio_memory.width / 2.0))

        #arrows

        arrow1 = Arrow(start = rendering_memory.get_bottom(), end=rendering.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow2 = Arrow(start = physics_memory.get_bottom(),   end=physics.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow3 = Arrow(start = ai_memory.get_bottom(), end=ai.get_top(), buff=0.1, color=WHITE, stroke_width=3) 
        arrow4 = Arrow(start = audio_memory.get_bottom(), end=audio.get_top(), buff=0.1, color=WHITE, stroke_width=3) 

        self.play(FadeIn(rendering_memory), GrowArrow(arrow1), run_time=1.0)
        self.play(FadeIn(physics_memory), GrowArrow(arrow2), run_time = 1.0)
        self.play(FadeIn(ai_memory), GrowArrow(arrow3), run_time = 1.0)
        self.play(FadeIn(audio_memory), GrowArrow(arrow4), run_time = 1.0)


        self.wait(2)