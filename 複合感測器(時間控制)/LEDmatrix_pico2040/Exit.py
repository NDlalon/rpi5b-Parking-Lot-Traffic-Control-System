import board
import displayio
import framebufferio
import rgbmatrix
import busio
import time
#LED矩陣參數設定
bit_depth_value = 6
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays()

#LED矩陣設定
matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)


group = displayio.Group()
#設定待機狀態 group[0]=待機畫面
idle_bitmap = displayio.Bitmap(width_value, height_value, 1)
palette = displayio.Palette(1)
palette[0] = 0x00FF00
group.append(displayio.TileGrid(idle_bitmap, pixel_shader=palette))
group[0].hidden=True
#設定車輛進入狀態 group[1]=進入畫面
entry_bitmap = displayio.Bitmap(width_value, height_value, 1)
palette = displayio.Palette(1)
palette[0] = 0xA00000
group.append(displayio.TileGrid(entry_bitmap, pixel_shader=palette))
group[1].hidden=True

group[0].hidden=False
display.root_group = group
display.refresh()

#切換至待機狀態[0]:待機 [1]:進入
def set_IdlePage():
    group[0].hidden=False
    group[1].hidden=True

#切換至進入狀態[0]:待機 [1]:進入
def set_EntryPage():
    group[0].hidden=True
    group[1].hidden=False
    
# 初始化 UART
uart = busio.UART(board.GP0, board.GP1, baudrate=115200,timeout=1)
nowState='idle'
while True:
    if uart.in_waiting > 0:  # 檢查是否有資料可讀
        data = uart.readline()
        try:
            data=data.decode("utf-8").strip()  # 讀取並解碼
            if(data=='Entry:idle'):    
                set_IdlePage()
                nowState='idle'
            elif(data=='Entry'):  
                set_EntryPage()
                nowState='Entry'
                
            display.refresh()
        except:
            pass    
