'''
    ModernGL Constants
'''

# pylint: disable=using-constant-test, too-many-public-methods

# from ModernGL import ModernGL as mgl
import importlib; _mgl = importlib.import_module('ModernGL', 'ModernGL')

from .common import Object
from .buffers import Buffer, detect_format
from .programs import ComputeShader, Shader, Program
from .vertex_arrays import VertexArray
from .textures import Texture
from .renderbuffers import Renderbuffer
from .framebuffer import Framebuffer


class Context(Object):
    '''
        Create a :py:class:`Context` using:

            - :py:func:`~ModernGL.create_context`
            - :py:func:`~ModernGL.create_standalone_context`

        Members:

            - :py:meth:`Context.Buffer`
            - :py:meth:`Context.DepthRenderbuffer`
            - :py:meth:`Context.DepthTexture`
            - :py:meth:`Context.Framebuffer`
            - :py:meth:`Context.Program`
            - :py:meth:`Context.Renderbuffer`
            - :py:meth:`Context.Shader`
            - :py:meth:`Context.SimpleVertexArray`
            - :py:meth:`Context.Texture`
            - :py:meth:`Context.VertexArray`
    '''

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = Context.__new__(Context)
        res.mglo = obj
        return res

    @property
    def line_width(self) -> float:
        '''
            Set the default line width.
        '''

        return self.mglo.line_width

    @line_width.setter
    def line_width(self, value):
        self.mglo.line_width = value

    @property
    def point_size(self) -> float:
        '''
            Set the default point size.
        '''

        return self.mglo.point_size

    @point_size.setter
    def point_size(self, value):
        self.mglo.point_size = value

    @property
    def viewport(self) -> tuple:
        '''
            The viewport.
        '''

        return self.mglo.viewport

    @viewport.setter
    def viewport(self, value):
        self.mglo.viewport = tuple(value)

    @property
    def default_texture_unit(self) -> int:
        '''
            The default texture unit.
        '''

        return self.mglo.default_texture_unit

    @default_texture_unit.setter
    def default_texture_unit(self, value):
        self.mglo.default_texture_unit = value

    @property
    def max_texture_units(self) -> int:
        '''
            The max texture units.
        '''

        return self.mglo.max_texture_units

    @property
    def default_framebuffer(self) -> Framebuffer:
        '''
            The default framebuffer.
        '''

        return self.mglo.default_framebuffer

    @property
    def vendor(self) -> str:
        '''
            vendor
        '''

        return self.mglo.vendor

    @property
    def renderer(self) -> str:
        '''
            renderer
        '''

        return self.mglo.renderer

    @property
    def version(self) -> str:
        '''
            version
        '''

        return self.mglo.version

    def clear(self, red=0, green=0, blue=0, alpha=0):
        '''
            Clear the framebuffer.

            Args:
                red, green, blue: color components.
                alpha: alpha component.
        '''

        self.mglo.clear(red, green, blue, alpha)

    def enable(self, flag):
        '''
            Enable flags.

            Args:
                flags: flags to enable.
        '''

        self.mglo.enable(flag)

    def disable(self, flag):
        '''
            Disable flags.

            Args:
                flags: flags to disable.
        '''

        self.mglo.disable(flag)

    def finish(self):
        '''
            Wait for all drawing commands to finish.
        '''

        self.mglo.finish()

    def copy_buffer(self, dst, src, size=-1, *, read_offset=0, write_offset=0):
        '''
            Copy buffer content.

            Args:
                dst: Destination buffer.
                src: Source buffer.
                optional size: Size to copy.

            Keyword Args:
                read_offset: Read offset.
                write_offset: Write offset.
        '''

        self.mglo.copy_buffer(dst.mglo, src.mglo, size, read_offset, write_offset)

    def copy_framebuffer(self, dst, src):
        '''
            Copy framebuffer content.
        '''

        self.mglo.copy_framebuffer(dst.mglo, src.mglo)

    def buffer(self, data=None, reserve=0, dynamic=False) -> Buffer:
        '''
            Create a Buffer.

            Args:
                data: Content of the new buffer.

            Keyword Args:
                reserve: The number of bytes to reserve.
                dynamic: Treat buffer as dynamic.

            Returns:
                :py:class:`Buffer`
        '''

        return Buffer.new(self.mglo.buffer(data, reserve, dynamic))

    def texture(self, size, components, data=None, floats=False) -> Texture:
        '''
            Create a Texture.

            Args:
                size: Width, height.
                components: The number of components 1, 2, 3 or 4.
                optional data: Content of the image.

            Keyword Args:
                floats: Use floating point precision.

            Returns:
                :py:class:`Texture`
        '''

        return Texture.new(self.mglo.texture(size, components, data, floats))

    def depth_texture(self, size, data=None) -> Texture:
        '''
            Create a DepthTexture.

            Args:
                size: The width and height.
                optional data: The pixels.

            Returns:
                :py:class:`Texture`
        '''

        return Texture.new(self.mglo.depth_texture(size, data))

    def vertex_array(self, program, content, index_buffer=None) -> VertexArray:
        '''
            Create a VertexArray.

            Args:
                program: The program used by `render` and `transform`.
                content: A list of (buffer, format, attributes).
                optional index_buffer: An index buffer.

            Returns:
                :py:class:`VertexArray`
        '''

        if index_buffer is not None:
            index_buffer = index_buffer.mglo

        content = tuple((a.mglo, b, tuple(c)) for a, b, c in content)
        return VertexArray.new(self.mglo.vertex_array(program.mglo, content, index_buffer))

    def simple_vertex_array(self, program, buffer, attributes, index_buffer=None) -> VertexArray:
        '''
            Create a SimpleVertexArray.

            Args:
                program: The program used by `render` and `transform`.
                buffer: The buffer.
                attributes: A list of attribute names.
                optional index_buffer: An index buffer.

            Keyword Args:
                skip_errors: Ignore missing attributes.

            Returns:
                :py:class:`VertexArray`
        '''

        content = [(buffer, detect_format(program, attributes), attributes)]
        return self.vertex_array(program, content, index_buffer)

    def program(self, shaders, varyings=()) -> Program:
        '''
            Create a Program.

            Args:
                shaders: A list of :py:class:`Shader` objects.
                optional varyings: A list of varying names.

            Returns:
                :py:class:`Program`
        '''

        if isinstance(shaders, Shader):
            shaders = [shaders]

        return Program.new(self.mglo.program(tuple(x.mglo for x in shaders), tuple(varyings)))

    def vertex_shader(self, source) -> Shader:
        '''
            Create a VertexShader.

            Args:
                source: The source code in GLSL.

            Returns:
                :py:class:`Shader`
        '''

        return Shader.new(self.mglo.vertex_shader(source))

    def fragment_shader(self, source) -> Shader:
        '''
            Create a FragmentShader.

            Args:
                source: The source code in GLSL.

            Returns:
                :py:class:`Shader`
        '''

        return Shader.new(self.mglo.fragment_shader(source))

    def geometry_shader(self, source) -> Shader:
        '''
            Create a GeometryShader.

            Args:
                source: The source code in GLSL.

            Returns:
                :py:class:`Shader`
        '''

        return Shader.new(self.mglo.geometry_shader(source))

    def tess_evaluation_shader(self, source) -> Shader:
        '''
            Create a TessEvaluationShader.

            Args:
                source: The source code in GLSL.

            Returns:
                :py:class:`Shader`
        '''

        return Shader.new(self.mglo.tess_evaluation_shader(source))

    def tess_control_shader(self, source) -> Shader:
        '''
            Create a TessControlShader.

            Args:
                source: The source code in GLSL.

            Returns:
                :py:class:`Shader`
        '''

        return Shader.new(self.mglo.tess_control_shader(source))

    def framebuffer(self, color_attachments, depth_attachment) -> Framebuffer:
        '''
            Create a Framebuffer.

            Args:
                attachments: A list of `Texture` or `Renderbuffer` objects.

            Returns:
                :py:class:`Framebuffer`
        '''

        if isinstance(color_attachments, Object):
            color_attachments = [color_attachments]

        color_attachments = tuple(x.mglo for x in color_attachments)

        return Framebuffer.new(self.mglo.framebuffer(color_attachments, depth_attachment.mglo))

    def renderbuffer(self, size, components=4, *, samples=0, floats=True) -> Renderbuffer:
        '''
            Create a Renderbuffer.

            Args:
                size: Width, height.
                components: The number of components 1, 2, 3 or 4.

            Keyword Args:
                floats: Use floating point precision.

            Returns:
                :py:class:`Renderbuffer`
        '''

        return Renderbuffer.new(self.mglo.renderbuffer(size, components, samples, floats))

    def depth_renderbuffer(self, size, *, samples=0) -> Renderbuffer:
        '''
            Create a Renderbuffer.

            Args:
                size: Width, height.

            Returns:
                :py:class:`Renderbuffer`
        '''

        return Renderbuffer.new(self.mglo.depth_renderbuffer(size, samples))

    def compute_shader(self, source) -> ComputeShader:
        '''
            Create a ComputeShader.

            Args:
                source: The source of the compute shader.

            Returns:
                :py:class:`ComputeShader`
        '''

        return ComputeShader.new(self.mglo.compute_shader(source))


