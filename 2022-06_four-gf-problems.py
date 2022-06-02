import random

from collections import defaultdict
from manim import *

BH_DARKGREEN = '#455D3E'
BH_ORANGE = '#E68330'

custom_tex_template = TexTemplate(
    documentclass=r"\documentclass[preview, varwidth=285px]{standalone}"
)
custom_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")
MathTex.set_default(tex_template=custom_tex_template)

config.background_color = BH_DARKGREEN

class ScrollingEquation(VGroup):
    def __init__(self, lhs, *rhs, **kwargs):
        self.equation = MathTex(
            lhs + "= {}",
            *[f" & {line} " + r"\\" for line in rhs],
            **kwargs
        )
        self.displayed_index = 1
        for i in range(len(rhs) - 1):
            self.equation[2 + i].set_opacity(0)
        super().__init__(*self.equation)

    @property
    def current_equation(self):
        return VGroup(self.equation[0], self.equation[self.displayed_index])

    @property
    def previous_rhs(self):
        return self.equation[self.displayed_index - 1]

    
    def next_equation(self, offset=0):
        current_rhs = self.equation[self.displayed_index]  
        next_rhs = self.equation[self.displayed_index+1]
        next_rhs.set_opacity(0)
        y_diff = current_rhs.get_y() - next_rhs.get_y() + offset
        shift_old_parts = []
        for i in range(1, self.displayed_index + 1):
            anim = self.equation[i].animate.shift(UP * y_diff)
            if abs(i - self.displayed_index) >= 1:
                anim.set_opacity(0)
            if i == self.displayed_index:
                anim.set_opacity(0.3)
            shift_old_parts.append(anim)
        anims = AnimationGroup(
            *shift_old_parts,
            next_rhs.animate.shift(UP * y_diff).set_opacity(1)
        )
        self.equation[self.displayed_index + 2:].shift(UP * y_diff)
        self.displayed_index += 1
        return anims

    def get_critical_point(self, direction):
        return VGroup(self.equation[:self.displayed_index + 1]).get_critical_point(direction)

class Problem1(Scene):
    def construct(self):
        title = Title("Problem 1: The Generating Function and the Die").to_edge(UP)
        p1_statement = Tex(
            r"\fontsize{11}{14}\selectfont Take the derivative of both sides of",
            r"\[ \frac{1}{1-x} = \sum_{n\geq 0} x^n. \]",
            "How can you use this to compute the expected number of times you "
            "have to roll a fair six-sided die before seeing the number 1?",
            tex_environment="flushleft",
        ).scale_to_fit_width(0.9*config.frame_width).next_to(title, DOWN, buff=1)

        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(Write(p1_statement[:2]), run_time=3)
        self.wait()
        self.play(Write(p1_statement[2:]), run_time=4)
        self.wait()

        # second part first
        self.play(Indicate(p1_statement[2], scale_factor=1.05, color=BH_ORANGE, run_time=2))
        self.wait()

        self.play(FadeOut(title, p1_statement, shift=DOWN))
        self.wait()



