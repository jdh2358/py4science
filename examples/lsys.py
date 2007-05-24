# encoding: utf-8
"""L-system (Lindenmayer systems) generation library.

See the class docstrings below for details on L-systems.

You can run the module as a script with

python lsys.py -e

to execute its test suite and generate example graphics.

DEPENDENCIES: this module requires the Python bindings to the Cairo
library.  These are available as python-cairo on many Linux
distributions; the project site is:

    http://cairographics.org/pycairo
"""

__author__ = 'Stefan van der Walt <stefan@sun.ac.za>'
__license__ = 'BSD'

__all__ = ['Canvas','LSystem','Plotter']

# Stdlib imports
from math import cos, sin, pi, sqrt
import string

# External imports
try:
    import cairo
except ImportError:
    # Since pycairo isn't very common, give some useful info to users
    # in case they don't have it.
    import sys
    err = lambda s: sys.stderr.write(s+'\n')
    err("ERROR: you need the Python bindings for Cairo")
    err("available from: http://cairographics.org/pycairo")
    err("")
    err("In many Linux distributions, you can find it as a package named")
    err("python-cairo which you can install.")
    err("")
    err("Aborting.")
    sys.exit(1)

###########################################################################
# Normal code begins here
class Canvas(object):
    def __init__(self, width=800, height=600):
        """Create a Cairo canvas.

        :Parameters:
            width : int
                Width of the canvas.

            height : int
                Height of the canvas.

        """
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        ctx.set_source_rgb(1,1,1)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_line_width(0.6)
        ctx.paint()

        self.surface = surface
        self.context = ctx

    def to_png(self,filename):
        """Store the canvas to PNG.

        :Parameters:
            filename : string
                Name of PNG file.

        """
        assert filename.endswith('.png')
        self.surface.write_to_png(filename)

class _Vector(list):
    def normalise(self,width,height):
        """Normalise the vector relative to the canvas width and height.

        This ensures that the vector fills the whole canvas.

        :Parameters:
            width : int
                Canvas width.
            height : int
                Canvas height.

        """
        max_x, max_y = 0,0
        min_x, min_y = width,height
        for stroke in self:
            for (x,y) in stroke:
                if x > max_x: max_x = x
                if y > max_y: max_y = y
                if x < min_x: min_x = x
                if y < min_y: min_y = y

        if max_x == min_x: max_x = min_x + 1
        if max_y == min_y: max_y = min_y + 1

        scale = min((width-10)/float(max_x-min_x),(height-10)/float(max_y-min_y))
        for k,stroke in enumerate(self):
            for i,(x,y) in enumerate(stroke):
                self[k][i] = (5 + (x-min_x)*scale, 5 + (y-min_y)*scale)

class LSystem(object):
    """L-System.

    From Wikipedia:

      An L-system or Lindenmayer system is a formal grammar (a set of
      rules and symbols) most famously used to model the growth
      processes of plant development, but also able to model the
      morphology of a variety of organisms. L-systems can also be used
      to generate self-similar fractals such as iterated function
      systems. L-systems were introduced and developed in 1968 by the
      Hungarian theoretical biologist and botanist from the University
      of Utrecht, Aristid Lindenmayer (1925–1989).

    """
    def __init__(self,state,rules,angle=pi/2,name='lsys'):
        """Initialise the L-System

        :Parameters:
            state : string
                Initial state, e.g. 'AF'.

            rules : dictionary
                Production rules, specified in the form
                variable : product, e.g.

                {'A': 'A-F+[FA]',
                 'F' : 'FA+AF'}

                For plotting purposes, certain symbols are special
                (see Plotter.plot for more detail).

            angle : float
                Angle to turn at symbols '+' and '-'.

            name : string
                Optional English name for the system.

        """
        self.initial_state = state
        self.state = state
        self.state_nr = 0
        self.rules = rules
        self.angle = angle
        self.name = name

    def set_level(self,N):
        """Evolve N times.

        Previous state is taken to account, i.e. if N=5 and current
        state is N=4, only one iteration is done.

        """
        if self.state_nr > N:
            self.state = self.initial_state
            self.state_nr = 0

        while self.state_nr < N:
            new_state = []
            self.state_nr = self.state_nr + 1
            for v in self.state:
                new_state += self.rules.get(v,v)
            self.state = ''.join(new_state)

    def get_level(self):
        return self.state_nr

    level = property(fget=get_level,fset=set_level)

