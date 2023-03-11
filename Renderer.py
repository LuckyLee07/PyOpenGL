import glfw
import array
from Shader import *
from VertexArray import *
from VertexBuffer import *

from OpenGL.GL import *

class Renderer:
	def __init__(self, width, height):
		# 初始化GLFW
	    if not glfw.init(): return

	    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

	    # 创建窗口
	    self.window = glfw.create_window(width, height, "My OpenGL Window", None, None)
	    if not self.window:
	        glfw.terminate()
	        raise Exception("Failed to create GLFW window")

	    glfw.make_context_current(self.window)

	    glClearColor(0.2, 0.3, 0.3, 1.0)


	def pre_render(self):
		# 创建顶点着色器
	    self.vertex_shader = Shader(GL_VERTEX_SHADER, 'shaders/basic.vs')

	    # 创建片段着色器
	    self.fragment_shader = Shader(GL_FRAGMENT_SHADER, 'shaders/basic.fs')

	    # 创建着色器程序
	    self.shader_program = glCreateProgram()
	    glAttachShader(self.shader_program, self.vertex_shader.gid())
	    glAttachShader(self.shader_program, self.fragment_shader.gid())
	    glLinkProgram(self.shader_program)

	    # 设置顶点数据
	    verticesx = [
	        -0.5, -0.5, 0.0,
	         0.5, -0.5, 0.0,
	         0.0,  0.5, 0.0
	    ]
	    vertices = array.array('f', verticesx)

	    layout = VertexArrayLayout()
	    layout.push(3, GL_FLOAT, False) # position
	    #layout.push(4, GL_UNSIGNED_BYTE, True) # color
	    #layout.push(2, GL_FLOAT, False) # texture coordinates

	    self.vao = VertexArray()
	    data_size = vertices.itemsize * len(vertices)
	    self.vbo = VertexBuffer(vertices, data_size)
	    self.vao.add_buffer(self.vbo, layout)


	def after_render(self):
		# 先释放vbo再释放vao
		del self.vbo
		del self.vao
		# 先释放program再释放shader
		glDeleteProgram(self.shader_program)
		del self.vertex_shader
		del self.fragment_shader


	def render(self):
		# 清空缓冲区
		glClear(GL_COLOR_BUFFER_BIT)

		# 绘制三角形
		glUseProgram(self.shader_program)

		self.vao.bind()
		glDrawArrays(GL_TRIANGLES, 0, 3)
		self.vao.unbind()
		
		glUseProgram(0)

		# 交换缓冲区
		glfw.swap_buffers(self.window)


	def run(self): # 渲染循环
		self.pre_render()
		while not glfw.window_should_close(self.window):
			glfw.poll_events()
			self.render() # 主渲染逻辑

		self.after_render()

		# 关闭窗口
		glfw.terminate()
		