class ThrowDiagram(Scene):
    def construct(self):
        N = 7
        dots = VGroup(*[Dot() for i in range(N)]).arrange(RIGHT, buff=2)
        arrows_right = VGroup(*[Arrow(dots[i], dots[i+1], buff=0.2) for i in range(N-1)])
        five_sixths = VGroup(*[MathTex(r"\frac{5}{6}", font_size=36).next_to(arrows_right[i], UP) for i in range(N-1)])
        dots[-1].set_opacity(0)
        arrows_right[-1].set_opacity(0.5)
        five_sixths[-1].set_opacity(0.5)
        etc = MathTex(r"\cdots").move_to(dots[-1]).shift(RIGHT*0.25).set_opacity(0.25)
        outcomes = VGroup(*[MathTex(str(i)).move_to(dots[i]).shift(2*DOWN + 0.75*RIGHT) for i in range(N-1)]).set_color_by_gradient(WHITE, BH_ORANGE)
        arrows_down = VGroup(*[Arrow(dots[i], outcomes[i], buff=0.2) for i in range(N-1)])
        one_sixths = VGroup(*[MathTex(r"\frac{1}{6}", font_size=36).next_to(arrows_down[i], RIGHT) for i in range(N-1)]) 

        diagram = VGroup(dots, arrows_right, arrows_down, five_sixths, one_sixths, outcomes, etc)
        diagram.center()
        
        self.wait()
        self.play(FadeIn(dots[0]))
        self.wait()
        self.play(Write(one_sixths[0]), Write(arrows_down[0]), Write(outcomes[0]))
        self.wait()
        self.play(Write(arrows_right[0]), Write(five_sixths[0]), FadeIn(dots[1]))

        for i in range(1, N-1):
            self.play(
                Write(one_sixths[i]),
                Write(arrows_down[i]),
                Write(outcomes[i]),
            )
            self.play(
                Write(arrows_right[i]),
                Write(five_sixths[i]),
                FadeIn(dots[i+1])
            )
            self.wait()
        
        self.play(Write(etc))
        self.wait()

        # construction of expected value
        self.play(diagram.animate.to_edge(UP))
        self.wait()
        
        expectation = MathTex(
            r"\mathbb{E} &= ", 
            r"0\cdot \frac{1}{6}", 
            r"+ 1\cdot \frac{5}{6} \cdot \frac{1}{6}",
            r"+ 2\cdot \bigg(\frac{5}{6}\bigg)^2 \frac{1}{6}",
            r"+ 3\cdot \bigg(\frac{5}{6}\bigg)^3 \frac{1}{6}",
            r"+ \cdots\\",
            r"&= \sum_{n\geq 0} n\cdot \frac{1}{6} \cdot \bigg(\frac{5}{6}\bigg)^n \\",
            r"&= \frac{1}{6}\cdot \sum_{n\geq 0} n\cdot \bigg(\frac{5}{6}\bigg)^n"
        )
        expectation.scale_to_fit_width(0.8*config.frame_width).next_to(diagram, DOWN, buff=1)
        self.play(Write(expectation[0]))
        self.wait()
        diagram.save_state()
        self.play(VGroup(arrows_down[0]).animate.set_color(BH_ORANGE))
        self.play(ReplacementTransform(outcomes[0].copy(), expectation[1][0]))
        self.play(ReplacementTransform(arrows_down[0].copy(), expectation[1][1:]))
        self.play(Restore(diagram))
        self.wait()
        for i in range(1, 4):
            self.play(
                VGroup(*[arrows_right[k] for k in range(i)], arrows_down[i]).animate.set_color(BH_ORANGE)
            )
            self.play(
                Write(expectation[i+1][0]),
                ReplacementTransform(outcomes[i].copy(), expectation[i+1][1])
            )
            self.play(ReplacementTransform(arrows_down[i].copy(), expectation[i+1][2:]))
            self.play(Restore(diagram))
            self.wait()

        self.play(Write(expectation[5]))
        self.wait()
        self.play(Write(expectation[6]))
        self.wait()
        expectation[7].set_y(expectation[0].get_y())
        self.play(
            expectation[6].animate.set_y(expectation[0].get_y()),
            expectation[6][0].animate.set_opacity(0),
            FadeOut(expectation[1:6])
        )

        self.wait()
        self.play(TransformMatchingShapes(expectation[6][1:10], expectation[7][1:10], transform_mismatches=True))
        self.wait()
        self.play(Indicate(VGroup(expectation[0], expectation[6][10:], expectation[7][1:10]), color=BH_ORANGE))
        self.wait()
        


class GeometricSeries(Scene):
    def construct(self):
        geo_sum = MathTex(r"\frac{1}{1-x}", "=", r"\sum_{n\geq 0} x^n", font_size=42)
        self.wait()
        self.play(Write(geo_sum), run_time=2)
        self.wait()

        self.play(FadeOut(geo_sum, shift=UP))

        # proof of geometric series
        s_eq = MathTex(
            r"S_n &= 1 + x + x^2 + \cdots + x^n\\", 
            r"-x S_n &= -x - x^2 - \cdots - x^n - x^{n+1}\\",
            r"S_n - x S_n &= 1 - x^{n+1}",
            font_size=56
        ).center()
        self.play(Write(s_eq[0]))
        self.wait()
        self.play(Write(s_eq[1]))
        self.wait()
        ul = Underline(s_eq[1])
        self.play(Create(ul))
        s_eq[2].next_to(ul, DOWN, coor_mask=np.array([0, 1, 0]))
        self.play(Write(s_eq[2]))
        self.wait()
        self.play(
            FadeOut(s_eq[:2], ul, shift=UP),
            s_eq[2].animate.center()
        )
        self.wait()
        factored_lhs = MathTex("S_n", "(", "1 - x", ")", "=", "1 - x^{n+1}", font_size=56)
        s_n_eq = MathTex(r"S_n", "=", "{", "1 - x^{n+1}", "\over", "1 - x", "}", font_size=56)
        self.play(TransformMatchingShapes(s_eq[2], factored_lhs, fade_transform_mismatches=True))
        self.wait()
        self.play(TransformMatchingTex(factored_lhs, s_n_eq))
        self.wait()

        self.play(s_n_eq.animate.to_edge(UP))
        self.wait()

        ax = Axes(x_range=(1, 40), y_range=(0, 1), x_length=9, y_length=3, tips=False)
        y_lab = MathTex("x^{n+1}").next_to(ax.y_axis, UP)
        x_lab = MathTex("n").next_to(ax.x_axis, RIGHT)
        plots = VGroup(*[
            ax.plot(lambda n: x**n) for x in [0.95, 0.9, 0.75, 0.5, 0.3, 0.1, 0.01]
        ]).set_color_by_gradient(BH_ORANGE, YELLOW)
        self.play(Create(ax))
        self.play(Write(x_lab), Write(y_lab))
        self.play(Write(plots))
        self.wait()

        self.play(FadeOut(ax, x_lab, y_lab, plots))
        self.wait()

        geom_limit = MathTex(r"1 + x + x^2 + x^3 + \cdots = \frac{1 - 0}{1 - x}")
        arr = Arrow(s_n_eq.get_edge_center(DOWN), geom_limit.get_edge_center(UP))
        lim_lab = MathTex(r"n\to\infty").next_to(arr, RIGHT)
        geom_limit.shift(1.5*LEFT)
        
        self.play(Create(arr), Write(lim_lab))
        self.play(Write(geom_limit))
        self.wait()
        frac_num = geom_limit[0][14:17]
        just_one = MathTex("1").scale_to_fit_height(frac_num.height).move_to(frac_num)
        self.play(ReplacementTransform(frac_num, just_one))
        self.wait()



