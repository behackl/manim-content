from collections import defaultdict
from manim import *

BH_DARKGREEN = '#455D3E'

custom_tex_template = TexTemplate()
custom_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")
MathTex.set_default(tex_template=custom_tex_template)

config.background_color = BH_DARKGREEN


def partitions(n, I=1):  # from https://stackoverflow.com/a/44209393/18189631
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield (i,) + p

def unique_to_odd(partition):
    r"""Given a partition with unique parts, returns the
    corresponding (w.r.t. Glaisher's bijection) partition
    with only odd parts.
    """
    assert len(partition) == len(set(partition))
    odd_parts_map = defaultdict(int)
    for part in partition:
        j = 0
        while part % 2 == 0:
            part //= 2
            j += 1
        odd_parts_map[part] += 2**j
    return tuple(sum([[p]*v for p, v in sorted(odd_parts_map.items(), reverse=True)], []))     


class YoungTableau(VMobject):
    def __init__(self, *parts, square_length=1, **kwargs):
        super().__init__(**kwargs)
        self.integer_parts = parts
        part_groups = [
            VGroup(*[Square(side_length=square_length) for x in range(part)]).arrange(RIGHT, buff=0)
            for part in parts
        ]
        VGroup(*part_groups).arrange(DOWN, buff=0)
        for part_group in part_groups[1:]:
            part_group.set_x(part_groups[0].get_x(LEFT), LEFT)
        for part_group in part_groups:
            for part in part_group:
                self.add(part)


class Intro(Scene):
    def construct(self):
        part1 = MathTex("5 + 5 + 1 + 1 + 1", "=", "13", font_size=100)
        part2 = MathTex("10 + 2 + 1", "=", "13", font_size=100)
        part2_rev = MathTex("13", "=", "10 + 2 + 1", font_size=100)
        self.wait()
        self.play(Write(part1, run_time=4))
        self.wait()
        self.play(part1.animate.scale(0.5).move_to(2*UP))
        self.wait()
        self.play(Write(part2, run_time=3))
        self.wait()
        self.play(part2.animate.scale(0.5).next_to(part1, DOWN, buff=1))
        part2_rev.scale(0.5).shift(part2[1].get_center() - part2_rev[1].get_center())
        self.wait()
        self.play(TransformMatchingTex(part2, part2_rev, path_arc=PI/2))
        self.wait()
        identity = MathTex("5 + 5 + 1 + 1 + 1", "=", "10 + 2 + 1", font_size=100).next_to(part2, DOWN, buff=1.5)
        self.play(
            FadeTransform(part1[0].copy(), identity[0]),
            Write(identity[1]),
            FadeTransform(part2_rev[2].copy(), identity[2]),
            run_time=2
        )
        self.wait()
        self.play(
            AnimationGroup(
                FadeOut(part1, shift=UP),
                FadeOut(part2_rev, shift=UP),
                identity.animate.move_to(ORIGIN),
                lag_ratio=0.5
            )
        )
        self.play(Unwrite(identity))
        self.wait()

