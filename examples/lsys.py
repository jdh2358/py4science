# encoding: utf-8
"""L-system (Lindenmayer systems) generation library.

See the class docstrings below for details on L-systems.

You can run the module as a script to generate examples.  See

python lsys.py --help

for more information.

Dependencies:
=============

This module has a number of plotting back-ends:

Cairo:

    Cairo requires the Python bindings available from

        http://cairographics.org/pycairo

    (on Linux systems, these are often packaged as python-cairo).
    This backend is fast, and renders anti-aliased output to PNG.

Matplotlib:
-----------

    Matplotlib is available from

        http://matplotlib.sf.net

    Renders anti-aliased output to many different formats.

PyX:
----

    PyX is available from

        http://pyx.sf.net

    Renders output to EPS or PDF.

Visual:
-------

    Visual Python is available from

        http://vpython.org

    Renders output on-screen in 3D.

"""

__author__ = 'Stefan van der Walt <stefan@sun.ac.za>'
__license__ = 'BSD'

__all__ = ['LSystem','Plotter',
           'CairoCanvas','MatplotlibCanvas','PyXCanvas','VisualCanvas']
__canvas__ = 'visual'

# Stdlib imports
from math import cos, sin, pi, sqrt
import string
import sys

class Canvas(object):
    __description__ = 'Generic Canvas'
    __save_extensions__ = ['.png']

    # ----------------------------------------------------------
    # Subclassed canvases should implement the following methods
    # ----------------------------------------------------------

    def __init__(self, width=800, height=600):
        """Create a drawing canvas.

        :Parameters:
            width : int
                Width of the canvas.

            height : int
                Height of the canvas.

        """
        self.width = width
        self.height = height
        self.__palette = [(0,0,0),(0.0,0.2,0.4),(0.2,0.5,0.7),(0,0.2,0.5)]
        self.__colour = 0
        self.pos = (0,0)

    def save_to_file(self,filename):
        """Save the canvas to the given image file.

        """
        raise NotImplementedError

    def move_to(self, (x,y)):
        """Move the cursor to position (x,y).

        """
        raise NotImplementedError

    def line_to(self, (x,y)):
        """Draw a line from the current position to (x,y).

        """
        raise NotImplementedError

    def text(self, text):
        """Print the given text at the current position.

        """
        raise NotImplementedError

    def set_colour_rgb(self, (r,g,b)):
        """Set the current RGB colour to (r,g,b).

        """
        raise NotImplementedError

    # --------------------------------------------
    # The methods below do not need to be modified
    # --------------------------------------------

    def save(self, filename):
        """Store the canvas as an image file.

        This function calls save_to_file after determining
        the correct filename.

        """
        default_ext = self.__save_extensions__[0]
        self._filename = filename
        for ext in self.__save_extensions__:
            if filename.endswith(ext):
                default_ext = ''
        self._filename = self._filename + default_ext
        self.save_to_file()

    def set_palette(self, palette):
        """Set the entries of the palette.  The palette must be a list
        of 3-tuples, indicating R, G and B values, e.g.

        [(0,0,0),(0,1,0),(1,0,0),(0,0,1)] which indicates

        [black,green,red,blue]

        """
        self.__palette = palette

    def get_palette(self):
        """Return the current palette.

        """
        return self.__palette

    palette = property(fset=set_palette,fget=get_palette)

    def set_colour(self, c):
        """Set the colour to entry nr c in the palette.

        """
        ignored,self.__colour = divmod(c,len(self.palette))
        self.set_colour_rgb(self.palette[self.colour])

    def get_colour(self):
        """Return the current colour number.

        """
        return self.__colour

    colour = property(fset=set_colour,fget=get_colour)
    color = colour

class CairoCanvas(Canvas):
    __description__ = "Cairo (http://cairographics.org/pycairo)"

    def __init__(self, width=800, height=600):
        import cairo

        Canvas.__init__(self,width,height)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        ctx.set_source_rgb(1,1,1)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_line_width(0.6)
        ctx.paint()

        self._surface = surface
        self._ctx = ctx
        self.colour = 0

    def save_to_file(self):
        """NOTE: Cairo only supports saving to PNG.

        """
        self._surface.write_to_png(self._filename)

    def move_to(self,(x,y)):
        # Complete any undrawn lines before moving to new position
        self._ctx.stroke()
        self._ctx.move_to(x,y)

    def line_to(self,(x,y)):
        self._ctx.line_to(x,y)

    def set_colour_rgb(self,(r,g,b)):
        self._ctx.stroke()
        self._ctx.set_source_rgb(r,g,b)

    def text(self,text):
        ctx = self._ctx
        ctx.select_font_face("Sans")
        ctx.set_font_size(20)
        ctx.set_source_rgb(0.3,0.3,0.9)
        ctx.text_path(text)
        ctx.fill()