class GeometricDerivative(Scene):
    def construct(self):
        geo_sum = MathTex(
            r"\frac{1}{1-x}", "=", r"\sum_{n\geq 0} x^n",
            font_size=42
        ).to_edge(UP)
        self.wait()
        self.play(Write(geo_sum), run_time=2)
        self.wait()

        LHS = ScrollingEquation(
            r"\frac{\partial}{\partial x} \frac{1}{1-x}",
            r"\frac{\partial}{\partial x} (1 - x)^{-1}",
            r"(-1)\cdot (1 - x)^{-2} \cdot (-1)",
            r"\frac{1}{(1 - x)^2}",
            font_size=42
        ).center().to_edge(LEFT, buff=1)
        self.play(ReplacementTransform(geo_sum[0].copy(), LHS[0][4:9]))
        self.play(Write(LHS[0][:4]), Write(LHS[0][9:]), Write(LHS[1]))
        self.wait()
        self.play(LHS.next_equation())
        self.wait()
        self.play(LHS.next_equation())
        self.wait()


        RHS = ScrollingEquation(
            r"\frac{\partial}{\partial x} \sum_{n\geq 0} x^n",
            r"\sum_{n\geq 0} \frac{\partial}{\partial x} x^n",
            r"\sum_{n\geq 0} n\cdot x^{n-1}",
            font_size=42,
        ).center().to_edge(RIGHT, buff=1)
        self.play(ReplacementTransform(geo_sum[2].copy(), RHS[0][4:10]))
        self.play(Write(RHS[0][:4]), Write(RHS[0][10:]), Write(RHS[1]))
        self.wait()
        self.play(RHS.next_equation(offset=-0.07))
        self.wait()

        derivative_identity = MathTex(
            r"\frac{1}{(1-x)^2}", "=", r"\sum_{n\geq 0} n\cdot x^{n-1}",
            font_size=42
        ).to_edge(DOWN)
        self.play(
            ReplacementTransform(LHS[-1].copy(), derivative_identity[0]),
            ReplacementTransform(RHS[-1].copy(), derivative_identity[2]),
        )
        self.play(Write(derivative_identity[1]))
        self.wait()
        self.play(Indicate(derivative_identity, color=BH_ORANGE))
        self.wait()

        # move up identity, arrow for multiplication with x

        derivative_identity.generate_target()
        mult_arrow = Arrow(UP, DOWN, buff=0)
        arrow_label = MathTex(r"{} \cdot x", font_size=36)
        derivative_identity_mult_x = MathTex(
            r"\frac{x}{(1-x)^2}", "=", r"\sum_{n\geq 0} n\cdot x^{n}",
            font_size=42
        )
        VGroup(
            derivative_identity.target,
            mult_arrow,
            derivative_identity_mult_x
        ).arrange(DOWN)
        arrow_label.next_to(mult_arrow, RIGHT, buff=0)

        self.play(
            FadeOut(geo_sum, LHS, RHS),
            MoveToTarget(derivative_identity)
        )
        self.wait()
        self.play(
            Create(mult_arrow),
            Write(arrow_label),
        )
        self.wait()
        self.play(Write(derivative_identity_mult_x))
        self.wait()

        derivative_identity_mult_x.generate_target()

        final_eq = MathTex(
            r"\mathbb{E} = \frac{1}{6}\cdot \sum_{n\geq 0} n\cdot \bigg(\frac{5}{6}\bigg)^n",
            "=",
            r"\frac{1}{6}\cdot \frac{5/6}{(1 - 5/6)^2} = \frac{1}{6} \cdot 30 = 5",
            font_size=42,
        )

        VGroup(
            derivative_identity_mult_x.target,
            final_eq
        ).arrange(DOWN, buff=2).shift(UP)

        self.play(
            FadeOut(derivative_identity, mult_arrow, arrow_label, shift=UP),
            MoveToTarget(derivative_identity_mult_x)
        )
        self.wait()
        self.play(Write(final_eq[:2]))
        argument_arrow = Arrow(
            derivative_identity_mult_x[1].get_edge_center(DOWN) + 0.1*DOWN,
            final_eq[1].get_edge_center(UP) + 0.1*UP,
        )
        argument_label = MathTex(
            r"x = \frac{5}{6}",
            font_size=30,
        ).next_to(argument_arrow, RIGHT, buff=0)
        self.play(
            Create(argument_arrow),
            Write(argument_label)
        )
        self.wait()
        self.play(Write(final_eq[2:]))
        self.wait()
        result = Tex(
            "There are $\mathbb{E} = 5$ expected throws before we roll a 1 with a fair die."
        ).next_to(final_eq, DOWN, buff=0.5)
        ul = Underline(result, color=BH_ORANGE)
        self.play(Write(result))
        self.play(ShowPassingFlash(ul, run_time=2))
        self.wait()



