import numpy as np
from manim import *


class ThetaCreature(VGroup):
    """Channel mascot: a thick θ (ring + bar) with eyes and a mouth.

    `color` restyles it and `size` scales it (1.0 is about 2.4 units tall).
    Eyes sit above the bar; the mouth is a wavy black slot cut into the bar,
    which gives it a questioning, unsure look.
    """

    def __init__(self, color="#4FC3F7", size=1.0, **kwargs):
        super().__init__(**kwargs)
        s = size
        width, height, thickness = 1.5 * s, 2.2 * s, 18 * s

        self.ring = Ellipse(
            width=width, height=height, color=color, stroke_width=thickness
        )
        self.bar = Line(
            LEFT * (width / 2 - 0.03 * s),
            RIGHT * (width / 2 - 0.03 * s),
            color=color,
            stroke_width=thickness,
            cap_style=CapStyleType.ROUND,
        )
        self.eye_whites = VGroup(
            *[
                Circle(
                    radius=0.19 * s, stroke_width=0, fill_color=WHITE, fill_opacity=1
                ).move_to(RIGHT * x * s + UP * 0.48 * s)
                for x in (-0.3, 0.3)
            ]
        )
        self.pupils = VGroup(
            *[
                Dot(radius=0.085 * s, color=BLACK).move_to(eye.get_center())
                for eye in self.eye_whites
            ]
        )
        # Mouth: a wavy black slot on the bar (left end low, right end high).
        self.mouth_closed_width = 8 * s
        self.mouth_open_width = 13 * s
        self.mouth = CubicBezier(
            np.array([-0.22, -0.03, 0.0]) * s,
            np.array([-0.10, 0.14, 0.0]) * s,
            np.array([0.06, -0.16, 0.0]) * s,
            np.array([0.22, 0.04, 0.0]) * s,
            color=BLACK,
            stroke_width=self.mouth_closed_width,
            cap_style=CapStyleType.ROUND,
        )
        self.gaze_amount = 0.07 * s

        self.add(self.ring, self.bar, self.eye_whites, self.pupils, self.mouth)

    def _pupil_targets(self, direction):
        direction = np.array(direction, dtype=float)
        direction = direction / np.linalg.norm(direction)
        return [eye.get_center() + direction * self.gaze_amount for eye in self.eye_whites]

    def set_gaze(self, direction):
        """Point the pupils toward `direction` instantly."""
        for pupil, target in zip(self.pupils, self._pupil_targets(direction)):
            pupil.move_to(target)
        return self

    def gaze(self, direction):
        """Animations that move the pupils toward `direction`."""
        return [
            pupil.animate.move_to(target)
            for pupil, target in zip(self.pupils, self._pupil_targets(direction))
        ]

    def blink(self):
        """Animations for a blink; play with rate_func=there_and_back."""
        return [m.animate.stretch(0.1, 1) for m in (*self.eye_whites, *self.pupils)]

    def open_mouth(self):
        return [self.mouth.animate.set_stroke(width=self.mouth_open_width)]

    def close_mouth(self):
        return [self.mouth.animate.set_stroke(width=self.mouth_closed_width)]


def make_speech_bubble(
    width=3.8,
    height=1.8,
    tail_tip=RIGHT + DOWN,
    tail_angles=(-62, -25),
    points=240,
):
    """A speech bubble as ONE closed outline: an oval whose edge runs out to a
    pointed tail and back (no overlapping shapes).

    The bubble is built centered on the oval's center (ORIGIN); shift it into
    place afterwards. `tail_tip` is the tail's tip relative to that center and
    `tail_angles` (degrees) are where the tail leaves the oval.
    """
    a, b = width / 2, height / 2
    start = np.radians(tail_angles[1])
    end = np.radians(tail_angles[0]) + TAU
    outline = [
        np.array([a * np.cos(t), b * np.sin(t), 0.0])
        for t in np.linspace(start, end, points)
    ]
    bubble = VMobject(
        stroke_color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=1
    )
    bubble.set_points_as_corners([*outline, np.array(tail_tip, dtype=float), outline[0]])
    return bubble