class MatplotlibCanvas(Canvas):
    __description__ = "Matplotlib (http://matplotlib.sf.net)"
    __save_extensions__ = ['.png','.jpg','.png','.pdf','.ps','.svg']

    def __init__(self, width=800, height=600):
        import pylab
        self.P = pylab

        Canvas.__init__(self,width,height)

        dpi = float(pylab.rcParams['savefig.dpi'])
        pylab.rcParams['figure.figsize'] = (width/dpi,height/dpi)

        pylab.figure()
        pylab.axis([0,width,height,0])
        pylab.axis('off')
        pylab.axis('equal')

        self._pos = 0,0
        self._rgb = (0,0,0)

    def save_to_file(self):
        self.P.savefig(self._filename)

    def move_to(self, (x,y)):
        pass

    def line_to(self, (x,y)):
        x0,y0 = self.pos
        self.P.plot([x0,x],[y0,y],color=self._rgb,
                    linewidth=0.6)

    def set_colour_rgb(self,(r,g,b)):
        self._rgb = (r,g,b)

    def text(self,text):
        x,y = self.pos
        self.P.figtext(x/float(self.width),1-y/float(self.height),
                       text,color=self.palette[self.color])

class PyXCanvas(Canvas):
    __description__ = "PyX (http://pyx.sf.net)"
    __save_extensions__ = ['.eps','.pdf']

    def __init__(self,width=10,height=10):
        import pyx
        self.pyx = pyx

        Canvas.__init__(self,width,height)
        self._pyx_canvas = pyx.canvas.canvas()
        self._path = []
        self._rgb = pyx.color.rgb(0,0,0)

    def save_to_file(self):
        self.stroke()
        self._pyx_canvas.writeEPSfile(self._filename)

    def stroke(self):
        if len(self._path) > 0:
            self._pyx_canvas.stroke(self.pyx.path.path(*self._path),[self._rgb])
        self._path = []

    def move_to(self, (x,y)):
        # Complete any undrawn lines before moving to new position
        self.stroke()
        self._path.append(self.pyx.path.moveto(*self.mapped_pos((x,y))))

    def line_to(self, (x,y)):
        self._path.append(self.pyx.path.lineto(*self.mapped_pos((x,y))))

    def set_colour_rgb(self,(r,g,b)):
        self.stroke()
        self._rgb = self.pyx.color.rgb(r,g,b)

    def text(self,text):
        x,y = self.mapped_pos(self.pos)
        self._pyx_canvas.text(x,y,self.pyx.text.escapestring(text),
                              [self.pyx.text.halign.flushright,self._rgb])

    def mapped_pos(self,(x,y)):
        return x,self.height-y

class VisualCanvas(Canvas):
    __description__ = "Visual Python (http://vpython.org)"
    _canvas = None

    def __init__(self,*args,**kwargs):
        import visual
        self.V = visual

        Canvas.__init__(self,*args,**kwargs)
        self.scene = visual.display(height=self.height,width=self.width,
                                    background=(1,1,1))
        self.scene.center = (self.width/2.,self.height/2.,0)
        self.scene.up = (0,-1,0)
        self.scene.forward = (0,0,1)
        self.scene.autoscale = True
#        self.scene.scale = (2./self.width,2./self.height,1)
        self._rgb = (0,0,0)

    def save_to_file(self):
        print "ERROR: VPython does not support saving to file"

    def move_to(self,(x,y)):
        self.pos = (x,y)
        self.curve = self.V.curve(pos=[(x,y)])

    def line_to(self,(x,y)):
        self.curve.append((x,y),color=self._rgb)

    def set_colour_rgb(self,(r,g,b)):
        self._rgb = (r,g,b)

    def text(self,text):
        x,y = self.pos
        self.V.label(pos=(x,y),text=text,opacity=0,
                     color=self._rgb)

    def __del__(self):
        while (self.scene.kb.getkey() != 'q'): pass

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

        scale = min((79/80.*width)/float(max_x-min_x),(59/60.*height)/float(max_y-min_y))
        for k,stroke in enumerate(self):
            for i,(x,y) in enumerate(stroke):
                self[k][i] = (1/160.*width + (x-min_x)*scale, 1/120.*height + (y-min_y)*scale)

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
    def __init__(self,state='F',rules={},angle=pi/2,name='lsys'):
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
        self._state_nr = 0
        self.rules = rules
        self.angle = angle
        self.name = name

    def set_level(self,N):
        """Evolve to level N.

        Previous state is taken to account, i.e. if N=5 and current
        state is N=4, only one iteration is done.

        """
        if self._state_nr > N:
            self._state = self.initial_state
            self._state_nr = 0

        while self._state_nr < N:
            new_state = []
            self._state_nr = self._state_nr + 1
            for v in self._state:
                new_state += self.rules.get(v,v)
            self._state = new_state

    def get_level(self):
        return self._state_nr

    level = property(fget=get_level,fset=set_level)

    def get_state(self):
        return ''.join(self._state)

    def set_state(self,state):
        self._state = []
        self._state.append(state)

    state = property(fget=get_state,fset=set_state)

    def __str__(self):
        return self.name

