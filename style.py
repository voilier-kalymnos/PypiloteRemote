import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT, SERIF, BOLD, NORMAL
from toga.constants import RED, GREEN, WHITE, BLACK, BLUE, GREY, YELLOW


class Style():

	COLOR_ON         = "#090"   ##GREEN
	COLOR_OFF        = GREY
	COLOR_UNAVAILABLE= "#444444"
	COLOR_TARGET     = RED
	COLOR_TEXT       = WHITE
	COLOR_PUSH       = "#909090"
	COLOR_BOX        = "#333333"
	COLOR_BOX_LIGHT  = "#444444"

	FONT             = "Quicksand"
	MARGIN           = 10
	BUTTON_HEIGHT    = 80
	FONT_SIZE        = 16
	TARGET_SIZE      = 50


	def __init__(self):
			
		print("Initialize Style")
		#toga.Font.register("Roboto", "resources/Roboto-Regular.ttf",weight=NORMAL)
		toga.Font.register("Roboto", "resources/Roboto-ExtraBold.ttf",weight=BOLD)
		
		
		self.value=Pack( 
						text_align=CENTER,
						color=YELLOW,
						font_size=72,
						font_family="Roboto",
						font_weight=BOLD
						)
		
		self.title=Pack(
						margin_left=self.MARGIN, 
						text_align=LEFT,
						color=YELLOW,
						font_size=20,
						)

		self.metric=Pack(
						margin_right=self.MARGIN, 
						text_align=RIGHT,
						color=YELLOW,
						font_size=20,
						)
												
		self.inputBox=Pack(
						margin=self.MARGIN, 
						text_align=CENTER,
						color=BLACK,
						background_color=WHITE,
						font_size=self.FONT_SIZE,
						flex=1
						)
		self.button=Pack(
						margin=self.MARGIN, 
						height=self.BUTTON_HEIGHT,
						color=WHITE,
						background_color=self.COLOR_TARGET, 
						font_size=self.FONT_SIZE,
						font_family="Roboto",
						font_weight=BOLD,
						flex=1
						)
		self.target=Pack(
						margin=self.MARGIN, 
						text_align=CENTER,
						color=WHITE,
						font_family="Roboto",
						font_weight=BOLD,
						font_size=self.TARGET_SIZE,
						flex=1
						)
		self.small=Pack(
						margin=self.MARGIN, 
						text_align=CENTER,
						color=WHITE,
						font_size=self.FONT_SIZE,
						flex=1
						)
		self.child_box=Pack(
						direction=ROW,
						flex=1
						)
		self.child_box_column=Pack(
						margin = 5,
						direction=COLUMN,
						align_items=CENTER,
						background_color=self.COLOR_BOX,
						flex=1
						)
		
		self.child_box_cap=Pack(
						margin = 0,
						direction=COLUMN,
						align_items=CENTER,
						background_color=self.COLOR_BOX_LIGHT,
						flex=1
						)
								
		self.main_box=Pack(
						direction=COLUMN,
						align_items=CENTER,
						background_color=BLACK,
						flex=1
						)

