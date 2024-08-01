from manim import *
import numpy as np


class Determinant(MovingCameraScene):

    scale = 1.5
    matrix1 = np.array([[1, 1], [0, 2]])  # attention, c'est une liste de lignes ici pas de colonnes
    matrix2 = np.array([[1, 2], [1, -1]])
    matrix3 = np.array([[2, -1], [1, -1/2]])

    def get_matrix_latex(self, mat) -> str:
        return f"A = \\begin{{bmatrix}} { mat[0][0]} & { mat[0][1] } \\\\ { mat[1][0] } & { mat[1][1] } \\end{{bmatrix}}"

    def get_matrix_mathtex(self, mat) -> MathTex:
        return MathTex(self.get_matrix_latex(mat), color=GREEN_B)

    # Calcule l'aire du carré unité au cours de la transformation
    def calculate_area(self, unit_square: Square) -> float:
        points = unit_square.get_vertices()
        area = 0
        if len(points) >= 4:
            side1 = points[1] - points[0]
            side2 = points[3] - points[0]
            area = np.linalg.norm(np.cross(side1, side2)) / (self.scale ** 2)
        return round(area, 2)

    def get_area_tex(self, area : str, color : ManimColor = RED) -> MathTex:
        return MathTex(f"\\boldsymbol{{{area}}}", font_size=50, color=color)

    def update_area(self, unit_square: Square, color : ManimColor = RED) -> MathTex:
        area = self.calculate_area(unit_square)
        return self.get_area_tex(f"{area}", color).move_to(unit_square.get_center())

    def get_area_tex_ellipse(self, area : str, color : ManimColor = RED) -> MathTex:
        return MathTex(f"\\boldsymbol{{{area}}}\cdot\mathcal{{A}}", font_size=50, color=color)

    def update_area_ellipse(self, unit_square: Square, ellipse: Ellipse, color : ManimColor = RED) -> MathTex:
        # On a quand même besoin du carré unité pour savoir l'aire en temps réelle
        area = self.calculate_area(unit_square)
        return self.get_area_tex_ellipse(f"{area}", color).move_to(ellipse.get_center())

    def get_transformed_vector(self, vector : Vector, matrix, color : ManimColor = GREEN_E) -> Vector:
        # On crée un nouveau vecteur qui pointe vers l'arrivée plutôt que de réutiliser le
        # vecteur transformé pour des effets pûrement esthétiques (éviter la distorsion)
        return Vector(vector.copy().apply_matrix(matrix).get_end(), color=color)

    def add_background(self, mobject : Mobject):
        mobject.add_background_rectangle(color=DARKER_GRAY, opacity=1)

    def get_det_tex(self, matrix_tex : MathTex, det : str = "") -> MathTex:
        tex =  MathTex("\\text{det}(A) = " + det, font_size=50, color=GREEN_B).next_to(matrix_tex, DOWN)
        self.add_background(tex)
        self.add_foreground_mobjects(tex)
        return tex

    def create(self, *objects : VMobject, run_time : float = 1):
        self.play(*[Create(ob) for ob in objects], run_time=run_time)

    def do_linear_transformation(self, mat, group : Group, u1 : Vector, v1 : Vector, u2 : Vector, v2 : Vector, run_time : int):
        self.play(
            ApplyMatrix(mat, group),
            Transform(u1, u2), # techniquement les vecteurs de bases ne subissent la transformation linéaire (effets esthétiques)
            Transform(v1, v2),
            run_time=run_time
        )

    def do_transition_sub(self, title : Text, sub_title : Text, matrix1 : MathTex, matrix2 : MathTex):
        self.create(title, matrix1, sub_title)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(sub_title), ReplacementTransform(matrix1, matrix2))
        self.add_foreground_mobjects(matrix2)

    def do_transition(self, title: Text, matrix1: MathTex, matrix2: MathTex): # sans sous-titre
        self.create(title, matrix1)
        self.wait(2)
        self.play(FadeOut(title), ReplacementTransform(matrix1, matrix2))
        self.add_foreground_mobjects(matrix2)

    def clear(self, *objects : VMobject):
        self.play(*[Uncreate(ob) for ob in objects])
        self.wait(1)

    def get_title(self, txt : str) -> Text:
        return Text(txt, font_size=40).set_color_by_gradient(BLUE, GREEN_A).align_to(ORIGIN)

    def get_subtitle(self, txt : str) -> Text:
        return Text(txt, font_size=35, slant=ITALIC).set_opacity(0.6).align_to(ORIGIN)



    def construct(self):

        self.camera.background_color = DARKER_GRAY
        Text.set_default(font="Helvetica")
        MarkupText.set_default(font="Helvetica")

        # Introduction

        intro = MarkupText("Le <b>déterminant</b> est le facteur par\nlequel les aires sont multipliées.", font_size=40, line_spacing=1, gradient=(BLUE,GREEN)).align_to(ORIGIN)
        self.create(intro, run_time=0.5)
        self.wait(3)
        self.play(FadeOut(intro), run_time=0.5)

        # Construction

        desc_tex1 = self.get_title("Premier scénario : le déterminant est positif").shift(UP * 0.6)
        matrix_tex1 = self.get_matrix_mathtex(self.matrix1).shift(DOWN * 0.6)
        matrix_tex2 = matrix_tex1.copy().to_edge(UL, 0.6)
        self.add_background(matrix_tex2)

        grid = NumberPlane().set_opacity(0.5).set_color(GRAY_D)
        omoving_grid = NumberPlane(color=BLUE_D).set_opacity(0.5) # o pour original (stocker l'état initial) (de même ensuite)
        omoving_grid.x_axis.set_color(GREEN_D)
        omoving_grid.y_axis.set_color(GREEN_D)
        oi_hat = Vector(np.array([1, 0]), color=GREEN_E, z_index=1)
        oj_hat = Vector(np.array([0, 1]), color=GREEN_E, z_index=1)
        unit_square = Square(1, fill_opacity=0.1, stroke_opacity=0.5, fill_color=GREEN_D).move_to(UR * 0.5)

        Group(grid, omoving_grid, oi_hat, oj_hat, unit_square).scale(self.scale) # on aggrandit les objets

        i_hat = oi_hat.copy()
        j_hat = oj_hat.copy()
        moving_grid = omoving_grid.copy()
        transformed_i_hat = self.get_transformed_vector(oi_hat, self.matrix1)
        transformed_j_hat = self.get_transformed_vector(oj_hat, self.matrix1)
        area = self.get_area_tex("1.0").move_to(unit_square.get_center())
        # il faut régler la taille du unit_square (avec scale) avant de mettre le texte dedans (c'est pour ça que l'on créé cet objet après)

        Group(matrix_tex1, matrix_tex2, self.camera.frame, desc_tex1).move_to(UR) # on déplace les objets
        group = Group(moving_grid, unit_square) # groupe des objets transformés

        # Transformations : transition

        self.create(grid)
        self.wait(1)
        self.do_transition(desc_tex1, matrix_tex1, matrix_tex2)
        self.create(moving_grid, i_hat, j_hat, unit_square, area)
        area.add_updater(lambda text: text.become(self.update_area(unit_square)))
        self.wait(1)

        # Transformation : déformation du carré unité

        self.do_linear_transformation(self.matrix1, group, i_hat, j_hat, transformed_i_hat, transformed_j_hat, 3)
        self.wait(1)

        det_text = self.get_det_tex(matrix_tex2).shift(LEFT * 0.5)
        self.create(det_text, run_time=0.6)
        result_tex = MathTex(f"{np.linalg.det(self.matrix1)}", font_size=60, color=RED).next_to(det_text, RIGHT)
        self.add_background(result_tex)
        self.play(ReplacementTransform(area.copy(), result_tex), run_time=1) # copy pour garder area aussi à l'emplacement initial
        self.add_foreground_mobjects(result_tex)
        self.wait(1)

        # Transformations : retour au point de départ

        self.do_linear_transformation(np.linalg.inv(self.matrix1), group, i_hat, j_hat, oi_hat, oj_hat, 1)
        area.set(tex_strings=f"\\boldsymbol{{1.0}}").clear_updaters() # sinon on risque d'avoir 1.01 (imprécision de l'enchainement des 2 transformations
        # il faut supprimer les updaters avant de faire disparaitre un objet (sinon il reste visible)
        self.play(FadeOut(unit_square), FadeOut(area), run_time=1)

        # Transformations : déformation d'une ellipse quelconque

        ellipse = Ellipse(fill_color=TEAL, color=TEAL, fill_opacity=0.1).scale(self.scale).shift(RIGHT*2.5 + UP)
        group.add(ellipse) # on l'ajoute au groupe des objets déformables
        ellipse_area = self.get_area_tex_ellipse("1.0").move_to(ellipse.get_center())
        self.create(ellipse, ellipse_area)

        self.remove(oi_hat, oj_hat) # ils ont été rendu visibles par ReplacementTransform mais on continue de manipuler i_hat j_hat
        ellipse_area.add_updater(lambda text: text.become(self.update_area_ellipse(unit_square, ellipse)))
        unit_square.set_opacity(0)  # on le rend invisible mais on ne le supprime pas pour connaitre le facteur multiplicateur d'aire

        self.do_linear_transformation(self.matrix1, group, i_hat, j_hat, transformed_i_hat, transformed_j_hat, 3)
        ellipse_area.clear_updaters() # obligé pour la destruction
        self.wait(1)

        # Transformations : nettoyage

        self.clear(i_hat, j_hat, matrix_tex2, det_text, result_tex, ellipse_area, ellipse, moving_grid, ellipse)

        # Transformations : transition

        desc_tex2 = self.get_title("Second scénario : le déterminant est négatif").shift(UR + UP*0.9)
        precision_text = self.get_subtitle("L'orientation de la base est inversée").shift(UR+UP*0.2)
        matrix_tex3 = self.get_matrix_mathtex(self.matrix2).shift(DOWN*0.9).shift(UR)
        matrix_tex4 = matrix_tex3.copy().move_to(matrix_tex1)
        self.add_background(matrix_tex4)
        self.do_transition_sub(desc_tex2, precision_text, matrix_tex3, matrix_tex4)

        i_hat = oi_hat.copy().set_color(BLUE_E)
        j_hat = oj_hat.copy()
        moving_grid = omoving_grid.copy()
        unit_square = Square(1, fill_opacity=0.4, stroke_opacity=0.3, fill_color=[BLUE, GREEN]).move_to(UR * 0.75).scale(self.scale).set_z_index(0)
        area = self.get_area_tex("1.0", WHITE).move_to(unit_square.get_center())
        self.create(moving_grid, unit_square, i_hat, j_hat, area)

        # Transformations : inversion des vecteurs de base

        transformed_i_hat = self.get_transformed_vector(oi_hat, self.matrix2, BLUE_E)
        transformed_j_hat = self.get_transformed_vector(oj_hat, self.matrix2)
        transformed_unit_square = unit_square.copy().apply_matrix(self.matrix2).set_fill([GREEN, BLUE])
        # si on applique juste la transformation linéaire sur le carré, le degradé n'est pas inversé
        transformed_area = self.get_area_tex(f"-{self.calculate_area(transformed_unit_square)}", (RED_D - GRAY_D)).move_to(transformed_unit_square.get_center())

        self.wait(1)
        self.play(
            ApplyMatrix(self.matrix2, moving_grid),
            Transform(i_hat, transformed_i_hat),
            Transform(j_hat, transformed_j_hat),
            Transform(unit_square, transformed_unit_square),
            Transform(area, transformed_area),
            run_time=3
        )
        self.wait(1)

        det_text = self.get_det_tex(matrix_tex2, f"{np.linalg.det(self.matrix2):.1f}")
        self.create(det_text)
        self.wait(2)

        # Transformations : nettoyage

        self.clear(i_hat, j_hat, unit_square, moving_grid, matrix_tex4, area, det_text)

        # Transformations : transition

        desc_tex3 = self.get_title("Troisième scénario : le déterminant est nul").shift(UR + UP*0.9)
        precision_text2 = self.get_subtitle("Une dimension est perdue").shift(UR+UP*0.1)
        matrix_tex5 = self.get_matrix_mathtex(self.matrix3).shift(DOWN*0.9 + UR)
        matrix_tex6 = matrix_tex5.copy().move_to(matrix_tex1).shift(RIGHT*0.3)
        self.add_background(matrix_tex6)
        self.do_transition_sub(desc_tex3, precision_text2, matrix_tex5, matrix_tex6)

        i_hat = oi_hat.copy()
        j_hat = oj_hat.copy()
        moving_grid = omoving_grid.copy()
        unit_square = Square(1, fill_opacity=0.3, stroke_opacity=0.5, fill_color=BLUE_D, z_index=0).scale(self.scale).move_to(UR * 0.75)
        area = self.get_area_tex("1.0").move_to(unit_square.get_center())
        self.create(moving_grid, unit_square, i_hat, j_hat, area)
        self.wait(1)

        # Transformations : perte d'une dimension

        transformed_i_hat = self.get_transformed_vector(oi_hat, self.matrix3)
        transformed_j_hat = self.get_transformed_vector(oj_hat, self.matrix3)

        self.wait(1)
        group = Group(moving_grid, unit_square, area)
        self.do_linear_transformation(self.matrix3, group, i_hat, j_hat, transformed_i_hat, transformed_j_hat, 3)
        self.wait(1)

        det_text = self.get_det_tex(matrix_tex2, f"{np.linalg.det(self.matrix3)}").shift(0.2*RIGHT)
        self.create(det_text)
        self.wait(2)

        # Transformations : nettoyage

        self.clear(i_hat, j_hat, unit_square, moving_grid, matrix_tex6, det_text)

        # Transformation : conclusion

        Text.set_default(font_size=28, line_spacing=0.7)

        conclu1 = Text("Ce qu'il faut retenir", font_size=40).set_color_by_gradient(RED, RED_B).to_edge(UP,0.7).shift(UR)
        conclu2 = Text("Dans le plan cartésien, le déterminant est le facteur par lequel \nles aires sont multipliées.").shift(UP*2.7+LEFT*0.3)
        conclu3 = Text("Dans l'espace, on parle de volume ou d'hyper volume.").next_to(conclu2, DOWN, 0.4).shift(LEFT*0.7)
        conclu4 = Text("Si le déterminant est négatif, l'orientation est inversée.").next_to(conclu3, DOWN, 0.6).shift(RIGHT*0.025)
        conclu5 = Text("Lorsque le déterminant est nul, la dimension de l'espace d'image \nest strictement inférieure à celle de l'espace de départ.").next_to(conclu4, DOWN, 0.6).shift(RIGHT*0.85)
        conclu6 = Text("Ainsi, une matrice est inversible ssi son déterminant est non nul.").next_to(conclu5, DOWN, 0.6).shift(RIGHT*0.075)

        Group(conclu2, conclu4, conclu6).set_color_by_gradient(GREEN, GREEN_B)
        Group(conclu3, conclu5).set_color_by_gradient(BLUE, BLUE_B)

        self.create(conclu1, conclu2, conclu3, conclu4, conclu5, conclu6)
        self.wait(5)