class Problem2(Scene):
    def construct(self):
        title = Title("Problem 2: A Binomial Sum").to_edge(UP)
        statement = Tex(
            r"\fontsize{11}{14}\selectfont Compute the sum ",
            r"\[ \sum_{k=0}^n \binom{n}{k} 2^k. \]",
            tex_environment="flushleft",
        ).next_to(title, DOWN, buff=1)
        statement[0].to_edge(LEFT, buff=0).shift(0.05*config.frame_width * RIGHT)

        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(Write(statement), run_time=3)
        self.wait()

        self.play(FadeOut(title, statement, shift=DOWN))
        self.wait()

        # binomial theorem
        binomial_theorem = MathTex(
            r"(a + b)^n",
            "=",
            r"\sum_{k=0}^n \binom{n}{k} a^k\, b^{n-k}",
            font_size=56
        )
        self.play(Write(binomial_theorem))
        a_subs = MathTex("a = x", font_size=42)
        b_subs = MathTex("b = 1", font_size=42)
        x = MathTex("x", font_size=56)
        one = MathTex("1", font_size=56)
        VGroup(
            a_subs, b_subs
        ).arrange(RIGHT, buff=2).next_to(binomial_theorem, UP, buff=1)
        self.play(Write(a_subs), Write(b_subs))
        self.wait()

        first_x = x.copy().move_to(binomial_theorem[0][1])
        self.play(
            Transform(
                binomial_theorem[0][1],
                first_x
            ),
            FadeTransform(a_subs[0][2].copy(), first_x),
        )
        second_x = x.copy().move_to(binomial_theorem[2][9])
        self.play(
            Transform(
                binomial_theorem[2][9],
                second_x
            ),
            FadeTransform(a_subs[0][2].copy(), second_x),
        )
        self.wait()

        first_one = one.copy().move_to(binomial_theorem[0][3])
        self.play(
            Transform(
                binomial_theorem[0][3],
                first_one
            ),
            FadeTransform(b_subs[0][2].copy(), first_one),
        )
        second_one = one.copy().move_to(binomial_theorem[2][11])
        self.play(
            Transform(
                binomial_theorem[2][11],
                second_one
            ),
            FadeTransform(b_subs[0][2].copy(), second_one),
        )
        self.wait()

        self.remove(first_x, second_x, first_one, second_one)
        one_power = binomial_theorem[2][-4:]
        self.play(
            FadeOut(one_power)
        )
        binomial_theorem[2].remove(*one_power)
        self.wait()

        subs_arrow = Arrow(UP, DOWN)
        arrow_label = MathTex("x = 2", font_size=42)
        identity = MathTex(
            r"(2 + 1)^n",
            "=",
            r"\sum_{k=0}^n \binom{n}{k} 2^k",
            font_size=56
        )

        binomial_theorem.generate_target()

        VGroup(
            binomial_theorem.target,
            subs_arrow,
            identity,
        ).arrange(DOWN)
        arrow_label.next_to(subs_arrow, RIGHT, buff=0)

        self.play(
            FadeOut(a_subs, b_subs, shift=UP),
            MoveToTarget(binomial_theorem),
        )
        self.wait()
        self.play(
            Create(subs_arrow),
            Write(arrow_label),
        )
        self.wait()
        self.play(Write(identity))
        self.wait()
        eval_lhs = MathTex(
            "3^n", font_size=56
        ).move_to(identity[0].get_right(), aligned_edge=RIGHT)
        self.play(
            Transform(identity[0], eval_lhs)
        )
        self.wait()
        ul = Underline(identity, color=BH_ORANGE)
        self.play(ShowPassingFlash(ul, run_time=2))
        self.wait()

        # setup combinatorial proof
        self.play(FadeOut(*[mob for mob in self.mobjects if mob != identity]))
        self.wait()
        self.play(identity.animate.center().to_edge(UP))
        ul = Underline(identity, buff=0.2)
        separator = Line(
            ul.get_y()*UP,
            config.frame_y_radius*DOWN,
            stroke_width=5
        )
        
        self.play(Create(separator), Create(ul))
        self.wait()

        left_circles = VGroup(*[
            Dot(stroke_color=BLACK, stroke_width=1) for _ in range(6*7)
        ]).arrange_in_grid(6, 7, buff=0.1).scale_to_fit_width(0.4*config.frame_width)
        left_circles.to_corner(LEFT + DOWN)

        right_circles = left_circles.copy().to_corner(RIGHT + DOWN)
        self.play(FadeIn(left_circles, right_circles))

        # color left group: one ball at a time
        color_dict = {
            ind: random.choice([RED, GREEN, BLUE])
            for ind in range(42)
        }
        self.play(
            AnimationGroup(*[
                circle.animate.set_style(fill_color=color_dict[ind])
                for ind, circle in enumerate(left_circles)
            ], lag_ratio=0.5, run_time=10)
        )
        self.wait()

        self.play(*[
            circle.animate.set_style(fill_color=[RED, GREEN])
            for ind, circle in enumerate(right_circles)
            if color_dict[ind] in [RED, GREEN]
        ])
        self.wait(0.5)
        self.play(*[
            circle.animate.set_style(fill_color=BLUE)
            for ind, circle in enumerate(right_circles)
            if color_dict[ind] == BLUE
        ])
        self.wait()
        self.play(
            AnimationGroup(*[
                circle.animate.set_style(fill_color=color_dict[ind])
                for ind, circle in enumerate(right_circles)
                if color_dict[ind] in [RED, GREEN]
            ], lag_ratio=0.5, run_time=7)
        )
        self.wait()
        



