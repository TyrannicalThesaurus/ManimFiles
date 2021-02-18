from manimlib.imports import *
import os
import pyclbr

class Introduction(Scene):
    #introduce integral
    def construct(self):
        hellotext = TextMobject("Hello everyone!")
        intintro = TextMobject("today we're going to talk about a cool integration trick:")
        integral = TextMobject("Integration with respect to an inverse!")
        self.add(hellotext)
        self.wait(3)
        self.play(Transform(hellotext,intintro))
        self.wait(6)
        self.play(Transform(hellotext,integral))
        self.wait(10)

class graphx(GraphScene):
    CONFIG={
        "x_min": -4,
        "x_max": 4,
        "y_min": -2,
        "y_max": 2,
        "x_axis_label": "$x$",
        "y_axis_label": "$y$",
        "graph_origin": 0.5 * DOWN + 0 * LEFT,
    }

    # Defining graph functions
    def construct(self):
        self.setup_axes(animate=True)

        def Tetration(x,n):
            if(n == 1):
                return x
            else:
                return x ** Tetration(x,(n-1))

        # Play graphs
        firstTetration = self.get_graph(lambda x : Tetration(x,1),x_min=0,x_max=np.e ** (1/np.e))
        self.play(ShowCreation(firstTetration,run_time = 1))
        for a in range(2,30):
            newTetration = self.get_graph(lambda x : Tetration(x,a),x_min=0,x_max=np.e ** (1/np.e))
            self.play(Transform(firstTetration,newTetration))

class inverseIntegration(GraphScene):
    CONFIG={
        "x_min": -6,
        "x_max": 6,
        "y_min": -6,
        "y_max": 6,
        "x_axis_label": "$x$",
        "x_axis_width": 6,
        "y_axis_label": "$y$",
        "graph_origin": 0 * DOWN + 0 * LEFT,
    }

    def construct(self):
        self.setup_axes(animate=True)

        functionGraph = self.get_graph(lambda x : math.sqrt(x), x_min=0,x_max=10)
        self.play(ShowCreation(functionGraph,run_time=1))

        inverseFunctionGraph = self.get_graph(lambda x : x ** 2, x_min=0, x_max=math.sqrt(10))
        #self.play(ShowCreation(inverseFunctionGraph,run_time=1))

        #Theres like 80 bajillion objects here because who needs memory conservation right guys?
        inverseFunctionArea = self.get_riemann_rectangles(inverseFunctionGraph,1,2,dx=0.01)
        inverseFunctionArea.rotate(np.pi / 2,about_point = np.array([0,0,0]))
        inverseFunctionArea.flip(UP)
        inverseFunctionArea.shift(np.array([1.97,0,0]))
        inverseFunctionArea.set_opacity(0.25)
        inverseFunctionArea.set_color(GREEN)

        inverseAreaLabel = TextMobject("A1")
        inverseAreaLabel.shift(np.array([0.35,0.75,0]))
        inverseAreaLabel.scale(0.6)

        functionArea = self.get_riemann_rectangles(functionGraph,1,4,dx=0.01)
        functionArea.set_opacity(0.25)
        functionArea.set_color(RED)
        functionArea.shift(np.array([0,-0.01,0]))

        AreaLabel = TextMobject("A2")
        AreaLabel.shift(np.array([1.25,0.4,0]))
        AreaLabel.scale(0.6)

        boxThingy1 = Rectangle(height = 1, width = 2)
        boxThingy1.shift(np.array([1,0.5,0]))
        boxThingy1.set_color('#dd6713')

        boxThingy2 = Rectangle(height = 0.5, width = 0.5)
        boxThingy2.shift(np.array([0.25,0.25,0]))
        boxThingy2.set_color('#4c0873')

        #Create placeholder objects so that I can modify them without changing the original boxes properties
        placeholderBT1 = copy.deepcopy(boxThingy1)
        placeholderBT2 = copy.deepcopy(boxThingy2)
        placeholderA1 = copy.deepcopy(inverseAreaLabel)
        placeholderA2 = copy.deepcopy(AreaLabel)

        bigSquareEq = Rectangle(height = 0.5, width = 1)
        bigSquareEq.shift(np.array([-5,-1,0]))
        bigSquareEq.set_color('#dd6713')

        minus = TextMobject("-")
        minus.shift(np.array([-4.20,-1,0]))

        lilSquareEq = Rectangle(height = 0.375, width = 0.375)
        lilSquareEq.shift(np.array([-3.75,-1,0]))
        lilSquareEq.set_color('#4c0873')

        equals = TextMobject("=")
        equals.shift(np.array([-3.2,-1,0]))

        eqA1 = TextMobject("A1")
        eqA1.set_color(GREEN)
        eqA1.shift(np.array([-2.65,-1,0]))

        plus = TextMobject("+")
        plus.shift(np.array([-2.1,-1,0]))

        eqA2 = TextMobject("A2")
        eqA2.set_color(RED)
        eqA2.shift(np.array([-1.55,-1,0]))

        self.play(ShowCreation(boxThingy1))
        self.play(ShowCreation(boxThingy2))
        self.play(ShowCreation(inverseFunctionArea))
        self.play(ShowCreation(inverseAreaLabel),run_time=0.25)
        self.play(ShowCreation(functionArea))
        self.play(ShowCreation(AreaLabel),run_time=0.25)
        self.play(Transform(placeholderBT1,bigSquareEq))
        self.play(ShowCreation(minus))
        self.play(Transform(placeholderBT2,lilSquareEq))
        self.play(ShowCreation(equals))
        self.play(Transform(placeholderA1,eqA1))
        self.play(ShowCreation(plus))
        self.play(Transform(placeholderA2,eqA2))