if False:
    def _create_context() -> Context:
        return Context()

    def _create_standalone_context(*args) -> Context:
        return Context(*args)

    mgl.create_context = _create_context
    mgl.create_standalone_context = _create_standalone_context


def create_context(require=None) -> Context:
    '''
        Create a context and load OpenGL functions.
        An OpenGL context must exists.

        Keyword Arguments:
            require (Version): OpenGL version.

        Returns:
            :py:class:`ModernGL.Context`
    '''

    ctx = Context.new(mgl.create_context())

    if require is not None and ctx.version < require:
        raise Exception('TODO')

    return ctx


def create_standalone_context(size=(256, 256), require=None) -> Context:
    '''
        Create a context and load OpenGL functions.
        An OpenGL context must exists.

        Keyword Arguments:
            size (tuple): Initial framebuffer size.
            require (:py:class:`ModernGL.Version`): OpenGL version.

        Returns:
            :py:class:`ModernGL.Context`
    '''

    ctx = Context.new(mgl.create_standalone_context(*size))

    if require is not None and ctx.version < require:
        raise Exception('TODO')

    return ctx


class ContextManager:
    '''
        ContextManager
    '''

    cache = {}

    @staticmethod
    def create_context(name='primary', standalone=False) -> Context:
        '''
            Create a named OpenGL context.
        '''

        ctx = ContextManager.cache.get(name)

        if not ctx:
            if standalone:
                ctx = create_standalone_context()
            else:
                ctx = create_context()

        ContextManager.cache[name] = ctx

        return ctx

    @staticmethod
    def release_context(name):
        '''
            Release a named context.
            Fails silently.
        '''

        ctx = ContextManager.cache.get(name)

        if not ctx:
            return

        ctx.release()

        del ContextManager.cache[name]