class Problem3(Scene):
    def construct(self):
        title = Title("Problem 3: Fibonacci and a Differential Equation").to_edge(UP)
        statement = Tex(
            r"\fontsize{11}{14}\selectfont Let $f_n$ be the $n$-th Fibonacci number"
            " and consider the generating function",
            r"\[ F(x) = \sum_{n\geq 0} f_n \frac{x^n}{n!}. \]",
            "Explain why the differential equation $F''(x) = F'(x) + F(x)$"
            " is true. ", "For bonus points, solve this equation and use it to"
            " find a closed-form expression for $f_n$.",
            tex_environment="flushleft",
        ).scale_to_fit_width(0.9*config.frame_width).next_to(title, DOWN, buff=1)
        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(Write(statement[0:2]), run_time=3)
        self.wait()
        self.play(Write(statement[2]), run_time=2)
        self.wait()
        self.play(Write(statement[3], run_time=2))
        self.wait()
        exp_gf = statement[1]
        self.play(
            FadeOut(title, statement[0], shift=UP),
            FadeOut(statement[2:], shift=DOWN),
            exp_gf[:-1].animate.center().shift(DOWN),
            FadeOut(exp_gf[-1]),
        )
        exp_gf.remove(exp_gf[-1])
        self.wait()

        gf_label = Tex(r"``Exponential Generating Function''").next_to(exp_gf, DOWN, buff=1)
        self.play(Indicate(exp_gf[14:16], color=BH_ORANGE))
        self.play(Write(gf_label))

        exp_as_gf = MathTex(
            r"e^x", 
            r"= 1 + 1\cdot\frac{x}{1!} + 1\cdot\frac{x^2}{2!} + 1\cdot\frac{x^3}{3!} + \cdots",
            r"= \sum_{n\geq 0} 1\cdot \frac{x^n}{n!}",
        )
        constant_sequence = MathTex(
            r"(1, 1, 1, 1, \dots) \leftrightsquigarrow e^x"
        )
        VGroup(exp_as_gf, constant_sequence).arrange(DOWN).next_to(exp_gf, UP, buff=2)
        exp_arr = CurvedArrow(gf_label.get_left() + LEFT*0.1, exp_as_gf[0].get_corner(DL), angle=-TAU/4)
        self.play(
            Create(exp_arr),
            Write(exp_as_gf[0])
        )
        self.wait(0.5)
        self.play(
            Write(exp_as_gf[1:])
        )
        self.wait()
        self.play(Write(constant_sequence))

        self.wait()
        self.play(
            FadeOut(exp_arr, shift=LEFT),
            FadeOut(exp_as_gf, constant_sequence, shift=UP),
            FadeOut(gf_label, shift=DOWN),
            exp_gf.animate.to_edge(UP)
        )

        derivative = ScrollingEquation(
            r"F'(x)",
            r"\frac{\partial\,}{\partial x} \sum_{n\geq 0} f_n \frac{x^n}{n!}",
            r"\frac{\partial\,}{\partial x} \left(f_0 + f_1x + f_2 \frac{x^2}{2!} + f_3 \frac{x^3}{3!} + f_4 \frac{x^4}{4!} + \cdots\right)",
            r"\frac{\partial\,}{\partial x} f_0 +  \frac{\partial\,}{\partial x} f_1x + \frac{\partial\,}{\partial x} f_2 \frac{x^2}{2!} + \frac{\partial\,}{\partial x} f_3 \frac{x^3}{3!} + \frac{\partial\,}{\partial x} f_4 \frac{x^4}{4!} + \cdots",
            r"0 + f_1 + f_2 \frac{2\cdot x^{2-1}}{2!} + f_3 \frac{3\cdot x^{3-1}}{3!} + f_4 \frac{4\cdot x^{4-1}}{4!}  + \cdots",
            r"f_1 + f_2 \frac{x^{1}}{1!} + f_3 \frac{x^{2}}{2!} + f_4 \frac{x^{3}}{3!} + \cdots",
            r"\sum_{n\geq 0} f_{n+1} \frac{x^n}{n!}"
        )
        VGroup(*derivative).next_to(exp_gf, DOWN, buff=3)
        self.play(
            Write(derivative)
        )
        self.wait()
        offset_dict = defaultdict(float)
        offset_dict[0] = 0.1
        for i in range(len(derivative) - 2):
            self.play(derivative.next_equation(offset=offset_dict[i]))
            self.wait()
        
        d1 = derivative.current_equation
        self.play(
            FadeOut(derivative[-2]),
            d1.animate.next_to(exp_gf, DOWN)    
        )

        second_derivative = ScrollingEquation(
            r"F''(x)",
            r"\sum_{n\geq 0} f_{n+2} \frac{x^n}{n!}",
            r"\sum_{n\geq 0} (f_{n+1} + f_n) \frac{x^n}{n!}",
            r"\sum_{n\geq 0} f_{n+1} \frac{x^n}{n!} + \sum_{n\geq 0} f_{n} \frac{x^n}{n!}",
            r"F'(x) + F(x)",
        ).next_to(d1, DOWN)
        self.wait()
        self.play(Write(second_derivative))

        fibonacci_recurrence = MathTex("f_{n+2} = f_{n+1} + f_n")
        exp_gf.generate_target()
        d1.generate_target()
        VGroup(exp_gf.target, d1.target, fibonacci_recurrence).arrange(RIGHT, buff=1.5).to_edge(UP)
        ul = Line(
            config.frame_x_radius*LEFT + (exp_gf.get_y(DOWN) - 0.25)*UP, 
            config.frame_x_radius*RIGHT + (exp_gf.get_y(DOWN) - 0.25)*UP,
            stroke_width=5
        )
        self.play(
            MoveToTarget(exp_gf),
            MoveToTarget(d1),
            Create(ul)
        )
        self.wait()
        self.play(Write(fibonacci_recurrence))
        self.play(VGroup(*second_derivative).animate.move_to(ORIGIN, coor_mask=RIGHT).shift(DOWN))
        self.play(second_derivative.next_equation())
        self.wait()
        self.play(second_derivative.next_equation())
        self.wait()
        self.play(second_derivative.next_equation(offset=0.1))
        self.wait()
        self.play(
            FadeOut(second_derivative.previous_rhs),
            second_derivative.current_equation.animate.center()
        )
        ul_emph = Underline(second_derivative.current_equation, color=BH_ORANGE)
        self.play(ShowPassingFlash(ul_emph, run_time=2))

        self.wait()
        self.play(
            Uncreate(ul),
            FadeOut(exp_gf, shift=UP),
            FadeOut(derivative.current_equation, shift=UP),
        )
        self.play(
            second_derivative.current_equation.animate.move_to(DOWN),
            fibonacci_recurrence.animate.move_to(UP)
        )
        self.wait()