class ButWait1(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        tex_group = VGroup(
            Tex("Wait.", font_size=100),
            Tex("There is more.", font_size=100)
        ).arrange(DOWN, buff=1)
        self.add(tex_group[0])

class ButWait2(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        tex_group = VGroup(
            Tex("Wait.", font_size=100),
            Tex("There is more.", font_size=100)
        ).arrange(DOWN, buff=1)
        self.add(tex_group)

class PartitionIntro(Scene):
    def construct(self):
        part1 = MathTex("5 + 5 + 1 + 1 + 1", "=", "13", font_size=75)
        part2 = MathTex("10 + 2 + 1", "=", "13", font_size=75)
        VGroup(part1, part2).arrange(DOWN, buff=1.5)
        self.add(part1, part2)
        self.wait()
        # repetitions are allowed
        self.play(
            AnimationGroup(
                Indicate(VGroup(part1[0][0], part1[0][2])),
                Indicate(VGroup(part1[0][4], part1[0][6], part1[0][8])),
                lag_ratio=0.75
            )
        )
        self.wait()
        # parts
        label = Tex("parts", font_size=75)
        label.next_to(part1[0], UP).shift(1*UP)
        Arrow.get_default_tip_length = lambda self: 0.15
        Arrow.set_default(stroke_width=3)
        arrows = VGroup(
            Arrow(label.get_center(), part1[0][0]),
            Arrow(label.get_center(), part1[0][2]),
            Arrow(label.get_center(), part1[0][4]),
            Arrow(label.get_center(), part1[0][6]),
            Arrow(label.get_center(), part1[0][8]),
        )
        self.add(arrows, label)
        self.play(Write(label), Create(arrows), lag_ratio=0.5)
        self.wait()
        self.play(FadeOut(arrows, shift=UP), FadeOut(label, shift=UP))
        self.wait()

        # visualization as Young Tableaux
        yt1 = YoungTableau(5, 5, 1, 1, 1, square_length=0.5)\
                .set_style(stroke_color=BH_DARKGREEN, fill_opacity=1)
        yt2 = YoungTableau(10, 2, 1, square_length=0.5)\
                .set_style(stroke_color=BH_DARKGREEN, fill_opacity=1)
        part1.generate_target()
        part2.generate_target()
        VGroup(
            VGroup(part1.target, yt1).arrange(DOWN, buff=0.25),
            VGroup(part2.target, yt2).arrange(DOWN, buff=0.25)
        ).arrange(DOWN, buff=1)
        self.play(MoveToTarget(part1), MoveToTarget(part2))
        part1.generate_target()
        part1_parts = VGroup(
            *part1.target.submobjects[0][0::2],
        ).set_color_by_gradient(RED, YELLOW)
        part1_colors = [part.fill_color for part in part1_parts]
        VGroup(*yt1.submobjects[0:5]).set_style(fill_opacity=1, fill_color=part1_colors[0])
        VGroup(*yt1.submobjects[5:10]).set_style(fill_opacity=1, fill_color=part1_colors[1])
        yt1.submobjects[10].set_style(fill_opacity=1, fill_color=part1_colors[2])
        yt1.submobjects[11].set_style(fill_opacity=1, fill_color=part1_colors[3])
        yt1.submobjects[12].set_style(fill_opacity=1, fill_color=part1_colors[4])
        self.play(MoveToTarget(part1))
        label = Tex(r"Young\\ tableau", font_size=75).next_to(yt1, LEFT, buff=2)
        arrow = Arrow(label.get_critical_point(RIGHT), yt1.get_critical_point(LEFT))
        self.play(Write(yt1), FadeIn(label, arrow))
        self.wait()
        part2.generate_target()
        part2_parts = VGroup(
            part2.target.submobjects[0][0],
            *part2.target.submobjects[0][3::2],
        ).set_color_by_gradient(RED, YELLOW)
        part2.target.submobjects[0][1].set_color(RED)
        part2_colors = [part.fill_color for part in part2_parts]
        VGroup(*yt2.submobjects[0:10]).set_style(fill_opacity=1, fill_color=part2_colors[0])
        VGroup(*yt2.submobjects[10:12]).set_style(fill_opacity=1, fill_color=part2_colors[1])
        yt2.submobjects[12].set_style(fill_opacity=1, fill_color=part2_colors[2])
        self.play(MoveToTarget(part2))
        CurvedArrow.get_default_tip_length = lambda self: 0.15
        arrow2 = CurvedArrow(label.get_critical_point(DOWN) + 0.25*DOWN, yt2.get_critical_point(LEFT) + 0.25*LEFT) 
        self.play(Write(yt2), FadeIn(arrow2))
        self.wait()
        

class YTEnumeration(Scene):
    def construct(self):
        self.next_section("Enumeration", skip_animations=False)
        pts = sorted(partitions(13), reverse=True, key=lambda pt: pt[::-1])
        yts = [
            YoungTableau(*partition[::-1], square_length=1)\
                .set_submobject_colors_by_gradient(RED, YELLOW)\
                .set_style(stroke_color=BH_DARKGREEN, fill_opacity=1)
            for partition in pts]
        current = yts[0]

        yts_bg = VGroup(*[yt.copy().set_style(stroke_width=2, fill_color=WHITE, fill_opacity=0.1) for yt in yts])
        yts_bg.arrange_in_grid(8, 13, buff=2).scale_to_fit_width(config.frame_width - 1)
        yts_bg[0].set_style(fill_opacity=0.4)
        for yt in yts:
            if yt.height > config.frame_height:
                yt.scale_to_fit_height(config.frame_height - 1)
        self.add(yts_bg)
        self.play(FadeIn(current))
        for ind, yt in enumerate(yts[1:]):
            self.play(
                Transform(current, yt),
                yts_bg[ind+1].animate.set_style(fill_opacity=0.4),
                run_time=0.15
            )
        self.wait()
        self.play(FadeOut(current))
        self.wait()

        # "the curious part"
        self.next_section("The Curious Part", skip_animations=False)
        self.wait()
        self.play(
            *[ytbg.animate.set_style(fill_color=RED, fill_opacity=1) for ytbg in yts_bg
            if len(ytbg.integer_parts) == len(set(ytbg.integer_parts))
            ],
        )
        self.wait()
        self.play(
            *[ytbg.animate.set_style(fill_color=WHITE, fill_opacity=0.4) for ytbg in yts_bg],
        )
        self.wait()
        self.play(
            *[ytbg.animate.set_style(fill_color=RED, fill_opacity=1) for ytbg in yts_bg
            if all(part % 2 == 1 for part in ytbg.integer_parts)
            ],
        )
        self.wait()


class Coincidence1(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        tex_group = VGroup(
            Tex("Coincidence?", font_size=140),
            Tex("I think not.", font_size=100)
        ).arrange(DOWN, buff=1.5)
        self.add(tex_group[0])

class Coincidence2(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        tex_group = VGroup(
            Tex("Coincidence?", font_size=140),
            Tex("I think not.", font_size=100)
        ).arrange(DOWN, buff=1.5)
        self.add(tex_group)

class EulerGlaisher(Scene):
    def construct(self):
        euler_img = ImageMobject("euler.jpg").scale_to_fit_width(3)
        euler_img.to_corner(DOWN + RIGHT, buff=0)
        euler_lab = Tex("Leonhard Euler").scale_to_fit_width(2.75).next_to(euler_img, UP, buff=0.1)
        self.play(FadeIn(euler_img, euler_lab))
        theorem = VGroup(
            MathTex(
                r"\#\bigg({\text{partitions of } n\atop \text{with different parts}}\bigg)",
                font_size = 60
            ),
            MathTex("=", font_size=60),
            MathTex(
                r"\#\bigg({\text{partitions of } n\atop \text{with odd parts}}\bigg)",
                font_size = 60
            ),
        ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.75)
    
        unique_partitions = VGroup(
            *[YoungTableau(*p[::-1]) for p in partitions(13) if len(set(p)) == len(p)]
        ).set_style(stroke_color="#455D3E", stroke_width=2, fill_color=WHITE, fill_opacity=0.5)
        unique_partitions.arrange_in_grid(5, 4, buff=1.5)\
                         .scale_to_fit_width(config.frame_width/3 - 0.5)
        odd_partitions = VGroup(
            *[YoungTableau(*p[::-1]) for p in partitions(13) if all(pt % 2 == 1 for pt in p)]
        ).set_style(stroke_color="#455D3E", stroke_width=2, fill_color=WHITE, fill_opacity=0.5)
        odd_partitions.arrange_in_grid(5, 4, buff=1.5)\
                      .scale_to_fit_height(unique_partitions.height + 1)
        VGroup(unique_partitions, odd_partitions).arrange(RIGHT, buff=1.5).set_x(-3/2).to_edge(DOWN)

        self.play(Write(theorem[0]), FadeIn(unique_partitions), run_time=3)
        self.wait()
        self.play(FadeIn(theorem[1]), run_time=0.5)
        self.play(Write(theorem[2]), FadeIn(odd_partitions), run_time=3)
        self.wait()

        gf_proof = MathTex(
            r"\prod_{n=1}^{\infty} (1 + q^n)", 
            r" = \prod_{n=1}^{\infty} \frac{1 - q^{2n}}{1 - q^n}",
            r" = \prod_{n=1}^{\infty} \frac{1}{1 - q^{2n-1}}",
            font_size=50
        ).next_to(theorem, DOWN, buff=1).set_x(-3/2)
        self.play(
            ReplacementTransform(unique_partitions.copy(), gf_proof[0]),
        )
        self.play(FadeIn(gf_proof[1]))
        self.play(FadeIn(gf_proof[2]))
        cp = gf_proof[2].copy()
        self.play(Transform(cp, odd_partitions))
        self.remove(cp)
        self.wait()

        glaisher_img = ImageMobject("glaisher.jpg")
        glaisher_img.scale_to_fit_width(3).to_corner(DOWN + RIGHT, buff=0)
        glaisher_lab = Tex("James W. L. Glaisher")
        glaisher_lab.scale_to_fit_width(2.75).next_to(glaisher_img, UP, buff=0.1)
        self.play(
            FadeOut(euler_img, euler_lab),
            FadeIn(glaisher_img, glaisher_lab),
            FadeOut(gf_proof),
            run_time=2
        )
        self.play(
            unique_partitions.animate.arrange_in_grid(9, 2, buff=0.25)\
                                     .scale_to_fit_width(2.5)\
                                     .to_edge(DOWN),
            odd_partitions.animate.arrange_in_grid(6, 3, buff=0.15)\
                                  .scale_to_fit_width(3.25)\
                                  .to_edge(DOWN),
        )
        self.wait()
        
        map_target = {}
        for k in range(len(unique_partitions)):
            target_partition = unique_to_odd(unique_partitions[k].integer_parts)
            [target_yt] = [yt for yt in odd_partitions if yt.integer_parts == target_partition]
            map_target[k] = odd_partitions.submobjects.index(target_yt)

        bijection = VGroup(*[
            ArcBetweenPoints(
                unique_partitions[k].get_center(),
                odd_partitions[map_target[k]].get_center(),
                angle=-TAU/6, stroke_opacity=0.5, stroke_width=2,
                color=ORANGE,
            )
            for k in range(18)
        ])
        self.play(AnimationGroup(*[Create(line) for line in bijection], lag_ratio=0.75), run_time=4)
        self.wait()
        

class Correspondence(Scene):
    def construct(self):
        self.wait()

        yt = YoungTableau(5, 5, 1, 1, 1)
        yt.set_style(stroke_color="#455D3E", fill_color=WHITE, fill_opacity=1)
        self.play(FadeIn(yt))
        self.wait()
        self.play(
            yt[:10].animate.set_fill(RED),
            yt[10:].animate.set_fill(YELLOW)
        )
        brace_5 = BraceBetweenPoints(
            yt[0].get_critical_point(UL) + 0.05*DOWN,
            yt[5].get_critical_point(DL) + 0.05*UP,
            buff=0.1
        )
        bin_eq_5 = MathTex("[10]_2", r"\times", "5", "=", "2", r"\times", "5")
        bin_eq_5.next_to(brace_5, LEFT)
        bin_eq_5.set_color_by_tex("5", RED)
        unique_part_1 = MathTex("2^1", r"\cdot", "5", "=", "10").next_to(bin_eq_5, DOWN)
        unique_part_1[2].set_color(RED)

        self.play(Write(brace_5), Write(bin_eq_5[4:]))
        self.wait()
        self.play(Write(bin_eq_5[:4]))
        self.wait()

        brace_1 = BraceBetweenPoints(
            yt[10].get_critical_point(UL) + 0.05*DOWN,
            yt[12].get_critical_point(DL) + 0.05*UP,
            buff=0.1
        )
        bin_eq_1 = MathTex("[11]_2", r"\times", "1", "=", "3", r"\times", "1")
        bin_eq_1.next_to(brace_1, LEFT)
        bin_eq_1.set_color_by_tex("1", YELLOW, substring=False)
        unique_part_2 = MathTex("2^1", r"\cdot", "1", "=", "2").next_to(bin_eq_1, DOWN)
        unique_part_2[2].set_color(YELLOW)
        unique_part_3 = MathTex("2^0", r"\cdot", "1", "=", "1").next_to(unique_part_2, DOWN)
        unique_part_3[2].set_color(YELLOW)

        self.play(Write(brace_1), Write(bin_eq_1[4:]))
        self.wait()
        self.play(Write(bin_eq_1[:4]))
        self.wait()

        self.play(ReplacementTransform(bin_eq_5[0][1].copy(), unique_part_1[0]))
        self.play(Write(unique_part_1[1:]))
        self.wait()

        self.play(ReplacementTransform(bin_eq_1[0][1].copy(), unique_part_2[0]))
        self.play(Write(unique_part_2[1:]))
        self.wait(0.5)
        self.play(ReplacementTransform(bin_eq_1[0][2].copy(), unique_part_3[0]))
        self.play(Write(unique_part_3[1:]))

        yt_img = YoungTableau(10, 2, 1).shift(RIGHT)
        yt_img.set_style(stroke_color="#455D3E", fill_color=WHITE, fill_opacity=1)
        yt_img[:10].set_fill(RED)
        yt_img[10:].set_fill(YELLOW)

        self.play(FadeOut(brace_5, brace_1, bin_eq_5, bin_eq_1,))

        self.wait()

        self.play(
            Transform(yt, yt_img), 
            unique_part_1.animate.next_to(yt_img[0], LEFT),
            unique_part_2.animate.next_to(yt_img[10], LEFT),
            unique_part_3.animate.next_to(yt_img[12], LEFT),
        )
        self.wait()


class LargerExample(Scene):
    def construct(self):
        colors = color_gradient([RED, YELLOW], 4)
        yt = YoungTableau(9, 7, 7, 7, 3, 3, 1, 1, 1, 1, 1, 1, square_length=0.6)
        yt.shift(2.5*RIGHT).set_style(stroke_color="#455D3E", fill_color=WHITE, fill_opacity=1)
        braces = VGroup(
            BraceBetweenPoints(
                yt[0].get_critical_point(UL) + 0.05*DOWN,
                yt[0].get_critical_point(DL) + 0.05*UP,
                buff=0.1
            ),
            BraceBetweenPoints(
                yt[9].get_critical_point(UL) + 0.05*DOWN,
                yt[23].get_critical_point(DL) + 0.05*UP,
                buff=0.1
            ),
            BraceBetweenPoints(
                yt[30].get_critical_point(UL) + 0.05*DOWN,
                yt[33].get_critical_point(DL) + 0.05*UP,
                buff=0.1
            ),
            BraceBetweenPoints(
                yt[36].get_critical_point(UL) + 0.05*DOWN,
                yt[41].get_critical_point(DL) + 0.05*UP,
                buff=0.1
            ),
        )
        bin_eqs = VGroup(
            MathTex(r"[1]_2 \times", "9"),
            MathTex(r"[11]_2 \times", "7"),
            MathTex(r"[10]_2 \times", "3"),
            MathTex(r"[110]_2 \times", "1")
        )
        for k in range(4):
            bin_eqs[k].next_to(braces[k], LEFT)
            bin_eqs[k][1].set_color(colors[k])

        
        self.wait()
        self.play(FadeIn(yt))
        self.wait()
        self.play(
            yt[:9].animate.set_fill(colors[0]),
            yt[9:30].animate.set_fill(colors[1]),
            yt[30:36].animate.set_fill(colors[2]),
            yt[36:].animate.set_fill(colors[3]),
        )
        for k in range(4):
            self.wait()
            self.play(Write(braces[k]), Write(bin_eqs[k]))
        
        self.wait()

        new_parts = VGroup(
            MathTex("9 =", r"2^0 \cdot", "9").set_color_by_tex("9", colors[0], substring=False),
            MathTex("14 =", r"2^1 \cdot", "7").set_color_by_tex("7", colors[1]),
            MathTex("7 =", r"2^0 \cdot", "7").set_color_by_tex("7", colors[1], substring=False),
            MathTex("6 =", r"2^1 \cdot", "3").set_color_by_tex("3", colors[2]),
            MathTex("4 =", r"2^2 \cdot", "1").set_color_by_tex("1", colors[3], substring=False),
            MathTex("2 =", r"2^1 \cdot", "1").set_color_by_tex("1", colors[3], substring=False),
        )

        yt_img = YoungTableau(14, 9, 7, 6, 4, 2, square_length=0.8).shift(RIGHT)
        yt_img.set_style(stroke_color="#455D3E", fill_color=WHITE, fill_opacity=1)
        yt_img[:14].set_fill(colors[1])
        yt_img[23:30].set_fill(colors[1])
        yt_img[14:23].set_fill(colors[0])
        yt_img[30:36].set_fill(colors[2])
        yt_img[36:].set_fill(colors[3])
        yt_img.submobjects = yt_img.submobjects[14:23] + yt_img.submobjects[0:14] + yt_img.submobjects[23:30] + yt_img.submobjects[30:36] + yt_img.submobjects[36:40] + yt_img.submobjects[40:]

        new_parts[0].next_to(yt_img[0], LEFT)
        new_parts[1].next_to(yt_img[9], LEFT)
        new_parts[2].next_to(yt_img[23], LEFT)
        new_parts[3].next_to(yt_img[30], LEFT)
        new_parts[4].next_to(yt_img[36], LEFT)
        new_parts[5].next_to(yt_img[40], LEFT)
        

        # 2^0 * 9
        self.play(
            ReplacementTransform(bin_eqs[0][0][1].copy(), new_parts[0][1]),
            ReplacementTransform(bin_eqs[0][-1].copy(), new_parts[0][-1])
        )
        self.play(Write(new_parts[0][0]))
        # 2^1 * 7
        self.play(
            ReplacementTransform(bin_eqs[1][0][1].copy(), new_parts[1][1]),
            ReplacementTransform(bin_eqs[1][-1].copy(), new_parts[1][-1])
        )
        self.play(Write(new_parts[1][0]))
        # 2^0 * 7
        self.play(
            ReplacementTransform(bin_eqs[1][0][2].copy(), new_parts[2][1]),
            ReplacementTransform(bin_eqs[1][-1].copy(), new_parts[2][-1])
        )
        self.play(Write(new_parts[2][0]))
        # 2^1 * 3
        self.play(
            ReplacementTransform(bin_eqs[2][0][1].copy(), new_parts[3][1]),
            ReplacementTransform(bin_eqs[2][-1].copy(), new_parts[3][-1])
        )
        self.play(Write(new_parts[3][0]))
        # 2^2 * 1
        self.play(
            ReplacementTransform(bin_eqs[3][0][1].copy(), new_parts[4][1]),
            ReplacementTransform(bin_eqs[3][-1].copy(), new_parts[4][-1])
        )
        self.play(Write(new_parts[4][0]))
        # 2^1 * 1
        self.play(
            ReplacementTransform(bin_eqs[3][0][2].copy(), new_parts[5][1]),
            ReplacementTransform(bin_eqs[3][-1].copy(), new_parts[5][-1])
        )
        self.play(Write(new_parts[5][0]))
        self.wait()

        self.play(FadeOut(braces, bin_eqs))
        self.wait()

        yt_copy = yt.copy()
        self.play(ReplacementTransform(yt, yt_img))

        self.wait()
        self.play(FadeOut(yt_img))
        self.wait()

        
        relabel = VGroup(
            MathTex(r"2^0 \times", "9").set_color_by_tex("9", colors[0]),
            MathTex(r"(2^1 + 2^0) \times", "7").set_color_by_tex("7", colors[1]),
            MathTex(r"2^1 \times", "3").set_color_by_tex("3", colors[2]),
            MathTex(r"(2^2 + 2^1) \times", "1").set_color_by_tex("1", colors[3], substring=False),
        )
        for k in range(4):
            relabel[k].next_to(braces[k], LEFT)

        # 2^0 * 9
        self.play(Transform(new_parts[0][1].copy(), relabel[0]))

        # (2^1 + 2^0) * 7
        self.play(Transform(VGroup(new_parts[1][1].copy(), new_parts[2][1].copy()), relabel[1]))

        # 2^1 * 3
        self.play(Transform(new_parts[3][1].copy(), relabel[2]))

        # (2^2 + 2^1) * 1
        self.play(Transform(VGroup(new_parts[4][1].copy(), new_parts[5][1].copy()), relabel[3]))

        
        self.wait()

        self.play(Write(braces[0]), Write(yt_copy[:9]))
        self.play(Write(braces[1]), Write(yt_copy[9:30]))
        self.play(Write(braces[2]), Write(yt_copy[30:36]))
        self.play(Write(braces[3]), Write(yt_copy[36:]))
        self.wait()




class PauseNow(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        tex_group = VGroup(
            Tex("Want to try yourself?", font_size=100),
            Tex("Pause now.", font_size=100)
        ).arrange(DOWN, buff=1)
        part = MathTex("9 + 7 + 7 + 7 + 3 + 3 + 1 + 1 + 1 + 1 + 1 + 1", font_size=50).next_to(tex_group, DOWN, buff=1.25)
        self.add(tex_group, part)


class ResultVisual(Scene):
    def construct(self):
        midline = Line(config.frame_y_radius*UP, config.frame_y_radius*DOWN, color=WHITE, stroke_width=5)
        label_unique = Tex("different parts", font_size=50).to_edge(UP).set_x(-config.frame_x_radius/2)
        label_odd = Tex("odd parts", font_size=50).to_edge(UP).set_x(config.frame_x_radius/2)
        self.play(Write(label_odd), Write(label_unique), Create(midline))
        self.wait()
        
        for ind, n in enumerate([6, 10, 15, 20]):
            n_label = MathTex(f"n = {n}", font_size=75).to_edge(UP).add_background_rectangle(config.background_color, opacity=1)
            unique_partititons = [pt for pt in partitions(n) if len(pt) == len(set(pt))]
            YT_map = {
                YoungTableau(*pt[::-1]): YoungTableau(*unique_to_odd(pt)) for pt in unique_partititons
            }
            unique_YT = VGroup(*YT_map.keys()).arrange_in_grid(cols=ind+2, buff=(1, 2))
            odd_YT = VGroup(*YT_map.values()).arrange_in_grid(buff=1)
            for yt in [unique_YT, odd_YT]:
                yt.set_style(
                    stroke_color="#455D3E",
                    stroke_width=2,
                    fill_color=WHITE,
                    fill_opacity=1
                )
                if yt.width / (config.frame_x_radius - 1) >= yt.height / (config.frame_height - 2.5):
                    yt.scale_to_fit_width(config.frame_x_radius - 1)
                else:
                    yt.scale_to_fit_height(config.frame_height - 2.5)
            unique_YT.next_to(label_unique, DOWN, buff=1)
            odd_YT.next_to(label_odd, DOWN, buff=1)

            bijection = VGroup(*[
                ArcBetweenPoints(
                    k.get_center(), v.get_center(),
                    angle=-TAU/4, stroke_width=2,
                    color=ORANGE, stroke_opacity=0.5)
                for k, v in YT_map.items()
            ])

            self.play(FadeIn(n_label), Write(unique_YT), Write(odd_YT))
            self.play(Write(bijection))
            self.wait(0.5)
            self.play(FadeOut(unique_YT, odd_YT, bijection, n_label, shift=UP))
            self.wait()



class Thumbnail(Scene):
    def construct(self):
        pts = sorted(partitions(13), reverse=True, key=lambda pt: pt[::-1])
        yts = [
            YoungTableau(*partition[::-1], square_length=1)\
                .set_submobject_colors_by_gradient(RED, YELLOW)\
                .set_style(stroke_color=BH_DARKGREEN, fill_opacity=1)
            for partition in pts]
        current = yts[0]

        yts_bg = VGroup(*[yt.copy().set_style(stroke_width=2, fill_color=WHITE, fill_opacity=0.1) for yt in yts])
        yts_bg.arrange_in_grid(8, 13, buff=2).scale_to_fit_width(config.frame_width - 0.5)
        self.add(yts_bg)

        title = MathTex("13 = 13.").scale_to_fit_width(config.frame_width-2)
        self.add(title)