class L1L2Video(Scene):
    def construct(self):
        title = Text(
            "What’s the difference between L1 and L2 regularization",
            font_size=48,
            weight=MEDIUM,
        )
        title.scale_to_fit_width(config.frame_width - 1.0)
        title.move_to(ORIGIN)

        # Section 1: write the question in the center.
        self.play(Write(title), run_time=1.8)

        # Section 2: move it upward to become the scene title.
        self.next_section("title_moves_up")
        self.play(title.animate.to_edge(UP, buff=0.55), run_time=1.2)
        self.wait(0.5)

        # Scene 2: a centered 3-3-1 network with indexed labels inside neurons.
        node_radius = 0.48
        network_shift = UP * 0.75  # raise the whole network so it clears the L1/L2 labels
        layer_positions = [
            [LEFT * 3.7 + UP * y + network_shift for y in (1.05, 0, -1.05)],
            [UP * y + network_shift for y in (1.05, 0, -1.05)],
            [RIGHT * 3.7 + network_shift],
        ]

        edges = VGroup()
        for source_layer, target_layer in zip(layer_positions, layer_positions[1:]):
            for source in source_layer:
                for target in target_layer:
                    direction = (target - source) / np.linalg.norm(target - source)
                    edges.add(
                        Line(
                            source + direction * node_radius,
                            target - direction * node_radius,
                            color=GRAY_B,
                            stroke_width=2,
                        )
                    )

        neurons = VGroup()
        weight_labels = VGroup()
        for layer_number, positions in enumerate(layer_positions, start=1):
            for neuron_number, position in enumerate(positions, start=1):
                neuron = Circle(
                    radius=node_radius,
                    stroke_color=BLUE_C,
                    stroke_width=2,
                    fill_color=BLACK,
                    fill_opacity=1,
                ).move_to(position)
                # Real LaTeX labels: W_{i,l} with proper subscripts.
                label = MathTex(
                    rf"W_{{{neuron_number},{layer_number}}}",
                    font_size=34,
                    color=YELLOW,
                ).move_to(position)
                neurons.add(VGroup(neuron, label))
                weight_labels.add(label)

        self.next_section("show_network_3_3_1")
        self.play(Create(edges), run_time=0.9)
        self.play(FadeIn(neurons, lag_ratio=0.12), run_time=0.9)

        # Keep the neuron labels in place; copies gather below to form a generic W.
        collection_center = LEFT * 2.75 + DOWN * 2.35
        gather_offsets = [
            LEFT * 0.18 + UP * 0.16,
            UP * 0.18,
            RIGHT * 0.18 + UP * 0.16,
            LEFT * 0.18,
            ORIGIN,
            RIGHT * 0.18,
            DOWN * 0.16,
        ]

        weight_copies = VGroup(*[label.copy() for label in weight_labels])
        self.add(weight_copies)
        self.next_section("gather_weights")
        self.play(
            *[
                label_copy.animate.move_to(collection_center + offset)
                for label_copy, offset in zip(weight_copies, gather_offsets)
            ],
            run_time=1.2,
        )
        collected_weight = MathTex(r"W", font_size=60, color=YELLOW).move_to(collection_center)
        self.play(ReplacementTransform(weight_copies, collected_weight), run_time=0.6)

        # ---- L1 expression: \sum_{i,l} |W_{i,l}| ----
        # Split into parts so only the weight is colored; \limits puts the
        # index under the sigma (display-style) like in a notebook.
        left_expression = MathTex(
            r"\sum\limits_{i,l}",
            r"\left|",
            r"W_{i,l}",
            r"\right|",
            font_size=64,
        )
        left_expression[2].set_color(YELLOW)
        left_expression.move_to(LEFT * 3.1 + DOWN * 2.45)
        left_label = MathTex(r"L_1", font_size=44, color=BLUE_C)
        left_label.next_to(left_expression, UP, buff=0.3)

        self.next_section("form_absolute_sum")
        self.play(
            FadeOut(collected_weight),
            Write(left_expression),
            FadeIn(left_label),
            run_time=0.9,
        )

        # ---- L2 expression: \sum_{i,l} W_{i,l}^2 ----
        right_expression = MathTex(
            r"\sum\limits_{i,l}",
            r"W_{i,l}^{2}",
            font_size=64,
        )
        right_expression[1].set_color(YELLOW)
        right_expression.move_to(RIGHT * 3.1 + DOWN * 2.45)
        right_label = MathTex(r"L_2", font_size=44, color=GREEN_C)
        right_label.next_to(right_expression, UP, buff=0.3)

        self.next_section("copy_sum_to_right")
        self.play(
            TransformFromCopy(left_expression, right_expression),
            FadeIn(right_label),
            run_time=1.0,
        )

        self.wait(0.5)

        # ---- Scene 3: remove L2, center L1 under the network ----
        self.next_section("l1_to_center")
        left_group = VGroup(left_expression, left_label)
        self.play(
            FadeOut(right_expression),
            FadeOut(right_label),
            left_group.animate.set_x(0),
            run_time=1.0,
        )

        # ---- Replace the symbolic weights with actual numbers ----
        # Red = weights that L1 will push to exactly zero, yellow = the rest.
        weight_values = [0.82, 0.07, -0.47, 0.12, 0.65, -0.09, 0.73]
        zero_indices = [1, 3, 5]
        flat_positions = [p for layer in layer_positions for p in layer]

        number_labels = VGroup()
        for idx, (value, position) in enumerate(zip(weight_values, flat_positions)):
            number = DecimalNumber(
                value,
                num_decimal_places=2,
                font_size=28,
                color=RED if idx in zero_indices else YELLOW,
                edge_to_fix=ORIGIN,  # keep the number centered while its value changes
            ).move_to(position)
            number_labels.add(number)

        # The shrinking weights grow a bit, change value, then return to normal size.
        emphasis = 1.3

        def grow(indices):
            return [number_labels[i].animate.scale(emphasis) for i in indices]

        def settle(indices):
            return [number_labels[i].animate.scale(1 / emphasis) for i in indices]

        self.next_section("weights_to_numbers")
        self.play(FadeOut(weight_labels), FadeIn(number_labels), run_time=1.0)
        self.wait(0.8)

        # "L1 regularization can push some weights all the way to zero,
        #  especially when the corresponding features aren't useful."
        self.next_section("l1_pushes_weights_to_zero")
        self.play(*grow(zero_indices), run_time=0.6)
        self.play(
            *[ChangeDecimalToValue(number_labels[i], 0) for i in zero_indices],
            run_time=2.5,
        )
        self.play(*settle(zero_indices), run_time=0.6)
        self.wait(1.0)

        # ---- Scene 4: swap L1 for L2, restore the weights, shrink them again ----
        self.next_section("l2_swap_and_restore")
        l2_expression = MathTex(
            r"\sum\limits_{i,l}",
            r"W_{i,l}^{2}",
            font_size=64,
        )
        l2_expression[1].set_color(YELLOW)
        l2_expression.move_to(left_expression.get_center())
        l2_label = MathTex(r"L_2", font_size=44, color=GREEN_C)
        l2_label.next_to(l2_expression, UP, buff=0.3)

        self.play(
            FadeOut(left_expression),
            FadeOut(left_label),
            FadeIn(l2_expression),
            FadeIn(l2_label),
            # bring the red weights back to their original values
            *[
                ChangeDecimalToValue(number_labels[i], weight_values[i])
                for i in zero_indices
            ],
            run_time=1.2,
        )
        self.wait(0.8)

        # "L2 regularization also pulls weights toward zero, but it usually
        #  makes them smaller without setting them exactly to zero."
        self.next_section("l2_shrinks_weights")
        small_values = {1: 0.02, 3: 0.03, 5: -0.01}  # tiny, but never exactly 0
        self.play(*grow(zero_indices), run_time=0.6)
        self.play(
            *[
                ChangeDecimalToValue(number_labels[i], small_values[i])
                for i in zero_indices
            ],
            run_time=2.5,
        )
        self.play(*settle(zero_indices), run_time=0.6)
        self.wait(1.0)

        # ---- Scene 5: the θ mascot peeks in from the right, next to the network ----
        # (everything from the previous scene stays on screen)
        self.next_section("theta_enters")
        theta = ThetaCreature(size=0.75)
        theta_target = RIGHT * 6.1 + DOWN * 2.5
        theta.move_to(RIGHT * (config.frame_width / 2 + 1.5) + DOWN * 2.5)
        theta.set_gaze(UP + LEFT)  # looking toward where the bubble will appear
        self.add(theta)
        self.play(theta.animate.move_to(theta_target), run_time=1.0)

        # Bubble sits in the free area under the right side of the network,
        # just above-left of the θ.
        bubble_center = RIGHT * 3.7 + DOWN * 1.3
        tail_tip = RIGHT * 5.4 + DOWN * 2.3
        speech_bubble = make_speech_bubble(
            width=3.4,
            height=1.5,
            tail_tip=tail_tip - bubble_center,
            tail_angles=(-70, -38),
        ).shift(bubble_center)
        speech_text = Text(
            "So why does\nthat happen?", font_size=30, line_spacing=0.8
        ).move_to(bubble_center)

        # "So why does that happen? Let's look at the math."
        self.next_section("theta_asks")
        self.play(GrowFromPoint(speech_bubble, tail_tip), run_time=0.7)
        # the mouth opens while the question is written
        self.play(Write(speech_text), *theta.open_mouth(), run_time=1.2)
        self.play(*theta.close_mouth(), run_time=0.3)
        self.play(*theta.blink(), rate_func=there_and_back, run_time=0.3)
        self.wait(1.5)

        # ---- Scene 6: the math of L2 regularization ----
        self.next_section("l2_math_clear")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        math_size = 48
        # Equations are split into parts so TransformMatchingTex can reuse
        # the pieces that stay the same when the update rule is rearranged.
        section_title = Tex(r"$L_2$ regularization", font_size=48)
        section_title.to_corner(UL, buff=0.55)

        cost_eq = MathTex(
            r"J", r"=", r"\text{Loss}", r"+",
            r"\frac{\lambda}{2m}", r"\sum_j", r"w_j^2",
            font_size=math_size,
        )

        derivative_eq = MathTex(
            r"\frac{\partial J}{\partial w}", r"=",
            r"\frac{\partial \text{Loss}}{\partial w}", r"+",
            r"\frac{\lambda}{m}", r"w",
            font_size=math_size,
        )

        update_eq = MathTex(
            r"w", r"\leftarrow", r"w", r"-", r"\alpha", r"\Bigl(",
            r"\frac{\partial \text{Loss}}{\partial w}", r"+",
            r"\frac{\lambda}{m}", r"w", r"\Bigr)",
            font_size=math_size,
        )

        rearranged_eq = MathTex(
            r"w", r"\leftarrow", r"w", r"\Bigl(", r"1", r"-",
            r"\frac{\alpha\lambda}{m}", r"\Bigr)", r"-", r"\alpha",
            r"\frac{\partial \text{Loss}}{\partial w}",
            font_size=math_size,
        )

        # Stack: cost on top, derivative in the middle, update rule below.
        cost_top = UP * 1.9
        derivative_pos = UP * 0.2
        update_pos = DOWN * 1.6

        self.next_section("l2_cost_function")
        self.play(Write(section_title), run_time=1.0)
        self.play(Write(cost_eq), run_time=1.8)
        self.wait(1.0)

        # "Taking the derivative with respect to one weight w, we get:"
        self.next_section("l2_derivative")
        self.play(cost_eq.animate.move_to(cost_top), run_time=1.0)
        derivative_eq.move_to(derivative_pos)
        self.play(Write(derivative_eq), run_time=1.8)
        self.wait(1.0)

        # "So the gradient descent update becomes:"
        self.next_section("l2_update_rule")
        update_eq.move_to(update_pos)
        self.play(Write(update_eq), run_time=2.0)
        self.wait(1.0)

        # "Rearranging the terms:"
        self.next_section("l2_rearrange")
        rearranged_eq.move_to(update_pos)
        self.play(TransformMatchingTex(update_eq, rearranged_eq), run_time=2.0)
        self.wait(2.0)

        # ---- Scene 7: weight decay — shrinking by a factor never reaches zero ----
        # "Notice that the weight gets multiplied by a factor slightly smaller
        #  than one. This repeatedly shrinks it toward zero. That's why L2
        #  regularization is often associated with weight decay."
        self.next_section("weight_decay_focus")
        self.play(
            FadeOut(cost_eq),
            FadeOut(derivative_eq),
            rearranged_eq.animate.move_to(UP * 2.0),
            run_time=1.0,
        )
        # Box the weight-decay part w(1 - αλ/m) and dim the rest.
        decay_box = SurroundingRectangle(rearranged_eq[2:8], color=YELLOW, buff=0.15)
        decay_label = Text("weight decay", font_size=28, color=YELLOW)
        decay_label.next_to(decay_box, UP, buff=0.15)
        self.play(
            Create(decay_box),
            FadeIn(decay_label),
            rearranged_eq[0:2].animate.set_opacity(0.3),
            rearranged_eq[8:11].animate.set_opacity(0.3),
            run_time=1.0,
        )
        self.wait(1.0)

        # Under the box: the decay factor, then what it does to w each step.
        factor_eq = MathTex(
            r"\Bigl(1-\frac{\alpha\lambda}{m}\Bigr)\approx \times 0.99",
            font_size=40,
        )
        factor_eq.move_to(UP * 0.65)
        w_times = MathTex(r"w", r"\times", r"0.99", font_size=48)
        w_times[0].set_color(YELLOW)
        w_times[2].set_color(YELLOW)
        w_times.move_to(DOWN * 0.3)
        self.play(Write(factor_eq), run_time=1.2)
        self.wait(0.6)
        self.play(Write(w_times), run_time=0.9)
        self.wait(1.0)

        # The weight as a bar. Each step multiplies it by 0.99, and the piece
        # that L2 removes is shown in red.
        # "But as the weight gets smaller, the L2 penalty's pull gets smaller
        #  too, because it's proportional to w. So L2 usually keeps shrinking
        #  weights without pushing them exactly to zero."
        self.next_section("weight_decay_bar")
        full_width, bar_height, bar_y, factor = 6.0, 0.55, -1.35, 0.99
        bar_left = LEFT * 3.0

        def make_bar(v):
            bar = Rectangle(
                width=full_width * v,
                height=bar_height,
                stroke_width=0,
                fill_color=YELLOW,
                fill_opacity=0.9,
            )
            return bar.move_to(bar_left + UP * bar_y, aligned_edge=LEFT)

        bar = make_bar(1.0)
        zero_line = DashedLine(
            bar_left + UP * (bar_y + 0.5), bar_left + UP * (bar_y - 0.5),
            color=GRAY_B, dash_length=0.08,
        )
        zero_label = MathTex(r"0", font_size=32, color=GRAY_B).next_to(zero_line, LEFT, buff=0.15)
        w_eq = MathTex(r"w=", font_size=40, color=YELLOW)
        w_value = DecimalNumber(1.0, num_decimal_places=3, font_size=40, color=YELLOW)
        w_value.next_to(w_eq, RIGHT, buff=0.15)
        w_readout = VGroup(w_eq, w_value).move_to(UP * (bar_y - 1.05))

        self.play(
            FadeIn(bar), Create(zero_line), FadeIn(zero_label),
            FadeIn(w_readout),
            run_time=1.2,
        )
        self.wait(0.6)

        removed_caption = Text(
            "removed by L2 — smaller every step", font_size=26, color=RED
        ).move_to(DOWN * 3.3)

        v = 1.0
        for step in range(4):
            new_v = v * factor
            kept = make_bar(new_v)
            removed = Rectangle(
                width=full_width * (v - new_v),
                height=bar_height,
                stroke_width=0,
                fill_color=RED,
                fill_opacity=0.95,
            ).move_to(kept.get_right(), aligned_edge=LEFT)
            self.play(
                Transform(bar, kept),
                FadeIn(removed),
                ChangeDecimalToValue(w_value, new_v),
                run_time=0.6,
            )
            extra = [FadeIn(removed_caption)] if step == 1 else []
            self.play(
                removed.animate.shift(DOWN * 0.45).set_opacity(0),
                *extra,
                run_time=0.5,
            )
            self.remove(removed)
            v = new_v

        # Fast-forward: first to 100 steps, then to many more. It keeps
        # shrinking geometrically but never reaches zero.
        def fast_forward(v_from, v_to, label, run_time):
            return [
                UpdateFromAlphaFunc(
                    bar,
                    lambda m, a: m.become(make_bar(v_from * (v_to / v_from) ** a)),
                ),
                ChangeDecimalToValue(w_value, v_to),
            ]

        skip_label = Text("… 100 steps later …", font_size=30).move_to(DOWN * 3.3)
        mid_v = factor**100
        self.play(
            FadeOut(removed_caption),
            FadeIn(skip_label),
            *fast_forward(v, mid_v, skip_label, 2.0),
            run_time=2.0,
        )
        self.wait(0.6)

        final_v = factor**500
        skip_label_2 = Text("… 500 steps later …", font_size=30).move_to(DOWN * 3.3)
        self.play(
            ReplacementTransform(skip_label, skip_label_2),
            *fast_forward(mid_v, final_v, skip_label_2, 2.5),
            run_time=2.5,
        )
        skip_label = skip_label_2
        self.wait(0.8)

        # Bring the tiny sliver to the center of the screen, then zoom in on it.
        self.next_section("weight_decay_zoom")
        zoom_factor = 100
        sliver = VGroup(bar, zero_line, zero_label)
        self.play(
            FadeOut(skip_label),
            sliver.animate.shift(LEFT * bar.get_center()[0]),
            run_time=1.2,
        )
        self.wait(0.5)

        # Zoom about the center: the sliver grows ×100 (and gets a bit thicker,
        # to feel like a zoom) and the zero line is pushed out to its left end.
        zoomed_height = bar_height * 1.6
        zoomed_bar = Rectangle(
            width=full_width * final_v * zoom_factor,
            height=zoomed_height,
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.9,
        ).move_to(UP * bar_y)
        zoomed_zero_line = DashedLine(
            zoomed_bar.get_left() + UP * (zoomed_height / 2 + 0.1),
            zoomed_bar.get_left() + DOWN * (zoomed_height / 2 + 0.1),
            color=GRAY_B, dash_length=0.08,
        )
        zoomed_zero_label = MathTex(r"0", font_size=32, color=GRAY_B).next_to(
            zoomed_zero_line, LEFT, buff=0.15
        )
        zoom_caption = Text(f"×{zoom_factor} zoomed in", font_size=30).next_to(
            zoomed_bar, RIGHT, buff=0.5
        )
        self.play(
            Transform(bar, zoomed_bar),
            Transform(zero_line, zoomed_zero_line),
            Transform(zero_label, zoomed_zero_label),
            run_time=1.8,
        )
        self.play(FadeIn(zoom_caption), run_time=0.6)
        self.wait(0.6)

        # The final value settles just above zero: make it bigger to draw the eye.
        self.play(w_readout.animate.scale(1.5), run_time=0.8)
        self.wait(2.0)

        # ---- Scene 8: L1 regularization ----
        self.next_section("l1_clear")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        l1_title = Tex(r"$L_1$ regularization", font_size=48)
        l1_title.to_corner(UL, buff=0.55)

        l1_cost_eq = MathTex(
            r"J", r"=", r"\text{Loss}", r"+",
            r"\frac{\lambda}{m}", r"\sum_j", r"|w_j|",
            font_size=math_size,
        )
        l1_derivative_eq = MathTex(
            r"\frac{\partial J}{\partial w}", r"=",
            r"\frac{\partial \text{Loss}}{\partial w}", r"+",
            r"\frac{\lambda}{m}", r"\operatorname{sign}(w)",
            font_size=math_size,
        )
        l1_update_eq = MathTex(
            r"w", r"\leftarrow", r"w", r"-", r"\alpha",
            r"\frac{\partial \text{Loss}}{\partial w}", r"-",
            r"\frac{\alpha\lambda}{m}", r"\operatorname{sign}(w)",
            font_size=math_size,
        )

        # "Now let's use the sum of the absolute values of the weights:"
        self.next_section("l1_cost_function")
        self.play(Write(l1_title), run_time=1.0)
        self.play(Write(l1_cost_eq), run_time=1.8)
        self.wait(1.0)

        # "For a nonzero weight, the derivative of |w| is sign(w): positive for
        #  positive weights, and negative for negative weights."
        self.next_section("l1_derivative")
        self.play(l1_cost_eq.animate.move_to(UP * 2.2), run_time=1.0)
        l1_derivative_eq.move_to(UP * 0.4)
        self.play(Write(l1_derivative_eq), run_time=2.0)
        self.wait(1.0)

        # "So the update becomes:"
        self.next_section("l1_update_rule")
        l1_update_eq.move_to(DOWN * 1.7)
        self.play(Write(l1_update_eq), run_time=2.0)
        self.wait(1.5)

        # "Here, the regularization term pulls with a roughly constant strength,
        #  whether the weight is large or small. That can push small weights
        #  all the way to zero."
        self.next_section("l1_constant_pull_focus")
        self.play(
            FadeOut(l1_cost_eq),
            FadeOut(l1_derivative_eq),
            l1_update_eq.animate.move_to(UP * 2.0),
            run_time=1.0,
        )
        pull_box = SurroundingRectangle(l1_update_eq[6:9], color=YELLOW, buff=0.15)
        pull_label = Text("constant pull", font_size=28, color=YELLOW)
        pull_label.next_to(pull_box, UP, buff=0.15)
        self.play(
            Create(pull_box),
            FadeIn(pull_label),
            l1_update_eq[0:6].animate.set_opacity(0.3),
            run_time=1.0,
        )
        self.wait(1.0)

        # Under the box: the size of the pull, and what it does to w each step.
        pull_eq = MathTex(r"\frac{\alpha\lambda}{m}", r"=", r"0.1", font_size=44)
        pull_eq[2].set_color(YELLOW)
        pull_eq.move_to(UP * 0.65)
        w_minus = MathTex(r"w", r"-", r"0.1", font_size=48)
        w_minus[0].set_color(YELLOW)
        w_minus[2].set_color(YELLOW)
        w_minus.move_to(DOWN * 0.3)
        self.play(Write(pull_eq), run_time=1.0)
        self.wait(0.6)
        self.play(Write(w_minus), run_time=0.9)
        self.wait(1.0)

        # The weight as a bar: the same amount (0.1) is removed every step.
        self.next_section("l1_bar")
        l1_step = 0.1

        def make_l1_bar(v):
            # never exactly zero-width (degenerate); 1e-4 is invisible anyway
            return make_bar(max(v, 1e-4))

        l1_bar = make_l1_bar(1.0)
        l1_zero_line = DashedLine(
            bar_left + UP * (bar_y + 0.5), bar_left + UP * (bar_y - 0.5),
            color=GRAY_B, dash_length=0.08,
        )
        l1_zero_label = MathTex(r"0", font_size=32, color=GRAY_B).next_to(
            l1_zero_line, LEFT, buff=0.15
        )
        l1_w_eq = MathTex(r"w=", font_size=40, color=YELLOW)
        l1_w_value = DecimalNumber(1.0, num_decimal_places=3, font_size=40, color=YELLOW)
        l1_w_value.next_to(l1_w_eq, RIGHT, buff=0.15)
        l1_readout = VGroup(l1_w_eq, l1_w_value).move_to(UP * (bar_y - 1.05))
        self.play(
            FadeIn(l1_bar), Create(l1_zero_line), FadeIn(l1_zero_label),
            FadeIn(l1_readout),
            run_time=1.2,
        )
        self.wait(0.6)

        l1_caption = Text(
            "removed by L1 — the same every step", font_size=26, color=RED
        ).move_to(DOWN * 3.3)

        v = 1.0
        for step in range(10):
            new_v = round(v - l1_step, 6)
            kept = make_l1_bar(new_v)
            removed = Rectangle(
                width=full_width * l1_step,
                height=bar_height,
                stroke_width=0,
                fill_color=RED,
                fill_opacity=0.95,
            ).move_to(bar_left + RIGHT * full_width * max(new_v, 0), aligned_edge=LEFT)
            removed.set_y(bar_y)
            self.add(removed)
            extra = [FadeIn(l1_caption)] if step == 1 else []
            self.play(
                Transform(l1_bar, kept),
                ChangeDecimalToValue(l1_w_value, max(new_v, 0)),
                removed.animate.shift(DOWN * 0.5).set_opacity(0),
                *extra,
                run_time=0.25,
                rate_func=linear,
            )
            self.remove(removed)
            v = new_v
        self.wait(0.6)

        # "If a feature doesn't help reduce the loss enough to counter that
        #  pull, its weight can end up at zero. That's why L1 regularization
        #  can produce sparse models: models where some weights are exactly zero."
        self.next_section("l1_exactly_zero")
        self.play(
            FadeOut(l1_caption),
            l1_readout.animate.scale(1.5).set_color(RED),
            run_time=0.9,
        )
        self.wait(2.0)


# Lets VS Code's Python "Run Python File" button render this scene too,
# provided VS Code is using Manim's uv tool interpreter.
if __name__ == "__main__":
    import subprocess
    import sys

    subprocess.run(
        [
            sys.executable,
            "-m",
            "manim",
            "--save_sections",
            "-pql",
            __file__,
            "L1L2Video",
        ],
        check=True,
    )