class Plotter(object):
    """Turtle graphics plotter for L-systems.

    """
    def __init__(self,delta=10,direction=0.):
        self.vec = _Vector([[(0.,0.)]])
        self.direction = direction
        self.delta = delta

        self._switch_turn = 1
        self._state_stack = []

    def forward(self,distance=None):
        """Move forward in the current direction.

        """
        if distance is None: distance = self.delta
        x,y = self.vec[-1][-1]
        x = x + distance*cos(self.direction)
        y = y + distance*sin(self.direction)
        self.vec[-1].append((x,y))

    def forward_no_draw(self,distance=None):
        """Move forward in the current direction but do not draw.

        """
        self.forward(distance)
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
                    'G': self.forward_no_draw,
                    '>': (self.forward_no_draw,0)} # Start a new segment.
                                                   # Hack to cycle the palette.

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
        canvas.colour = 0
        self.vectorise(lsys)
        self.vec.normalise(canvas.width,canvas.height)
        for stroke in self.vec:
            x0,y0 = stroke[0]
            canvas.move_to((x0,y0))
            canvas.pos = x0,y0
            for (x,y) in stroke[1:]:
                canvas.line_to((x,y))
                canvas.pos = x,y
            canvas.colour += 1

        # Print name of L-System
        canvas.colour = 1
        pos = (1/40.*canvas.width,29/30.*canvas.height)
        canvas.move_to(pos)
        canvas.pos = pos
        canvas.text(lsys.name)
        filename = canvas.save(filename)

        return canvas._filename

    __call__ = plot

canvases = {}
for cname in __all__:
    try:
        name = cname.replace('Canvas','').lower()
        cls = eval(cname)
        if issubclass(cls,Canvas): canvases[name] = cls
    except:
        pass

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

def _demo(*args):
    plot = Plotter()
    example_params = {'koch': 5,
                      'sierpinski': 6,
                      'dragon': 10,
                      'fern0': 6,
                      'fern1': 8,
                      'fern2': 4,
                      'weed': 10,
                      'alien': 10}

    for (lsys,level) in example_params.iteritems():
        # Generate list of canvases, with default canvas first
        cvs = canvases.keys()
        try:
            i = cvs.index(__canvas__)
        except:
            print 'Invalid default canvas "%s".' % __canvas__
            i = 0
        cvs = [cvs[i]] + cvs[:i] + cvs[i+1:]

        c = None
        _announce_canvas = False
        for cname in cvs:
            try:
                if _announce_canvas:
                    print "Loading %s backend." % cname
                c = canvases[cname]()
                # Sucessfully loaded canvas.  Set as default.
                globals()['__canvas__'] = cname
                break
            except ImportError, e:
                print "Failed to load %s backend." % cname
                _announce_canvas = True

        if c is None:
            print "Could not load any backends.  Exiting."
            sys.exit(-1)

        s = systems[lsys]
        print 'Generating %s...' % s.name,
        s.level = level
        name = s.name.replace(' ','').lower()
        outfile = '%s_%i' % (name,s.level)
        outfile = plot(s,c,outfile)
        print "%s saved." % outfile

def _print_dict(*args,**kwargs):
    d = args[-1]

    header = kwargs.get('header','')
    if header:
        print header
        print '='*len(header)

    max_len = max(len(key) for key in d)
    for k,v in d.iteritems():
        print k.ljust(max_len+1), getattr(v,'__description__',v)
    print

def _set_default_canvas(option, opt, value, parser):
    canvas = value
    globals()['__canvas__'] = canvas

###########################################################################
if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--lb',
                      action='callback',callback=_print_dict,
                      callback_kwargs={'header': 'Graphical Canvases'},
                      callback_args=(canvases,),
                      help='list available backends')
    parser.add_option('--ls',
                      action='callback',callback=_print_dict,
                      callback_kwargs={'header': 'L-Systems'},
                      callback_args=(systems,),
                      help='list available L-systems')
    parser.add_option('-q',action='store_true',dest='no_tests',
                      help='do not run unit tests',default=False)
    parser.add_option('-b','--backend',
                      action='callback',callback=_set_default_canvas,
                      type="string",nargs=1,
                      help='Available backends: ' + ', '.join(canvases.keys()))
    parser.add_option('-d','--demo',
                      action='callback',callback=_demo,
                      help='generate example output files')
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

        def testPaletteCycleHack(self):
            lsys = LSystem('F>F',{})
            v = self.plot.vectorise(lsys)
            v_expected = [[(0,0),(10,0)],[(10,0),(20,0)]]
            self.assertEqual(v,v_expected)

    # run unittests, but ignore command line arguments
    if not options.no_tests:
        import sys
        sys.argc = 1
        sys.argv = sys.argv[:1]
        unittest.main()