class startExplaining(GraphScene):
    #graph config
    CONFIG={
        "x_min": 0,
        "x_max": 10,
        "y_min": 0,
        "y_max": 10,
        "x_axis_label": "$x$",
        "x_axis_width": 5,
        "y_axis_label": "$y$",
        "y_axis_height": 5,
        "graph_origin": 3 * DOWN + 6 * LEFT,
    }

#construct scene
    def construct(self):
        #draw axes
        self.setup_axes(animate = True)

        #draw f(x)
        functionGraph = self.get_graph(lambda x : math.sqrt(x), x_min=0,x_max=10)
        self.play(ShowCreation(functionGraph,run_time=1))

        #lower bound object
        lowerBound = self.get_vertical_line_to_graph(1,functionGraph)
        lowerBound.set_color(WHITE)

        #upper bound object
        upperBound = self.get_vertical_line_to_graph(4,functionGraph)
        upperBound.set_color(WHITE)

        #draw both bound objects at the same time
        self.play(
        ShowCreation(upperBound),
        ShowCreation(lowerBound)
        )

        #area object
        functionArea = self.get_riemann_rectangles(functionGraph,1,4,dx=0.01)
        functionArea.set_opacity(0.25)
        functionArea.set_color(RED)
        functionArea.shift(np.array([0,-0.01,0]))
        self.play(ShowCreation(functionArea))


        #
        functionGraphInverse = self.get_graph(lambda x : x ** 2, x_min=0, x_max=math.sqrt(10),color = BLUE)

        #A1 label, helps keep track of which quantity is which while they move.
        rAreaLabel = TexMobject("Area_{1}", "= \int_{a}^{b} f(x) dx")
        rAreaLabel.move_to(3*UP + 1.5*RIGHT)
        rAreaLabel.scale(1.1)
        rAreaLabel[0].set_color(RED)
        self.play(ShowCreation(rAreaLabel))

        functionAreaFlipped = copy.deepcopy(functionArea)
        functionAreaFlipped.flip(np.array([1,1,0]))
        functionAreaFlipped.move_to(1.75*DOWN+5.5*LEFT)

        lowerBoundFlipped = copy.deepcopy(lowerBound)
        lowerBoundFlipped.flip(np.array([1,1,0]))
        lowerBoundFlipped.move_to(2.5*DOWN+5.75*LEFT)

        upperBoundFlipped = copy.deepcopy(upperBound)
        upperBoundFlipped.flip(np.array([1,1,0]))
        upperBoundFlipped.move_to(1*DOWN+5.5*LEFT)

        #move all of the pieces at the same time.
        self.play(
        Transform(functionArea,functionAreaFlipped),
        Transform(functionGraph,functionGraphInverse),
        Transform(lowerBound,lowerBoundFlipped),
        Transform(upperBound,upperBoundFlipped),
        # Transform(x_axis_label,y_axis_label),
        # Transform(y_axis_label,x_axis_label)
        )

        invFuncUpperBound = self.get_vertical_line_to_graph(2,functionGraphInverse)
        invFuncUpperBound.set_color(WHITE)

        invFuncLowerBound = self.get_vertical_line_to_graph(1,functionGraph)
        invFuncLowerBound.set_color(WHITE)

        self.play(
        ShowCreation(invFuncLowerBound),
        ShowCreation(invFuncUpperBound)
        )

        inverseFunctionArea = self.get_riemann_rectangles(functionGraphInverse,1,2,dx=0.01)
        inverseFunctionArea.set_opacity(0.25)
        inverseFunctionArea.set_color(GREEN)
        self.play(ShowCreation(inverseFunctionArea))

        rAreaLabel2 = TexMobject("Area_{2}"," = \int_{f(a)}^{f(b)} f^{-1}(x) dx")
        rAreaLabel2.next_to(rAreaLabel,DOWN)
        rAreaLabel2.scale(1.1)
        rAreaLabel2[0].set_color(GREEN)
        self.play(ShowCreation(rAreaLabel2))

        self.wait(1)

        #create an object for the equation split into several pieces. This allows for moving specific parts of the equation around.
        totalAreaEq = TexMobject(
        #   0       1       2      3       4    5      6         7           8         9
        "\\int_", "{a}^", "{b}", "f(x)", "dx", "+", "\\int_", "{f(a)}", "^{f(b)}", "f^{-1}(x)", "dx", "=", "f(b)", "b", "-", "f(a)", "a"
        )
        totalAreaEq.scale(1.1)
        totalAreaEq.next_to(rAreaLabel2,DOWN*3)
        self.play(ShowCreation(totalAreaEq),run_time=3)
        self.wait(2)

        #create object
        shiftEq = totalAreaEq[11:17]
        shiftEq.generate_target()
        shiftEq.target.next_to(totalAreaEq[4],RIGHT)

        #create object for the integral from f(a) to f(b) of f^-1(x).
        invers_part = totalAreaEq[5:11]
        invers_part.generate_target()
        invers_part.target.next_to(shiftEq.target, RIGHT)

        #create minus object to replace plus object
        minus = TexMobject("-")
        minus.next_to(shiftEq.target)

        #move term to right side of eq.
        self.play(
        MoveToTarget(invers_part,path_arc=-np.pi/2),
        MoveToTarget(shiftEq),
        Transform(totalAreaEq[5],minus,path_arc=-np.pi/2,)
        )