class Plotter(object):
    """Turtle graphics plotter for L-systems.

    """
    def __init__(self,delta=10,direction=0.):
        self.vec = _Vector([[(0.,0.)]])
        self.direction = direction
        self.delta = delta

        self._switch_turn = 1
        self._state_stack = []

    def forward(self):
        """Move forward in the current direction.

        """
        x,y = self.vec[-1][-1]
        x = x + self.delta*cos(self.direction)
        y = y + self.delta*sin(self.direction)
        self.vec[-1].append((x,y))

    def forward_no_draw(self):
        """Move forward in the current direction but do not draw.

        """
        self.forward()
        pos = self.vec[-1][-1]
        del self.vec[-1][-1] # remove from list only -- does not clear pos
        self.vec.append([]) # start new stroke
        self.vec[-1].append(pos)

    def turn_left(self,angle):
        """Turn turtle left by delta.

        """
        self.direction += self._switch_turn * angle

    def turn_right(self,angle):
        """Turn turtle right by delta.

        """
        self.direction -= self._switch_turn * angle

    def get_state(self):
        return (self.vec[-1][-1],self.direction,self.delta,self._switch_turn)

    def set_state(self,state):
        (x,y),direction,delta,switch_turn = state
        self.direction = direction
        self.delta = delta
        self._switch_turn = switch_turn
        x_cur,y_cur = self.vec[-1][-1]
        if (x != x_cur) or (y != y_cur):
            self.vec.append([])
            self.vec[-1].append((x,y))

    state = property(fget=get_state, fset=set_state)

    def push_state(self):
        """Store the current turtle state.

        """
        self._state_stack.append(self.state)

    def pop_state(self):
        """Restore the current turtle state.

        """
        self.state = self._state_stack.pop()

    def switch_turn(self):
        """Swap around 'turn left' and 'turn right'.

        """
        self._switch_turn *= -1

    def vectorise(self,lsys):
        """Vectorise the L-system.

        """
        self.__init__()

        plotter =  {'A': self.forward,
                    'B': self.forward,
                    'F': self.forward,
                    '+': (self.turn_right,lsys.angle),
                    '-': (self.turn_left,lsys.angle),
                    '[': self.push_state,
                    ']': self.pop_state,
                    '!': self.switch_turn,
                    'G': self.forward_no_draw}

        read_forward = False

        # replace '@' by '<SPACE>@' to simplify parsing of consecutive '@'
        # sequences and '@' sequences at the end of the state
        state = lsys.state.upper().replace('@',' @') + ' '

        for v in state:
            if v == '@':
                read_forward = True
                _read_sofar = ''
                _float_sqrt = False
                _float_inv = False
                continue

            if read_forward:
                if v in string.digits + '.':
                    _read_sofar += v
                elif v == 'Q':
                    _float_sqrt = not _float_sqrt
                elif v == 'I':
                    _float_inv = not _float_inv
                else:
                    read_forward = False
                    f = float(_read_sofar)
                    if _float_sqrt: f = sqrt(f)
                    if _float_inv: f = 1/f
                    self.delta = f*self.delta

            cmd = plotter.get(v,None)
            if cmd is None:
                continue
            if isinstance(cmd,tuple):
                plot,args = cmd[0],cmd[1:]
            else:
                plot = cmd
                args = tuple()

            plot(*args)

        return self.vec

    def plot(self,lsys,canvas,filename):
        """Plot the L-system to canvas.

        :Parameters:
            lsys : LSystem
               The system to plot.
            canvas : Canvas
               Canvas to plot to.
            filename : string
               Filename of output PNG.

        The different symbols in the L-system state are interpreted as follows:

        + : Turn right by angle radians
        - : Turn left by angle radians
        F,A,B : Draw forward
        G : Move forward, but do not draw
        [ : Remember current plotter state (position, direction, length, etc.)
        ] : Restore last stored plotter state
        ! : Swap around 'turn left' and 'turn right'
        @ : Adjust the forward step length by the factor following
            '@', i.e. @0.5 or @2.  When @ is followed by Q, the
            square-root of the given number is used, i.e. @Q2.  Similarly,
            I indicates the inverse, i.e. @I2 is equivalent to @.5.

        See also: vectorise.

        """
        ctx = canvas.context
        ctx.set_source_rgb(0,0,0)
        self.vectorise(lsys)
        self.vec.normalise(canvas.surface.get_width(),
                           canvas.surface.get_height())
        for stroke in self.vec:
            x0,y0 = stroke[0]
            ctx.move_to(x0,y0)
            for (x,y) in stroke[1:]:
                ctx.line_to(x,y)
            ctx.stroke()

        # Print name of L-System
        ctx.move_to(20, canvas.surface.get_height()-20)
        ctx.select_font_face("Sans")
        ctx.set_font_size(20)
        ctx.set_source_rgb(0.3,0.3,0.9)
        ctx.text_path(lsys.name)
        ctx.fill()

        canvas.to_png(filename)

    __call__ = plot

