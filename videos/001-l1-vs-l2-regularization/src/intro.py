"""
Channel intro video: the θ mascot introduces Ramz and the channel.

Render (landscape, for YouTube / LinkedIn):
    manim -pql intro_video.py ChannelIntro
Render (vertical 9:16, for TikTok / Shorts):
    manim -pql -r 1080,1920 intro_video.py ChannelIntro
Use -pqh instead of -pql for the final high-quality render.

The layout adapts to the frame shape automatically.

Timing: every beat lasts (number of words in its voiceover line / WORDS_PER_SECOND)
seconds. Record your voiceover first, then tune WORDS_PER_SECOND until the
animation matches your pace (or drop your audio in AUDIO_FILE and adjust).
"""
import numpy as np
from manim import *

# ---- things you will probably want to edit ---------------------------------
CHANNEL_NAME = ""            # e.g. "Theta"; shown under the logo at the end
WORDS_PER_SECOND = 2.6       # your speaking pace; lower = slower animation
AUDIO_FILE = None            # e.g. "voiceover.mp3" to play it inside the render
THETA_COLOR = "#4FC3F7"
THETA_SIZE = 0.9
GREETING = "Hi, I'm Ramez!"   # text inside the speech bubble
UPCOMING_VIDEOS = ["L1 L2 Regularization", "Adam Optimizer", "activation functions"]