class SolveODE(Scene):
    def construct(self):
        diff_eq = MathTex("F''(x)", "-", "F'(x)", "-", "F(x)", "= 0").to_edge(UP)
        self.add(diff_eq)
        self.wait()

        ansatz_label = Tex(
            r"\emph{Ansatz}: ``guess'' shape of solution\\ and see how far we can take it."
        )
        ansatz = VGroup(
            MathTex("F(x) = ", r"e^{\lambda x}"),
            MathTex("F'(x) = ", r"\lambda e^{\lambda x}"),
            MathTex("F''(x) = ", r"\lambda^2 e^{\lambda x}"),
        ).arrange(RIGHT, buff=1.5).shift(1.5*UP)
        VGroup(ansatz_label, ansatz).arrange(DOWN, buff=1)
        self.play(Write(ansatz_label))
        self.play(Write(ansatz))
        plugging_in = diff_eq.copy()
        self.play(plugging_in.animate.next_to(ansatz, DOWN, buff=1))
        self.wait()
        F_rhs = ansatz[0][1].copy()
        Fd_rhs = ansatz[1][1].copy()
        Fdd_rhs = ansatz[2][1].copy()
        self.play(
            F_rhs.animate.move_to(plugging_in[4]),
            FadeOut(plugging_in[4])
        )
        self.play(
            Fd_rhs.animate.move_to(plugging_in[2]),
            FadeOut(plugging_in[2])
        )
        self.play(
            Fdd_rhs.animate.move_to(plugging_in[0]),
            FadeOut(plugging_in[0])
        )
        plugging_in.remove(plugging_in[0], plugging_in[2], plugging_in[4])
        self.wait()
        factored_eq = MathTex(
            r"e^{\lambda x} (\lambda^2 - \lambda - 1) = 0"
        ).move_to(plugging_in)
        self.play(
            FadeTransform(VGroup(F_rhs, Fd_rhs, Fdd_rhs, plugging_in), factored_eq),
        )
        self.wait()
        self.play(
            FadeOut(factored_eq[0][:4], factored_eq[0][-3])
        )
        factored_eq[0].remove(*factored_eq[0][:4], factored_eq[0][-3])
        self.wait()

        self.play(factored_eq.animate.shift(LEFT*6))

        lambdas = VGroup(
            MathTex(r"\lambda_+ = \frac{1 + \sqrt{5}}{2}"),
            MathTex(r"\lambda_- = \frac{1 - \sqrt{5}}{2}")
        ).arrange(RIGHT, buff=1).next_to(factored_eq, RIGHT, buff=3)
        arr = Arrow(factored_eq.get_right(), lambdas.get_left())
        self.play(Create(arr))
        self.play(Write(lambdas))

        lambdas.generate_target()
        lambdas.target.to_corner(UR)

        self.wait()
        self.play(
            FadeOut(arr, ansatz, ansatz_label, factored_eq, shift=DOWN),
            lambdas.animate.to_corner(UR),
            diff_eq.animate.next_to(lambdas.target, RIGHT).to_edge(LEFT)
        )
        aux_info = VGroup(diff_eq, lambdas)


        general_solution = Tex(
            "General solution: ", "$F(x) = c_+ e^{\lambda_+ x} + c_- e^{\lambda_- x}$"
        ).next_to(aux_info, DOWN, buff=0.5)
        gdiff = Tex(
            "$F'(x) = c_+ \lambda_+ e^{\lambda_+ x} + c_- \lambda_- e^{\lambda_- x}$"
        ).next_to(general_solution[1], DOWN)
        we_want = Tex(
            "We want $F$ with ", "$F(0) = f_0 = 0$ ", "and ", "$F'(0) = f_1 = 1$"
        ).next_to(general_solution, DOWN, buff=2)

        self.play(Write(general_solution))
        self.wait()
        self.play(Write(we_want))
        self.wait()

        c_eqs = MathTex(
            r"c_+ + c_- &= 0 \\",
            r"c_+ \lambda_+ + c_- \lambda_- &= 1 \\",
            r"c_- &{} = - c_+ \\",
            r"c_+ \lambda_+ - c_+ \lambda_- &= 1 \\",
            r"c_+ (\lambda_+ - \lambda_-) &= 1 \\",
            r"c_+ &= 1/(\lambda_+ - \lambda_-) \\",
            r"c_+ &= 1/\sqrt{5} \\",
            r"c_- &= - 1/\sqrt{5} \\",
        ).next_to(we_want, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(VGroup(we_want[1].copy(), general_solution[1].copy()), c_eqs[0]),
        )
        self.wait()
        self.play(Write(gdiff))
        self.play(
            ReplacementTransform(VGroup(we_want[3].copy(), gdiff[0].copy()), c_eqs[1]),
        )
        self.wait()

        c_eqs[2].move_to(c_eqs[0], coor_mask=UP)
        c_eqs[7].move_to(c_eqs[0], coor_mask=UP)
        for ind in [3, 4, 5, 6]:
            c_eqs[ind].move_to(c_eqs[1], coor_mask=UP)
        self.play(Transform(c_eqs[0], c_eqs[2]))
        self.wait()
        self.play(Transform(c_eqs[1], c_eqs[3]))
        self.wait()
        self.play(Transform(c_eqs[1], c_eqs[4]))
        self.wait()
        self.play(Transform(c_eqs[1], c_eqs[5]))
        self.wait()
        self.play(Transform(c_eqs[1], c_eqs[6]))
        self.wait()
        self.play(Transform(c_eqs[0], c_eqs[7]))
        self.wait()
        self.play(
            ShowPassingFlash(SurroundingRectangle(VGroup(c_eqs[0], c_eqs[1]), color=BH_ORANGE))
        )

        fibo_gf = ScrollingEquation(
            "F(x)",
            r"\frac{1}{\sqrt{5}} e^{\lambda_+ x} - \frac{1}{\sqrt{5}} e^{\lambda_- x}",
            r"\frac{1}{\sqrt{5}} \sum_{n\geq 0} \lambda_+^n \frac{x^n}{n!} "
            r"- \frac{1}{\sqrt{5}} \sum_{n\geq 0} \lambda_-^n \frac{x^n}{n!}",
            r"\sum_{n\geq 0} \frac{1}{\sqrt{5}} (\lambda_+^n - \lambda_-^n)\cdot \frac{x^n}{n!}"
        ).center()

        self.play(FadeOut(we_want, gdiff))
        self.play(
            FadeOut(general_solution[0]),
            ReplacementTransform(VGroup(general_solution[1], c_eqs[0], c_eqs[1]), fibo_gf.current_equation)
        )
        self.wait()
        self.play(fibo_gf.next_equation())
        self.wait()
        self.play(fibo_gf.next_equation())
        self.wait()

        binet = MathTex(
            r"f_n = \frac{1}{\sqrt{5}} \bigg(\bigg(\frac{1 + \sqrt{5}}{2}\bigg)^n - \bigg(\frac{1 - \sqrt{5}}{2}\bigg)^n\bigg)"
        ).shift(2.25*DOWN)

        self.play(Write(binet))
        self.play(ShowPassingFlash(Underline(binet, color=BH_ORANGE), run_time=2))
        self.wait()