systems = {'koch': LSystem('F',{'F':'F+F-F-F+F'},pi/2,
                           name='Koch'),

           'sierpinski': LSystem('DA',{'A':'B-A-B',
                                       'B':'A+B+A',
                                       'D':'!D'},
                                 pi/3.,
                                 name='Sierpinski Triangle'),

           'dragon': LSystem('FX',{'X':'X+YF+',
                                   'Y':'-FX-Y'},
                             pi/2,
                             name = 'Dragon Curve'),

           'fern0': LSystem('++++X',{'X':'F-[[X]+X]+F[+FX]-X',
                                     'F':'FF'},
                            25/180.*pi,
                            'Fern #0'),

           'fern1': LSystem('++++X',{'X':'F[+X]F[-X]+X',
                                     'F':'FF'},
                            20/180.*pi,
                            'Fern #1'),

           'fern2': LSystem('++++F',{'F':'FF-[-F+F+F]+[+F-F-F]'},
                            22.5/180.*pi,
                            'Fern #2'),

           'weed': LSystem('+++++++++++++X',
                           {'X':'F[@.5+++++++++X]-F[@.4-----------!X]@.6X'},
                           7.2/180.*pi,
                           'Weed'),
           'alien': LSystem('X',{'X':'[@Q2@I2-FX]G[@Q2@I2---FX]',
                                 'F':''},
                            32.72/180.*pi,
                            'Alien'),
           }

def _example(*args):
    plot = Plotter()
    example_params = {'koch': 5,
                      'sierpinski': 6,
                      'dragon': 10,
                      'fern0': 6,
                      'fern1': 8,
                      'fern2': 4,
                      'weed': 10,
                      'alien': 10}

    for (sys,level) in example_params.iteritems():
        c = Canvas(800,600)
        s = systems[sys]
        print 'Generating %s...' % s.name,
        s.level = level
        name = s.name.replace(' ','').lower()
        outfile = '%s_%i.png' % (name,s.level)
        plot(s,c,outfile)
        print "%s saved." % outfile

def _list_lsystems(*args):
    max_len = max(len(sysname) for sysname in systems)
    for s in systems:
        print s.ljust(max_len), systems[s].name

###########################################################################
if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-e','--example',
                      action='callback',callback=_example,
                      help='generate example output files')
    parser.add_option('-l','--list',
                      action='callback',callback=_list_lsystems,
                      help='list available L-systems')
    (options,args) = parser.parse_args()

    import unittest
    class TestLSystem(unittest.TestCase):
        def testReproduce(self):
            koch = systems['koch']
            koch_states = ('F','F+F-F-F+F',
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F',
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F+'
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F-'
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F-'
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F+'
                           'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F')
            for nr,state in enumerate(koch_states):
                koch.level = nr
                self.assertEqual(koch.state,state)

        def testReproduce2(self):
            lsys = LSystem('A',{'A':'B','B':'AB'})
            states = {0 : 'A',
                      1 : 'B',
                      2 : 'AB',
                      3 : 'BAB',
                      4 : 'ABBAB',
                      5 : 'BABABBAB',
                      6 : 'ABBABBABABBAB',
                      7 : 'BABABBABABBABBABABBAB'}
            for level,state in states.iteritems():
                lsys.level = level
                self.assertEqual(lsys.state,state)

    class TestPlotter(unittest.TestCase):
        def setUp(self):
            self.plot = Plotter(delta=10,direction=0.)

        def testVectorise(self):
            koch = systems['koch']
            koch.level = 1

            v = self.plot.vectorise(koch)
            v_expected = [[(0,0), (10,0), (10,-10),
                           (20,-10), (20,0), (30,0)]]

            self.assertEqual(v,v_expected)

        def testLengthFactor(self):
            lsys = LSystem('@I2@Q2',{})
            lsys.level = 1

            self.plot.vectorise(lsys)

            assert(abs(self.plot.delta - sqrt(2)/2*10) < 1e-10)

        def testForwardSkip(self):
            lsys = LSystem('FGF',{})
            v = self.plot.vectorise(lsys)
            v_expected = [[(0,0),(10,0)],
                          [(20,0),(30,0)]]
            self.assertEqual(v,v_expected)

        def testSaveState(self):
            lsys = LSystem('[F+F]F',{})
            v = self.plot.vectorise(lsys)
            v_expected = [[(0,0),(10,0),(10,-10)],
                          [(0,0),(10,0)]]
            self.assertEqual(self.plot.direction,0)
            self.assertEqual(v,v_expected)

        def testSwapLeftRight(self):
            lsys = LSystem('!F+F',{})
            v = self.plot.vectorise(lsys)
            v_expected = [[(0,0),(10,0),(10,10)]]
            self.assertEqual(v,v_expected)

    # run unittests, but ignore command line arguments
    import sys
    sys.argc = 1
    sys.argv = sys.argv[:1]
    unittest.main()