# Vertical renders (-r 1080,1920): make the frame narrow instead of stretched.
if config.pixel_height > config.pixel_width:
    config.frame_width = config.frame_height * config.pixel_width / config.pixel_height


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

    def center_gaze(self):
        """Animations that bring the pupils back to the middle of the eyes."""
        return [
            pupil.animate.move_to(eye.get_center())
            for pupil, eye in zip(self.pupils, self.eye_whites)
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


class TalkingTheta(ThetaCreature):
    """ThetaCreature whose mouth flaps while `talking` is True."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.talking = False
        self._clock = 0.0
        self._openness = 0.0

    def tick(self, dt):
        """Called every frame by the scene's driver (not an updater on the
        creature itself, so move/rotate animations don't freeze the mouth)."""
        if self.talking:
            self._clock += dt
            target = abs(np.sin(self._clock * 9.0)) * (
                0.55 + 0.45 * abs(np.sin(self._clock * 3.1))
            )
            self._openness += (target - self._openness) * min(1.0, dt * 18)
        else:
            self._openness += (0.0 - self._openness) * min(1.0, dt * 12)
        width = self.mouth_closed_width + (
            self.mouth_open_width - self.mouth_closed_width
        ) * self._openness
        self.mouth.set_stroke(width=width)


# ---- the four mini-animations shown next to θ ------------------------------
# Each builder returns (mobjects, update). `update(alpha)` (alpha from 0 to 1)
# puts the panel into its state at that moment, so all four can be driven by
# one clock and play at the same time.
def clip01(x):
    return float(np.clip(x, 0.0, 1.0))


def ramp(alpha, start, end):
    """0 before `start`, 1 after `end`, smooth in between."""
    return smooth(clip01((alpha - start) / (end - start)))


def make_panel(center, w, h):
    return RoundedRectangle(
        corner_radius=0.15,
        width=w,
        height=h,
        stroke_color=GRAY_D,
        stroke_width=2,
        fill_color="#10141A",
        fill_opacity=1,
    ).move_to(center)


def build_standardization(center, w, h):
    """Raw data on a scatter plot, then shifted to mean 0 and scaled to std 1."""
    rng = np.random.default_rng(3)
    raw = rng.normal(size=(30, 2)) @ np.array([[1.7, 0.5], [0.0, 1.0]]) + np.array([6.0, 6.0])
    mean, std = raw.mean(axis=0), raw.std(axis=0)

    axes = Axes(
        x_range=[-5, 10, 5],
        y_range=[-5, 10, 5],
        x_length=w * 0.84,
        y_length=h * 0.80,
        tips=False,
        axis_config={"include_numbers": False, "include_ticks": False, "color": GRAY_B, "stroke_width": 2},
    ).move_to(center)
    r = 0.024 * min(w, h)
    dots = VGroup(*[Dot(axes.c2p(*p), radius=r, color=YELLOW) for p in raw])
    marker = Dot(axes.c2p(*mean), radius=r * 1.8, color=ORANGE)  # the mean

    def update(alpha):
        s_shift = ramp(alpha, 0.12, 0.45)   # subtract the mean
        s_scale = ramp(alpha, 0.50, 0.85)   # divide by the std
        scale = 1 + (std - 1) * s_scale
        for d, p in zip(dots, raw):
            d.move_to(axes.c2p(*((p - mean * s_shift) / scale)))
        marker.move_to(axes.c2p(*((mean - mean * s_shift) / scale)))

    update(0.0)
    return VGroup(axes, dots, marker), update


def build_forward_prop(center, w, h):
    """A small network; the signal travels layer by layer and lights the nodes."""
    sizes = [3, 4, 4, 2]
    xs = np.linspace(-w * 0.36, w * 0.36, len(sizes))
    gap = h * 0.24
    layers = [
        [center + np.array([x, (i - (k - 1) / 2) * gap, 0.0]) for i in range(k)]
        for x, k in zip(xs, sizes)
    ]
    rn = 0.04 * min(w, h)

    edges, signals, hops = VGroup(), VGroup(), []  # hops[l] = [(edge, signal, a, b)]
    for l in range(len(sizes) - 1):
        hop = []
        for a in layers[l]:
            for b in layers[l + 1]:
                e = Line(a, b, color=GRAY_C, stroke_width=1.5, stroke_opacity=0.35)
                s = Dot(a, radius=rn * 0.45, color=YELLOW).set_opacity(0)
                edges.add(e)
                signals.add(s)
                hop.append((e, s, a, b))
        hops.append(hop)
    nodes = [
        VGroup(*[Circle(radius=rn, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_C, fill_opacity=0).move_to(p) for p in layer])
        for layer in layers
    ]

    def update(alpha):
        for n in nodes[0]:
            n.set_fill(BLUE_C, opacity=ramp(alpha, 0.0, 0.08))
        for l, hop in enumerate(hops):
            s = clip01((alpha - (0.08 + 0.29 * l)) / 0.24)  # progress of this hop
            for e, sig, a, b in hop:
                sig.move_to(a + (b - a) * smooth(s))
                sig.set_opacity(min(1.0, 5 * s, 5 * (1 - s)) if 0 < s < 1 else 0.0)
                e.set_stroke(opacity=0.35 + 0.45 * smooth(s))
            for n in nodes[l + 1]:
                n.set_fill(BLUE_C, opacity=smooth(clip01((s - 0.75) / 0.25)))

    update(0.0)
    return VGroup(edges, *nodes, signals), update


def build_descent_3d(center, w, h):
    """Gradient descent on a 3D bowl, drawn with a hand-made projection so it
    sits inside a normal Scene. The view rotates slowly while the ball rolls."""
    zs = 0.55                      # vertical squash of the surface
    f = lambda x, y: 0.1 * x**2 + 0.5 * y**2
    grad = lambda x, y: np.array([0.2 * x, 1.0 * y])

    # a real gradient-descent run: p <- p - lr * grad f(p)
    xy = [np.array([-2.5, 1.6])]
    for _ in range(12):
        xy.append(xy[-1] - 1.55 * grad(*xy[-1]))
    path = np.array([[x, y, zs * f(x, y) + 0.04] for x, y in xy])

    xr, yr, n = 3.0, 2.2, 25
    grid_pts = []
    for x in np.linspace(-xr, xr, 13):
        ys = np.linspace(-yr, yr, n)
        grid_pts.append(np.stack([np.full(n, x), ys, zs * f(x, ys)], axis=1))
    for y in np.linspace(-yr, yr, 9):
        xs_ = np.linspace(-xr, xr, n)
        grid_pts.append(np.stack([xs_, np.full(n, y), zs * f(xs_, y)], axis=1))

    el = np.radians(36)
    az_of = lambda a: np.radians(-40 + 55 * a)

    def raw_project(P, az):
        P = np.atleast_2d(P)
        x, y, z = P[:, 0], P[:, 1], P[:, 2]
        depth = x * np.sin(az) + y * np.cos(az)
        return np.stack([x * np.cos(az) - y * np.sin(az), depth * np.sin(el) + z * np.cos(el)], axis=1)

    # fit the whole rotation range inside the panel
    allp = np.concatenate(grid_pts)
    boxes = np.concatenate([raw_project(allp, az_of(a)) for a in np.linspace(0, 1, 12)])
    lo, hi = boxes.min(axis=0), boxes.max(axis=0)
    k = min(w * 0.88 / (hi[0] - lo[0]), h * 0.86 / (hi[1] - lo[1]))
    mid = (lo + hi) / 2

    def project(P, az):
        p2 = (raw_project(P, az) - mid) * k
        return np.concatenate([p2, np.zeros((len(p2), 1))], axis=1) + center

    surface = VGroup(*[VMobject(stroke_color=BLUE_D, stroke_width=1.6, stroke_opacity=0.85) for _ in grid_pts])
    trail = VMobject(stroke_color=ORANGE, stroke_width=4)
    ball = Dot(radius=0.035 * min(w, h), color=YELLOW)
    minimum = Dot(radius=0.02 * min(w, h), color=GREEN_C)
    ball.set_z_index(2)
    trail.set_z_index(1)

    def update(alpha):
        az = az_of(alpha)
        for line, pts in zip(surface, grid_pts):
            line.set_points_as_corners(project(pts, az))
        steps = len(path) - 1
        p = clip01((alpha - 0.12) / 0.78) * steps
        i = min(int(p), steps - 1)
        pos = path[i] + (path[i + 1] - path[i]) * smooth(p - i)
        pts3 = np.concatenate([path[: i + 1], [pos]])
        if len(pts3) < 2 or np.allclose(pts3[-1], pts3[-2]):
            pts3 = np.concatenate([pts3[:-1], [pts3[-1] + 1e-3]])
        trail.set_points_as_corners(project(pts3, az))
        ball.move_to(project(pos, az)[0])
        minimum.move_to(project(np.array([0.0, 0.0, 0.0]), az)[0])

    update(0.0)
    return VGroup(surface, minimum, trail, ball), update


def build_linear_map(center, w, h):
    """A grid and its basis vectors being squeezed by a 2x2 matrix."""
    M = np.array([[1.0, 0.8], [0.4, 1.0]])
    g = 2
    u = min(w * 0.42 / (1.8 * g), h * 0.40 / (1.4 * g))
    to_screen = lambda P: center + u * np.array([P[0], P[1], 0.0])

    lines_ends = []
    for k in range(-g, g + 1):
        lines_ends.append((np.array([k, -g]), np.array([k, g]), k == 0))
        lines_ends.append((np.array([-g, k]), np.array([g, k]), k == 0))
    ghost = VGroup(*[Line(to_screen(a), to_screen(b), color=GRAY_D, stroke_width=1.2, stroke_opacity=0.4) for a, b, _ in lines_ends])
    grid = VGroup(
        *[
            Line(to_screen(a), to_screen(b), color=GRAY_B if axis else BLUE_C, stroke_width=2.4 if axis else 1.6, stroke_opacity=1 if axis else 0.8)
            for a, b, axis in lines_ends
        ]
    )
    square = VMobject(stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.28)
    i_arrow = Arrow(center, center + RIGHT * u, buff=0, color=GREEN_C)
    j_arrow = Arrow(center, center + UP * u, buff=0, color=RED_C)

    def arrow(start, end, color):
        return Arrow(start, end, buff=0, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.3)

    def update(alpha):
        Mt = np.eye(2) + (M - np.eye(2)) * ramp(alpha, 0.12, 0.70)
        for line, (a, b, _) in zip(grid, lines_ends):
            line.put_start_and_end_on(to_screen(Mt @ a), to_screen(Mt @ b))
        corners = [Mt @ np.array(c, dtype=float) for c in ([0, 0], [1, 0], [1, 1], [0, 1], [0, 0])]
        square.set_points_as_corners([to_screen(c) for c in corners])
        i_arrow.become(arrow(to_screen(np.zeros(2)), to_screen(Mt @ np.array([1.0, 0.0])), GREEN_C))
        j_arrow.become(arrow(to_screen(np.zeros(2)), to_screen(Mt @ np.array([0.0, 1.0])), RED_C))

    update(0.0)
    return VGroup(ghost, grid, square, i_arrow, j_arrow), update



class ChannelIntro(Scene):
    # ------------------------------------------------------------ helpers
    def beat(self, voiceover, *anims, anim_time=1.0, min_time=0.0, pause=0.25):
        """One spoken line: theta talks and `anims` play. The beat lasts as
        long as the line takes to say (no text is shown on screen)."""
        total = max(len(voiceover.split()) / WORDS_PER_SECOND, anim_time, min_time)
        self.theta.talking = True
        if anims:
            self.play(*anims, run_time=anim_time)
        else:
            self.wait(anim_time)
        if total > anim_time:
            self.wait(total - anim_time)
        self.theta.talking = False
        self.wait(pause)

    def blink(self):
        self.play(*self.theta.blink(), rate_func=there_and_back, run_time=0.25)

    @staticmethod
    def pill(label, color, font_size):
        t = Text(label, font_size=font_size, weight=BOLD)
        box = RoundedRectangle(
            corner_radius=0.2,
            width=t.width + 0.5,
            height=t.height + 0.35,
            stroke_color=color,
            fill_color=color,
            fill_opacity=0.25,
        )
        t.move_to(box)
        return VGroup(box, t)

    # -------------------------------------------------------------- scene
    def construct(self):
        v = self.vertical = config.frame_height > config.frame_width
        if AUDIO_FILE:
            self.add_sound(AUDIO_FILE)

        self.theta = theta = TalkingTheta(color=THETA_COLOR, size=THETA_SIZE)
        driver = Mobject()  # drives the mouth every frame
        driver.add_updater(lambda m, dt: theta.tick(dt))
        self.add(driver)

        home = UP * (1.3 if v else 0.5)
        side = UP * 2.7 if v else LEFT * 4.9 + UP * 0.3
        look_at_visuals = DOWN if v else RIGHT
        theta.move_to(home)
        theta.set_z_index(1)  # so the stars can come out from behind it

        # ---- 0:00  θ draws itself, then a speech bubble comes out of it ----
        self.play(Create(theta.ring), run_time=1.1)
        self.play(Create(theta.bar), run_time=0.5)
        self.play(
            FadeIn(theta.eye_whites, scale=0.4),
            FadeIn(theta.pupils, scale=0.4),
            Create(theta.mouth),
            run_time=0.7,
        )
        self.blink()

        if v:  # bubble below the θ, tail pointing up at it
            bubble_center = home + DOWN * 2.5
            bubble = make_speech_bubble(
                width=3.3, height=1.4,
                tail_tip=(home + DOWN * 1.15) - bubble_center,
                tail_angles=(62, 98),
            )
            text_size = 34
        else:  # bubble to the right of the θ, tail pointing left at it
            bubble_center = home + RIGHT * 3.6 + UP * 0.9
            bubble = make_speech_bubble(
                width=3.8, height=1.7,
                tail_tip=(home + RIGHT * 0.85 + DOWN * 0.1) - bubble_center,
                tail_angles=(-178, -148),
            )
            text_size = 40
        bubble.shift(bubble_center)
        bubble_text = Text(GREETING, font_size=text_size, weight=MEDIUM)
        bubble_text.scale_to_fit_width(min(bubble_text.width, 2.9 if not v else 2.6))
        bubble_text.move_to(bubble_center)
        self.beat(
            "Hey! I'm Ramz.",
            Create(bubble),
            Write(bubble_text),
            Wiggle(theta, scale_value=1.06, rotation_angle=0.03 * TAU, n_wiggles=2),
            anim_time=1.3,
            min_time=2.2,
        )

        # ---- 0:05  about me ----
        self.beat(
            "I'm a fourth-year Computer Science student at Ain Shams University,",
            FadeOut(VGroup(bubble, bubble_text)),
            anim_time=0.5,
        )
        badge_font = 26 if v else 30
        dx = 1.55 if v else 3.0
        ai_badge = self.pill("AI", BLUE_C, badge_font).move_to(home + LEFT * dx + UP * 0.8)
        math_badge = self.pill("Math", GREEN_C, badge_font).move_to(home + RIGHT * dx + UP * 0.8)
        self.beat(
            "and I'm really into AI and math.",
            FadeIn(ai_badge, scale=0.5),
            FadeIn(math_badge, scale=0.5),
            anim_time=0.8,
        )
        self.blink()

        # ---- 0:15  the idea: four mini-animations at the same time ----
        idea_setup = "The idea here is simple: any concept in AI or math that looks complicated,"
        idea_rest = (
            "I'll try to explain it with animation, "
            "so you can actually see it and understand it, not just memorize it."
        )
        idea_secs = len(idea_rest.split()) / WORDS_PER_SECOND

        # the screen next to θ is split into a 2x2 grid
        gap = 0.18
        if v:
            x0, x1, y0, y1 = -2.1, 2.1, -3.85, 1.35
        else:
            x0, x1, y0, y1 = -3.5, 6.85, -3.8, 3.8
        pw, ph = (x1 - x0 - gap) / 2, (y1 - y0 - gap) / 2
        centers = [
            np.array([x0 + pw / 2, y1 - ph / 2, 0.0]),  # top left
            np.array([x1 - pw / 2, y1 - ph / 2, 0.0]),  # top right
            np.array([x0 + pw / 2, y0 + ph / 2, 0.0]),  # bottom left
            np.array([x1 - pw / 2, y0 + ph / 2, 0.0]),  # bottom right
        ]
        builders = [build_standardization, build_forward_prop, build_descent_3d, build_linear_map]
        panels, updates = VGroup(), []
        for c, build in zip(centers, builders):
            content, upd = build(c, pw, ph)
            panels.add(VGroup(make_panel(c, pw, ph), content))
            updates.append(upd)

        theta.set_gaze(look_at_visuals)
        self.beat(
            idea_setup,
            theta.animate.move_to(side),
            FadeOut(VGroup(ai_badge, math_badge)),
            LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.2),
            anim_time=1.8,
        )
        self.beat(
            idea_rest,
            *[
                UpdateFromAlphaFunc(p, lambda m, a, upd=upd: upd(a), rate_func=linear)
                for p, upd in zip(panels, updates)
            ],
            anim_time=idea_secs,
        )
        self.blink()

        # ---- 0:30  more videos coming ----
        card_w, card_h = (3.9, 0.85) if v else (2.9, 1.4)
        if v:
            card_pos = [UP * 0.8, DOWN * 0.3, DOWN * 1.4]
        else:
            card_pos = [RIGHT * x + UP * 0.3 for x in (-2.0, 1.2, 4.4)]
        cards = VGroup()
        for title, pos in zip(UPCOMING_VIDEOS, card_pos):
            box = RoundedRectangle(
                corner_radius=0.15, width=card_w, height=card_h,
                stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_E, fill_opacity=0.25,
            )
            play_icon = Triangle(color=WHITE, fill_opacity=1, stroke_width=0).scale(0.15).rotate(-PI / 2)
            label = Text(title, font_size=22 if v else 24, color=GRAY_A)
            if v:
                play_icon.move_to(box.get_left() + RIGHT * 0.45)
                avail = card_w - 0.45 - 0.35 - 0.25
                if label.width > avail:
                    label.scale_to_fit_width(avail)
                label.next_to(play_icon, RIGHT, buff=0.3)
            else:
                play_icon.move_to(box.get_center() + UP * 0.25)
                if label.width > card_w - 0.3:
                    label.scale_to_fit_width(card_w - 0.3)
                label.next_to(play_icon, DOWN, buff=0.25)
            cards.add(VGroup(box, play_icon, label).move_to(pos))
        self.beat(
            "This is just the beginning, and there are a lot more videos on the way.",
            FadeOut(panels),
            LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.25),
            anim_time=1.6,
        )

        # ---- 0:38  ask the audience: θ comes back to the middle of the screen ----
        center = ORIGIN
        self.play(*theta.center_gaze(), run_time=0.3)  # look at the viewer again
        q_mark = Text("?", font_size=60, color=YELLOW).move_to(center + RIGHT * 1.2 + UP * 0.9)
        self.beat(
            "If there's a topic you'd like me to explain, drop it in the comments and I'll take it into account.",
            FadeOut(cards),
            theta.animate.move_to(center).rotate(12 * DEGREES),
            FadeIn(q_mark, shift=DOWN * 0.2),
            anim_time=1.5,
        )

        # stars come out from underneath θ, which stays in the middle
        stars = VGroup(
            *[Star(5, outer_radius=0.25 if v else 0.3, color=YELLOW, stroke_width=3) for _ in range(5)]
        ).arrange(RIGHT, buff=0.25).move_to(center + DOWN * 2.1)
        emerge_from = theta.ring.get_bottom() + UP * 0.1
        self.beat(
            "And I'd love your honest feedback too, on the quality of the explanations or the animation.",
            FadeOut(q_mark),
            theta.animate.rotate(-12 * DEGREES),
            LaggedStart(*[GrowFromPoint(s, emerge_from) for s in stars], lag_ratio=0.2),
            anim_time=1.4,
        )
        self.beat(
            "Anything you tell me, I'll really appreciate it, and it'll help me improve.",
            LaggedStart(*[s.animate.set_fill(YELLOW, opacity=1) for s in stars], lag_ratio=0.2),
            anim_time=1.4,
        )

        # ---- 0:52  goodbye, θ becomes the logo (still in the middle) ----
        self.beat(
            "Thanks for making it this far.",
            FadeOut(stars),
            anim_time=1.0,
        )
        self.beat(
            "See you in the first video. Bye!",
            Wiggle(theta, scale_value=1.1, rotation_angle=0.05 * TAU, n_wiggles=3),
            anim_time=1.2,
        )
        self.play(
            FadeOut(theta.eye_whites),
            FadeOut(theta.pupils),
            FadeOut(theta.mouth),
            run_time=0.8,
        )
        if CHANNEL_NAME:
            name = Text(CHANNEL_NAME, font_size=48, weight=BOLD, color=THETA_COLOR)
            name.next_to(theta, DOWN, buff=0.4)
            self.play(Write(name), run_time=1.0)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# Lets VS Code's "Run Python File" button render the scene.
if __name__ == "__main__":
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-m", "manim", "-pql", __file__, "ChannelIntro"],
        check=True,
    )