class Problem4(Scene):
    def construct(self):
        title = Title("Problem 4: A Useful Product").to_edge(UP)
        statement = Tex(
            r"\fontsize{11}{14}\selectfont Suppose that $f(x) = \sum_{n\geq 0} a_n x^n$.",
            r" What do the coefficients of "
            r"\[ \frac{f(x)}{1-x}\]"
            r"tell you?",
            tex_environment="flushleft",
        ).scale_to_fit_width(0.9*config.frame_width).next_to(title, DOWN, buff=1)
        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(Write(statement[0]), run_time=2)
        self.wait()
        self.play(Write(statement[1]), run_time=2)
        self.wait()

        self.play(FadeOut(title, shift=UP), FadeOut(statement, shift=DOWN))

        product = ScrollingEquation(
            r"\frac{f(x)}{1 - x}",
            r"\frac{1}{1 - x} \sum_{\ell \geq 0} a_{\ell} x^{\ell}",
            r"\sum_{\ell\geq 0} a_{\ell} x^{\ell}\cdot \frac{1}{1 - x}",
            r"\sum_{\ell\geq 0} a_{\ell} x^{\ell} \cdot (1 + x + x^2 + x^3 + \cdots)",
            r"\sum_{\ell\geq 0} a_{\ell} (x^{\ell} + x^{\ell + 1} + x^{\ell + 2} + x^{\ell + 3} + \cdots)",
            r"\sum_{\ell\geq 0} a_{\ell} \sum_{n\geq \ell} x^n",
            r"\sum_{n\geq 0} \left( \sum_{\ell = 0}^n a_{\ell} \right) x^n",
        ).center().shift(UP)
        VGroup(*product).move_to(ORIGIN, coor_mask=RIGHT)

        expanded = VGroup(
            MathTex(r"a_0(1 + x + x^2 + x^3 + \cdots) + a_1 (x + x^2 + x^3 + \cdots) + a_2 (x^2 + x^3 + \cdots) + a_3 (x^3 + \cdots) + \cdots").scale_to_fit_width(0.9*config.frame_width),
            MathTex(r"a_0 + (a_0 + a_1) x + (a_0 + a_1 + a_2) x^2 + (a_0 + a_1 + a_2 + a_3) x^3 + \cdots"),
        ).arrange(DOWN, buff=0.5)

        axes = Axes(x_range=(-0.15, 6), y_range=(-0.15, 6), x_length=7, y_length=7)
        dots = VDict({(n, ell): Dot(color=ORANGE).move_to(axes.c2p(ell, n)) for ell in range(6) for n in range(ell, 6)})
        axes.x_axis.add_labels({k:k for k in range(6)})
        axes.y_axis.add_labels({k:k for k in range(6)})
        ell_lab = MathTex(r"\ell").next_to(axes.x_axis[0], RIGHT)
        n_lab = MathTex(r"n").next_to(axes.y_axis[0], UP)
        grid = VGroup(axes, dots, ell_lab, n_lab).scale(2/3).next_to(product.current_equation, RIGHT, buff=1).shift(1.5*DOWN)

        self.play(Write(product))
        self.wait()
        self.play(product.next_equation())
        self.wait()
        self.play(product.next_equation())
        self.wait()
        self.play(product.next_equation())
        self.wait()
        self.play(product.next_equation())
        self.wait()

        self.play(Create(grid))
        self.wait()
        self.play(AnimationGroup(*[
            Indicate(VGroup(*[dots[(n, ell)] for n in range(ell, 6)]))
            for ell in range(0, 6)
        ], lag_ratio=0.5))
        self.wait(0.5)
        self.play(AnimationGroup(*[
            Indicate(VGroup(*[dots[(n, ell)] for ell in range(n+1)]))
            for n in range(0, 6)
        ], lag_ratio=0.5))

        self.wait()

        self.play(product.next_equation(offset=0.15))
        self.wait()
        self.play(FadeOut(grid, shift=RIGHT))

        expanded.next_to(product, DOWN, buff=1)
        self.play(Write(expanded[0]))
        self.wait()
        self.play(Write(expanded[1]))
        self.wait()
        self.play(FadeOut(expanded, shift=DOWN))
        self.wait()

        result = Tex(
            r"The coefficients of $\frac{f(x)}{1 - x}$ are \\"
            r"partial sums of the coefficients of $f(x)$."
        ).to_edge(DOWN)
        self.play(Write(result))
        self.play(
            ShowPassingFlash(Underline(result, color=BH_ORANGE), run_time=2)
        )
        self.wait()


        




class OrderSummation(Scene):
    def construct(self):
        axes = Axes(x_range=(-0.15, 6), y_range=(-0.15, 6), x_length=7, y_length=7)
        dots = VGroup(*[Dot(color=ORANGE).move_to(axes.c2p(ell, n)) for ell in range(6) for n in range(ell, 6)])
        axes.x_axis.add_labels({k:k for k in range(6)})
        axes.y_axis.add_labels({k:k for k in range(6)})
        ell_lab = MathTex(r"\ell").next_to(axes.x_axis[0], RIGHT)
        n_lab = MathTex(r"n").next_to(axes.y_axis[0], UP)
        self.add(axes, dots, ell_lab, n_lab)
        VGroup(*self.mobjects).center()


class FourProblemsThumbnail(Scene):
    def construct(self):
        hl = Line(
            config.frame_x_radius*LEFT,
            config.frame_x_radius*RIGHT,
            color=WHITE,
            stroke_width=5
        )
        vl = Line(
            config.frame_y_radius*UP,
            config.frame_y_radius*DOWN,
            color=WHITE,
            stroke_width=5
        )
        p1 = MathTex(
            r"\frac{1}{1 - x} = \sum_{n\geq 0} x^n",
            font_size=60,
        ).move_to(config.frame_x_radius*1/2*LEFT + config.frame_y_radius*1/2*UP)
        p2 = MathTex(
            r"\sum_{k=0}^n \binom{n}{k} 2^k = {}?",
            font_size=60,
        ).move_to(config.frame_x_radius*1/2*RIGHT + config.frame_y_radius*1/2*UP)
        p3 = MathTex(
            r"F''(x) = F'(x) + F(x)",
            font_size=60,
        ).move_to(config.frame_x_radius*1/2*LEFT + config.frame_y_radius*1/2*DOWN)
        p4 = MathTex(
            r"[x^n] \frac{f(x)}{1 - x} = {}?",
            font_size=60,
        ).move_to(config.frame_x_radius*1/2*RIGHT + config.frame_y_radius*1/2*DOWN)
        self.add(hl, vl, p1, p2, p3, p4)